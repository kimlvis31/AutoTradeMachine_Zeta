import multiprocessing
import time
import pprint
import termcolor

_PORTDIRECTION_R = 0
_PORTDIRECTION_T = 1

_TIDISSUELIMIT  = 100000
_RRIDISSUELIMIT = 100000

class IPCAssistant:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, processName1, processName2, IPCB_R, IPCBStatusFlagAccessIndex_R_R, IPCBStatusFlagAccessIndex_R_T, IPCBStatusFlagAccessIndex_R_MP, IPCB_T, IPCBStatusFlagAccessIndex_T_R, IPCBStatusFlagAccessIndex_T_T, IPCBStatusFlagAccessIndex_T_MP, IPCBStatusFlagMemoryName):
        #Shared-Memory Instantiation
        self.processName1 = processName1
        self.processName2 = processName2

        self.IPCB_R                         = IPCB_R
        self.IPCBStatusFlagAccessIndex_R_R  = IPCBStatusFlagAccessIndex_R_R
        self.IPCBStatusFlagAccessIndex_R_T  = IPCBStatusFlagAccessIndex_R_T
        self.IPCBStatusFlagAccessIndex_R_MP = IPCBStatusFlagAccessIndex_R_MP

        self.IPCB_T                         = IPCB_T
        self.IPCBStatusFlagAccessIndex_T_R  = IPCBStatusFlagAccessIndex_T_R
        self.IPCBStatusFlagAccessIndex_T_T  = IPCBStatusFlagAccessIndex_T_T
        self.IPCBStatusFlagAccessIndex_T_MP = IPCBStatusFlagAccessIndex_T_MP
                
        self.IPCBStatusFlagMemory = multiprocessing.shared_memory.SharedMemory(name = IPCBStatusFlagMemoryName)
        self.IPCBStatusFlag = self.IPCBStatusFlagMemory.buf

        #IPC Thread Control Variable
        self.continueIPCThread = True

        #IPC Control Variables
        self.PRD_R = dict()
        self.PRDEDIT_T   = dict(); self.PRDEDIT_T_PendingRATIDs   = list()
        self.PRDREMOVE_T = dict(); self.PRDREMOVE_T_PendingRATIDs = list()
        self.FAR_R = list()
        self.FAR_T = dict(); self.FAR_T_PendingRATIDs = list()
        self.FARR_R = dict()
        self.FARR_T = dict(); self.FARR_T_PendingRATIDs = list()

        self.IPCB_T_Buffer = {'RC': list()}
        self.IPCB_R_Buffer = {'RC': list()}

        self.tid_Availables = set(range(0, _TIDISSUELIMIT))
        self.tid_Issued = dict()
        
        self.rrid_Availables = set(range(0, _RRIDISSUELIMIT))

        self.FARHandlers = dict()
        self.FARRHandlers = dict()
        
        #Initialize the IPCB availability flags from this side
        self.__raiseIPCBAvailabilityFlag(_PORTDIRECTION_R)
        self.__raiseIPCBAvailabilityFlag(_PORTDIRECTION_T)
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










    #Thread Call Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self):
        self.__readIPCB()
        self.__reallocateTMessages()
        self.__writeIPCB()
        return self.continueIPCThread
    #Thread Call Functions END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










    #Manager & Process Call Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getPRD(self, dataAddress):
        try:
            ad = dataAddress
            if ((type(ad) == list) or (type(ad) == tuple)):
                adLen = len(ad)
                if   (adLen == 1):  return self.PRD_R[ad[0]]
                elif (adLen == 2):  return self.PRD_R[ad[0]][ad[1]]
                elif (adLen == 3):  return self.PRD_R[ad[0]][ad[1]][ad[2]]
                elif (adLen == 4):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]]
                elif (adLen == 5):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]]
                elif (adLen == 6):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]]
                elif (adLen == 7):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]]
                elif (adLen == 8):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]]
                elif (adLen == 9):  return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]]
                elif (adLen == 10): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]]
                elif (adLen == 11): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]]
                elif (adLen == 12): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]]
                elif (adLen == 13): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]]
                elif (adLen == 14): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]]
                elif (adLen == 15): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]]
                elif (adLen == 16): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]]
                elif (adLen == 17): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]]
                elif (adLen == 18): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]]
                elif (adLen == 19): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]]
                elif (adLen == 20): return self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]][ad[19]]
            else: return self.PRD_R[ad]
        except: return "#DNF#"

    def processFARs(self):
        while (0 < len(self.FAR_R)):
            far = self.FAR_R.pop(0)
            functionID = far['FunctionID']; functionParams = far['FunctionParams']; rrID = far['RRID']
            if (functionID in self.FARHandlers.keys()):
                handlerFunction = self.FARHandlers[functionID]
                if (rrID == None): handlerFunction(functionParams)
                else:              self.__sendFARR(handlerFunction(functionParams), rrID)
            elif (rrID != None): self.__sendFARR("#FNF#", rrID) #'#FNF#' = Function Not Found

    def processFARRs(self):
        for rrid, faResult in self.FARR_R.items():
            self.FARRHandlers[rrid](faResult)
            del self.FARRHandlers[rrid]
            self.__retrieveRRID(rrid)
        self.FARR_R.clear()

    def sendPRDEDIT(self, dataAddress, dataContent, timeout = 3000, nMaxDispatch = 5):
        tID = self.__issueTID("PRDEDIT")
        if (tID != None):
            self.PRDEDIT_T[tID] = {'PRDAddress': dataAddress, 'PRDContent': dataContent,
                                   'status': 'pending', 'tDispatch': None, 'nDispatch': 0, 'nDispatchLimit': nMaxDispatch, 'timeout': timeout, 'tRegistration': time.perf_counter_ns()}
            self.PRDEDIT_T_PendingRATIDs.append(tID)
            return True
        else: return False

    def sendPRDREMOVE(self, dataAddress, timeout = 3000, nMaxDispatch = 5):
        tID = self.__issueTID("PRDREMOVE")
        if (tID != None):
            self.PRDREMOVE_T[tID] = {'PRDAddress': dataAddress,
                                     'status': 'pending', 'tDispatch': None, 'nDispatch': 0, 'nDispatchLimit': nMaxDispatch, 'timeout': timeout, 'tRegistration': time.perf_counter_ns()}
            self.PRDREMOVE_T_PendingRATIDs.append(tID)
            return True
        else: return False

    def sendFAR(self, functionID, functionParams = None, FARRHandler = None, timeout = 3000, nMaxDispatch = 5):
        tID = self.__issueTID("FAR")
        if (tID != None):
            if (FARRHandler == None): rrID = None
            else:                     rrID = self.__issueRRID(); self.FARRHandlers[rrID] = FARRHandler
            self.FAR_T[tID] = {'FunctionID': functionID, 'FunctionParams': functionParams, 'RRID': rrID,
                               'status': 'pending', 'tDispatch': None, 'nDispatch': 0, 'nDispatchLimit': nMaxDispatch, 'timeout': timeout, 'tRegistration': time.perf_counter_ns()}
            self.FAR_T_PendingRATIDs.append(tID)
            return True
        else: return False
     
    def __sendFARR(self, faResult, rrID): #Not a manager call function, but placed here for better readability
        tID = self.__issueTID("FARR")
        if (tID != None):
            self.FARR_T[tID] = {'FAResult': faResult, 'RRID': rrID,
                                'status': 'pending', 'tDispatch': None, 'nDispatch': 0, 'nDispatchLimit': 'INF', 'timeout': 3000, 'tRegistration': time.perf_counter_ns()}
            self.FARR_T_PendingRATIDs.append(tID)
            return True
        else: return False

    def addFARHandler(self, functionID, handlerFunction):
        self.FARHandlers[functionID] = handlerFunction

    def removeFARHandler(self, functionID):
        if (functionID in self.FARHandlers): del self.FARHandlers[functionID]

    def terminate(self):
        print(termcolor.colored("[{:s}->{:s}] IPCA Termination Command Received, one last process will be performed".format(self.processName1, self.processName2), 'cyan'))
        self.continueIPCThread = False
    #Manager Call Functions END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










    #Internal Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #IPCB_R Read ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __readIPCB(self):
        #Check if there are any messages to read
        if (self.__isIPCBPending(_PORTDIRECTION_R)):                         #1. Check if there exists any pending message
            if (self.__lowerIPCBAvailabilityFlag(_PORTDIRECTION_R) == True): #2. Attempt to lower the IPCB availability flag to indicate that it is being used
                self.IPCB_R_Buffer = self.IPCB_R.copy()                      #3. Localize the data from IPCB_R
                self.IPCB_R.clear()                                          #4. Clear IPCB_R
                self.__lowerIPCBPendingFlag(_PORTDIRECTION_R)                #5. Lower the IPCB pending flag to indicate there exist no messages to read
                self.__raiseIPCBAvailabilityFlag(_PORTDIRECTION_R)           #6. Raise the IPCB availability flag to indicate that it is now available
                self.__reallocateRMessages()                                 #7. Reallocate & interpret received messages
                self.__processExpiredMessages()                              #8. Determine and handle expired messages
    #IPCB_R Read END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    
    #R-Messages Re-allocation ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __reallocateRMessages(self):
        try:
            #Handle Receival Confirmed TIDs
            for tID_RCed in self.IPCB_R_Buffer['RC']:
                #Get the tID holder type
                tIDHolder = self.tid_Issued[tID_RCed]
                #For PRDEDIT and PRDREMOVE, simply retrieve the tIDs
                if   ((tIDHolder == "PRDEDIT")   and (tID_RCed in self.PRDEDIT_T)):   del self.PRDEDIT_T[tID_RCed]
                elif ((tIDHolder == "PRDREMOVE") and (tID_RCed in self.PRDREMOVE_T)): del self.PRDREMOVE_T[tID_RCed]
                elif ((tIDHolder == "FAR")       and (tID_RCed in self.FAR_T)):       del self.FAR_T[tID_RCed]
                elif ((tIDHolder == "FARR")      and (tID_RCed in self.FARR_T)):      del self.FARR_T[tID_RCed]
                self.__retrieveTID(tID_RCed)
            del self.IPCB_R_Buffer['RC']
            #Handle Inter-Modular Messages
            msgs = [(tID,)+self.IPCB_R_Buffer[tID] for tID in self.IPCB_R_Buffer];msgs.sort(key = lambda x: x[2])

            for msg in msgs:
                msgType = msg[1]
                if   (msgType == "PRDEDIT"):   self.__interpret_PRDEDIT(msg[3], msg[4])
                elif (msgType == "PRDREMOVE"): self.__interpret_PRDREMOVE(msg[3])
                elif (msgType == "FAR"):       self.__interpret_FAR(msg[3], msg[4], msg[5])
                elif (msgType == "FARR"):      self.__interpret_FARR(msg[3], msg[4])
                self.IPCB_T_Buffer['RC'].append(msg[0]) #Send Receival Complete Message to indicate the message has been successfully received
            self.IPCB_R_Buffer = {'RC': list()}
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] Error Occured During RMessages Reallocation:\n *".format(self.processName1, self.processName2), 'light_red'), termcolor.colored(e, 'light_red'))
    #R-Messages Re-allocation END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    

    #Expired Messages Handling --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __processExpiredMessages(self):
        try:
            expiredMessages = list()
            #Check for any time-out messages
            checkTime = time.perf_counter_ns()

            #Expired PRDEDIT_T Search
            searchTarget = 'PRDEDIT'
            for tID in list(self.PRDEDIT_T.keys()):
                if (self.PRDEDIT_T[tID]['status'] == 'dispatched') and (self.PRDEDIT_T[tID]['timeout']*1e6 < (checkTime - self.PRDEDIT_T[tID]['tDispatch'])): #If the message has been dispatched & Timeout has occured
                    if ((self.PRDEDIT_T[tID]['nDispatchLimit'] == 'INF') or (self.PRDEDIT_T[tID]['nDispatch'] < self.PRDEDIT_T[tID]['nDispatchLimit'])): #If the message is still re-dispatchable,
                        self.IPCB_T_Buffer[tID] = ("PRDEDIT", self.PRDEDIT_T[tID]['tRegistration'], self.PRDEDIT_T[tID]['PRDAddress'], self.PRDEDIT_T[tID]['PRDContent']) #Add the message to the IPCB_T buffer for a re-dispatch
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A PRDEDIT added back to the IPCB_T_Buffer for a re-dispatch\n - TID: {:d}\n - PRDAddress: {:s}\n - PRDContent: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID,
                                                                                                                                                                                                                   str(self.PRDEDIT_T[tID]['PRDAddress']), str(self.PRDEDIT_T[tID]['PRDContent']),
                                                                                                                                                                                                                   self.PRDEDIT_T[tID]['nDispatch']+1, str(self.PRDEDIT_T[tID]['nDispatchLimit'])), 'light_cyan'))
                    else: #If the message is no longer re-dispatchable
                        expiredMessages.append((tID, "PRDEDIT")) #Append the message to the expired message handling queue
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A PRDEDIT Expired\n - TID: {:d}\n - PRDAddress: {:s}\n - PRDContent: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID,
                                                                                                                                                                         str(self.PRDEDIT_T[tID]['PRDAddress']), str(self.PRDEDIT_T[tID]['PRDContent']),
                                                                                                                                                                         self.PRDEDIT_T[tID]['nDispatch'], str(self.PRDEDIT_T[tID]['nDispatchLimit'])), 'cyan'))

            #Expired PRDREMOVE_T Search
            searchTarget = 'PRDREMOVE'
            for tID in list(self.PRDREMOVE_T.keys()):
                if (self.PRDREMOVE_T[tID]['status'] == 'dispatched') and (self.PRDREMOVE_T[tID]['timeout']*1e6 < (checkTime - self.PRDREMOVE_T[tID]['tDispatch'])): #If the message has been dispatched & Timeout has occured
                    if ((self.PRDREMOVE_T[tID]['nDispatchLimit'] == 'INF') or (self.PRDREMOVE_T[tID]['nDispatch'] < self.PRDREMOVE_T[tID]['nDispatchLimit'])): #If the message is still re-dispatchable,
                        self.IPCB_T_Buffer[tID] = ("PRDREMOVE", self.PRDREMOVE_T[tID]['tRegistration'], self.PRDREMOVE_T[tID]['PRDAddress'])  #Add the message to the IPCB_T buffer for a re-dispatch
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A PRDREMOVE added back to the IPCB_T_Buffer for a re-dispatch\n - TID: {:d}\n - PRDAddress: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID,
                                                                                                                                                                                                str(self.PRDREMOVE_T[tID]['PRDAddress']),
                                                                                                                                                                                                self.PRDREMOVE_T[tID]['nDispatch']+1, str(self.PRDREMOVE_T[tID]['nDispatchLimit'])), 'light_cyan'))
                    else: #If the message is no longer re-dispatchable
                        expiredMessages.append((tID, "PRDREMOVE"))  #Append the message to the expired message handling queue
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A PRDREMOVE Expired\n - TID: {:d}\n - PRDAddress: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID,
                                                                                                                                                      str(self.PRDREMOVE_T[tID]['PRDAddress']),
                                                                                                                                                      self.PRDREMOVE_T[tID]['nDispatch'], str(self.PRDREMOVE_T[tID]['nDispatchLimit'])), 'cyan'))

            #Expired FAR Search
            searchTarget = 'FAR'
            for tID in list(self.FAR_T.keys()):
                if (self.FAR_T[tID]['status'] == 'dispatched') and (self.FAR_T[tID]['timeout']*1e6 < (checkTime - self.FAR_T[tID]['tDispatch'])): #If the message has been dispatched & Timeout has occured
                    if ((self.FAR_T[tID]['nDispatchLimit'] == 'INF') or (self.FAR_T[tID]['nDispatch'] < self.FAR_T[tID]['nDispatchLimit'])): #If the message is still re-dispatchable,
                        self.IPCB_T_Buffer[tID] = ("FAR", self.FAR_T[tID]['tRegistration'], self.FAR_T[tID]['FunctionID'], self.FAR_T[tID]['FunctionParams'], self.FAR_T[tID]['RRID'])  #Add the message to the IPCB_T buffer for a re-dispatch
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A FAR added back to the IPCB_T_Buffer for a re-dispatch\n - TID: {:d}\n - RRID: {:s}\n - FunctionID: {:s}\n - FunctionParams: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID, str(self.FAR_T[tID]['RRID']),
                                                                                                                                                                                                                                  str(self.FAR_T[tID]['FunctionID']), str(self.FAR_T[tID]['FunctionParams']),
                                                                                                                                                                                                                                  self.FAR_T[tID]['nDispatch']+1, str(self.FAR_T[tID]['nDispatchLimit'])), 'light_cyan'))
                    else: #If the message is no longer re-dispatchable
                        expiredMessages.append((tID, "FAR"))  #Append the message to the expired message handling queue
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A FAR Expired\n - TID: {:d}\n - RRID: {:s}\n - FunctionID: {:s}\n - FunctionParams: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID, str(self.FAR_T[tID]['RRID']),
                                                                                                                                                                                        str(self.FAR_T[tID]['FunctionID']), str(self.FAR_T[tID]['FunctionParams']),
                                                                                                                                                                                        self.FAR_T[tID]['nDispatch'], str(self.FAR_T[tID]['nDispatchLimit'])), 'cyan'))

            #Expired FARR Search
            searchTarget = 'FARR'
            for tID in list(self.FARR_T.keys()):
                if (self.FARR_T[tID]['status'] == 'dispatched') and (self.FARR_T[tID]['timeout']*1e6 < (checkTime - self.FARR_T[tID]['tDispatch'])): #If the message has been dispatched & Timeout has occured
                    if ((self.FARR_T[tID]['nDispatchLimit'] == 'INF') or (self.FARR_T[tID]['nDispatch'] < self.FARR_T[tID]['nDispatchLimit'])): #If the message is still re-dispatchable,
                        self.IPCB_T_Buffer[tID] = ("FARR", self.FARR_T[tID]['tRegistration'], self.FARR_T[tID]['FAResult'], self.FARR_T[tID]['RRID'])  #Add the message to the IPCB_T buffer for a re-dispatch
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A FARR added back to the IPCB_T_Buffer for a re-dispatch\n - TID: {:d}\n - RRID: {:s}\n - FAResult: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID, str(self.FARR_T[tID]['RRID']),
                                                                                                                                                                                                        str(self.FARR_T[tID]['FAResult']),
                                                                                                                                                                                                        self.FARR_T[tID]['nDispatch']+1, str(self.FARR_T[tID]['nDispatchLimit'])), 'light_cyan'))
                    else: #If the message is no longer re-dispatchable
                        expiredMessages.append((tID, "FARR"))  #Append the message to the expired message handling queue
                        #Print Report
                        print(termcolor.colored('[{:s}->{:s}] A FARR Expired\n - TID: {:d}\n - RRID: {:s}\n - FAResult: {:s}\n nDispatch: {:d} / {:s}'.format(self.processName1, self.processName2, tID, str(self.FARR_T[tID]['RRID']),
                                                                                                                                                              str(self.FARR_T[tID]['FAResult']),
                                                                                                                                                              self.FARR_T[tID]['nDispatch'], str(self.FARR_T[tID]['nDispatchLimit'])), 'cyan'))

        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] Error Occured During Expired Messages {:s} Search\n *".format(self.processName1, self.processName2, searchTarget), 'light_red'), termcolor.colored(e, 'light_red'))

        try:
            #Handle Expired Messages
            for expiredMsg in expiredMessages:
                tID_Expired = expiredMsg[0]; tIDHolder = expiredMsg[1]
                msgContent = None
                if   ((tIDHolder == "PRDEDIT")   and (tID_Expired in self.PRDEDIT_T)):   msgContent = self.PRDEDIT_T[tID_Expired];   del self.PRDEDIT_T[tID_Expired]
                elif ((tIDHolder == "PRDREMOVE") and (tID_Expired in self.PRDREMOVE_T)): msgContent = self.PRDREMOVE_T[tID_Expired]; del self.PRDREMOVE_T[tID_Expired]
                elif ((tIDHolder == "FAR")       and (tID_Expired in self.FAR_T)):       msgContent = self.FAR_T[tID_Expired];       del self.FAR_T[tID_Expired]
                elif ((tIDHolder == "FARR")      and (tID_Expired in self.FARR_T)):      msgContent = self.FARR_T[tID_Expired];      del self.FARR_T[tID_Expired]
                self.__retrieveTID(tID_Expired)
                print(termcolor.colored("[{:s}<->{:s}] An expired TID retrieved and the corresponding message is destoryed <tID: {:d}, tIDHolder: {:s}>\n * <{:s}>".format(self.processName1, self.processName2, tID_Expired, tIDHolder, str(msgContent))))
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] Error Occured During Expired Messages Handling\n *".format(self.processName1, self.processName2), 'light_red'), termcolor.colored(e, 'light_red'))

    #Expired Messages Handling END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #T-Messages Re-allocation ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __reallocateTMessages(self):
        try:
            while (0 < len(self.PRDEDIT_T_PendingRATIDs)):   tID = self.PRDEDIT_T_PendingRATIDs.pop();   self.IPCB_T_Buffer[tID] = ("PRDEDIT",   self.PRDEDIT_T[tID]['tRegistration'],   self.PRDEDIT_T[tID]['PRDAddress'], self.PRDEDIT_T[tID]['PRDContent'])
            while (0 < len(self.PRDREMOVE_T_PendingRATIDs)): tID = self.PRDREMOVE_T_PendingRATIDs.pop(); self.IPCB_T_Buffer[tID] = ("PRDREMOVE", self.PRDREMOVE_T[tID]['tRegistration'], self.PRDREMOVE_T[tID]['PRDAddress'])
            while (0 < len(self.FAR_T_PendingRATIDs)):       tID = self.FAR_T_PendingRATIDs.pop();       self.IPCB_T_Buffer[tID] = ("FAR",       self.FAR_T[tID]['tRegistration'],       self.FAR_T[tID]['FunctionID'], self.FAR_T[tID]['FunctionParams'], self.FAR_T[tID]['RRID'])
            while (0 < len(self.FARR_T_PendingRATIDs)):      tID = self.FARR_T_PendingRATIDs.pop();      self.IPCB_T_Buffer[tID] = ("FARR",      self.FARR_T[tID]['tRegistration'],      self.FARR_T[tID]['FAResult'], self.FARR_T[tID]['RRID'])
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] Error Occured During TMessages Reallocation\n *".format(self.processName1, self.processName2), 'light_red'), termcolor.colored(e, 'light_red'))
    #T-Messages Re-allocation END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #IPCB_T Write ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __writeIPCB(self):
        try:
            #If the IPCB_T is available, patch the messages in the buffer
            if ((1 < len(self.IPCB_T_Buffer)) or (0 < len(self.IPCB_T_Buffer['RC']))):                                                               #1. If there exist any messages to write              
                if (self.__lowerIPCBAvailabilityFlag(_PORTDIRECTION_T) == True):                                                                     #2. Attempt to lower the IPCB status flag to indicate that it is being used
                    if (self.__isIPCBPending(_PORTDIRECTION_T)):                                                                                     #3. If the IPCB is already in MP (Message Pending) State,
                        try:    self.IPCB_T_Buffer['RC'] += self.IPCB_T['RC']                                                                            #Try to retrieve the rcList before it is overwritten
                        except: pass                                                                                                                     #If there exists no rcList in the IPCB, simply pass
                    self.IPCB_T.update(self.IPCB_T_Buffer)                                                                                           #3. Patch the messages in the buffer to the IPCB_T
                    dispatchTime = time.perf_counter_ns()                                                                                            #4. Record the dispatch time
                    self.__raiseIPCBPendingFlag(_PORTDIRECTION_T)                                                                                    #5. Raise the IPCB Message Pending Flag
                    self.__raiseIPCBAvailabilityFlag(_PORTDIRECTION_T)                                                                               #6. Lower the IPCB_T status flag to indicate that it is now available
                    del self.IPCB_T_Buffer['RC']                                                                                                     #7. Remove ReceivalComplete list from the buffer
                    for tID in self.IPCB_T_Buffer:                                                                                                   #8. Write the dispatch time to the local IPCB message records
                        msgType = self.IPCB_T_Buffer[tID][0]
                        if (msgType == "PRDEDIT"):
                            self.PRDEDIT_T[tID]['status']    = 'dispatched'
                            self.PRDEDIT_T[tID]['tDispatch'] = dispatchTime
                            self.PRDEDIT_T[tID]['nDispatch'] += 1
                        elif (msgType == "PRDREMOVE"):
                            self.PRDREMOVE_T[tID]['status']    = 'dispatched'
                            self.PRDREMOVE_T[tID]['tDispatch'] = dispatchTime
                            self.PRDREMOVE_T[tID]['nDispatch'] += 1
                        elif (msgType == "FAR"):
                            self.FAR_T[tID]['status']    = 'dispatched'
                            self.FAR_T[tID]['tDispatch'] = dispatchTime
                            self.FAR_T[tID]['nDispatch'] += 1
                        elif (msgType == "FARR"):
                            self.FARR_T[tID]['status']    = 'dispatched'
                            self.FARR_T[tID]['tDispatch'] = dispatchTime
                            self.FARR_T[tID]['nDispatch'] += 1
                    self.IPCB_T_Buffer = {'RC': list()}                                                                                              #9. Reset the local IPCB_T buffer
        except Exception as e: 
            print(termcolor.colored("[IPCA {:s}->{:s}] Error Occured During IPCB Write\n *".format(self.processName1, self.processName2), 'light_red'), termcolor.colored(e, 'light_red'))
    #IPCB_T Write END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #Auxiallry Internal Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __raiseIPCBAvailabilityFlag(self, portDirection):
        if   (portDirection == _PORTDIRECTION_R): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_R] = 1
        elif (portDirection == _PORTDIRECTION_T): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_T] = 1
        
    def __lowerIPCBAvailabilityFlag(self, portDirection):
        if (portDirection == _PORTDIRECTION_R):
            if (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_T] == 1):                   #[1]: First check if the receival port is available according to the transmitter (the other side)
                self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_R] = 0                      #[2]: Lower the availability flag from this side
                if   (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_T] == 1): return True #[3-1]: If the availability flag from the other side is still 1 (meaning nothing happened on the otherside), return True to indicate successful flag lowering
                elif (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_T] == 0):             #[3-2]: If the availability flag from the other side is now 0 (meaning something happened on the otherside), return False to indicate failed flag lowering
                    self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_R] = 1
                    return False
            
        elif (portDirection == _PORTDIRECTION_T):
            if (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_R] == 1):                   #[1]: First check if the transmission port is available according to the receiver (the other side)
                self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_T] = 0                      #[2]: Lower the availability flag from this side
                if   (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_R] == 1): return True #[3-1]: If the availability flag from the other side is still 1 (meaning nothing happened on the otherside), return True to indicate successful flag lowering
                elif (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_R] == 0):             #[3-2]: If the availability flag from the other side is now 0 (meaning something happened on the otherside), return False to indicate failed flag lowering
                    self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_T] = 1
                    return False
                
    def __isIPCBPending(self, portDirection):
        if   (portDirection == _PORTDIRECTION_R): return (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_MP] == 1)
        elif (portDirection == _PORTDIRECTION_T): return (self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_MP] == 1)
        
    def __raiseIPCBPendingFlag(self, portDirection):
        if   (portDirection == _PORTDIRECTION_R): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_MP] = 1
        elif (portDirection == _PORTDIRECTION_T): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_MP] = 1
    
    def __lowerIPCBPendingFlag(self, portDirection):
        if   (portDirection == _PORTDIRECTION_R): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_R_MP] = 0
        elif (portDirection == _PORTDIRECTION_T): self.IPCBStatusFlag[self.IPCBStatusFlagAccessIndex_T_MP] = 0
        
    def __issueTID(self, holder):
        if (0 < len(self.tid_Availables)):
            tID = self.tid_Availables.pop()
            self.tid_Issued[tID] = holder
            return tID
        else: 
            print("[IPCA {:s}->{:s}] TID Issue Rejected: There exists no available TID".format(self.processName1, self.processName2))
            return None
    def __retrieveTID(self, tID):
        if (tID in self.tid_Issued):
            if (tID not in self.tid_Availables):
                self.tid_Availables.add(tID)
                del self.tid_Issued[tID]
            else: print("[IPCA {:s}->{:s}]".format(self.processName1, self.processName2), "TID {:d} Retreival Failed, TID is already in the availables set".format(tID))
        else: print("[IPCA {:s}->{:s}]".format(self.processName1, self.processName2), "TID {:d} Retreival Failed, the TID is not in the issued TID dictionary".format(tID))
    def __issueRRID(self):
        if (0 < len(self.rrid_Availables)):
            rrID = self.rrid_Availables.pop()
            return rrID
        else:
            print("[IPCA {:s}->{:s}] RRID Issue Rejected: There exists no available RRID".format(self.processName1, self.processName2))
            return None
    def __retrieveRRID(self, rrID):
        if (rrID not in self.rrid_Availables): self.rrid_Availables.add(rrID)
        else: print("[IPCA {:s}->{:s}]".format(self.processName1, self.processName2), "RRID {:d} Retreival Failed, RRID is already in the availables set".format(rrID))

    def __interpret_PRDEDIT(self, prdAddress, prdContent):
        try:
            ad = prdAddress
            if ((type(ad) == list) or (type(ad) == tuple)):
                adLen = len(ad)
                if  (adLen==1):  self.PRD_R[ad[0]] = prdContent
                elif(adLen==2):  self.PRD_R[ad[0]][ad[1]] = prdContent
                elif(adLen==3):  self.PRD_R[ad[0]][ad[1]][ad[2]] = prdContent
                elif(adLen==4):  self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]] = prdContent
                elif(adLen==5):  self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]] = prdContent
                elif(adLen==6):  self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]] = prdContent
                elif(adLen==7):  self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]] = prdContent
                elif(adLen==8):  self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]] = prdContent
                elif(adLen==10): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]] = prdContent
                elif(adLen==10): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]] = prdContent
                elif(adLen==11): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]] = prdContent
                elif(adLen==12): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]] = prdContent
                elif(adLen==13): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]] = prdContent
                elif(adLen==14): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]] = prdContent
                elif(adLen==15): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]] = prdContent
                elif(adLen==16): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]] = prdContent
                elif(adLen==17): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]] = prdContent
                elif(adLen==18): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]] = prdContent
                elif(adLen==19): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]] = prdContent
                elif(adLen==20): self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]][ad[19]] = prdContent
                else: print("PRD EDIT FAILED: Address Length Limit of 20 Reached\n * PRDAddress: {:s}".format(str(ad)))
            else: self.PRD_R[ad] = prdContent
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] An error occured during a PRDEDIT Interpretation (prdAddress: {:s}, prdContent: {:s})\n * ".format(self.processName1, self.processName2, str(prdAddress), str(prdContent)), 'light_red'), termcolor.colored(e, 'light_red'))
    def __interpret_PRDREMOVE(self, prdAddress):
        try:
            ad = prdAddress
            if ((type(ad) == list) or (type(ad) == tuple)):
                adLen = len(ad)
                if  (adLen==1):  del self.PRD_R[ad[0]]
                elif(adLen==2):  del self.PRD_R[ad[0]][ad[1]]
                elif(adLen==3):  del self.PRD_R[ad[0]][ad[1]][ad[2]]
                elif(adLen==4):  del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]]
                elif(adLen==5):  del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]]
                elif(adLen==6):  del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]]
                elif(adLen==7):  del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]]
                elif(adLen==8):  del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]]
                elif(adLen==10): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]]
                elif(adLen==10): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]]
                elif(adLen==11): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]]
                elif(adLen==12): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]]
                elif(adLen==13): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]]
                elif(adLen==14): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]]
                elif(adLen==15): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]]
                elif(adLen==16): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]]
                elif(adLen==17): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]]
                elif(adLen==18): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]]
                elif(adLen==19): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]]
                elif(adLen==20): del self.PRD_R[ad[0]][ad[1]][ad[2]][ad[3]][ad[4]][ad[5]][ad[6]][ad[7]][ad[8]][ad[9]][ad[10]][ad[11]][ad[12]][ad[13]][ad[14]][ad[15]][ad[16]][ad[17]][ad[18]][ad[19]]
                else: print("PRD REMOVAL FAILED: Address Length Limit of 20 Reached\n * PRDAddress: {:s}".format(str(ad)))
            else: del self.PRD_R[ad]
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] An error occured during a PRDREMOVE Interpretation (prdAddress: {:s})\n * ".format(self.processName1, self.processName2, str(prdAddress)), 'light_red'), termcolor.colored(e, 'light_red'))
    def __interpret_FAR(self, functionID, functionParams, rrid):
        try:
            self.FAR_R.append({'FunctionID': functionID, 'FunctionParams': functionParams, 'RRID': rrid})
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] An error occured during a FAR Interpretation: (FunctionID: {:s}, FunctionParams: {:s}, RRID: {:d})\n * ".format(self.processName1, self.processName2, functionID, str(functionParams), rrid), 'light_red'), termcolor.colored(e, 'light_red'))
    def __interpret_FARR(self, faResult, rrid):
        try:
            self.FARR_R[rrid] = faResult
        except Exception as e: print(termcolor.colored("[IPCA {:s}->{:s}] An error occured during a FARR interpretation (faResult: {:s}, RRID: {:d})\n * ".format(self.processName1, self.processName2, str(faResult), rrid), 'light_red'), termcolor.colored(e, 'light_red'))

    #Auxiallry Internal Functions END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Internal Functions END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    








#IPCA THREAD PROCESS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_PROCESSLOOP_SLEEPTIME = 0.05
def ipcAssistantThreadProcess(ipcAssistant):
    procContinue = True
    while (procContinue == True):
        #IPC Assistant Message Process (PRDEDIT & PRDREMOVE are handled here)
        try: procContinue = ipcAssistant.process()
        except Exception as e: print(termcolor.colored("[{:s}->{:s}] An error occured during IPC processing:\n *".format(ipcAssistant.processName1, ipcAssistant.processName2), 'light_red'), termcolor.colored(e, 'light_red'))
        time.sleep(_PROCESSLOOP_SLEEPTIME)
#IPCA THREAD PROCESS END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------