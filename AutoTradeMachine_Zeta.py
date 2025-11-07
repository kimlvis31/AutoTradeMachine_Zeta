#Import ATM Manager Modules
from ATM_Zeta_Manager_GUI            import manager_GUI
from ATM_Zeta_Manager_AUX            import manager_AUX
from ATM_Zeta_Manager_Central        import manager_Central
from ATM_Zeta_IPC                    import IPCAssistant, ipcAssistantThreadProcess
from ATM_Zeta_RTA                    import RTA

from threading import Thread
import asyncio
import multiprocessing
import pyglet
import os
import time
import termcolor
from datetime import datetime, timedelta, timezone

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

#PROCESSES ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Process Auxillary --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def processTarget_AUX(IPCB_AUX_MAIN, IPCB_MAIN_AUX, IPCB_AUX_ATM, IPCB_ATM_AUX, IPCBStatusFlagAccessID, IPCBStatusFlagMemoryName):
    #IPC Module And Thread Initialization
    ipcA_MAIN = IPCAssistant("AUX", "MAIN", IPCB_AUX_MAIN, IPCBStatusFlagAccessID["AUX-MAIN_R"], IPCBStatusFlagAccessID["AUX-MAIN_T"], IPCBStatusFlagAccessID["AUX-MAIN_MP"], IPCB_MAIN_AUX, IPCBStatusFlagAccessID["MAIN-AUX_R"], IPCBStatusFlagAccessID["MAIN-AUX_T"], IPCBStatusFlagAccessID["MAIN-AUX_MP"], IPCBStatusFlagMemoryName)
    ipcA_ATM  = IPCAssistant("AUX", "ATM",  IPCB_AUX_ATM,  IPCBStatusFlagAccessID["AUX-ATM_R"],  IPCBStatusFlagAccessID["AUX-ATM_T"],  IPCBStatusFlagAccessID["AUX-ATM_MP"],  IPCB_ATM_AUX,  IPCBStatusFlagAccessID["ATM-AUX_R"],  IPCBStatusFlagAccessID["ATM-AUX_T"],  IPCBStatusFlagAccessID["ATM-AUX_MP"],  IPCBStatusFlagMemoryName)
    ipcAThread_MAIN = Thread(name = "ATM_ZETA_THREAD_IPC_AUX_MAIN", target = ipcAssistantThreadProcess, args = (ipcA_MAIN,), daemon = True)
    ipcAThread_ATM  = Thread(name = "ATM_ZETA_THREAD_IPC_AUX_ATM",  target = ipcAssistantThreadProcess, args = (ipcA_ATM,),  daemon = True)
    ipcAThread_MAIN.start()
    ipcAThread_ATM.start()

    #Wait for initialization command
    while (ipcA_MAIN.getPRD("PROCCTRL_INITGO") != True): time.sleep(0.01)
    m_AUX = manager_AUX(ipcA_MAIN, ipcA_ATM, ipcAThread_MAIN, ipcAThread_ATM)
    m_AUX.postInitialization()
    #Wait for process command
    while (ipcA_MAIN.getPRD("PROCCTRL_PROCGO") != True): time.sleep(0.01)
    print(termcolor.colored("AUX Process Start!", 'light_green'))
    m_AUX.process()
    print(termcolor.colored("AUX Process Terminated!", 'light_cyan'))
