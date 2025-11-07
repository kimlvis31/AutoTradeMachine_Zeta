from locale import currency
from urllib import request
import ATM_Zeta_Auxillaries
import ATM_Zeta_Analyzers

from random import randint
import pyglet
import time
import os
import pprint
import termcolor

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

SIMULATIONPROCESSTIMELIMIT_NS = 1000*1e6
KLINESAVEPERPROCESSLIMIT = 10000

class manager_AUX:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, ipcA_MAIN, ipcA_ATM, ipcAThread_MAIN, ipcAThread_ATM):
        print(termcolor.colored("\nInitializing", 'green'), termcolor.colored("AUX", 'light_blue'), termcolor.colored("Manager --------------------------------------------------------------------------------------------------------------------------", 'green'))
        self.ipcA_MAIN = ipcA_MAIN
        self.ipcA_ATM  = ipcA_ATM
        self.ipcAThread_MAIN = ipcAThread_MAIN
        self.ipcAThread_ATM  = ipcAThread_ATM
        
        #Process Control
        self.process_terminate = False

        #Simulator
        self.simulator_Simulations_Processing = dict()
        self.simulator_Simulations_Completed  = dict()

        self.simualtor_SimulationQueue = list()
        self.simulator_RunningRunTimeAnalysis = False
        self.simulator_pause = False
        
        self.simStatus_lastReported = 0
        self.simStatus_reportInterval_ms = 10

        #DB Record Control
        self.dbConnected    = False
        self.dbRecordLoaded = False

        #FAR Registration - MAIN
        self.ipcA_MAIN.addFARHandler("ADDSIMULATIONQUEUE",  self.farHandler_ADDSIMULATIONQUEUE)
        self.ipcA_MAIN.addFARHandler("REMOVESIMULATION",    self.farHandler_REMOVESIMULATION)
        self.ipcA_MAIN.addFARHandler("PAUSESIMULATION",     self.farHandler_PAUSESIMULATION)
        self.ipcA_MAIN.addFARHandler("RESUMESIMULATION",    self.farHandler_RESUMESIMULATION)
        self.ipcA_MAIN.addFARHandler("TERMINATESIMULATION", self.farHandler_TERMINATESIMULATION)

        #FAR Registration - ATM
        self.ipcA_ATM.addFARHandler("RECEIVEANALYSISSUMMARYRECORDS", self.farHandler_RECEIVEANALYSISSUMMARYRECORDS)

        #IPC Call Function Registration
        self.ipcA_MAIN.addFARHandler("PROCCTRLFUNC_TERMINATE", self.far_RaiseTerminationFlag)

        print(termcolor.colored("AUX", 'light_blue'), termcolor.colored("Manager Initialization Complete! --------------------------------------------------------------------------------------------------------------", 'green'))
    def postInitialization(self):
        self.ipcA_MAIN.sendPRDEDIT("PROCSTATUS", "INITIALIZED", nMaxDispatch = 'INF')
        self.ipcA_ATM.sendPRDEDIT("PROCSTATUS",  "INITIALIZED", nMaxDispatch = 'INF')
        self.ipcA_ATM.sendPRDEDIT("PROCCTRL_INITGO", True, nMaxDispatch = 'INF')
        
        self.ipcA_MAIN.sendPRDEDIT("SIMULATIONS_PROCESSING", self.simulator_Simulations_Processing, nMaxDispatch = 'INF')
        self.ipcA_MAIN.sendPRDEDIT("SIMULATIONS_COMPLETED",  self.simulator_Simulations_Completed,  nMaxDispatch = 'INF')
        self.ipcA_MAIN.sendPRDEDIT("SIMULATION_RUNNING",     not(self.simulator_pause),  nMaxDispatch = 'INF')
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




    #Manager Process Loop ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self): 
        self.ipcA_MAIN.sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        self.ipcA_ATM.sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        while (self.process_terminate == False):
            #Check Database Connection
            self.__checkDBConnection()

            #Perform Simulator Process
            if (0 < len(self.simualtor_SimulationQueue) and (self.simulator_pause == False)):
                simulationCode = self.simualtor_SimulationQueue[0]
                simulation     = self.simulator_Simulations_Processing[simulationCode]

                #Simulation Processing
                simulationComplete = simulation.process()

                #Simulation Status Report
                if (self.simStatus_reportInterval_ms*1e6 < (time.perf_counter_ns() - self.simStatus_lastReported)): 
                    self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_PROCESSING", simulationCode, 'simulationProcess'),           simulation.getCurrentProcess(),          nMaxDispatch = 'INF')
                    self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_PROCESSING", simulationCode, 'simulationProcess_perc'),      simulation.getCompletionPerc(),          nMaxDispatch = 'INF')
                    self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_PROCESSING", simulationCode, 'simulationProcess_percTotal'), simulation.getCompletionPercTotal(),     nMaxDispatch = 'INF')
                    self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_PROCESSING", simulationCode, 'estimatedCompletionTime'),     simulation.getEstimatedCompletionTime(), nMaxDispatch = 'INF')
                    self.simStatus_lastReported = time.perf_counter_ns()

                #Simulation Queue Control
                if (simulationComplete == True): #If this is the case, the database must have completed saving the simulation result and will soon send FAR 'RECEIVEANALYSISSUMMARYRECORDS'
                    completionType = simulation.getCompletionType()
                    if   (completionType == 'COMPLETED'):  pass
                    elif (completionType == 'TERMINATED'): self.ipcA_MAIN.sendFAR(functionID = 'RESPOND_TERMINATESIMULATION', functionParams = {'result': True, 'resultMsg': "Simulation '{:s}' Successfully Terminated".format(simulationCode)}, nMaxDispatch = 'INF')
                    elif (completionType == 'REMOVAL'):    self.ipcA_MAIN.sendFAR(functionID = 'RESPOND_REMOVESIMULATION',    functionParams = {'result': True, 'resultMsg': "Simulation '{:s}' Successfully Performed Termination Process and Has Been Removed".format(simulationCode)}, nMaxDispatch = 'INF')
                    #self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation is Already Paused'}, nMaxDispatch = 'INF')

                    #Remove the Simulation From the Processing Simulations List
                    del self.simulator_Simulations_Processing[simulationCode]
                    self.simualtor_SimulationQueue.pop(0)
                    self.ipcA_MAIN.sendPRDREMOVE(("SIMULATIONS_PROCESSING", simulationCode))

                    #Next Simulator
                    if (0 < len(self.simualtor_SimulationQueue)): 
                        nextSimulationCode = self.simualtor_SimulationQueue[0]
                        self.ipcA_MAIN.sendPRDEDIT('CURRENTANALYSIS', nextSimulationCode, nMaxDispatch = 'INF')
                        self.simulator_Simulations_Processing[nextSimulationCode].startSimulator()
                    else: self.ipcA_MAIN.sendPRDEDIT('CURRENTANALYSIS', None, nMaxDispatch = 'INF')
            else: time.sleep(0.001)
            
            #Process FAR/FARR
            self.ipcA_MAIN.processFARs(); self.ipcA_ATM.processFARs()
            self.ipcA_MAIN.processFARRs(); self.ipcA_ATM.processFARRs()
            
        #Termination Sequence
        self.ipcA_ATM.terminate()
        self.ipcA_ATM.join()

        self.ipcA_MAIN.sendPRDEDIT("PROCSTATUS", "TERMINATED", nMaxDispatch = 'INF')
        self.ipcAThread_MAIN.terminate()
        self.ipcAThread_MAIN.join()

    #Manager Process Loop END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Manager Internal Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __issueSimulationCode(self, apiSymbol):
        indexOfInterest = 0
        while (True):
            simulationCode = "{:s}_{:d}".format(apiSymbol, indexOfInterest)
            if ((simulationCode in self.simulator_Simulations_Processing) or (simulationCode in self.simulator_Simulations_Completed)): indexOfInterest += 1
            else: break
        return simulationCode

    def __existsSimulationCode(self, simulationCode):
        return ((simulationCode in self.simulator_Simulations_Processing) or (simulationCode in self.simulator_Simulations_Completed))

    def __addSimulationQueue(self, simulationCode, currencyInfo, simulationConfig):
        self.simulator_Simulations_Processing[simulationCode] = simulation(self, simulationCode, currencyInfo, simulationConfig)
        self.simualtor_SimulationQueue.append(simulationCode)
        simulationStat_PRD = {'simulationProcess':           'PENDING',
                              'simulationProcess_perc':      0,
                              'simulationProcess_percTotal': 0,
                              'simulationRange':             simulationConfig['simulationRange'],
                              'simulationRange_realTime':    simulationConfig['simulationRange_RealTime'],
                              'estimatedCompletionTime':     None,
                              'resultType':                  simulationConfig['resultType']}
        self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_PROCESSING", simulationCode), simulationStat_PRD, nMaxDispatch = 'INF')
        if (len(self.simualtor_SimulationQueue) == 1): 
            self.simulator_Simulations_Processing[simulationCode].startSimulator()
            self.ipcA_MAIN.sendPRDEDIT('CURRENTANALYSIS', self.simualtor_SimulationQueue[0], nMaxDispatch = 'INF')

    def __checkDBConnection(self):
        dbConnected = self.ipcA_ATM.getPRD(('DBSTATUS', 'connected'))
        #Disconnection Handling
        if ((self.dbConnected == True) and (dbConnected == False)):
            self.dbConnected    = False
            self.dbRecordLoaded = False
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'DB Disconnection Detected'}, nMaxDispatch = 'INF')
        #Connection Handling
        elif ((self.dbConnected == False) and (dbConnected == True)):
            self.dbConnected    = True
            self.dbRecordLoaded = False
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'DB Connection Detected'}, nMaxDispatch = 'INF')
    #Manager Internal Functions END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




    #FAR Hanlder Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #<MAIN FAR Handlers>
    #Raise Process Termination Flag
    def far_RaiseTerminationFlag(self, functionParams): self.process_terminate = True

    #Add Simulation Verification Process
    def farHandler_ADDSIMULATIONQUEUE(self, functionParams):
        request_apiSymbol = functionParams['apiSymbol']
        request_simConfig = functionParams['simConfig']

        #Verification Step 1 - Database Connection and Availability Check
        #---DB Connectivity Check
        dbConnected = self.ipcA_ATM.getPRD(('DBSTATUS', 'connected'))
        if (dbConnected == False):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Database Not Connected'}, nMaxDispatch = 'INF')
            return False
        #---DB Volume Availability Check
        dbAvailability = self.ipcA_ATM.getPRD(('DBSTATUS', 'volume_classification', 'analysisSaveAvailable'))
        if (dbAvailability == False):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Check Database Space Availability'}, nMaxDispatch = 'INF')
            return False
        #---DB Record Load Check
        if (self.dbRecordLoaded == False):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Analysis Data Within The Database Not Yet Identified, Try Again Later'}, nMaxDispatch = 'INF')
            return False



        #Verification Step 2 - Check Simulation Code
        request_simulationCode            = request_simConfig['simulationCode']
        request_simulationCodeAutoReplace = request_simConfig['simulationCodeAutoReplace']
        effective_simulationCode = None
        #---If No Requested SimCode Exist, Use Auto-Generated Simulation Code
        if (request_simulationCode == None): effective_simulationCode = self.__issueSimulationCode(request_apiSymbol)
        #---If Requested SimCode Exists, Check it's existence within the database and if does, see if it can be auto-replace. If not auto-replacable, reject the request
        else:
            if (self.__existsSimulationCode(request_simulationCode) == True):
                #If the requested simulation code cannot be used and can be replaced automatically, issue a system generated simulation code
                if (request_simulationCodeAutoReplace == True): effective_simulationCode = self.__issueSimulationCode(request_apiSymbol)
                #If the requested simulation code cannot be used and cannot be replaced automatically, reject the request
                else:
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Requested Simulation Code Already Exists and Cannot Be Auto-Replaced'}, nMaxDispatch = 'INF')
                    return False
            else: effective_simulationCode = request_simulationCode



        #Verification Step 3 - Check Ranges
        request_simRange          = request_simConfig['simulationRange']
        request_simRange_RealTime = request_simConfig['simulationRange_RealTime']
        #---RunTime Analysis
        if (request_simRange_RealTime == True):
            daPerc = self.ipcA_ATM.getPRD(('MARKETASSETS', request_apiSymbol, 'dataRanges_perc', 0))
            if (daPerc == 100):
                mrktRegTS = self.ipcA_ATM.getPRD(('MARKETASSETS', request_apiSymbol, 'mrktRegTS', 0))
                if (mrktRegTS <= request_simRange[0]): request_simConfig['simulationRange'] = (request_simRange[0], None)
                else:
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Simulation Must Begin At or After The First Raw 1m Kline'}, nMaxDispatch = 'INF')
                    return False
            else:
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Kline Data Not Fully Prepared, Try Again Later'}, nMaxDispatch = 'INF')
                return False
        #---Non-RunTime Analysis
        else:
            dataRanges = self.ipcA_ATM.getPRD(('MARKETASSETS', request_apiSymbol, 'dataRanges', 0))
            testPassed = False
            for dataRange in dataRanges:
                if ((dataRange[0] <= request_simRange[0]) and (request_simRange[1] <= dataRange[1])): testPassed = True; break
            if (testPassed == False):
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Kline Data Block Not Fully Prepared For The Simulation Range, Try Again Later'}, nMaxDispatch = 'INF')
                return False



        #Verification Step 4 - Check Configurations
        time.sleep(0.5)



        #Verification Step 5 - Currency Market Info Gathering
        currencyInfo_ATM = self.ipcA_ATM.getPRD(("MARKETASSETS", request_apiSymbol))
        if (currencyInfo_ATM == '#DNF#'):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Append Failed: Currency Data Not Found Within the Market'}, nMaxDispatch = 'INF')
            return False
        currencyInfo_reformed = {'apiSymbol': request_apiSymbol}
        simulationConfig_reformed = {'resultType':               request_simConfig['resultType'],
                                     'simulationRange_RealTime': request_simConfig['simulationRange_RealTime'],
                                     'simulationRange':          request_simConfig['simulationRange']}



        #Verification Step 6 - Finalize
        self.__addSimulationQueue(simulationCode   = effective_simulationCode,
                                  currencyInfo     = currencyInfo_reformed,
                                  simulationConfig = simulationConfig_reformed)
        self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "Simulation '{:s}' Successfully Added To The Queue!".format(effective_simulationCode)}, nMaxDispatch = 'INF')
        return True



        
        
    #Pause Simulation
    def farHandler_PAUSESIMULATION(self, functionParams):
        if (self.simulator_pause == False):
            self.simulator_pause = True
            self.ipcA_MAIN.sendPRDEDIT("SIMULATION_RUNNING", not(self.simulator_pause), nMaxDispatch = 'INF')
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Paused'}, nMaxDispatch = 'INF')
        else: self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation is Already Paused'}, nMaxDispatch = 'INF')
        return True



    #Resume Simulation
    def farHandler_RESUMESIMULATION(self, functionParams):
        if (self.simulator_pause == True): 
            self.simulator_pause = False
            self.ipcA_MAIN.sendPRDEDIT("SIMULATION_RUNNING", not(self.simulator_pause), nMaxDispatch = 'INF')
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Resumed'}, nMaxDispatch = 'INF')
        else: self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation is Already Running'}, nMaxDispatch = 'INF')
        return True



    #Remove Simulation
    def farHandler_REMOVESIMULATION(self, functionParams):
        simulationCode = functionParams['simulationCode']
        if (simulationCode in self.simulator_Simulations_Processing):
        #If is a running simulation, have it enter termination sequence
            if (simulationCode == self.simualtor_SimulationQueue[0]): 
                self.simulator_Simulations_Processing[simulationCode].terminateSimulator('REMOVAL')
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Will Be Terminated And Removed'}, nMaxDispatch = 'INF')
        #If is a pending simulation, simply remove it from the queue
            else:
                del self.simulator_Simulations_Processing[simulationCode]
                self.simualtor_SimulationQueue.remove(simulationCode)
                self.ipcA_MAIN.sendPRDREMOVE(("SIMULATIONS_PROCESSING", simulationCode))
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation is Removed from the Queue'}, nMaxDispatch = 'INF')
            return True
        #If is a completed simulation, send analysis data removal request to ATM
        elif (simulationCode in self.simulator_Simulations_Completed):
            self.ipcA_ATM.sendFAR(functionID = 'REMOVEANALYSISDATA', functionParams = {'simulationCode': simulationCode}, FARRHandler = self.farHandler_REMOVESIMULATION_responseHandler, nMaxDispatch = 'INF')
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Data Removal Request Sent'}, nMaxDispatch = 'INF')
            return True
        #No Simulation Data Found
        else: 
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Removal Failed: Simulation Data Not Found'}, nMaxDispatch = 'INF')
            return False
    def farHandler_REMOVESIMULATION_responseHandler(self, functionResult):
        removalResult  = functionResult[0]
        simulationCode = functionResult[1]

        if (removalResult == True):
            del self.simulator_Simulations_Completed[simulationCode]
            self.ipcA_MAIN.sendPRDREMOVE(("SIMULATIONS_COMPLETED", simulationCode), nMaxDispatch = 'INF')
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "Simulation '{:s}' Data Successfully Removed From The Database".format(simulationCode)}, nMaxDispatch = 'INF')
            print(termcolor.colored("[AUX] Simulation '{:s}' Data Successfully Removed From The Database".format(simulationCode), 'light_green'))
        else:
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "Simulation Removal Failed: {:s}".format(str(functionResult))}, nMaxDispatch = 'INF')
            print(termcolor.colored("[AUX] Simulation Removal Failed: {:s}".format(str(functionResult)), 'light_red'))

    #Terminate Simulation (Only valid for real-time simulation)
    def farHandler_TERMINATESIMULATION(self, functionParams):
        simulationCode = functionParams['simulationCode']
        if (simulationCode in self.simulator_Simulations_Processing):
            if (simulationCode == self.simualtor_SimulationQueue[0]):
                currnetProcess = self.simulator_Simulations_Processing[simulationCode].getCurrentProcess()
                if (currnetProcess == 'RESULT SAVING'):
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: The Simulation is Already Saving Results'}, nMaxDispatch = 'INF')
                    return False
                elif (currnetProcess == 'TERMINATION SEQUENCE'): 
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: The Simulation is Already in Termination Sequence'}, nMaxDispatch = 'INF')
                    return False
                elif (currnetProcess == 'COMPLETE'):
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: The Simulation has Already Been Completed'}, nMaxDispatch = 'INF')
                    return False
                elif (currnetProcess == 'TERMINATED'):
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: The Simulation has Already Been Terminated'}, nMaxDispatch = 'INF')
                    return False
                else:
                    self.simulator_Simulations_Processing[simulationCode].terminateSimulator('TERMINATE')
                    self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'The Simulation Will Enter Termination Sequence'}, nMaxDispatch = 'INF')
                    return True
            else: 
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: Pending Simulation Cannot Be Terminated'}, nMaxDispatch = 'INF')
                return False
        elif (simulationCode in self.simulator_Simulations_Completed):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: Completed Simulation Cannot Be Terminated'}, nMaxDispatch = 'INF')
            return False
        else:
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': 'Simulation Termination Failed: Simulation Data Not Found'}, nMaxDispatch = 'INF')
            return False



    #<ATM FAR Handlers>
    def farHandler_RECEIVEANALYSISSUMMARYRECORDS(self, functionParams):
        self.dbConnected = True
        self.dbRecordLoaded = True
        analysisSummaries = functionParams['analysisSummaries']
        for simulationCode in analysisSummaries:
            summary = analysisSummaries[simulationCode]
            self.simulator_Simulations_Completed[simulationCode] = {'analysisType':    summary['analysisType'],
                                                                    'apiSymbol':       summary['apiSymbol'],
                                                                    'simulationRange': (summary['simulationRangeBEG'], summary['simulationRangeEND']),
                                                                    'simulatedRange':  (summary['simulatedRangeBEG'],  summary['simulatedRangeEND']),
                                                                    'resultType':      summary['resultType'],
                                                                    'resultSummary':   summary['resultSummary'],
                                                                    'dbTableName':     summary['dbTableName']}
            self.ipcA_MAIN.sendPRDEDIT(("SIMULATIONS_COMPLETED", simulationCode), self.simulator_Simulations_Completed[simulationCode], nMaxDispatch = 'INF')

    #FAR Hanlder Functions END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


















