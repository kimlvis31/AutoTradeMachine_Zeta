import ATM_Zeta_Manager_AutoTrader
import ATM_Zeta_Manager_BinanceAPI
import ATM_Zeta_Manager_DataManagement

from ATM_Zeta_Auxillaries import functionModifier
import ATM_Zeta_Auxillaries

from random import randint
from threading import Thread
import pyglet
import time
import os
import pprint
import termcolor
import multiprocessing
from datetime import datetime, timezone, tzinfo

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

class manager_Central:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, ipcAs, ipcAThreads, rtaList, rtaProcesses):
        print(termcolor.colored("\nInitializing", 'green'), termcolor.colored("Central", 'light_blue'), termcolor.colored("Manager ----------------------------------------------------------------------------------------------------------------------", 'green'))
        #Instances Localization & Generation
        self.ipcA = ipcAs
        self.ipcAThreads = ipcAThreads
        self.fModifier = functionModifier()
        self.RTAs = dict()
        self.RTAProcesses = rtaProcesses



        #Process Control
        self.process_terminate = False



        #Read ATM Configuration
        self.atmConfig = dict()
        self.__readATMConfig()



        #Main Control Variables
        self.m_AutoTrader     = ATM_Zeta_Manager_AutoTrader.manager_AutoTrader(self, self.ipcA)
        self.m_BinanceAPI     = ATM_Zeta_Manager_BinanceAPI.manager_BinanceAPI(self, self.ipcA)
        self.m_DataManagement = ATM_Zeta_Manager_DataManagement.manager_DataManagement(self, self.ipcA)
        self.m_AutoTrader.postInitialization(self.fModifier,     m_BinanceAPI = self.m_BinanceAPI, m_DataManagement = self.m_DataManagement)
        self.m_BinanceAPI.postInitialization(self.fModifier,     m_AutoTrader = self.m_AutoTrader, m_DataManagement = self.m_DataManagement)
        self.m_DataManagement.postInitialization(self.fModifier, m_AutoTrader = self.m_AutoTrader, m_BinanceAPI     = self.m_BinanceAPI)
        


        #IPC Interaction Variables
        self.klineSubscriptions = dict()
        self.klineSubscription_fetchLimit = 50000



        #FAR Registration
        self.subscribedAssets = list()
        self.subscribedAssets_analyzing     = list()
        self.subscribedAssets_streamingOnly = list()
        for rtaCode in rtaList:
            self.RTAs[rtaCode] = {'allocatedAPISymbols_SA': list(), 'allocatedAPISymbols_SSO': list(), 'allocatedAPISymbols_SO': list()} #SA: Subscribed and Analyze, SSO: Subscribed and Stream-Only, SO: Stream-Only 
            self.ipcA[rtaCode].addFARHandler("GETWEBSOCKETCONNECTIONPERMISSION", self.m_BinanceAPI.addWebSocketConnectionPermissionQueue)
            self.ipcA[rtaCode].addFARHandler("ONWEBSOCKETCONNECTIONCOMPLETION",  self.m_BinanceAPI.onWebSocketConnectionCompletion)
            self.ipcA[rtaCode].addFARHandler("ONFIRSTKLINESTREAMRECEIVAL",       self.m_BinanceAPI.on_firstKlineStreamReceival)
            self.ipcA[rtaCode].addFARHandler("ONANALYSISBEGIN",                  self.m_BinanceAPI.on_analysisBegin)
            self.ipcA[rtaCode].addFARHandler("ONKLINERECEIVAL",                  self.m_BinanceAPI.on_KlineReceival)
        


        #IPC Call Function Registration - MAIN
        self.ipcA['MAIN'].addFARHandler("PROCCTRLFUNC_TERMINATE",  self.farHandler_RaiseTerminationFlag)
        self.ipcA['MAIN'].addFARHandler("ADDKLINESUBSCRIPTION",       self.farHandler_addKlineSubscription_MAIN)
        self.ipcA['MAIN'].addFARHandler("REMOVEKLINESUBSCRIPTION",    self.farHandler_removeKlineSubscription_MAIN)
        self.ipcA['MAIN'].addFARHandler("GETKLINESUBSCRIPTIONSTATUS", self.farHandler_getKlineSubscriptionStatus_MAIN)

        self.ipcA['MAIN'].addFARHandler("REQUESTKLINEDEEPRANGECHECK", self.m_DataManagement.requestKlineDeepRangeCheck)

        self.ipcA['MAIN'].addFARHandler("GETANALYSISRESULT",                  self.m_DataManagement.getAnalysisResult)
        


        #IPC Call Function Registration - AUX
        self.ipcA['AUX'].addFARHandler("ADDKLINESUBSCRIPTION",               self.farHandler_addKlineSubscription_AUX)
        self.ipcA['AUX'].addFARHandler("REMOVEKLINESUBSCRIPTION",            self.farHandler_removeKlineSubscription_AUX)
        self.ipcA['AUX'].addFARHandler("GETKLINESUBSCRIPTIONSTATUS",         self.farHandler_getKlineSubscriptionStatus_AUX)

        self.ipcA['AUX'].addFARHandler("REQUESTKLINEDEEPRANGECHECK", self.m_DataManagement.requestKlineDeepRangeCheck)

        self.ipcA['AUX'].addFARHandler("SAVEANALYSISRESULT",                 self.m_DataManagement.saveAnalysisResult)
        self.ipcA['AUX'].addFARHandler("REMOVEANALYSISDATA",                 self.m_DataManagement.removeAnalysisResult)

        print(termcolor.colored("Central", 'light_blue'), termcolor.colored("Manager Initialization Complete! ----------------------------------------------------------------------------------------------------------", 'green'))
    def postInitialization(self):
        #Start Initializing RTAs
        for rtaCode in self.RTAs: self.ipcA[rtaCode].sendPRDEDIT("PROCCTRL_INITGO", True, nMaxDispatch = 'INF')
        for rtaCode in self.RTAs:
            while (self.ipcA[rtaCode].getPRD("PROCSTATUS") != "INITIALIZED"): time.sleep(0.01)
            self.ipcA['MAIN'].sendPRDEDIT("PROCSTATUS_"+rtaCode, "INITIALIZED", nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT("PROCSTATUS_"+rtaCode, "INITIALIZED", nMaxDispatch = 'INF')
            print(termcolor.colored(rtaCode, 'light_yellow'), termcolor.colored("Initialization Complete! -------------------------------------------------------------------------------------------------------------", 'green'))
        print()
        
        #Send PROCGO signal to the RTAs & Update RTA PROCSTAT on PRD
        for rtaCode in self.RTAs: 
            self.ipcA[rtaCode].sendPRDEDIT("PROCCTRL_PROCGO", True)
            self.ipcA['MAIN'].sendPRDEDIT("PROCSTATUS"+rtaCode, "PROCESSING", nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT("PROCSTATUS"+rtaCode, "PROCESSING", nMaxDispatch = 'INF')

        #Wait for all of the RTAs to start processing
        while (True):
            pendingRTADetected = False
            for rtaCode in self.RTAs:
                if (self.ipcA[rtaCode].getPRD("PROCSTATUS") != "PROCESSING"): pendingRTADetected = True; break
            if (pendingRTADetected == False): break
            else: time.sleep(0.1)

        #Send ATM Status to MAIN and AUX
        self.ipcA['MAIN'].sendPRDEDIT("PROCSTATUS", "INITIALIZED", nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("PROCSTATUS", "INITIALIZED", nMaxDispatch = 'INF')

        #Read Asset Subscription List File
        self.__readAssetSubscriptionList()

        #Start DB and Binance Server Connection Checkers
        self.fModifier.start(self.m_DataManagement.functionRepeaters['DBCONNECTIONCHECK']) #Start DB Connection Check Repeater
        self.fModifier.start(self.m_BinanceAPI.functionRepeaters['SERVERCONNECITONCHECK']) #Start Server Connection Check Repeater
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    









    #Manager Process Loop ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self):
        #Update ATM PROCSTAT on PRD
        self.ipcA['MAIN'].sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        
        #Start Process Loop
        while (self.process_terminate == False):
            #Process Managers and fModifier
            self.m_AutoTrader.process()
            self.m_BinanceAPI.process()
            self.m_DataManagement.process()
            self.fModifier.process()

            self.__processKlineSubscription()

            #Process FAR/FARR
            self.ipcA['MAIN'].processFARs()
            self.ipcA['AUX'].processFARs()
            for rtaCode in self.RTAs: self.ipcA[rtaCode].processFARs()
            self.ipcA['MAIN'].processFARRs()
            self.ipcA['AUX'].processFARRs()
            for rtaCode in self.RTAs: self.ipcA[rtaCode].processFARRs()
            
            time.sleep(0.001)
            
        #Termination Sequence
        for rtaCode in self.RTAs: self.ipcA[rtaCode].sendFAR(functionID = "PROCCTRLFUNC_TERMINATE", nMaxDispatch = 'INF')
        for rtaCode in self.RTAs:
            self.RTAProcesses[rtaCode].join()
            print(termcolor.colored("{:s} Process Terminated!".format(rtaCode), 'cyan'))
            self.ipcA[rtaCode].terminate()
            self.ipcAThreads[rtaCode].join()

        self.m_AutoTrader.terminate()
        self.m_BinanceAPI.terminate()
        self.m_DataManagement.terminate()
        
        self.ipcA['AUX'].terminate()
        self.ipcAThreads['AUX'].join()

        self.ipcA['MAIN'].sendPRDEDIT("PROCSTATUS", "TERMINATED", nMaxDispatch = 'INF')
        self.ipcA['MAIN'].terminate()
        self.ipcAThreads['MAIN'].join()
    #Manager Process Loop END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    


















    #Inter-Manager Call Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Binance Server Related
    #---Binance Server Connection Handler
    def on_ServerConnection(self):
        try:
            #Send FAR 'ONSERVERCONNECTION' and wait until all of the RTAs have finished server connection protocol
            for rtaCode in self.RTAs: self.ipcA[rtaCode].sendFAR(functionID = 'ONSERVERCONNECTION', nMaxDispatch = 'INF')
            while (True):
                allRTAsResponded = True
                for rtaCode in self.RTAs: 
                    if (self.ipcA[rtaCode].getPRD("SERVERCONNECTION") == False): allRTAsResponded = False; break
                if (allRTAsResponded == True): break
                else: time.sleep(0.1)
            #Confirm Asset Subscription List and Allocate Assets to RTAs
            self.__confirmAssetSubscriptionList()
            self.__allocateAssetsToRTAs()
        except Exception as e: print(termcolor.colored("An unexpected error ocrrured while attempting to handle Server Connection by the Central Manager\n *", 'light_red'), termcolor.colored(e, 'light_red'))



    #---Binance Server Disconnection Handler
    def on_ServerDisconnection(self):
        try:
            #Send FAR 'ONSERVERDISCONNECTION' and wait until all of the RTAs have finished server disconnection protocol
            for rtaCode in self.RTAs: self.ipcA[rtaCode].sendFAR(functionID = 'ONSERVERDISCONNECTION', nMaxDispatch = 'INF')
            while (True):
                allRTAsResponded = True
                for rtaCode in self.RTAs: 
                    if (self.ipcA[rtaCode].getPRD("SERVERCONNECTION") == True): allRTAsResponded = False; break
                if (allRTAsResponded == True): break
                else: time.sleep(0.1)
            for rtaCode in self.RTAs:
                self.RTAs[rtaCode]['allocatedAPISymbols_SA'].clear()
                self.RTAs[rtaCode]['allocatedAPISymbols_SSO'].clear()
                self.RTAs[rtaCode]['allocatedAPISymbols_SO'].clear()
            print(termcolor.colored(" * All RTAs Post-Server Disconnection Protocol Complete", 'light_red'))
        except Exception as e: print(termcolor.colored("An unexpected error ocrrured while attempting to handle Server Disconnection by the Central Manager\n *", 'light_red'), termcolor.colored(e, 'light_red'))






    #DB Related
    #---DB Connection Handler
    def on_DBConnection(self):
        try:
            #Process binanceAPI manager's database connection protocol
            self.m_BinanceAPI.on_DBConnection()
        
            #Send FAR 'ONDBCONNECTION' and wait until all of the RTAs have finished their database connection protocol
            dbDir = self.m_DataManagement.get_DBDir('klines')
            for rtaCode in self.RTAs: self.ipcA[rtaCode].sendFAR(functionID = 'ONDBCONNECTION', functionParams = {'dbDir': dbDir}, nMaxDispatch = 'INF')
            while (True):
                allRTAsResponded = True
                for rtaCode in self.RTAs: 
                    if ((self.ipcA[rtaCode].getPRD("DBCONNECTION") == False) or (self.ipcA[rtaCode].getPRD("DBDIR") != dbDir)): allRTAsResponded = False; break
                if (allRTAsResponded == True): break
                else: time.sleep(0.1)
        except Exception as e: print(termcolor.colored("An unexpected error ocrrured while attempting to handle DB Connection by the Central Manager\n *", 'light_red'), termcolor.colored(e, 'light_red'))



    #---DB Disconnection Handler
    def on_DBDisconnection(self):
        try:
            #Process binanceAPI manager's database disconnection protocol
            self.m_BinanceAPI.on_DBDisconnection()

            #Send FAR 'ONDBDISCONNECTION' and wait until all of the RTAs have finished their database disconnection protocol
            for rtaCode in self.RTAs: self.ipcA[rtaCode].sendFAR(functionID = 'ONDBDISCONNECTION', nMaxDispatch = 'INF')
            while (True):
                allRTAsResponded = True
                for rtaCode in self.RTAs: 
                    if ((self.ipcA[rtaCode].getPRD("DBCONNECTION") == True) or (self.ipcA[rtaCode].getPRD("DBDIR") != None)): allRTAsResponded = False; break
                if (allRTAsResponded == True): break
                else: time.sleep(0.1)
        except Exception as e: print(termcolor.colored("An unexpected error ocrrured while attempting to handle DB Disconnection by the Central Manager\n *", 'light_red'), termcolor.colored(e, 'light_red'))










    #General Central Manager Management Functions
    def get_allocatedSymbols_RTA(self, rtaCode):
        return (self.RTAs[rtaCode]['allocatedAPISymbols_SA']+self.RTAs[rtaCode]['allocatedAPISymbols_SSO']+self.RTAs[rtaCode]['allocatedAPISymbols_SO'])

    def allocateRTA_RunTime(self, apiSymbol):
        try:
            if (apiSymbol in self.subscribedAssets):
                nSymbols_Allocated_min = None
                nSymbols_Allocated_SA_min = None
                for rtaCode in self.RTAs:
                    nSymbols_Allocated    = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SSO']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])
                    nSymbols_Allocated_SA = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA'])
                    if ((nSymbols_Allocated_min == None) or (nSymbols_Allocated < nSymbols_Allocated_min)): nSymbols_Allocated_min = nSymbols_Allocated
                    if ((nSymbols_Allocated_SA_min == None) or (nSymbols_Allocated_SA < nSymbols_Allocated_SA_min)): nSymbols_Allocated_SA_min = nSymbols_Allocated_SA

                #SA Allocation
                if (nSymbols_Allocated_SA_min < self.atmConfig['maxAnalysisNPerRTA']):
                    for rtaCode in self.RTAs:
                        nSymbols_Allocated_SA = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA'])
                        if (nSymbols_Allocated_SA == nSymbols_Allocated_SA_min): break
                    self.RTAs[rtaCode]['allocatedAPISymbols_SA'].append(apiSymbol)
                    return (rtaCode, 'SO')

                #SSO Allocation
                else:
                    for rtaCode in self.RTAs:
                        nSymbols_Allocated = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SSO']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])
                        if (nSymbols_Allocated == nSymbols_Allocated_min): break
                    self.RTAs[rtaCode]['allocatedAPISymbols_SSO'].append(apiSymbol)
                    return (rtaCode, 'SSO')
            
            else:
                #SO Allocation
                nSymbols_Allocated_min = None
                for rtaCode in self.RTAs:
                    nSymbols_Allocated = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SSO']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])
                    if ((nSymbols_Allocated_min == None) or (nSymbols_Allocated < nSymbols_Allocated_min)): nSymbols_Allocated_min = nSymbols_Allocated

                for rtaCode in self.RTAs:
                    nSymbols_Allocated = len(self.RTAs[rtaCode]['allocatedAPISymbols_SA']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SSO']) + len(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])
                    if (nSymbols_Allocated == nSymbols_Allocated_min): break
                self.RTAs[rtaCode]['allocatedAPISymbols_SO'].append(apiSymbol)
                return (rtaCode, 'SO')
        except Exception as e: print(termcolor.colored("An unexpected error occured during run-time RTA allocation for {:s}\n *".format(apiSymbol), 'light_red'), termcolor.colored(e, 'light_red'))

    def updateRTAAllocation_onRemoval(self, apiSymbol, rtaCode, rtaAllocMode):
        pass

    def updateRTAAllocation_onStatusChange(self, apiSymbol, rtaCode, rtaAllocMode, previousStatus, currentStatus):
        pass
    #Inter-Manager Call Functions END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




















    #Manager Internal Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #ATM Config
    def __readATMConfig(self):
        print("Reading ATM Configuration...")
        configFile = open(os.path.join(path_PROJECT, 'config', 'atmConfig.txt'))
        configFileContents = configFile.readlines()
        configFile.close()
        for i in range (len(configFileContents)):
            try:
                configFileContents[i] = configFileContents[i].strip()
                contentLineContents = configFileContents[i].split("=")
                contentName = contentLineContents[0].strip(); contentData = contentLineContents[1].strip()
                if (contentName == "maxAnalysisNPerRTA"):
                    self.atmConfig[contentName] = int(contentData)
                else: print("Unrecognizable Content Name Detected During 'atmConfig.txt' Read: < {:s} >".format(configFileContents[i]))
            except Exception as e: print("Unrecognizable Content Detected During 'atmConfig.txt' Read: <{:s}> <{:s}>".format(configFileContents[i], str(e)))

        #Contents Verification


        #Console Print
        print("<self.atmConfig>")
        pprint.pprint(self.atmConfig)
        print("ATM Configuration Read Complete!")
        
        self.__saveATMConfig()

    def __saveATMConfig(self):
        configFile = open(os.path.join(path_PROJECT, 'config', 'atmConfig.txt'), 'w')
        configFile.write('maxAnalysisNPerRTA = {:d}'.format(self.atmConfig['maxAnalysisNPerRTA']))
        configFile.close()


    #Read Asset Subscription List File
    def __readAssetSubscriptionList(self):
        print("Reading Asset Subscription List...")
        fileDir = os.path.join(path_PROJECT, 'config', 'assetSubscriptionList.txt')
        if (os.path.exists(fileDir) == True):
            assetSubListFile = open(fileDir)
            assetSubListFileContents = assetSubListFile.readlines()
            assetSubListFile.close()
            for assetName in assetSubListFileContents: self.subscribedAssets.append(assetName.strip())
            print(" * {:d} Asset Subscription Detected!".format(len(self.subscribedAssets)))
        else:
            assetSubListFile = open(fileDir, 'w')
            assetSubListFile.close()
            print(" * No Asset Subscription File Was Detected: Generated 'assetSubscriptionList.txt'")
        print("Asset Subscription List Read Complete!\n")



    #Save asset subscription list
    def __saveAssetSubscriptionList(self):
        fileDir = os.path.join(path_PROJECT, 'config', 'assetSubscriptionList.txt')
        with open(fileDir, 'w') as asListFile: asListFile.writelines(self.subscribedAssets)



    #Confirm validity of the subscribed assets
    #[1]: Check the assets' existence within the market
    #[2]: Check the assets' status in the market
    # * This function assumes that both the DB and Binance Server are available
    def __confirmAssetSubscriptionList(self):
        print("Confirming Asset Subscription List...")

        #Identify the market status of the subscribed assets, below are three possible cases
        #[0]: Not Found In Market
        #[1]: Not Trading
        #[2]: Trading
        marketAssets_all     = self.m_BinanceAPI.get_AssetList(tradingOnly = False)
        marketAssets_trading = self.m_BinanceAPI.get_AssetList(tradingOnly = True)
        
        sa_onMarket = list(); sa_notonMarket = list(); sa_trading = list(); sa_notTrading = list()
        for apiSymbol in self.subscribedAssets:
            if (apiSymbol in marketAssets_all): 
                sa_onMarket.append(apiSymbol)                                          #API SYMBOL IN MARKET
                if (apiSymbol in marketAssets_trading): sa_trading.append(apiSymbol)   #API SYMBOL IN MARKET & TRADING
                else: sa_notTrading.append(apiSymbol)                                  #API SYMBOL IN MARKET & NOT TRADING
            else: sa_notonMarket.append(apiSymbol)                                     #API SYMBOL NOT IN MARKET

        print(" * {:d} subscribed assets are not on market:\n{:s}\n".format(len(sa_notonMarket), str(sa_notonMarket)))
        print(" * {:d} subscribed assets are not trading:\n{:s}\n".format(len(sa_notTrading), str(sa_notTrading)))
        print(" * {:d} subscriptions out of {:d} are market confirmed!:\n{:s}\n".format(len(sa_trading), len(self.subscribedAssets), str(sa_trading)))
        print("Asset Subscription List Confirmation Complete!\n")



    #Allocate all of the TRADING assets for streaming and subscribed assets for streaming & analysis
    def __allocateAssetsToRTAs(self):
        try:
            print("Allocating Assets to the RTAs...")
            marketAssets_trading = self.m_BinanceAPI.get_AssetList(tradingOnly = True)
        
            #Seperate market confirmed subscribed assets into 'Analyzing' and 'StreamingOnly' with nAnalyzableSymbols_max as the seperation standard
            apiSymbols_subscribedAndTrading = [apiSymbol for apiSymbol in self.subscribedAssets if apiSymbol in marketAssets_trading]
            nAnalyzableSymbols_max = len(self.RTAs)*self.atmConfig['maxAnalysisNPerRTA']
            if (nAnalyzableSymbols_max < len(apiSymbols_subscribedAndTrading)):
                self.subscribedAssets_analyzing     = apiSymbols_subscribedAndTrading[:nAnalyzableSymbols_max]
                self.subscribedAssets_streamingOnly = apiSymbols_subscribedAndTrading[nAnalyzableSymbols_max:]
            else: self.subscribedAssets_analyzing = apiSymbols_subscribedAndTrading
            
            #Create a list of non-subscribed symbols that are streaming only
            subscribedAssets_analyzing     = self.subscribedAssets_analyzing.copy()
            subscribedAssets_streamingOnly = self.subscribedAssets_streamingOnly.copy()
            apiSymbols_streamOnly          = [apiSymbol for apiSymbol in marketAssets_trading if apiSymbol not in self.subscribedAssets_analyzing and apiSymbol not in self.subscribedAssets_streamingOnly]

            listAccessIndex_SA  = 0
            listAccessIndex_SSO = 0
            listAccessIndex_SO  = 0

            #Allocate TRADING assets to RTAs
            RTAIndex = 0
            while (listAccessIndex_SO < len(apiSymbols_streamOnly)):
                #RTACode Generaiton
                rtaCode = 'RTA{:d}'.format(RTAIndex)
                
                #Asset Selection, priority is as follows [0]: subscribed and analyzable, subscribed but stream-only, not subscribed and stream-only
                if   (listAccessIndex_SA < len(subscribedAssets_analyzing)):      apiSymbol = subscribedAssets_analyzing[listAccessIndex_SA];      rtaAllocMode = 'SA';  listAccessIndex_SA  += 1 #SA:  Subscribed and Analyze
                elif (listAccessIndex_SSO < len(subscribedAssets_streamingOnly)): apiSymbol = subscribedAssets_streamingOnly[listAccessIndex_SSO]; rtaAllocMode = 'SSO'; listAccessIndex_SSO += 1 #SSO: Subscribed but Stream-Only
                else:                                                             apiSymbol = apiSymbols_streamOnly[listAccessIndex_SO];           rtaAllocMode = 'SO';  listAccessIndex_SO  += 1 #SO:  Stream-Only

                #RTA Allocation
                self.m_BinanceAPI.set_RTAAllocation(apiSymbol, rtaCode, rtaAllocMode)
                self.RTAs[rtaCode]['allocatedAPISymbols_'+rtaAllocMode].append(apiSymbol)

                RTAIndex += 1
                if (RTAIndex == len(self.RTAs)): RTAIndex = 0
            
            #Print-report Asset Allocation Result
            for rtaCode in self.RTAs:
                print("<{:s}> - <SA: {:d}, SSO: {:d}, SO: {:d}>".format(rtaCode, len(self.RTAs[rtaCode]['allocatedAPISymbols_SA']), len(self.RTAs[rtaCode]['allocatedAPISymbols_SSO']), len(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])))
                print(termcolor.colored("[SA]:  {:s}".format(str(self.RTAs[rtaCode]['allocatedAPISymbols_SA'])),  'light_green'))
                print(termcolor.colored("[SSO]: {:s}".format(str(self.RTAs[rtaCode]['allocatedAPISymbols_SSO'])), 'light_blue'))
                print(termcolor.colored("[SO]:  {:s}\n".format(str(self.RTAs[rtaCode]['allocatedAPISymbols_SO'])),  'blue'))

            #Set WebSocket Symbol Subscription List of RTAs
            for rtaCode in self.RTAs: self.m_BinanceAPI.on_RTAAllocComplete(rtaCode)

            print("Assets RTA Allocation Complete!\n")
        except Exception as e: print(termcolor.colored("An unexpected error occurred during RTA allocation of all assets\n *", 'light_red'), termcolor.colored(e, 'light_red'))




    #<IPC Kline Subscription & Fetch>
    def __addKlineSubscription(self, requesterProcess, requesterID, apiSymbol, intervalID, subscriptionRange):
        targetCode    = "{:s}_{:d}".format(apiSymbol, intervalID)
        requesterCode = "{:s}_{:s}".format(requesterProcess, requesterID)
        if (targetCode in self.klineSubscriptions): 
            if (requesterCode in self.klineSubscriptions[targetCode]): return False
        else: self.klineSubscriptions[targetCode] = dict()
        
        if (subscriptionRange == None):
            fetchTargetRanges = self.m_DataManagement.get_DataAvailability(apiSymbol, intervalID)

        elif (subscriptionRange[1] == None):
            fetchTargetRanges = list()
            dataRanges = self.m_DataManagement.get_DataAvailability(apiSymbol, intervalID)
            for dataRange in dataRanges:
                classification = 0
                delta_a0s0 = dataRange[0] - subscriptionRange[0]; classification += 0b1000*(0 <= delta_a0s0)
                delta_a1s0 = dataRange[1] - subscriptionRange[0]; classification += 0b0010*(0 <  delta_a1s0)
                if   (classification == 0b0010): fetchTargetRanges.append([subscriptionRange[0], dataRange[1]])
                elif (classification == 0b1010): fetchTargetRanges.append([dataRange[0],         dataRange[1]])

        else:
            fetchTargetRanges = list()
            dataRanges = self.m_DataManagement.get_DataAvailability(apiSymbol, intervalID)
            for dataRange in dataRanges:
                classification = 0
                delta_a0s0 = dataRange[0] - subscriptionRange[0]; classification += 0b1000*(0 <= delta_a0s0)
                delta_a0s1 = dataRange[0] - subscriptionRange[1]; classification += 0b0100*(0 <= delta_a0s1)
                delta_a1s0 = dataRange[1] - subscriptionRange[0]; classification += 0b0010*(0 <  delta_a1s0)
                delta_a1s1 = dataRange[1] - subscriptionRange[1]; classification += 0b0001*(0 <  delta_a1s1)
                if   (classification == 0b0010): fetchTargetRanges.append([subscriptionRange[0], dataRange[1]])
                elif (classification == 0b1010): fetchTargetRanges.append([dataRange[0],         dataRange[1]])
                elif (classification == 0b1011): fetchTargetRanges.append([dataRange[0],         subscriptionRange[1]]); break
                elif (classification == 0b0011): fetchTargetRanges.append([subscriptionRange[0], subscriptionRange[1]]); break

        self.klineSubscriptions[targetCode][requesterCode] = {'requesterProcess':  requesterProcess,
                                                              'requesterID':       requesterID,
                                                              'apiSymbol':         apiSymbol,
                                                              'intervalID':        intervalID,
                                                              'subscriptionRange': subscriptionRange,
                                                              'fetchTargetRanges': fetchTargetRanges,
                                                              'loadTargetWidth':   self.__klineSubscription_calculateLoadTargetWidth(apiSymbol, intervalID, subscriptionRange),
                                                              'loadedWidth':       0,
                                                              'lastStreamedTS':    None}
        pprint.pprint(self.klineSubscriptions[targetCode][requesterCode])
        return True

    def __removeKlineSubscription(self, requesterProcess, requesterID, apiSymbol, intervalID):
        try:
            targetCode    = "{:s}_{:d}".format(apiSymbol, intervalID)
            requesterCode = "{:s}_{:s}".format(requesterProcess, requesterID)
            if (targetCode in self.klineSubscriptions):
                if (requesterCode in self.klineSubscriptions[targetCode]): 
                    if (len(self.klineSubscriptions[targetCode]) == 1): del self.klineSubscriptions[targetCode]
                    else:                                               del self.klineSubscriptions[targetCode][requesterCode]
            return True
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to remove kline subscription\n *", 'light_red'), termcolor.colored(e, 'light_red'))
    
    def __getKlineSubscriptionStatus(self, requesterProcess, requesterID, apiSymbol, intervalID):
        targetCode    = "{:s}_{:d}".format(apiSymbol, intervalID)
        requesterCode = "{:s}_{:s}".format(requesterProcess, requesterID)
        if (targetCode in self.klineSubscriptions):
            if (requesterCode in self.klineSubscriptions[targetCode]): return self.klineSubscriptions[targetCode][requesterCode]['status']
            else: return None
        else: return None



    def __processKlineSubscription(self):
        expiredSubscriptions = list()
        for targetCode in self.klineSubscriptions:
            for requesterCode in self.klineSubscriptions[targetCode]:
                fetchTargetRanges = self.klineSubscriptions[targetCode][requesterCode]['fetchTargetRanges']
                if (0 < len(fetchTargetRanges)):
                    subscriptionRange = self.klineSubscriptions[targetCode][requesterCode]['subscriptionRange']
                    requesterProcess  = self.klineSubscriptions[targetCode][requesterCode]['requesterProcess']
                    requesterID       = self.klineSubscriptions[targetCode][requesterCode]['requesterID']
                    apiSymbol         = self.klineSubscriptions[targetCode][requesterCode]['apiSymbol']
                    intervalID        = self.klineSubscriptions[targetCode][requesterCode]['intervalID']

                    #Fetch Range Determination
                    fetchRangeWidthLimit = ATM_Zeta_Manager_BinanceAPI.KLINE_INTERVAL_SECs[intervalID]*self.klineSubscription_fetchLimit-1
                    fetchRangeWidth = fetchTargetRanges[-1][1] - fetchTargetRanges[-1][0]

                    if (fetchRangeWidth <= fetchRangeWidthLimit):
                        fetchRange = fetchTargetRanges.pop(-1)
                    else:
                        fetchRange = [fetchTargetRanges[-1][1]-fetchRangeWidthLimit, fetchTargetRanges[-1][1]]
                        fetchTargetRanges[-1] = [fetchTargetRanges[-1][0], fetchTargetRanges[-1][1]-fetchRangeWidthLimit-1]
                        
                    #Klines Fetch
                    klines = self.m_DataManagement.get_klines(apiSymbol, intervalID, fetchRange[0], fetchRange[1])
                    
                    #Completion Calculation
                    loadedWidth = klines[-1][1]-int(klines[0][0]%1e10)+1
                    self.klineSubscriptions[targetCode][requesterCode]['loadedWidth'] += loadedWidth
                    loadCompletion = self.__klineSubscription_calculateLoadCompletion(apiSymbol, intervalID, targetCode, requesterCode, subscriptionRange)

                    #Dispatch Klines
                    if   (requesterProcess == 'MAIN'): self.ipcA['MAIN'].sendFAR(functionID = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': klines, 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')
                    elif (requesterProcess == 'AUX'):  self.ipcA['AUX'].sendFAR(functionID  = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': klines, 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')

                    #If the defined fetch has completed, append to the removal queue
                    if ((subscriptionRange != None) and (subscriptionRange[1] != None) and (loadCompletion != None) and (100 <= loadCompletion)): expiredSubscriptions.append((targetCode, requesterCode))
        #Remove expired subscriptions
        for expiredSubscription in expiredSubscriptions:
            if (len(self.klineSubscriptions[expiredSubscription[0]]) == 1): del self.klineSubscriptions[expiredSubscription[0]]
            else:                                                           del self.klineSubscriptions[expiredSubscription[0]][expiredSubscription[1]]



    def klineSubscription_onKlineDownload(self, apiSymbol, intervalID, filteredKlines):
        expiredSubscriptions = list()
        targetCode = "{:s}_{:d}".format(apiSymbol, intervalID)
        if (targetCode in self.klineSubscriptions):
            for requesterCode in self.klineSubscriptions[targetCode]:
                subscriptionRange = self.klineSubscriptions[targetCode][requesterCode]['subscriptionRange']
                filteredKlines_le = int(filteredKlines[0][0]%1e10)
                filteredKlines_re = filteredKlines[-1][1]
                
                #Determine the range of klines to dispatch
                if (subscriptionRange == None): klinesToDispatch = filteredKlines
                elif (subscriptionRange[1] == None):
                    classification = 0
                    delta_a0s0 = filteredKlines_le[0] - subscriptionRange[0]; classification += 0b1000*(0 <= delta_a0s0)
                    delta_a1s0 = filteredKlines_re[1] - subscriptionRange[0]; classification += 0b0010*(0 <  delta_a1s0)
                    #Case 1 (Left-Clipped)
                    if (classification == 0b0010):
                        for index, kline in enumerate(filteredKlines):
                            if (subscriptionRange[0] <= int(kline[0]%1e10)): boundaryIndex = index; break
                        klinesToDispatch = filteredKlines[boundaryIndex:]
                    #Case 2 (Entirety)
                    elif (classification == 0b1010): klinesToDispatch = filteredKlines
                    #Case 3 (None)
                    else: klinesToDispatch = None
                else:
                    classification = 0
                    delta_a0s0 = filteredKlines_le[0] - subscriptionRange[0]; classification += 0b1000*(0 <= delta_a0s0)
                    delta_a0s1 = filteredKlines_le[0] - subscriptionRange[1]; classification += 0b0100*(0 <= delta_a0s1)
                    delta_a1s0 = filteredKlines_re[1] - subscriptionRange[0]; classification += 0b0010*(0 <  delta_a1s0)
                    delta_a1s1 = filteredKlines_re[1] - subscriptionRange[1]; classification += 0b0001*(0 <  delta_a1s1)
                    #Case 1 (Left-Clipped)
                    if (classification == 0b0010):
                        for index, kline in enumerate(filteredKlines):
                            if (subscriptionRange[0] <= int(kline[0]%1e10)): boundaryIndex = index; break
                        klinesToDispatch = filteredKlines[boundaryIndex:]
                    #Case 2 (Entirety)
                    elif (classification == 0b1010): klinesToDispatch = filteredKlines
                    #Case 3 (Right-Clipped)
                    elif (classification == 0b1011):
                        for index, kline in enumerate(filteredKlines):
                            if (int(kline[0]%1e10) < subscriptionRange[0]): boundaryIndex = index; break
                        klinesToDispatch = filteredKlines[:boundaryIndex]
                    #Case 4 (Left and Right Clipped)
                    elif (classification == 0b0011):
                        boundaryIndex_l = None; boundaryIndex_r = None
                        for index, kline in enumerate(filteredKlines):
                            if (boundaryIndex_l == None):
                                if (subscriptionRange[0] <= int(kline[0]%1e10)): boundaryIndex_l = index
                            else:
                                if (int(kline[0]%1e10) < subscriptionRange[0]):  boundaryIndex_r = index; break
                        klinesToDispatch = filteredKlines[boundaryIndex_l:boundaryIndex_r]
                    #Case 5 (None)
                    else: klinesToDispatch = None

                if (klinesToDispatch != None):
                    requesterProcess  = self.klineSubscriptions[targetCode][requesterCode]['requesterProcess']
                    requesterID       = self.klineSubscriptions[targetCode][requesterCode]['requesterID']

                    #Completion Calculation
                    loadedWidth = klinesToDispatch[-1][1]-int(klinesToDispatch[0][0]%1e10)+1
                    self.klineSubscriptions[targetCode][requesterCode]['loadedWidth'] += loadedWidth
                    loadCompletion = self.__klineSubscription_calculateLoadCompletion(apiSymbol, intervalID, targetCode, requesterCode, subscriptionRange)
                
                    #Dispatch Klines
                    if   (requesterProcess == 'MAIN'): self.ipcA['MAIN'].sendFAR(functionID = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': klinesToDispatch, 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')
                    elif (requesterProcess == 'AUX'):  self.ipcA['AUX'].sendFAR(functionID  = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': klinesToDispatch, 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')
                    
                    #If the defined fetch has completed, append to the removal queue
                    if ((subscriptionRange != None) and (subscriptionRange[1] != None) and (loadCompletion != None) and (100 <= loadCompletion)): expiredSubscriptions.append((targetCode, requesterCode))
        #Remove expired subscriptions
        for expiredSubscription in expiredSubscriptions:
            if (len(self.klineSubscriptions[expiredSubscription[0]]) == 1): del self.klineSubscriptions[expiredSubscription[0]]
            else:                                                           del self.klineSubscriptions[expiredSubscription[0]][expiredSubscription[1]]



    def klineSubscription_onKlineStreamReceival(self, apiSymbol, intervalID, kline):
        expiredSubscriptions = list()
        targetCode = "{:s}_{:d}".format(apiSymbol, intervalID)
        if (targetCode in self.klineSubscriptions):
            for requesterCode in self.klineSubscriptions[targetCode]:
                subscriptionRange = self.klineSubscriptions[targetCode][requesterCode]['subscriptionRange']
                
                if (subscriptionRange == None) or ((subscriptionRange[0] <= kline[0]) and ((subscriptionRange[1] == None) or (kline[1] <= subscriptionRange[1]))):
                    requesterProcess  = self.klineSubscriptions[targetCode][requesterCode]['requesterProcess']
                    requesterID       = self.klineSubscriptions[targetCode][requesterCode]['requesterID']

                    if (self.klineSubscriptions[targetCode][requesterCode]['lastStreamedTS'] != kline[0]):
                        self.klineSubscriptions[targetCode][requesterCode]['lastStreamedTS'] = kline[0]
                        self.klineSubscriptions[targetCode][requesterCode]['loadedWidth'] += kline[1]-kline[0]+1
                    loadCompletion = self.__klineSubscription_calculateLoadCompletion(apiSymbol, intervalID, targetCode, requesterCode, subscriptionRange)
                    
                    if   (requesterProcess == 'MAIN'): self.ipcA['MAIN'].sendFAR(functionID = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': [kline], 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')
                    elif (requesterProcess == 'AUX'):  self.ipcA['AUX'].sendFAR(functionID  = 'KLINERECEIVER_{:s}'.format(requesterID), functionParams = {'apiSymbol': apiSymbol, 'intervalID': intervalID, 'klines': [kline], 'completion': loadCompletion}, timeout = 10000, nMaxDispatch = 'INF')
                    
                    #If the defined fetch has completed, append to the removal queue
                    if ((subscriptionRange != None) and (subscriptionRange[1] != None) and (loadCompletion != None) and (100 <= loadCompletion)): expiredSubscriptions.append((targetCode, requesterCode))
        #Remove expired subscriptions
        for expiredSubscription in expiredSubscriptions:
            if (len(self.klineSubscriptions[expiredSubscription[0]]) == 1): del self.klineSubscriptions[expiredSubscription[0]]
            else:                                                           del self.klineSubscriptions[expiredSubscription[0]][expiredSubscription[1]]



    def __klineSubscription_calculateLoadCompletion(self, apiSymbol, intervalID, targetCode, requesterCode, subscriptionRange):
        loadTargetWidth = self.klineSubscriptions[targetCode][requesterCode]['loadTargetWidth']
        #If loadTargetWidth is not yet determined, attempt to determine it once again
        if (loadTargetWidth == None):
            loadTargetWidth = self.__klineSubscription_calculateLoadTargetWidth(apiSymbol, intervalID, subscriptionRange)
            #If loadTargetWidth is still not determined, let loadCompletion be 'None'
            if (loadTargetWidth == None): loadCompletion = None
            #If loadTargetWidth is now determined, calculate load completion
            else:
                self.klineSubscriptions[targetCode][requesterCode]['loadTargetWidth'] = loadTargetWidth
                loadCompletion = self.klineSubscriptions[targetCode][requesterCode]['loadedWidth']/self.klineSubscriptions[targetCode][requesterCode]['loadTargetWidth']*100
        #If loadTargetWidth is determined to be zero, let the completion be 100
        elif (loadTargetWidth == 0): loadCompletion = 100
        #If loadTargetWidth is determined, calculate load completion
        else: loadCompletion = self.klineSubscriptions[targetCode][requesterCode]['loadedWidth']/self.klineSubscriptions[targetCode][requesterCode]['loadTargetWidth']*100
        #Return the determined load completion
        return loadCompletion



    def __klineSubscription_calculateLoadTargetWidth(self, apiSymbol, intervalID, subscriptionRange):
        #Subscribe All Klines
        if (subscriptionRange == None):
            try:    loadTargetWidth = self.m_BinanceAPI.get_firstStreamedKlineTS(apiSymbol,intervalID) - self.m_BinanceAPI.get_mrktRegTS(apiSymbol,intervalID)
            except: loadTargetWidth = None
        #Subscribe only after a certain time
        elif (subscriptionRange[1] == None):
            try:
                mrktRegTS             = self.m_BinanceAPI.get_mrktRegTS(apiSymbol,intervalID)
                firstStreamedKlinesTS = self.m_BinanceAPI.get_firstStreamedKlineTS(apiSymbol,intervalID)
                if (subscriptionRange[0] < mrktRegTS): loadTargetWidth = firstStreamedKlinesTS - mrktRegTS + 1
                else:
                    if (subscriptionRange[0] < firstStreamedKlinesTS): loadTargetWidth = firstStreamedKlinesTS - subscriptionRange[0] + 1
                    else:                                              loadTargetWidth = 0
            except: loadTargetWidth = None
        #Subscribe only for a defined temporal range
        else:
            try:
                mrktRegTS = self.m_BinanceAPI.get_mrktRegTS(apiSymbol,intervalID)
                if (subscriptionRange[0] < mrktRegTS): 
                    if (subscriptionRange[1] < mrktRegTS): loadTargetWidth = 0
                    else:                                  loadTargetWidth = subscriptionRange[1] - mrktRegTS            + 1
                else:                                      loadTargetWidth = subscriptionRange[1] - subscriptionRange[0] + 1
            except: loadTargetWidth = None
        #Return the determined load target width
        return loadTargetWidth

    #Manager Internal Functions END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #FAR Hanlder Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def farHandler_RaiseTerminationFlag(self, functionParams): self.process_terminate = True

    def farHandler_onKlineReceival(self, functionParams):
        try: self.m_BinanceAPI.on_KlineReceival(functionParams['apiSymbol'], functionParams['interval'], functionParams['Kline'], functionParams['closed'])
        except Exception as e: print(termcolor.colored("An unexpected error occurred in 'farHandler_onKlineReceival'\n *", 'red'), termcolor(e, 'red'))
        
    def farHandler_addKlineSubscription_MAIN(self, functionParams):       return self.__addKlineSubscription('MAIN', functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'], functionParams.get('subscriptionRange', None))
    def farHandler_addKlineSubscription_AUX(self, functionParams):        return self.__addKlineSubscription('AUX',  functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'], functionParams.get('subscriptionRange', None))
    def farHandler_removeKlineSubscription_MAIN(self, functionParams):    return self.__removeKlineSubscription('MAIN', functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'])
    def farHandler_removeKlineSubscription_AUX(self, functionParams):     return self.__removeKlineSubscription('AUX',  functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'])
    def farHandler_getKlineSubscriptionStatus_MAIN(self, functionParams): return self.__getKlineSubscriptionStatus('MAIN', functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'])
    def farHandler_getKlineSubscriptionStatus_AUX(self, functionParams):  return self.__getKlineSubscriptionStatus('AUX',  functionParams['requesterID'], functionParams['apiSymbol'], functionParams['intervalID'])

    #FAR Hanlder Functions END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------