#Process Auxillary END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#Process ATM --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def processTarget_ATM(IPCB_ATM_MAIN, IPCB_MAIN_ATM, IPCB_ATM_AUX, IPCB_AUX_ATM, IPCBStatusFlagAccessID, IPCBStatusFlagMemoryName, nRTAs):
    #IPC Module And Thread Initialization
    ipcA = dict(); ipcAThreads = dict()
    ipcA['MAIN'] = IPCAssistant("ATM", "MAIN", IPCB_ATM_MAIN, IPCBStatusFlagAccessID["ATM-MAIN_R"], IPCBStatusFlagAccessID["ATM-MAIN_T"], IPCBStatusFlagAccessID["ATM-MAIN_MP"], IPCB_MAIN_ATM, IPCBStatusFlagAccessID["MAIN-ATM_R"], IPCBStatusFlagAccessID["MAIN-ATM_T"], IPCBStatusFlagAccessID["MAIN-ATM_MP"], IPCBStatusFlagMemoryName)
    ipcA['AUX']  = IPCAssistant("ATM", "AUX",  IPCB_ATM_AUX,  IPCBStatusFlagAccessID["ATM-AUX_R"],  IPCBStatusFlagAccessID["ATM-AUX_T"],  IPCBStatusFlagAccessID["ATM-AUX_MP"],  IPCB_AUX_ATM,  IPCBStatusFlagAccessID["AUX-ATM_R"],  IPCBStatusFlagAccessID["AUX-ATM_T"],  IPCBStatusFlagAccessID["AUX-ATM_MP"],  IPCBStatusFlagMemoryName)
    ipcAThreads['MAIN'] = Thread(name = "ATM_ZETA_THREAD_IPC_ATM_MAIN", target = ipcAssistantThreadProcess, args = (ipcA['MAIN'],), daemon = True)
    ipcAThreads['AUX']  = Thread(name = "ATM_ZETA_THREAD_IPC_ATM_AUX",  target = ipcAssistantThreadProcess, args = (ipcA['AUX'],),  daemon = True)
    ipcAThreads['MAIN'].start()
    ipcAThreads['AUX'].start()
    
    mpManager = multiprocessing.Manager()
    rtaList = list()
    rtaProcesses = dict()
    IPCBs = dict()
    IPCBStatusFlagAccessID_local = IPCBStatusFlagAccessID
    for i in range (nRTAs):
        rtaCode = "RTA"+str(i)
        rtaList.append(rtaCode)
        IPCBs["ATM-"+rtaCode] = mpManager.dict()
        IPCBs[rtaCode+"-ATM"] = mpManager.dict()
        IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_R"]  = len(IPCBStatusFlagAccessID_local)
        IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_T"]  = len(IPCBStatusFlagAccessID_local)
        IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_MP"] = len(IPCBStatusFlagAccessID_local)
        IPCBStatusFlagAccessID_local[rtaCode+"-ATM"+"_R"]  = len(IPCBStatusFlagAccessID_local)
        IPCBStatusFlagAccessID_local[rtaCode+"-ATM"+"_T"]  = len(IPCBStatusFlagAccessID_local)
        IPCBStatusFlagAccessID_local[rtaCode+"-ATM"+"_MP"] = len(IPCBStatusFlagAccessID_local)
        ipcA[rtaCode] = IPCAssistant("ATM", rtaCode, 
                                     IPCBs["ATM-"+rtaCode], IPCBStatusFlagAccessID["ATM-"+rtaCode+"_R"], IPCBStatusFlagAccessID["ATM-"+rtaCode+"_T"], IPCBStatusFlagAccessID["ATM-"+rtaCode+"_MP"], 
                                     IPCBs[rtaCode+"-ATM"], IPCBStatusFlagAccessID[rtaCode+"-ATM"+"_R"], IPCBStatusFlagAccessID[rtaCode+"-ATM"+"_T"], IPCBStatusFlagAccessID[rtaCode+"-ATM_MP"], 
                                     IPCBStatusFlagMemoryName)
        ipcAThreads[rtaCode] = Thread(name = "ATM_ZETA_THREAD_IPC_ATM_"+rtaCode, target = ipcAssistantThreadProcess, args = (ipcA[rtaCode],), daemon = True)
        ipcAThreads[rtaCode].start()
        rtaProcesses[rtaCode] = multiprocessing.Process(name = "ATM_ZETA_PROCESS_ATM", target = processTarget_RTA, args = (rtaCode, IPCBs[rtaCode+"-ATM"], IPCBs["ATM-"+rtaCode], IPCBStatusFlagAccessID_local, IPCBStatusFlagMemoryName))
        rtaProcesses[rtaCode].start()
        
    #Wait for initialization command
    while (ipcA['AUX'].getPRD("PROCCTRL_INITGO") != True): time.sleep(0.01)
    m_Central = manager_Central(ipcA, ipcAThreads, rtaList, rtaProcesses)
    m_Central.postInitialization()
    #Wait for process command
    while (ipcA['MAIN'].getPRD("PROCCTRL_PROCGO") != True): time.sleep(0.01)
    print(termcolor.colored("ATM Process Start!", 'light_green'))
    m_Central.process()
#Process ATM END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#Process RTA (Run-Time Analyzer) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def processTarget_RTA(rtaCode, IPCB_RTA_ATM, IPCB_ATM_RTM, IPCBStatusFlagAccessID_local, IPCBStatusFlagMemoryName):
    #IPC Module And Thread Initialization
    ipcA = IPCAssistant(rtaCode, "ATM", IPCB_RTA_ATM, IPCBStatusFlagAccessID_local[rtaCode+"-ATM"+"_R"], IPCBStatusFlagAccessID_local[rtaCode+"-ATM"+"_T"], IPCBStatusFlagAccessID_local[rtaCode+"-ATM_MP"], IPCB_ATM_RTM, IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_R"], IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_T"], IPCBStatusFlagAccessID_local["ATM-"+rtaCode+"_MP"], IPCBStatusFlagMemoryName)
    ipcAThread = Thread(name = "ATM_ZETA_THREAD_IPC_"+rtaCode+"_ATM", target = ipcAssistantThreadProcess, args = (ipcA,), daemon = True)
    ipcAThread.start()

    #Wait for initialization command
    while (ipcA.getPRD("PROCCTRL_INITGO") != True): time.sleep(0.01)
    rta = RTA(ipcA, ipcAThread, rtaCode)
    rta.postInitialization()
    #Wait for process command
    while (ipcA.getPRD("PROCCTRL_PROCGO") != True): time.sleep(0.01)
    print(termcolor.colored("{:s} Process Start!".format(rtaCode), 'green'))
    rta.process()