class simulation:
    def __init__(self, managerInstance, simulationCode, currencyInfo, simulationConfig):
        self.managerInstance = managerInstance
        self.ipcA_ATM  = self.managerInstance.ipcA_ATM
        self.ipcA_MAIN = self.managerInstance.ipcA_MAIN

        #Configurations
        self.simulationCode = simulationCode

        self.currencyInfo_apiSymbol = currencyInfo['apiSymbol']

        self.config_analysisType = 1
        self.config_resultType = simulationConfig['resultType']
        self.config_realTime   = simulationConfig['simulationRange_RealTime']
        self.config_simRange   = simulationConfig['simulationRange']
        
        if (self.config_realTime == True):
            self.effectiveSimulationRangeBeg = self.config_simRange[0]
            self.effectiveSimulationRangeEnd = None
        else:
            self.effectiveSimulationRangeBeg = self.config_simRange[0]
            self.effectiveSimulationRangeEnd = self.config_simRange[1]

        #Process Control Parameters
        if (self.config_realTime == True):
            self.simulationProcesses = {'PENDING': None,
                                        'KLINES COLLECTION':                self.__process_klinesCollection,               #Total Completion Contributor 1
                                        'PRE-REALTIME ANALYSIS':            self.__process_PreRealTimeAnalysis,            #Total Completion Contributor 2
                                        'REALTIME ANALYSIS':                self.__process_RealTimeAnalysis,
                                        'REALTIME ANALYSIS INTERPRETATION': self.__process_RealTimeAnalysisInterpretation,
                                        'TERMINATION SEQUENCE':             self.__process_terminationSequence,
                                        'TERMINATED':                       None}
            self.simluationProcesses_totalCompletion_max = 200
        else:
            self.simulationProcesses = {'PENDING':                 None,
                                        'KLINES COLLECTION':       self.__process_klinesCollection,       #Total Completion Contributor 1
                                        'ANALYSIS':                self.__process_analysis,               #Total Completion Contributor 2
                                        'ANALYSIS INTERPRETATION': self.__process_analysisInterpretation, #Total Completion Contributor 3
                                        'RESULT SAVING':           self.__process_resultSaving,           #Total Completion Contributor 4
                                        'COMPLETED':               None,
                                        'TERMINATION SEQUENCE':    self.__process_terminationSequence,
                                        'TERMINATED':              None}
            self.simluationProcesses_totalCompletion_max = 400

        self.process_currentProcess                   = "PENDING"
        self.process_currentProcess_currentSubProcess = 0
        self.simulationProcesses_currentCompletion = 0
        self.simluationProcesses_totalCompletion   = 0
        self.estimatedCompletionTime = None
        self.completionType = 'COMPLETED'

        #Analysis Parameters
        self.klines = dict()
        self.klines_timestamps = list()
        self.analyzedKlines = list()
        self.validInvestmentPoints = list()

        #Process-Dependent Analysis Parameters
        self.pdap_klinesCollection_fetchCompletion = None
        self.pdap_klinesCollection_fetchComplete = False

        self.pdap_analysis_analyzerFunction = ATM_Zeta_Analyzers.klineAnalyzer_tester
        self.pdap_analysis_targetKlineIndex = 0

        self.pdap_resultSaving_analyzedKlineFormat  = ATM_Zeta_Analyzers.klineAnalyzer_getFormatter()
        self.pdap_resultSaving_resultTableFormat    = ATM_Zeta_Analyzers.klineAnalyzer_getTableFormat()
        self.pdap_resultSaving_targetKlineIndex = 0
        self.pdap_resultSaving_collectionBlockIndex = 0
        self.pdap_resultSaving_isLastBlock = False
        
        self.pdap_termination_targetKlineIndex = 0

    def process(self):
        #Run current simulation process
        return (self.simulationProcesses[self.process_currentProcess]() == True)

    #SIMULATION CONTROL & INFORMATION ACCESS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Start the simulator by setting 'self.process_currentProcess' to 'KLINES COLLECTION'
    def startSimulator(self):
        self.process_currentProcess                   = 'KLINES COLLECTION'
        self.process_currentProcess_currentSubProcess = 0
        self.simulationProcesses_currentCompletion    = 0
        self.simluationProcesses_totalCompletion      = 0

    #Start the simulator's termination sequence
    def terminateSimulator(self, terminationCause):
        if   (terminationCause == 'TERMINATE'): self.completionType = 'TERMINATION'
        elif (terminationCause == 'REMOVAL'):   self.completionType = 'REMOVAL'
        self.ipcA_ATM.sendFAR(functionID = 'REMOVEKLINESUBSCRIPTION', functionParams = {'requesterID': 'SIMULATOR', 'apiSymbol': self.currencyInfo_apiSymbol, 'intervalID': 0}, 
                              FARRHandler = self.__terminateSimulator_klineSubscriptionRemovalResponseHandler, nMaxDispatch = 'INF')
    def __terminateSimulator_klineSubscriptionRemovalResponseHandler(self, functionResult):
        if (functionResult == True):
            self.process_currentProcess                   = 'TERMINATION SEQUENCE'
            self.process_currentProcess_currentSubProcess = 0
            self.simulationProcesses_currentCompletion    = 0
            self.simluationProcesses_totalCompletion      = 0
        else: 
            print(termcolor.colored("[SIMULATOR] User Attention Advised, Kline Subscription Removal Request For Entering Termination Sequence Rejected", 'light_red'))
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "User Attention Advised, Kline Subscription Removal Request For Entering Termination Sequence Rejected".format(self.simulationCode)}, nMaxDispatch = 'INF')

    def isRealTime(self):
        return self.config_realTime

    def getCompletionType(self):
        return self.completionType

    #Return the completion percentage of the current process
    def getCompletionPerc(self):
        if (self.simulationProcesses_currentCompletion == None): return None
        else:                                                    return round(self.simulationProcesses_currentCompletion, 3)

    #Return the completion percentage of the entire simulation
    def getCompletionPercTotal(self):
        if (self.config_realTime == True): 
            if (self.simluationProcesses_totalCompletion == None): return None
            else:                                                  return round(self.simluationProcesses_totalCompletion/300*100, 3)
        else:                                                      return round(self.simluationProcesses_totalCompletion/self.simluationProcesses_totalCompletion_max*100, 3)

    #Return the current process name
    def getCurrentProcess(self):
        return self.process_currentProcess

    #Return the estimated completion time of the current process
    def getEstimatedCompletionTime(self):
        return self.estimatedCompletionTime
    #SIMULATION CONTROL & INFORMATION ACCESS END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









    #SIMULATION PROCESSES ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #---General Sequences
    #------klineCollection
    def __process_klinesCollection(self): #'KLINES COLLECTION' -> 'KLINES VERIFICATION'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #SUBPROCESS 1/2: 'addKlinesSubscription'
        if (self.process_currentProcess_currentSubProcess == 0):
            self.ipcA_ATM.sendFAR(functionID = 'ADDKLINESUBSCRIPTION', 
                                  functionParams = {'requesterID': 'SIMULATOR', 'apiSymbol': self.currencyInfo_apiSymbol, 'intervalID': 0, 'subscriptionRange': (self.effectiveSimulationRangeBeg, self.effectiveSimulationRangeEnd)}, 
                                  FARRHandler = self.__klineSubscriptionResponseHandler, 
                                  nMaxDispatch = 'INF')
            self.ipcA_ATM.addFARHandler("KLINERECEIVER_SIMULATOR", self.__klineReceiver)
            self.pdap_klinesCollection_fetchCompletion = 0

            #Move to the next subprocess
            self.simulationProcesses_currentCompletion = 10
            self.process_currentProcess_currentSubProcess = 1

        #SUBPROCESS 2/2: 'trackKlinesFetchCompletion'
        elif (self.process_currentProcess_currentSubProcess == 1):
            if (self.pdap_klinesCollection_fetchCompletion < 100): self.simulationProcesses_currentCompletion = 10 + (80*self.pdap_klinesCollection_fetchCompletion/100)
            else:                                                  self.simulationProcesses_currentCompletion = 10 + 80; self.process_currentProcess_currentSubProcess = 2

        #SUBPROCESS 2/2: 'generateIndexedKlineAccess'
        elif (self.process_currentProcess_currentSubProcess == 2):
            self.klines_timestamps = list(self.klines.keys())
            self.klines_timestamps.sort()
            self.pdap_klinesCollection_fetchComplete = True
            self.simulationProcesses_currentCompletion = 100
            self.process_currentProcess_currentSubProcess = None

        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Completion Tracker Update
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simulationProcesses_currentCompletion = 0
            self.simluationProcesses_totalCompletion   = 100
            if (self.config_realTime == True): self.process_currentProcess = 'PRE-REALTIME ANALYSIS'
            else:                              self.process_currentProcess = 'ANALYSIS'
            self.process_currentProcess_currentSubProcess = 0
            return
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion
    def __klineReceiver(self, functionParams):
        if ((functionParams['apiSymbol'] == self.currencyInfo_apiSymbol) and (functionParams['intervalID'] == 0)):
            klines = functionParams['klines']
            if (self.pdap_klinesCollection_fetchComplete == True):
                for kline in klines:
                    open_ts = int(kline[0]%1e10)
                    self.klines[open_ts] = {'raw': (open_ts,) + kline[1:]}
                    self.klines_timestamps.append(open_ts)
            else:
                for kline in klines:
                    open_ts = int(kline[0]%1e10)
                    self.klines[open_ts] = {'raw': (open_ts,) + kline[1:]}
                if (('completion' in functionParams) and (functionParams['completion'] != None)): self.pdap_klinesCollection_fetchCompletion = functionParams['completion']
        else: print(termcolor.colored("[SIMULATOR] Unexpected Klines Received For {:s}_{:d} When {:s}_{:d} Was Expected".format(functionParams['apiSymbol'], functionParams['intervalID'], self.currencyInfo_apiSymbol, 0)))
    def __klineSubscriptionResponseHandler(self, functionResult):
        if (functionResult == False):
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "Simulation '{:s}' Aborted: Kline Subscription Request Rejected".format(self.simulationCode)}, nMaxDispatch = 'INF')
            self.terminateSimulator('REMOVAL')








        
    #---Real Time Sequences
    #------Perform Defined Analysis on Pre-RealTime Data
    def __process_PreRealTimeAnalysis(self): #'PRE-REALTIME ANALYSIS' -> 'REALTIME ANALYSIS'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #SUBPROCESS 1/1:
        if (self.process_currentProcess_currentSubProcess == 0):
            pass
            """
            increment = 0.01
            self.simulationProcesses_currentCompletion += increment

            #Process Completion Determiner
            if (100 <= self.simulationProcesses_currentCompletion): self.process_currentProcess_currentSubProcess = None
            """
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Upon Completion
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simulationProcesses_currentCompletion = None
            self.simluationProcesses_totalCompletion   = None
            self.process_currentProcess                   = 'REALTIME ANALYSIS'
            self.process_currentProcess_currentSubProcess = 0
            return
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion + 100



    #------Perform Real-Time Analysis
    def __process_RealTimeAnalysis(self): #'REALTIME ANALYSIS' -> 'REALTIME ANALYSIS INTERPRETATION' (Only called purposefully by the user, will keep runnning forever otherwise)
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        time.sleep(0.001)
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #------Interpret Analysis Result Created So Far
    def __process_RealTimeAnalysisInterpretation(self): #'REALTIME ANALYSIS INTERPRETATION' -> 'TERMINATION SEQUENCE'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #SUBPROCESS 1/1:
        if (self.process_currentProcess_currentSubProcess == 0):
            increment = 0.01
            self.simulationProcesses_currentCompletion += increment

            #Process Completion Determiner
            if (100 <= self.simulationProcesses_currentCompletion): self.process_currentProcess_currentSubProcess = None
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Upon Completion
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simulationProcesses_currentCompletion = 0
            self.simluationProcesses_totalCompletion   = 100
            self.process_currentProcess                   = 'TERMINATION SEQUENCE'
            self.process_currentProcess_currentSubProcess = 0
            return
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion










    #---Defined Range Simulation Sequences
    #------Perform First Order Analysis
    def __process_analysis(self): #'ANALYSIS' -> 'ANALYSIS INTERPRETATION'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #SUBPROCESS 1/1:
        if (self.process_currentProcess_currentSubProcess == 0):
            pass
            """
            #SIMULATIONPROCESSTIMELIMIT_NS
            startTime_ns = time.perf_counter_ns()
            nLoadedKlines = len(self.rawKlines)
            initialIndex = self.pdap_analysis_targetKlineIndex
            while (True):
                #Kline Analysis
                self.analyzedKlines.append(self.pdap_analysis_analyzerFunction(self.rawKlines[self.pdap_analysis_targetKlineIndex], self.pdap_analysis_targetKlineIndex))

                #Target Kline Index Update
                self.pdap_analysis_targetKlineIndex += 1
                if (self.pdap_analysis_targetKlineIndex == nLoadedKlines) or (SIMULATIONPROCESSTIMELIMIT_NS < time.perf_counter_ns()-startTime_ns): break

            #Estimated Completion Time Calculation
            endTime_ns = time.perf_counter_ns()
            nProcessedKlines  = self.pdap_analysis_targetKlineIndex - initialIndex
            processingTime_ns = endTime_ns - startTime_ns
            self.estimatedCompletionTime = processingTime_ns / nProcessedKlines * (nLoadedKlines - self.pdap_analysis_targetKlineIndex)

            #Completion Calculation
            self.simulationProcesses_currentCompletion = round(self.pdap_analysis_targetKlineIndex/nLoadedKlines*100, 3)

            #Completion Handling
            if (self.pdap_analysis_targetKlineIndex == nLoadedKlines):
                self.simulationProcesses_currentCompletion = 100
                self.process_currentProcess_currentSubProcess = None
            """
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Completion Tracker Update
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simulationProcesses_currentCompletion = 0
            self.simluationProcesses_totalCompletion   = 200
            self.process_currentProcess                   = 'ANALYSIS INTERPRETATION'
            self.process_currentProcess_currentSubProcess = 0
            return
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion + 100





    #------Interpret the first and the second order analysis results
    def __process_analysisInterpretation(self): #'ANALYSIS INTERPRETATION' -> 'RESULT SAVING'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #SUBPROCESS 1/1:
        if (self.process_currentProcess_currentSubProcess == 0):
            increment = 0.01
            self.simulationProcesses_currentCompletion += increment

            #Process Completion Determiner
            if (100 <= self.simulationProcesses_currentCompletion): self.process_currentProcess_currentSubProcess = None
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Completion Tracker Update
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simulationProcesses_currentCompletion = 0
            self.simluationProcesses_totalCompletion   = 300
            self.process_currentProcess                   = 'RESULT SAVING'
            self.process_currentProcess_currentSubProcess = 0
            return
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion + 200










    #---Completion & Termination Sequences
    #------Save Simulatino Result
    def __process_resultSaving(self): #'RESULT SAVING' -> 'COMPLETED'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # * SUBPROCESS 0: saveResultSummary
        # * SUBPROCESS 1: saveResultSummary_waitingATMResponse
        # * SUBPROCESS 2: saveFullResult
        # * SUBPROCESS 3: saveFullResult_waitingATMResponse
        # * SUBPROCESS 4: resultSaveComplete

        #SUBPROCESS 0: 'saveResultSummary'
        if (self.process_currentProcess_currentSubProcess == 0):
            if (0 < len(self.analyzedKlines)):
                simulatedRangeBeg = self.analyzedKlines[0][0]
                simulatedRangeEnd = self.analyzedKlines[-1][1]
            else:
                simulatedRangeBeg = None
                simulatedRangeEnd = None

            resultSummary = {'analysisType':      self.config_analysisType,
                             'simulationCode':    self.simulationCode,
                             'apiSymbol':         self.currencyInfo_apiSymbol,
                             'simulationRangeBEG': self.effectiveSimulationRangeBeg,
                             'simulationRangeEND': self.effectiveSimulationRangeEnd,
                             'simulatedRangeBEG':  simulatedRangeBeg,
                             'simulatedRangeEND':  simulatedRangeEnd,
                             'resultType':        self.config_resultType,
                             'resultSummary_str': "COMPLETED",
                             'resultTableFormat': self.pdap_resultSaving_resultTableFormat}
            self.ipcA_ATM.sendFAR(functionID = 'SAVEANALYSISRESULT', functionParams = {'saveRequestType': 'summary', 'result': resultSummary, 'returnRecords': (self.config_resultType == "SUMMARY")}, FARRHandler = self.__analysisResultSaveResponseHandler, nMaxDispatch = 'INF')
            if   (self.config_resultType == "COMPLETE"): self.simulationProcesses_currentCompletion = 10
            elif (self.config_resultType == "SUMMARY"):  self.simulationProcesses_currentCompletion = 50
            self.process_currentProcess_currentSubProcess = 1

        #SUBPROCESS 2: 'saveFullResult'
        elif (self.process_currentProcess_currentSubProcess == 2):
            startTime_ns = time.perf_counter_ns()
            nAnalyzedKlines = len(self.analyzedKlines)
            klinesCollection = list()

            #Collection Block Indexing
            if (self.pdap_resultSaving_collectionBlockIndex == None): self.pdap_resultSaving_collectionBlockIndex = 0
            else:                                                     self.pdap_resultSaving_collectionBlockIndex += 1

            #Analyzed Klines Collection
            while (True):
                #Klines Collection for Saving
                klinesCollection.append(self.analyzedKlines[self.pdap_resultSaving_targetKlineIndex])

                #Target Kline Index Update
                self.pdap_resultSaving_targetKlineIndex += 1
                if (self.pdap_resultSaving_targetKlineIndex == nAnalyzedKlines): self.pdap_resultSaving_isLastBlock = True; break #Collection Complete
                if (len(klinesCollection) == KLINESAVEPERPROCESSLIMIT):          break                                            #Collection Limit Reached

            self.ipcA_ATM.sendFAR(functionID = 'SAVEANALYSISRESULT', functionParams = {'saveRequestType':         'analyzedKlines', 
                                                                                       'simulationCode':          self.simulationCode, 
                                                                                       'analyzedKlines':          klinesCollection, 
                                                                                       'analyzedKlines_contents': self.pdap_resultSaving_analyzedKlineFormat, 
                                                                                       'blockIndex':              self.pdap_resultSaving_collectionBlockIndex, 
                                                                                       'isLastBlock':             self.pdap_resultSaving_isLastBlock},
                                  FARRHandler = self.__analysisResultSaveResponseHandler, nMaxDispatch = 'INF')

            #Estimated Completion Time Calculation
            self.estimatedCompletionTime = (time.perf_counter_ns()-startTime_ns) / len(klinesCollection) * (nAnalyzedKlines - self.pdap_resultSaving_targetKlineIndex)

            #Completion Calculation
            self.simulationProcesses_currentCompletion = 10 + round(self.pdap_resultSaving_targetKlineIndex/nAnalyzedKlines*85, 3)
            
            self.process_currentProcess_currentSubProcess = 3
            
        #SUBPROCESS 4: 'resultSaveComplete'
        elif (self.process_currentProcess_currentSubProcess == 4):
            self.simulationProcesses_currentCompletion = 100
            self.process_currentProcess_currentSubProcess = None
        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Completion Tracker Update
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simluationProcesses_totalCompletion = 400
            self.process_currentProcess                   = 'COMPLETED'
            self.process_currentProcess_currentSubProcess = 0
            return True
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion + 300





    #------Termination Sequence
    def __process_terminationSequence(self): #'TERMINATION SEQUENCE' -> 'TERMINATED'
        #<SUB PROCESSES> --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # * SUBPROCESS 0: removalOrSummarySaveRequest
        # * SUBPROCESS 1: removalRequest_waitingATMResponse
        # * SUBPROCESS 2: summarySaveRequest_waitingATMResponse
        # * SUBPROCESS 3: saveFullResult
        # * SUBPROCESS 4: saveFullResult_waitingATMResponse
        # * SUBPROCESS 5: terminationCompletion

        #SUBPROCESS 0:
        if (self.process_currentProcess_currentSubProcess == 0):
            #If this is terminating for 'REMOVAL'
            if (self.completionType == 'REMOVAL'):
                self.ipcA_ATM.sendFAR(functionID = 'REMOVEANALYSISDATA', functionParams = {'simulationCode': self.simulationCode}, FARRHandler = self.__process_terminationSequence_analysisRemovalResponseHandler, nMaxDispatch = 'INF')
                self.simulationProcesses_currentCompletion = 50
                self.process_currentProcess_currentSubProcess = 1

            #If this is terminating for 'TERMINATE'
            elif (self.completionType == 'TERMINATION'):
                if (0 < len(self.analyzedKlines)):
                    simulatedRangeBeg = self.analyzedKlines[0][0]
                    simulatedRangeEnd = self.analyzedKlines[-1][1]
                else:
                    simulatedRangeBeg = None
                    simulatedRangeEnd = None

                resultSummary = {'analysisType':      self.config_analysisType,
                                 'simulationCode':    self.simulationCode,
                                 'apiSymbol':         self.currencyInfo_apiSymbol,
                                 'simulationRangeBEG': self.effectiveSimulationRangeBeg,
                                 'simulationRangeEND': self.effectiveSimulationRangeEnd,
                                 'simulatedRangeBEG':  simulatedRangeBeg,
                                 'simulatedRangeEND':  simulatedRangeEnd,
                                 'resultType':        self.config_resultType,
                                 'resultSummary_str': "TERMINATED",
                                 'resultTableFormat': self.pdap_resultSaving_resultTableFormat}
                self.ipcA_ATM.sendFAR(functionID = 'SAVEANALYSISRESULT', functionParams = {'saveRequestType': 'summary', 'result': resultSummary, 'returnRecords': ((self.config_resultType == "SUMMARY") or (0 == len(self.analyzedKlines)))}, FARRHandler = self.__analysisResultSaveResponseHandler, nMaxDispatch = 'INF')
                if   (self.config_resultType == "COMPLETE"): self.simulationProcesses_currentCompletion = 10
                elif (self.config_resultType == "SUMMARY"):  self.simulationProcesses_currentCompletion = 50
                self.process_currentProcess_currentSubProcess = 2
            
        #SUBPROCESS 3:
        elif (self.process_currentProcess_currentSubProcess == 3):
            startTime_ns = time.perf_counter_ns()
            nAnalyzedKlines = len(self.analyzedKlines)
            klinesCollection = list()

            #Collection Block Indexing
            if (self.pdap_resultSaving_collectionBlockIndex == None): self.pdap_resultSaving_collectionBlockIndex = 0
            else:                                                     self.pdap_resultSaving_collectionBlockIndex += 1

            #Analyzed Klines Collection
            while (True):
                #Klines Collection for Saving
                print(self.pdap_termination_targetKlineIndex, nAnalyzedKlines)
                klinesCollection.append(self.analyzedKlines[self.pdap_termination_targetKlineIndex])

                #Target Kline Index Update
                self.pdap_termination_targetKlineIndex += 1
                if (self.pdap_termination_targetKlineIndex == nAnalyzedKlines): self.pdap_resultSaving_isLastBlock = True; break #Collection Complete
                if (len(klinesCollection) == KLINESAVEPERPROCESSLIMIT):         break                                            #Collection Limit Reached
                
            self.ipcA_ATM.sendFAR(functionID = 'SAVEANALYSISRESULT', functionParams = {'saveRequestType':         'analyzedKlines', 
                                                                                       'simulationCode':          self.simulationCode, 
                                                                                       'analyzedKlines':          klinesCollection, 
                                                                                       'analyzedKlines_contents': self.pdap_resultSaving_analyzedKlineFormat, 
                                                                                       'blockIndex':              self.pdap_resultSaving_collectionBlockIndex, 
                                                                                       'isLastBlock':             self.pdap_resultSaving_isLastBlock},
                                  FARRHandler = self.__analysisResultSaveResponseHandler, nMaxDispatch = 'INF')

            #Estimated Completion Time Calculation
            self.estimatedCompletionTime = (time.perf_counter_ns()-startTime_ns) / len(klinesCollection) * (nAnalyzedKlines - self.pdap_termination_targetKlineIndex)

            #Completion Calculation
            self.simulationProcesses_currentCompletion = 10 + round(self.pdap_termination_targetKlineIndex/nAnalyzedKlines*85, 3)
            
            self.process_currentProcess_currentSubProcess = 4
            
        #SUBPROCESS 5:
        elif (self.process_currentProcess_currentSubProcess == 5):
            self.simulationProcesses_currentCompletion = 100
            self.process_currentProcess_currentSubProcess = None

        #<SUB PROCESSES END> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Completion Tracker Update
        elif (self.process_currentProcess_currentSubProcess == None):
            self.simluationProcesses_totalCompletion = 100
            self.process_currentProcess                   = 'TERMINATED'
            self.process_currentProcess_currentSubProcess = 0
            return True
        self.simluationProcesses_totalCompletion = self.simulationProcesses_currentCompletion
        
    def __process_terminationSequence_analysisRemovalResponseHandler(self, functionResult):
        if (functionResult[0] == True):
            if (self.process_currentProcess_currentSubProcess == 1): self.process_currentProcess_currentSubProcess = 5
            else:
                self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "User attention advised, analysis removal completion signal received when not expected".format(self.simulationCode)}, nMaxDispatch = 'INF')
                print(termcolor.colored("[SIMULATOR {:s}] User attention advised, analysis removal completion signal received when not expected".format(self.simulationCode), 'light_red'))
        else:
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "User attention advised, analysis removal for termination sequence failed".format(self.simulationCode)}, nMaxDispatch = 'INF')
            print(termcolor.colored("[SIMULATOR {:s}] User attention advised, analysis removal for termination sequence failed".format(self.simulationCode), 'light_red'))

    #SIMULATION PROCESSES END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    


    def __analysisResultSaveResponseHandler(self, functionResult):
        saveResult  = functionResult['saveResult']
        requestType = functionResult['requestType']
        blockIndex  = functionResult['blockIndex']

        if (saveResult == True):
            #Save Completion during 'RESULT SAVING'
            if (self.process_currentProcess == 'RESULT SAVING'):
                if (requestType == 'summary'):
                    if (self.process_currentProcess_currentSubProcess == 1): 
                        if   (self.config_resultType == 'COMPLETE'): self.process_currentProcess_currentSubProcess = 2
                        elif (self.config_resultType == 'SUMMARY'):  self.process_currentProcess_currentSubProcess = 4
                    else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: SubProcess Mismatch (Expected: 1, Current: {:d}".format(self.process_currentProcess_currentSubProcess), 'light_red'))
                elif (requestType == 'analyzedKlines'):
                    if (self.process_currentProcess_currentSubProcess == 3):
                        if (blockIndex == self.pdap_resultSaving_collectionBlockIndex):
                            if (self.pdap_resultSaving_isLastBlock == True): self.process_currentProcess_currentSubProcess = 4
                            else:                                            self.process_currentProcess_currentSubProcess = 2
                        else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: Block Index Mismatch (Received: {:s}, Current: {:s}".format(blockIndex, self.pdap_resultSaving_collectionBlockIndex), 'light_red'))
                    else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: SubProcess Mismatch (Expected: 3, Current: {:d}".format(self.process_currentProcess_currentSubProcess), 'light_red'))

            #Save Completion during 'TERMINATION SEQUENCE'
            elif (self.process_currentProcess == 'TERMINATION SEQUENCE'):
                if (requestType == 'summary'):
                    if (self.process_currentProcess_currentSubProcess == 2): 
                        if (self.config_resultType == 'COMPLETE'): 
                            if (0 < len(self.analyzedKlines)):       self.process_currentProcess_currentSubProcess = 3
                            else:                                    self.process_currentProcess_currentSubProcess = 5
                        elif (self.config_resultType == 'SUMMARY'):  self.process_currentProcess_currentSubProcess = 5
                    else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: SubProcess Mismatch (Expected: 1, Current: {:d}".format(self.process_currentProcess_currentSubProcess), 'light_red'))
                elif (requestType == 'analyzedKlines'):
                    if (self.process_currentProcess_currentSubProcess == 4):
                        if (blockIndex == self.pdap_resultSaving_collectionBlockIndex):
                            if (self.pdap_resultSaving_isLastBlock == True): self.process_currentProcess_currentSubProcess = 5
                            else:                                            self.process_currentProcess_currentSubProcess = 3
                        else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: Block Index Mismatch (Received: {:s}, Current: {:s}".format(blockIndex, self.pdap_resultSaving_collectionBlockIndex), 'light_red'))
                    else: print(termcolor.colored("[AUX] An unexpected analysis save completion message received: SubProcess Mismatch (Expected: 3, Current: {:d}".format(self.process_currentProcess_currentSubProcess), 'light_red'))
        else:
            self.ipcA_MAIN.sendFAR(functionID = 'SIMULATORMESSAGE', functionParams = {'simulatorMsg': "User attention advised, analysis result save for termination sequence failed".format(self.simulationCode)}, nMaxDispatch = 'INF')
            print(termcolor.colored("[SIMULATOR {:s}] User attention advised, analysis result save for termination sequence failed".format(self.simulationCode), 'light_red'))