#Process RTA (Run-Time Analyzer) END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#PROCESSES END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#MAIN -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#'__main__' Function
if __name__ == "__main__":
    programStartTime = time.time()
    n_CPU = os.cpu_count()
    nRTAs = n_CPU - 5
    print(termcolor.colored("Starting AUTO TRADE MACHINE - ZETA!", 'cyan'))
    print("Program Start Time:  {:s} LOCAL".format(datetime.fromtimestamp(programStartTime).strftime("%Y-%m-%d %H:%M")))
    print("                     {:s} UTC".format(datetime.fromtimestamp(programStartTime, tz = timezone.utc).strftime("%Y-%m-%d %H:%M")))
    print("Existing CPU Cores: {:d}".format(n_CPU))
    print("Number of RTAs: {:d}".format(nRTAs))

    #Processes and IPC Connections Generation
    print("\nGenerating Processes and IPC Connections...")
    multiprocessing.freeze_support()

    #IPC Buffer Initialization
    mpManager = multiprocessing.Manager()

    #Multiprocessing Setup
    IPCBs = dict()

    nAttempts = 0
    while (True):
        try:
            IPCBStatusFlagMemory = multiprocessing.shared_memory.SharedMemory(name = "ATM_Zeta_IPCBStatusFlagMemory", create = True, size = 4096)
            break
        except:
            if (nAttempts < 10): nAttempts += 1; time.sleep(0.5)
            else: exit()

    IPCBStatusFlagAccessID = dict()
    connections = ("MAIN-AUX", "MAIN-ATM", "AUX-MAIN", "AUX-ATM", "ATM-MAIN", "ATM-AUX")
    for connection in connections:
        IPCBs[connection] = mpManager.dict()
        IPCBStatusFlagAccessID[connection+"_R"]  = len(IPCBStatusFlagAccessID)
        IPCBStatusFlagAccessID[connection+"_T"]  = len(IPCBStatusFlagAccessID)
        IPCBStatusFlagAccessID[connection+"_MP"] = len(IPCBStatusFlagAccessID)

    process_AUX = multiprocessing.Process(name = "ATM_ZETA_PROCESS_AUX", target = processTarget_AUX, args = (IPCBs["AUX-MAIN"], IPCBs["MAIN-AUX"], IPCBs["AUX-ATM"], IPCBs["ATM-AUX"], IPCBStatusFlagAccessID, IPCBStatusFlagMemory.name))
    process_ATM = multiprocessing.Process(name = "ATM_ZETA_PROCESS_ATM", target = processTarget_ATM, args = (IPCBs["ATM-MAIN"], IPCBs["MAIN-ATM"], IPCBs["ATM-AUX"], IPCBs["AUX-ATM"], IPCBStatusFlagAccessID, IPCBStatusFlagMemory.name, nRTAs))
    process_AUX.start()
    process_ATM.start()

    ipcA_MAIN_AUX = IPCAssistant("MAIN", "AUX", IPCBs["MAIN-AUX"], IPCBStatusFlagAccessID["MAIN-AUX_R"], IPCBStatusFlagAccessID["MAIN-AUX_T"], IPCBStatusFlagAccessID["MAIN-AUX_MP"], IPCBs["AUX-MAIN"], IPCBStatusFlagAccessID["AUX-MAIN_R"], IPCBStatusFlagAccessID["AUX-MAIN_T"], IPCBStatusFlagAccessID["AUX-MAIN_MP"], IPCBStatusFlagMemory.name)
    ipcA_MAIN_ATM = IPCAssistant("MAIN", "ATM", IPCBs["MAIN-ATM"], IPCBStatusFlagAccessID["MAIN-ATM_R"], IPCBStatusFlagAccessID["MAIN-ATM_T"], IPCBStatusFlagAccessID["MAIN-ATM_MP"], IPCBs["ATM-MAIN"], IPCBStatusFlagAccessID["ATM-MAIN_R"], IPCBStatusFlagAccessID["ATM-MAIN_T"], IPCBStatusFlagAccessID["ATM-MAIN_MP"], IPCBStatusFlagMemory.name)
    ipcA_MAIN_AUX_Thread = Thread(name = "ATM_ZETA_THREAD_IPC_MAIN_AUX", target = ipcAssistantThreadProcess, args = (ipcA_MAIN_AUX,), daemon = True)
    ipcA_MAIN_ATM_Thread = Thread(name = "ATM_ZETA_THREAD_IPC_MAIN_ATM", target = ipcAssistantThreadProcess, args = (ipcA_MAIN_ATM,), daemon = True)
    ipcA_MAIN_AUX_Thread.start()
    ipcA_MAIN_ATM_Thread.start()
    print("MAIN Processes and IPC Connections Generation Complete!")
    
    #GUI Manager Instantiation
    m_GUI = manager_GUI(ipcA_MAIN_AUX, ipcA_MAIN_ATM, ipcA_MAIN_AUX_Thread, ipcA_MAIN_ATM_Thread, process_AUX, process_ATM)
    m_GUI.postInitialization()
    
    #Termination Sequence, by this point, all of the child processes and threads are terminated
    print("<<<<< PROGRAM TERMINATION SEQUENCE COMPLETE! >>>>>")
    countDown = 10
    for i in range (countDown):
        print("Exiting Terminal in {:d}...".format(countDown-i))
        time.sleep(1)

#MAIN END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------