from tokenize import Ignore
from ATM_Zeta_Auxillaries import functionModifier

import time
import binance
import termcolor
import pprint
import os
import math
import random
import socket
from datetime import datetime, timezone, tzinfo

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

KLINE_INTERVAL_ID_1m  = 0;  
KLINE_INTERVAL_ID_3m  = 1;  
KLINE_INTERVAL_ID_5m  = 2;  
KLINE_INTERVAL_ID_15m = 3;  
KLINE_INTERVAL_ID_30m = 4;  
KLINE_INTERVAL_ID_1h  = 5;  
KLINE_INTERVAL_ID_2h  = 6;  
KLINE_INTERVAL_ID_4h  = 7;  
KLINE_INTERVAL_ID_6h  = 8;  
KLINE_INTERVAL_ID_8h  = 9;  
KLINE_INTERVAL_ID_12h = 10; 
KLINE_INTERVAL_ID_1d  = 11; 
KLINE_INTERVAL_ID_3d  = 12; 
KLINE_INTERVAL_ID_1W  = 13; 
KLINE_INTERVAL_ID_1M  = 14; 
KLINE_INTERVAL_IDs = (KLINE_INTERVAL_ID_1m, KLINE_INTERVAL_ID_3m, KLINE_INTERVAL_ID_5m, KLINE_INTERVAL_ID_15m, KLINE_INTERVAL_ID_30m, KLINE_INTERVAL_ID_1h, KLINE_INTERVAL_ID_2h, KLINE_INTERVAL_ID_4h, KLINE_INTERVAL_ID_6h, KLINE_INTERVAL_ID_8h, KLINE_INTERVAL_ID_12h, 
                      KLINE_INTERVAL_ID_1d, KLINE_INTERVAL_ID_3d, KLINE_INTERVAL_ID_1W, KLINE_INTERVAL_ID_1M)

KLINE_INTERVAL_SECs = {KLINE_INTERVAL_ID_1m:      60,
                       KLINE_INTERVAL_ID_3m:     180,
                       KLINE_INTERVAL_ID_5m:     300,
                       KLINE_INTERVAL_ID_15m:    900,
                       KLINE_INTERVAL_ID_30m:   1800,
                       KLINE_INTERVAL_ID_1h:    3600,
                       KLINE_INTERVAL_ID_2h:    7200,
                       KLINE_INTERVAL_ID_4h:   14400,
                       KLINE_INTERVAL_ID_6h:   21600,
                       KLINE_INTERVAL_ID_8h:   28800,
                       KLINE_INTERVAL_ID_12h:  43200,
                       KLINE_INTERVAL_ID_1d:   86400,
                       KLINE_INTERVAL_ID_3d:  259200,
                       KLINE_INTERVAL_ID_1W:  604800,
                       KLINE_INTERVAL_ID_1M: 2678400}

KLINE_INTERVAL_BINANCEAPICORRESPONDENCES = {KLINE_INTERVAL_ID_1m:  binance.Client.KLINE_INTERVAL_1MINUTE,
                                            KLINE_INTERVAL_ID_3m:  binance.Client.KLINE_INTERVAL_3MINUTE,
                                            KLINE_INTERVAL_ID_5m:  binance.Client.KLINE_INTERVAL_5MINUTE,
                                            KLINE_INTERVAL_ID_15m: binance.Client.KLINE_INTERVAL_15MINUTE,
                                            KLINE_INTERVAL_ID_30m: binance.Client.KLINE_INTERVAL_30MINUTE,
                                            KLINE_INTERVAL_ID_1h:  binance.Client.KLINE_INTERVAL_1HOUR,
                                            KLINE_INTERVAL_ID_2h:  binance.Client.KLINE_INTERVAL_2HOUR,
                                            KLINE_INTERVAL_ID_4h:  binance.Client.KLINE_INTERVAL_4HOUR,
                                            KLINE_INTERVAL_ID_6h:  binance.Client.KLINE_INTERVAL_6HOUR,
                                            KLINE_INTERVAL_ID_8h:  binance.Client.KLINE_INTERVAL_8HOUR,
                                            KLINE_INTERVAL_ID_12h: binance.Client.KLINE_INTERVAL_12HOUR,
                                            KLINE_INTERVAL_ID_1d:  binance.Client.KLINE_INTERVAL_1DAY,
                                            KLINE_INTERVAL_ID_3d:  binance.Client.KLINE_INTERVAL_3DAY,
                                            KLINE_INTERVAL_ID_1W:  binance.Client.KLINE_INTERVAL_1WEEK,
                                            KLINE_INTERVAL_ID_1M:  binance.Client.KLINE_INTERVAL_1MONTH}

KLINE_INTERVAL_ATMCORRESPONDENSEs = {binance.Client.KLINE_INTERVAL_1MINUTE:  KLINE_INTERVAL_ID_1m,
                                     binance.Client.KLINE_INTERVAL_3MINUTE:  KLINE_INTERVAL_ID_3m,
                                     binance.Client.KLINE_INTERVAL_5MINUTE:  KLINE_INTERVAL_ID_5m,
                                     binance.Client.KLINE_INTERVAL_15MINUTE: KLINE_INTERVAL_ID_15m,
                                     binance.Client.KLINE_INTERVAL_30MINUTE: KLINE_INTERVAL_ID_30m,
                                     binance.Client.KLINE_INTERVAL_1HOUR:    KLINE_INTERVAL_ID_1h,
                                     binance.Client.KLINE_INTERVAL_2HOUR:    KLINE_INTERVAL_ID_2h,
                                     binance.Client.KLINE_INTERVAL_4HOUR:    KLINE_INTERVAL_ID_4h,
                                     binance.Client.KLINE_INTERVAL_6HOUR:    KLINE_INTERVAL_ID_6h,
                                     binance.Client.KLINE_INTERVAL_8HOUR:    KLINE_INTERVAL_ID_8h,
                                     binance.Client.KLINE_INTERVAL_12HOUR:   KLINE_INTERVAL_ID_12h,
                                     binance.Client.KLINE_INTERVAL_1DAY:     KLINE_INTERVAL_ID_1d,
                                     binance.Client.KLINE_INTERVAL_3DAY:     KLINE_INTERVAL_ID_3d,
                                     binance.Client.KLINE_INTERVAL_1WEEK:    KLINE_INTERVAL_ID_1W,
                                     binance.Client.KLINE_INTERVAL_1MONTH:   KLINE_INTERVAL_ID_1M}

TIMEZONE = datetime.now(timezone.utc).astimezone()
TIMEZONE_DELTA_SEC = TIMEZONE.utcoffset().seconds

BINANCEFUTURES_STARTYEAR_TIMESTAMP  = 1546300800
BINANCEFUTURES_STARTMONTH_TIMESTAMP = 1564617600
BINANCEFUTURES_STARTYEAR           = 2019
BINANCEFUTURES_STARTMONTH          = 8

MARKETEXCHANGEINFO_MAXATTEMPT      = 3
MARKETEXCHANGEINFO_ATTEMPTINTERVAL = 0.2

IPADDRESS_INTERNAL = '127.0.0.1'

SERVERCONNECTIONCHECKINTERVAL_MS = 1000

REQUESTWEIGHTALLOCPERSYMBOL = 10

class manager_BinanceAPI:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, centralManager, ipcA):
        #Creating local instances of passed parameters
        self.centralManager = centralManager
        self.ipcA = ipcA

        #Process Control
        self.eventHandlerPending_Server = None
        self.eventHandlerPending_DB     = None
        
        #Network Control
        self.sys_HostName = socket.gethostname()
        self.sys_IPAddress = socket.gethostbyname(self.sys_HostName)

        #Binance Control Variables
        self.binance = {'serverStatus': {'available': False, 'status': None, 'lastCheckTime': 0},
                        'marketAssets': dict(), 'marketAssets_trading': list(), 'marketAssets_currentKline': dict(),
                        'APIRateLimits': {'serverDefined': dict(),
                                          'usedByThisIP': {'req_weight_min': float('inf'), 'req_weight_min_LocalLimit': float('inf'), #The values within 'usedByThisIP' are intentionally set to 'int('inf')' at initialization in order to wait for the next minute
                                                           'orders_min': float('inf'), 
                                                           'orders_sec': float('inf')}}, 
                        'clients': {'default': {'client': None, 'permissions': None}},
                        'RTAAllocationCompletionQueue': list(), 'RTAAllocationCompletionQueue_RunTime': list(),
                        'WebSocketConnectionPermissionQueue': list(), 'lastWebSocketConnection': 0, 'streamingSymbols': dict(),
                        'mrktRegTSCheckQueue': list(),
                        'downloadRanges': {'SA': dict(), 'SSO': dict(), 'SO': dict()}, 'downloadTarget': None, 'downloadTarget_userDefined': list(), 'downloadTemporalPriority': 'LATEST'}

        #self.aClient = binance.Client()
        #self.aClient.futures_historical_klines()

        #---Market Asset Info Variation Trackers
        self.assetUpdateHandler_addedAssets   = None
        self.assetUpdateHandler_removedAssets = None
        self.assetUpdateHandler_updatedAssets = None

        #Stream Klines Control
        self.binance_firstStreamReceivals = list()

        self.binance_streamedKlines          = dict()
        self.binance_streamedKlines_ranges   = dict()
        self.binance_streamedKlines_existing = list()
        self.binance_streamedKlines_nTotal = 0

        self.binance_streamedKlinesLastSaved_ms    = 0
        self.binance_streamedKlinesSaveInterval_ms = 3000

        #Initialization Completion Message
        print(termcolor.colored("Binance API", 'blue'), termcolor.colored("Manager Initialization Complete! --------------------------------------------------------------------------------------------", 'green'))
    def postInitialization(self, fModifier, m_AutoTrader, m_DataManagement):
        self.fModifier = fModifier; self.m_AutoTrader = m_AutoTrader; self.m_DataManagement = m_DataManagement
        self.functionRepeaters = dict()

        self.functionRepeaters['SERVERCONNECITONCHECK'] = self.fModifier.addFixedRepeatedFunction(self.checkServerConnection, interval = SERVERCONNECTIONCHECKINTERVAL_MS, startUponInit = False)
        self.functionRepeaters['REQLIMITKEEPER0']       = self.fModifier.addFixedRepeatedFunction(self.__periodUpdater_10sec, interval = 10000)
        self.functionRepeaters['REQLIMITKEEPER1']       = self.fModifier.addFixedRepeatedFunction(self.__periodUpdater_min,   interval = 60000)
        
        self.ipcA['MAIN'].sendPRDEDIT("SERVERSTATUS", self.binance['serverStatus'], nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("SERVERSTATUS",  self.binance['serverStatus'], nMaxDispatch = 'INF')
        self.ipcA['MAIN'].sendPRDEDIT("MARKETASSETS", self.binance['marketAssets'], nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("MARKETASSETS",  self.binance['marketAssets'], nMaxDispatch = 'INF')
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Process Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self):
        currentTime_ns = time.perf_counter_ns()

        if ((self.eventHandlerPending_Server == None) and (self.eventHandlerPending_DB == None)):
            if (self.binance['serverStatus']['available'] == True):
                #RTA Connection
                try: self.__processRTAAllocation()
                except Exception as e: print(termcolor.colored("An error occurred during RTA Allocation Processing\n *", 'red'), termcolor.colored(e, 'red'))
                
                #RTA Related
                try: self.__processFirstKlineReceivals()
                except Exception as e: print(termcolor.colored("An error occurred during First Kline Receival Processing\n *", 'red'), termcolor.colored(e, 'red'))
                try: self.__processWebSocketConnectionPermissionQueue(currentTime_ns)
                except Exception as e: print(termcolor.colored("An error occurred during WebSocket Connection Permission Queue Processing\n *", 'red'), termcolor.colored(e, 'red'))

                #Klines Download and MrktRegTS & Streamed Data Save
                try:
                    processKlineDownloadQueue = not(self.__processMrktRegTSCheckQueue())
                    try:
                        if (processKlineDownloadQueue == True): self.__processKlineDownloadQueue()
                    except Exception as e: print(termcolor.colored("An error occurred during Kline Download Queue Processing\n *", 'red'), termcolor.colored(e, 'red'))
                except Exception as e: print(termcolor.colored("An error occurred during Market Registration Timestamp Check Queue Processing\n *", 'red'), termcolor.colored(e, 'red'))
                try: self.__saveStreamedKlines(currentTime_ns)
                except Exception as e: print(termcolor.colored("An error occurred during Streamed Klines Saving\n *", 'red'), termcolor.colored(e, 'red'))
        else:
            #Server Related Events
            if   (self.eventHandlerPending_Server == 'SERVERCONNECTION'):    self.__on_ServerConnection();    self.eventHandlerPending_Server = None
            elif (self.eventHandlerPending_Server == 'SERVERDISCONNECTION'): self.__on_ServerDisconnection(); self.eventHandlerPending_Server = None
            elif (self.eventHandlerPending_Server == 'SERVER_ASSETSTATUSUPDATE'):
                if (self.assetUpdateHandler_addedAssets != None):   self.__handleAddedAssets(self.assetUpdateHandler_addedAssets[0], self.assetUpdateHandler_addedAssets[1], uponNewConnection = False); self.assetUpdateHandler_addedAssets   = None
                if (self.assetUpdateHandler_removedAssets != None): self.__handleRemovedAssets(self.assetUpdateHandler_removedAssets,                                        uponNewConnection = False); self.assetUpdateHandler_removedAssets = None
                if (self.assetUpdateHandler_updatedAssets != None): self.__handleStatusUpdatedAssets(self.assetUpdateHandler_updatedAssets,                                  uponNewConnection = False); self.assetUpdateHandler_updatedAssets = None
                self.eventHandlerPending_Server = None
            #DB Related Events
            if   (self.eventHandlerPending_DB == 'DBCONNECTION'):    self.__on_DBConnection();    self.eventHandlerPending_DB = None
            elif (self.eventHandlerPending_DB == 'DBDISCONNECTION'): self.__on_DBDisconnection(); self.eventHandlerPending_DB = None



    def terminate(self):
        pass
    #Process Functions END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Inter-Manager Call Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #<Server Status Related>
    def checkServerConnection(self):
        if (self.eventHandlerPending_Server == None): #Only perform connection check when there exist no pending connection event handler
            """
            There exists three possible cases
             [1]: Server Connection Problem - Exception will be raised
             [2]: Server In Maintenance     - 'binanceSystemStatus' will be 1 for 'status'
             [3]: Server Normal             - 'binanceSystemStatus' will be 0 for 'status'
            """
            #Record connection check time and previous serverStatus
            currentTime = time.time()
            previousAvailability = self.binance['serverStatus']['available']
            previousStatus       = self.binance['serverStatus']['status']

            #Check server status
            while (True):
                try:    self.sys_IPAddress = socket.gethostbyname(self.sys_HostName); break
                except: pass
        
            if (self.sys_IPAddress == IPADDRESS_INTERNAL): # <--- Network Currently Internal
                self.binance['serverStatus']['available'] = False
                self.binance['serverStatus']['status']    = 'disconnected'
            else: # <--- Network Currently External
                try:
                    if (self.binance['clients']['default']['client'] == None):
                        client = binance.Client()
                        binanceSystemStatus = client.get_system_status()['status']
                        self.binance['clients']['default']['client'] = client
                    else:
                        binanceSystemStatus = self.binance['clients']['default']['client'].get_system_status()['status']

                    #Server Response Interpretation
                    if (binanceSystemStatus == 0): #System Available
                        self.binance['serverStatus']['available'] = True
                        self.binance['serverStatus']['status']    = 'connected'
                    elif (binanceSystemStatus == 1): #System Under Maintenance
                        self.binance['serverStatus']['available'] = False
                        self.binance['serverStatus']['status']    = 'maintenance'
                except Exception as e:
                    self.binance['serverStatus']['available'] = False
                    self.binance['serverStatus']['status']    = 'disconnected'

            #State Update Handling
            if (previousAvailability == True):
                if (self.binance['serverStatus']['available'] == True): 
            #-----# CASE 0: Available -> Available --------------------------------------------------------------------------------------------------------------------------------------------------------
                    if (int(self.binance['serverStatus']['lastCheckTime']/60) != int(currentTime/60)): self.__checkMarketExchangeInfo()
                    if ((self.assetUpdateHandler_addedAssets != None) or (self.assetUpdateHandler_removedAssets != None) or (self.assetUpdateHandler_updatedAssets != None)): self.eventHandlerPending_Server = 'SERVER_ASSETSTATUSUPDATE'
                    self.binance['serverStatus']['lastCheckTime'] = currentTime
                    if (previousStatus != self.binance['serverStatus']['status']):
                        self.ipcA['MAIN'].sendPRDEDIT("SERVERSTATUS", self.binance['serverStatus'], nMaxDispatch = 'INF')
                        self.ipcA['AUX'].sendPRDEDIT("SERVERSTATUS",  self.binance['serverStatus'], nMaxDispatch = 'INF')
                    self.ipcA['MAIN'].sendPRDEDIT(("SERVERSTATUS", 'lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT(("SERVERSTATUS", ' lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
            #-----# CASE 0 END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                else:
            #-----# CASE 1: Available -> Not Available ----------------------------------------------------------------------------------------------------------------------------------------------------
                    self.eventHandlerPending_Server = 'SERVERDISCONNECTION'
                    self.binance['serverStatus']['lastCheckTime'] = currentTime
                    self.ipcA['MAIN'].sendPRDEDIT("SERVERSTATUS", self.binance['serverStatus'], nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT("SERVERSTATUS",  self.binance['serverStatus'], nMaxDispatch = 'INF')
                    self.ipcA['MAIN'].sendPRDEDIT(("SERVERSTATUS", 'lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT(("SERVERSTATUS",  'lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
            #-----# CASE 1 END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            else:
                if (self.binance['serverStatus']['available'] == True):
            #-----# CASE 2: Not Available -> Available ----------------------------------------------------------------------------------------------------------------------------------------------------
                    self.eventHandlerPending_Server = 'SERVERCONNECTION'
                    self.binance['serverStatus']['lastCheckTime'] = currentTime
                    self.ipcA['MAIN'].sendPRDEDIT("SERVERSTATUS", self.binance['serverStatus'], nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT("SERVERSTATUS",  self.binance['serverStatus'], nMaxDispatch = 'INF')
                    self.ipcA['MAIN'].sendPRDEDIT(("SERVERSTATUS", 'lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT(("SERVERSTATUS",  'lastCheckTime'), self.binance['serverStatus']['lastCheckTime'], nMaxDispatch = 'INF')
            #-----# CASE 2 END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #Return server availability
            return self.binance['serverStatus']['available']

    def isServerAvailable(self): return self.binance['serverStatus']['available']





    #<Database Status Related>
    def on_DBConnection(self):    self.eventHandlerPending_DB = 'DBCONNECTION'
    def on_DBDisconnection(self): self.eventHandlerPending_DB = 'DBDISCONNECTION'



    #<Client Control Related>
    def addClientByKeys(self, apiKey, secretKey):
        try:
            newClient = binance.Client(api_key = apiKey, api_secret = secretKey)
            apiPermissions = newClient.get_account_api_permissions() #An exception will be raised here if 'apiKey' or 'secretKey' is invalid
            #Below is when the API account connection was successful

        except Exception as e: print("An error occured while attempting to make a API account connection: <{:s}>".format(str(e))); return False

    def addClientByCode(self, clientCode):
        try: pass
        except Exception as e: print("A")

    def removeClient(self, clientNum):
        pass





    #<Asset Data Related>
    #---Return clientSymbol of the specified asset
    def get_ClientSymbol(self, apiSymbol): return self.binance['marketAssets'][apiSymbol]['symbol']

    #---Check if the specified asset exists in the market
    def check_SymbolExists(self, apiSymbol): return (apiSymbol in self.binance['marketAssets'])
    
    #---Return Asset List
    def get_AssetList(self, tradingOnly = False):
        if (tradingOnly == True): return self.binance['marketAssets_trading']
        else:                     return list(self.binance['marketAssets'].keys())

    #---Return Number of Assets
    def get_nAssets(self, tradingOnly = False):
        if (tradingOnly == True): return len(self.binance['marketAssets_trading'])
        else:                     return len(self.binance['marketAssets'])

    #---Return the specified asset's status
    def getAssetStatus(self, apiSymbol):
        if apiSymbol in self.binance['marketAssets']: return self.binance['marketAssets'][apiSymbol]['status']
        else:                                         return None

    #---Return the price, quantity, and quote precision of the specified asset
    def get_Precisions(self, apiSymbol):
        return {'prec_Price': self.binance['marketAssets'][apiSymbol]['pricePrecision'], 'prec_Quantity': self.binance['marketAssets'][apiSymbol]['quantityPrecision'], 'prec_Quote': self.binance['marketAssets'][apiSymbol]['quotePrecision']}

    #---Return the first streamed kline TS for the corresponding apiSymbol and interval
    def get_firstStreamedKlineTS(self, apiSymbol, intervalID):
        return self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID]

    #---Return the mrktReg kline TS for the corresponding apiSymbol and interval
    def get_mrktRegTS(self, apiSymbol, intervalID):
        return self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID]

    #---Recalculate the download ranges for the corrensponding apiSymbol and intervalID, and re-select the download target
    def recalculateDownloadRanges(self, apiSymbol, intervalID):
        self.__calculateDownloadRanges(apiSymbol, intervalID)
        self.__selectDownloadTarget()
         
    def set_DataAvailability(self, apiSymbol, intervalID, newDataRanges):
        self.binance['marketAssets'][apiSymbol]['dataRanges'][intervalID] = newDataRanges
        self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'dataRanges', intervalID), newDataRanges, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'dataRanges', intervalID), newDataRanges, nMaxDispatch = 'INF')

        if (self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID] != None) and (self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID] != None):
            firstStreamedKlineTS = self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID]
            mrktRegTS            = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID]

            totalDataWidth = firstStreamedKlineTS - mrktRegTS
            if (totalDataWidth == 0): dataRanges_perc_new = 100
            else: 
                availableWidth = 0
                for dataRange in newDataRanges: 
                    if (dataRange[0] < firstStreamedKlineTS):
                        if (dataRange[1] < firstStreamedKlineTS): availableWidth += dataRange[1]         - dataRange[0]
                        else:                                     availableWidth += firstStreamedKlineTS - dataRange[0]
                dataRanges_perc_new = round(availableWidth/totalDataWidth*100, 3)
            self.binance['marketAssets'][apiSymbol]['dataRanges_perc'][intervalID] = dataRanges_perc_new
            self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'dataRanges_perc', intervalID), dataRanges_perc_new, nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'dataRanges_perc', intervalID), dataRanges_perc_new, nMaxDispatch = 'INF')





    #<RTA Related>
    #---Set RTA Allocation of the corresponding apiSymbol
    def set_RTAAllocation(self, apiSymbol, rtaCode, allocationMode):
        #Internal Variable Setting
        self.binance['marketAssets'][apiSymbol]['RTAAlloc']     = rtaCode
        self.binance['marketAssets'][apiSymbol]['RTAAllocMode'] = allocationMode

        #PRD Announcement
        self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'RTAAlloc'), rtaCode, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'RTAAlloc'), rtaCode, nMaxDispatch = 'INF')
        self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'RTAAllocMode'), allocationMode, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'RTAAllocMode'), allocationMode, nMaxDispatch = 'INF')



    #---Once RTA Allocation by Central Manager Completes
    def on_RTAAllocComplete(self, rtaCode):
        self.binance['RTAAllocationCompletionQueue'].append(rtaCode)



    #---Handle a new socket connection request from RTA
    def addWebSocketConnectionPermissionQueue(self, functionParams):
        rtaCode = functionParams['rtaCode']
        self.binance['WebSocketConnectionPermissionQueue'].append(rtaCode)



    #---Handle a WebSocket Connection Completion Flag
    def onWebSocketConnectionCompletion(self, functionParams):
        rtaCode                = functionParams['rtaCode']
        connectionCompletionTS = functionParams['connectionCompletionTS']

        if (self.binance['lastWebSocketConnection'] == 'waiting'):
            self.binance['lastWebSocketConnection'] = connectionCompletionTS
            print("{:s} WebSocket Connection Completed at {:.3f} s!".format(rtaCode, connectionCompletionTS))
        else: print(termcolor.colored("Unexpected WebSocket Connection Completion Signal Received: {:s} at {:d}".format(rtaCode, connectionCompletionTS), 'light_red'))



    #---Handle a first kline stream receival from RTA since DB connection
    def on_firstKlineStreamReceival(self, functionParams):
        #Function Parameters Localization
        apiSymbol            = functionParams['apiSymbol']
        intervalID           = KLINE_INTERVAL_ATMCORRESPONDENSEs[functionParams['interval']]
        firstStreamedKlineTS = functionParams['timestamp']

        #Retrive the request weight that was allocated to the RTA
        if (intervalID == KLINE_INTERVAL_ID_3d): self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit'] += REQUESTWEIGHTALLOCPERSYMBOL

        #Local Variables Update and PRD Announcement
        self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID] = firstStreamedKlineTS

        self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'firstStreamedKlineTSs', intervalID), firstStreamedKlineTS, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'firstStreamedKlineTSs', intervalID), firstStreamedKlineTS, nMaxDispatch = 'INF')
        
        #Receival Target Appending for post-receival handling
        self.binance_firstStreamReceivals.append((apiSymbol, intervalID))



    #---Once RTA begins analysis on the specified asset
    def on_analysisBegin(self, functionParams):
        apiSymbol = functionParams['apiSymbol']

        self.binance['marketAssets'][apiSymbol]['analyzing'] = True
        self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'analyzing'), True, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'analyzing'), True, nMaxDispatch = 'INF')



    #---Kline Receival Handler
    def on_KlineReceival(self, functionParams):
        try:
            apiSymbol  = functionParams['apiSymbol']
            intervalID = KLINE_INTERVAL_ATMCORRESPONDENSEs[functionParams['interval']]
            kline      = functionParams['Kline']
            closed     = functionParams['closed']
            #Kline Handling
            self.binance['marketAssets_currentKline'][apiSymbol][intervalID] = kline
            #Closed Kline Handling
            if ((closed == True) and (self.m_DataManagement.isKlinesSaveAvailable() == True)): self.on_closedKlineReceival(apiSymbol, intervalID, kline)
            #Kline Announcement
            self.centralManager.klineSubscription_onKlineStreamReceival(apiSymbol, intervalID, kline)


        except Exception as e: print(termcolor.colored("An unexpected error occurred during kline receival handling\n *", 'light_red'), termcolor.colored(e, 'light_red'))

    #---Closed Kline Receival Handler
    def on_closedKlineReceival(self, apiSymbol, intervalID, kline):
        try:
            #Stream Order Twist Handling
            openTS  = kline[0]
            if (openTS < self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID]): return
            closeTS = kline[1]
            
            #Update the corresponding range in the buffer
            currentKlineRanges = self.binance_streamedKlines_ranges[apiSymbol][intervalID].copy()
            if (len(currentKlineRanges) == 0): currentKlineRanges = [[openTS, closeTS]]
            else:
                #Find the position at which the the left edge of the fetched kline data range is greater than the right edge of the previous kline data range
                insertionPosition = 0
                for currentStreamedKlineRange in currentKlineRanges:
                    if   (currentStreamedKlineRange[1] < openTS): insertionPosition += 1
                    elif (closeTS < currentStreamedKlineRange[0]): break
                    else:
                        #Overlap Detected
                        print(termcolor.colored("Data Range Overlap detected while attempting to save streamed klines data in buffer for {:s}_{:d}\n * Insertion Position: {:d}\n * Kline Range: [{:d}~{:d}]\n * Overlapped Previous Range: [{:d}~{:d}]".format(apiSymbol, intervalID, insertionPosition,
                                                                                                                                                                                                                                                                kline[0], kline[1],
                                                                                                                                                                                                                                                                currentStreamedKlineRange[0], currentStreamedKlineRange[1]), 
                                                'light_red'))
                        for index, existingStreamedKlineRange in enumerate(self.binance_streamedKlines_ranges[apiSymbol][intervalID]): print(termcolor.colored(" - Previous Data Range {:d}: [{:d}~{:d}]".format(index, existingStreamedKlineRange[0], existingStreamedKlineRange[1]), 'light_red'))
                        self.m_DataManagement.performKlineDeepRangeCheck(apiSymbol = apiSymbol, intervalID = intervalID, recalculateDownloadRanges = True)
                        return
                
                #Identify Mergible Adjacent Data Ranges
                mergeL = False; mergeR = False
                if (0 < insertionPosition):
                    if (currentKlineRanges[insertionPosition-1][1]+1 == openTS): mergeL = True
                if (insertionPosition < len(currentKlineRanges)):
                    if (closeTS+1 == currentKlineRanges[insertionPosition][0]): mergeR = True
                    
                #Perform Data Ranges Merging
                if (mergeL == True):
                    if (mergeR == True): #Merge with both sides
                        currentKlineRanges[insertionPosition-1] = [currentKlineRanges[insertionPosition-1][0], currentKlineRanges[insertionPosition][1]]
                        currentKlineRanges.pop(insertionPosition)
                    else: #Merge with left side only
                        currentKlineRanges[insertionPosition-1] = [currentKlineRanges[insertionPosition-1][0], closeTS] 
                else:
                    if (mergeR == True): #Merge with right side only
                        currentKlineRanges[insertionPosition] = [openTS, currentKlineRanges[insertionPosition][1]]  
                    else: #Merge with none
                        currentKlineRanges.insert(insertionPosition, [openTS, closeTS])
                        
            #Apply the changes
            self.binance_streamedKlines_ranges[apiSymbol][intervalID] = currentKlineRanges

            if (len(self.binance_streamedKlines[apiSymbol][intervalID]) == 0): self.binance_streamedKlines_existing.append((apiSymbol, intervalID))
            self.binance_streamedKlines[apiSymbol][intervalID].append(kline)
            self.binance_streamedKlines_nTotal += 1
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attmpeting to handle a closed kline receival\n *", 'red'), termcolor.colored(e, 'red'))
    #Inter-Manager Call Functions END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Internal Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #<Market Information Related>
    #---Server connection Handler
    def __on_ServerConnection(self):
        print(termcolor.colored("<CONNECTED TO BINANCE SERVER!>", 'light_green'))
        print(" Reading Binance Futures Exchange Info...")
        #Get Exchange Information From the Server
        self.__checkMarketExchangeInfo(uponNewConnection = True)

        #Report Data Read Result
        print("  * <PERPETUAL FUTURES>")
        statusCounter = dict()
        for index, apiSymbol in enumerate(self.binance['marketAssets']): 
            apiSymbolStatus = self.binance['marketAssets'][apiSymbol]['status']
            if (apiSymbolStatus in statusCounter): statusCounter[apiSymbolStatus] += 1
            else:                                  statusCounter[apiSymbolStatus] = 1
            if (apiSymbolStatus == 'TRADING'): statusColor = 'light_green'
            else:                              statusColor = 'light_red'
            print("   [{:d} / {:d}] {:s}:".format(index+1, len(self.binance['marketAssets']), apiSymbol), termcolor.colored(apiSymbolStatus, statusColor))
        print("   - {:d} PERPETUAL futures found!".format(len(self.binance['marketAssets'])))
        for status in statusCounter: print("    - {:d} {:s}".format(statusCounter[status], status))

        print("  * <API Rate Limits>")
        for rateLimit in self.binance['APIRateLimits']['serverDefined'].keys(): print("     - {:s}: {:d}".format(rateLimit, self.binance['APIRateLimits']['serverDefined'][rateLimit]))
        print(" Binance Futures Exchange Info Read Complete!\n")

        #del self.binance['marketAssets']['BTC/USDT:USDT']
        #self.binance['marketAssets']['ETH/USDT:USDT'] = {'status': 'SETTLING'}

        #Update the asset subscription file and allocate assets to the RTAs
        self.centralManager.on_ServerConnection()



    #---Server disconnection handler
    def __on_ServerDisconnection(self):
        print(termcolor.colored("<DISCONNECTED FROM BINANCE SERVER!>", 'light_red'))

        #Save streamed Klines in the buffer
        self.__saveStreamedKlines()

        #Initialize Market-Releated Data Keepers
        self.binance['marketAssets'].clear()
        self.binance['marketAssets_trading'].clear()
        self.binance['streamingSymbols'].clear()
        for rtaCode in self.binance['WebSocketConnectionPermissionQueue']: self.ipcA[rtaCode].sendFAR(functionID = 'RECEIVEWEBSOCKETCONNECTIONPERMISSION', functionParams = {'permissionGiven': False}, nMaxDispatch = 'INF')
        self.binance['WebSocketConnectionPermissionQueue'].clear()
        
        #Clear Queues
        self.binance['downloadRanges'] = {'SA': dict(), 'SSO': dict(), 'SO': dict()} #Download ranges and selected downloadTarget must be re-computed upon server re-connection, but user defined download target does not need to be reset
        self.binance['downloadTarget'] = None
        self.binance['mrktRegTSCheckQueue'].clear()

        self.binance_firstStreamReceivals.clear()

        print(termcolor.colored(" * Binance API Manager Post-Server Disconnection Protocol Complete", 'light_red'))
        self.centralManager.on_ServerDisconnection()
        





    #<DB Status Related>
    #---DB Connection Handler
    def __on_DBConnection(self):
        #Process any removable mrktRegTSCheckQueue
        processedQueueIndexes = list()
        for index, queue in enumerate(self.binance['mrktRegTSCheckQueue']):
            apiSymbol = queue[0]; intervalID = queue[1]
            mrktRegTS_corresponding = self.m_DataManagement.get_mrktRegistrationTS(apiSymbol, intervalID)
            if (mrktRegTS_corresponding != None): 
                self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID] = mrktRegTS_corresponding
                processedQueueIndexes.append(index)
        nRemoved = 0
        for processedQueueIndex in processedQueueIndexes: self.binance['mrktRegTSCheckQueue'].pop(processedQueueIndex-nRemoved); nRemoved += 1
        
        #Read coinIDIndex for all assets
        if (self.m_DataManagement.isDBAvailable() == True):
            for apiSymbol in self.binance['marketAssets']:
                if (self.m_DataManagement.exists_asset(apiSymbol) == True): self.binance['marketAssets'][apiSymbol]['coinIDIndex'] = self.m_DataManagement.get_coinIDIndex(apiSymbol)                                           #If the corresponding asset data exists in the connected database
                else:                                                       self.binance['marketAssets'][apiSymbol]['coinIDIndex'] = self.m_DataManagement.register_asset(apiSymbol, self.binance['marketAssets']['mrktRegTS']) #If the corresponding asset data does not exist in the connected database
        else:
            for apiSymbol in self.binance['marketAssets']: self.binance['marketAssets'][apiSymbol]['coinIDIndex'] = None



    #---DB Disconnection Handler
    def __on_DBDisconnection(self):
        #Reset coinIDIndex for all assets
        for apiSymbol in self.binance['marketAssets']:
            self.binance['marketAssets'][apiSymbol]['coinIDIndex'] = None

        #Reset Streamed Klines Buffer
        self.binance_streamedKlines.clear()
        self.binance_streamedKlines_nTotal = 0

        #Lower 'pauseProcessingFlag'
        self.pauseProcessing = False



    #---Read and analyze market exchange info
    def __checkMarketExchangeInfo(self, uponNewConnection = False):
        try:
            #Market Exchange Info Read Attempt
            nTry = 0
            while (True):
                try:
                    nTry += 1
                    exchangeInfo_futures = self.binance['clients']['default']['client'].futures_exchange_info()
                    break
                except Exception as e:
                    if (nTry == MARKETEXCHANGEINFO_MAXATTEMPT):
                        print(termcolor.colored("An error occured while attempting to get market exchange info, attempt limit reached [{:d} / {:d}]\n *".format(nTry, MARKETEXCHANGEINFO_MAXATTEMPT), 'light_magenta'), termcolor.colored(e, 'light_magenta'))
                        return False
                    else: time.sleep(MARKETEXCHANGEINFO_ATTEMPTINTERVAL)

            #Analyze Asset Info
            assetInfo_server = exchangeInfo_futures['symbols']
            assetStatus_server = dict()
            for assetExchangeInfo in assetInfo_server:
                if (assetExchangeInfo['contractType'] == "PERPETUAL"):
                    apiSymbol = "{:s}/{:s}:{:s}".format(assetExchangeInfo['baseAsset'], assetExchangeInfo['quoteAsset'], assetExchangeInfo['marginAsset'])
                    assetStatus_server[apiSymbol] = assetExchangeInfo
        
            assetStatus_server_keys = list(assetStatus_server.keys())
            assetInfo_local_keys    = list(self.binance['marketAssets'].keys())

            #---Find the added assets and add the local market assets data
            addedAssets = [apiSymbol for apiSymbol in assetStatus_server_keys if apiSymbol not in assetInfo_local_keys]
            if (0 < len(addedAssets)): print("Asset Addition to the Binance Server Detected: nAdded: {:d}, {:s}".format(len(addedAssets), str(addedAssets)))
            addedAssetsInfo = dict()
            for apiSymbol in addedAssets: addedAssetsInfo[apiSymbol] = assetStatus_server[apiSymbol]

            #---Find the removed assets
            removedAssets = [apiSymbol for apiSymbol in assetInfo_local_keys if apiSymbol not in assetStatus_server_keys]
            if (0 < len(removedAssets)): print("Asset Removal from the Binance Server Detected: nRemoved: {:d}, {:s}".format(len(removedAssets), str(removedAssets)))

            #---Find assets with updated status
            statusUpdatedAssets = list()
            for apiSymbol in self.binance['marketAssets']:
                if (apiSymbol not in removedAssets):
                    status_previous = self.binance['marketAssets'][apiSymbol]['status']
                    status_current  = assetStatus_server[apiSymbol]['status']
                    if (status_previous != status_current): statusUpdatedAssets.append((apiSymbol, status_previous, status_current))
            if (0 < len(statusUpdatedAssets)): print("Asset Status Updated Detected: nUpdated: {:d}, {:s}".format(len(statusUpdatedAssets), str(statusUpdatedAssets)))

            #Read Server-Defined Rate Limit and Handle any updates on asset information
            if (uponNewConnection == True):
                self.__handleAddedAssets(addedAssets, assetStatus_server, uponNewConnection)
                self.__handleRemovedAssets(removedAssets,                 uponNewConnection)
                self.__handleStatusUpdatedAssets(statusUpdatedAssets,     uponNewConnection)
                for rateLimit in exchangeInfo_futures['rateLimits']: self.binance['APIRateLimits']['serverDefined'][rateLimit['rateLimitType']+"_"+rateLimit['interval']+"_"+str(rateLimit['intervalNum'])] = rateLimit['limit']
                self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit'] = self.binance['APIRateLimits']['serverDefined']['REQUEST_WEIGHT_MINUTE_1'] - (int(60000/SERVERCONNECTIONCHECKINTERVAL_MS)+1) #nConnectionChecks per min & 1 for minutely exchange info check
            else:
                self.assetUpdateHandler_addedAssets   = (addedAssets, assetStatus_server)
                self.assetUpdateHandler_removedAssets = removedAssets
                self.assetUpdateHandler_updatedAssets = statusUpdatedAssets

            #Return 'True' to indicate successful market exchange info check
            return True
        except Exception as e: print(termcolor.colored("An unexpected error occured during market exchange info check\n *", 'light_red'), termcolor.colored(e, 'light_red'))
        


    #---Handle Added Assets
    def __handleAddedAssets(self, addedAssets, addedAssetsInfo, uponNewConnection):
        for apiSymbol in addedAssets:
            #Binance Server Asset Data Copy
            self.binance['marketAssets'][apiSymbol] = addedAssetsInfo[apiSymbol]
            self.binance['marketAssets_currentKline'][apiSymbol] = dict()

            #ATM Market Asset Data Initialization
            self.binance['marketAssets'][apiSymbol]['RTAAlloc']      = None
            self.binance['marketAssets'][apiSymbol]['RTAAllocMode']  = None
            self.binance['marketAssets'][apiSymbol]['analyzing']     = False
            mrktRegTS             = dict()
            firstStreamedKlineTSs = dict()
            dataRanges            = dict()
            dataRanges_perc       = dict()
            self.binance_streamedKlines[apiSymbol]        = dict()
            self.binance_streamedKlines_ranges[apiSymbol] = dict()
            for intervalID in KLINE_INTERVAL_IDs:
                mrktRegTS_corresponding = self.m_DataManagement.get_mrktRegistrationTS(apiSymbol, intervalID)
                if (mrktRegTS_corresponding == None): self.binance['mrktRegTSCheckQueue'].append((apiSymbol, intervalID))
                mrktRegTS[intervalID]             = mrktRegTS_corresponding
                firstStreamedKlineTSs[intervalID] = None
                dataRanges[intervalID]            = self.m_DataManagement.get_DataAvailability(apiSymbol, intervalID)
                dataRanges_perc[intervalID]       = None
                self.binance_streamedKlines[apiSymbol][intervalID]        = list()
                self.binance_streamedKlines_ranges[apiSymbol][intervalID] = list()
                self.binance['marketAssets_currentKline'][intervalID] = None
            self.binance['marketAssets'][apiSymbol]['mrktRegTS']             = mrktRegTS
            self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'] = firstStreamedKlineTSs
            self.binance['marketAssets'][apiSymbol]['dataRanges']            = dataRanges
            self.binance['marketAssets'][apiSymbol]['dataRanges_perc']       = dataRanges_perc

            self.binance['marketAssets'][apiSymbol]['coinIDIndex'] = self.m_DataManagement.register_asset(apiSymbol, mrktRegTS)

            #If this asset is trading, add to the trading assets list
            if (self.binance['marketAssets'][apiSymbol]['status'] == 'TRADING'): 
                self.binance['marketAssets_trading'].append(apiSymbol)
                #If this is a run-time addition of the asset, allocate RTA now
                if (uponNewConnection == False):
                    rtaAllocation = self.centralManager.allocateRTA(apiSymbol)
                    self.binance['marketAssets'][apiSymbol]['RTAAlloc']     = rtaAllocation[0]
                    self.binance['marketAssets'][apiSymbol]['RTAAllocMode'] = rtaAllocation[1]
                    self.binance['RTAAllocationCompletionQueue_RunTime'].append(apiSymbol)

            #Announce the asset data via IPC
            self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol), self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS", apiSymbol), self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')
            
    #---Handle Removed Assets
    def __handleRemovedAssets(self, removedAssets, uponNewConnection):
        for apiSymbol in removedAssets:
            #Variables Localization
            rtaCode      = self.binance['marketAssets'][apiSymbol]['RTAAlloc']
            rtaAllocMode = self.binance['marketAssets'][apiSymbol]['RTAAllocMode']
            
            #Local Market Data Update
            self.binance['marketAssets'][apiSymbol]['status'] = 'REMOVED'
            if (apiSymbol in self.binance['marketAssets_trading']): self.binance['marketAssets_trading'].remove(apiSymbol)

            #Allocation Control
            self.centralManager.updateRTAAllocation_onRemoval(apiSymbol, rtaCode, rtaAllocMode)
            self.binance['marketAssets'][apiSymbol]['RTAAlloc']     = None
            self.binance['marketAssets'][apiSymbol]['RTAAllocMode'] = None

            #Update Announcement via PRD
            self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol), self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS", apiSymbol),  self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')

    #---Handle Status Updated Assets
    def __handleStatusUpdatedAssets(self, updatedAssets, uponNewConnection):
        for updatedContent in updatedAssets:
            #Variables Localization
            apiSymbol = updatedContent[0]
            rtaCode      = self.binance['marketAssets'][apiSymbol]['RTAAlloc']
            rtaAllocMode = self.binance['marketAssets'][apiSymbol]['RTAAllocMode']
            previousStatus = updatedContent[1]
            currentStatus  = updatedContent[2]

            #Local Market Data Update
            self.binance['marketAssets'][apiSymbol]['status'] = currentStatus
            if (previousStatus == 'TRADING'):
                if (apiSymbol in self.binance['marketAssets_trading']): self.binance['marketAssets_trading'].remove(apiSymbol)

                
            #Allocation Control
            newAllocation = self.centralManager.updateRTAAllocation_onStatusChange(apiSymbol, rtaCode, rtaAllocMode, previousStatus, currentStatus)
            self.binance['marketAssets'][apiSymbol]['RTAAlloc']     = newAllocation[0]
            self.binance['marketAssets'][apiSymbol]['RTAAllocMode'] = newAllocation[1]
            
            #Update Announcement via PRD
            self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'status'), self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')
            self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'status'),  self.binance['marketAssets'][apiSymbol], nMaxDispatch = 'INF')










    #<RTA Related>
    #Complete any prepared RTA Allocation. RTA is prepared when all of its allocated symbols' mrktRegTS is identified
    def __processRTAAllocation(self):
        if (0 < len(self.binance['RTAAllocationCompletionQueue'])):
            allocCompletedRTAs = list()
            #Check if apiSymbols allocated to the corresponding rtaCode all have mrktRegTS identified, and if are all identified, send FAR 'SETWEBSOCKETSYMBOLSUBSCRIPTIONLIST' to the corresponding RTA
            for rtaCode in self.binance['RTAAllocationCompletionQueue']:
                allocatedSymbols = self.centralManager.get_allocatedSymbols_RTA(rtaCode)
                allReady = True
                for apiSymbol in allocatedSymbols:
                    for intervalID in self.binance['marketAssets'][apiSymbol]['mrktRegTS']:
                        if (self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID] == None): allReady = False
                #If the RTA is ready to launch, prep the data and send FAR 'SETWEBSOCKETSYMBOLSUBSCRIPTIONLIST'
                if (allReady == True):
                    #Allocate 10 weight limit for the RTA until the first stream data for '3d' interval is received
                    self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit'] -= len(allocatedSymbols) * REQUESTWEIGHTALLOCPERSYMBOL

                    #Data Prep
                    symbolsData = dict()
                    for apiSymbol in allocatedSymbols:
                        symbolsData[apiSymbol] = {'allocMode':    self.binance['marketAssets'][apiSymbol]['RTAAllocMode'],
                                                  'clientSymbol': self.binance['marketAssets'][apiSymbol]['symbol'],
                                                  'mrktRegTS':    self.binance['marketAssets'][apiSymbol]['mrktRegTS'],
                                                  'precisions':   self.get_Precisions(apiSymbol)}

                    #FAR Send    
                    self.ipcA[rtaCode].sendFAR(functionID = 'SETWEBSOCKETSYMBOLSUBSCRIPTIONLIST', functionParams = {'symbolsData': symbolsData}, nMaxDispatch = 'INF')
                    #Completion List Appending
                    allocCompletedRTAs.append(rtaCode)
            #Remove the allocation completed RTAs from the queue
            for rtaCode in allocCompletedRTAs: self.binance['RTAAllocationCompletionQueue'].remove(rtaCode)
            
        if (0 < len(self.binance['RTAAllocationCompletionQueue_RunTime'])):
            allocCompletedSymbols = list()
            for apiSymbol in allocCompletedSymbols:
                allReady = True
                for intervalID in self.binance['marketAssets'][apiSymbol]['mrktRegTS']:
                    if (self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID] == None): allReady = False
                if (allReady == True):
                    #Allocate 10 weight limit for the RTA until the first stream data for '3d' interval is received
                    self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit'] -= REQUESTWEIGHTALLOCPERSYMBOL

                    #Data Prep
                    symbolsData = {apiSymbol: {'allocMode':    self.binance['marketAssets'][apiSymbol]['RTAAllocMode'],
                                               'clientSymbol': self.binance['marketAssets'][apiSymbol]['symbol'],
                                               'mrktRegTS':    self.binance['marketAssets'][apiSymbol]['mrktRegTS'],
                                               'precisions':   self.get_Precisions(apiSymbol)}}

                    #FAR Send
                    self.ipcA[rtaCode].sendFAR(functionID = 'SETWEBSOCKETSYMBOLSUBSCRIPTIONLIST', functionParams = {'symbolsData': symbolsData}, nMaxDispatch = 'INF')

                    #Completion List Appending
                    allocCompletedSymbols.append(apiSymbol)
            #Remove the allocation completed apiSymbols from the queue
            for apiSymbol in allocCompletedSymbols: self.binance['RTAAllocationCompletionQueue_RunTime'].remove(apiSymbol)



        
    #---If the server is connected, process any remaining Websocket Stream Subscription Queue
    def __processWebSocketConnectionPermissionQueue(self, currentTime):
        if (0 < len(self.binance['WebSocketConnectionPermissionQueue'])):
            if ((self.binance['lastWebSocketConnection'] != 'waiting') and (1e9 < currentTime - self.binance['lastWebSocketConnection'])):
                self.binance['lastWebSocketConnection'] = 'waiting'
                rtaCode = self.binance['WebSocketConnectionPermissionQueue'].pop(0)
                self.ipcA[rtaCode].sendFAR(functionID = 'RECEIVEWEBSOCKETCONNECTIONPERMISSION', functionParams = {'permissionGiven': self.binance['serverStatus']['available']}, nMaxDispatch = 'INF')



    def __processFirstKlineReceivals(self):
        try:
            if ((self.m_DataManagement.isDBAvailable() == True) and (0 < len(self.binance_firstStreamReceivals))):
                receivalInfo = self.binance_firstStreamReceivals.pop(0)

                #Function Parameters and variables localization
                apiSymbol  = receivalInfo[0]
                intervalID = receivalInfo[1]
                
                #Calculate the downloadRange
                self.__calculateDownloadRanges(apiSymbol, intervalID)
                #Download Target Selection
                self.__selectDownloadTarget()
        except Exception as e: 
            try:    print(termcolor.colored("An error occurred during a first kline stream receival handling for {:s}_{:d}\n *".format(apiSymbol, intervalID), 'light_red'), termcolor.colored(e, 'light_red'))
            except: print(termcolor.colored("An error occurred during a first kline stream receival handling\n *",                                             'light_red'), termcolor.colored(e, 'light_red'))


    def __calculateDownloadRanges(self, apiSymbol, intervalID):
        try:
            #Get firstStreamedKlinesTS
            firstStreamedKlineTS = self.binance['marketAssets'][apiSymbol]['firstStreamedKlineTSs'][intervalID]
            if (firstStreamedKlineTS == None): print(termcolor.colored("Download ranges calculation for {:s}_{:d} terminated: no first streamed timestamp exists for the corresponding symbol and interval".format(apiSymbol, intervalID), 'light_yellow')); return

            #Get Data Availability
            dataRanges = self.m_DataManagement.get_DataAvailability(apiSymbol = apiSymbol, intervalID = intervalID)
            if (dataRanges == None): print(termcolor.colored("Download ranges calculation for {:s}_{:d} terminated: no availability data exists for the corresponding symbol and interval\n * It is possible DB was disconnected mid-process".format(apiSymbol, intervalID), 'light_yellow')); return
            
            self.set_DataAvailability(apiSymbol, intervalID, self.m_DataManagement.get_DataAvailability(apiSymbol = apiSymbol, intervalID = intervalID))
            mrktRegTS = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID]

            #---No Data Exists
            if (len(dataRanges) == 0):
                if (mrktRegTS == firstStreamedKlineTS): downloadRanges = list()
                else:                                   downloadRanges = [(mrktRegTS, firstStreamedKlineTS-1)]
            #---Singular Data Range Exists
            elif (len(dataRanges) == 1):
                downloadRanges = list()
                if (mrktRegTS < dataRanges[0][0]):              downloadRanges.append((mrktRegTS, dataRanges[0][0]-1))
                if (dataRanges[0][1]+1 < firstStreamedKlineTS): downloadRanges.append((dataRanges[0][1]+1, firstStreamedKlineTS-1))
            #---Multiple Data Ranges Exist
            else:
                downloadRanges = list()
                for dataRangeIndex in range (len(dataRanges)):
                    #Left-most Data Range
                    if (dataRangeIndex == 0):
                        if (mrktRegTS != dataRanges[dataRangeIndex][0]): downloadRanges.append((mrktRegTS, dataRanges[dataRangeIndex][0]-1))
                    #Right-most, Middle Data Ranges
                    else:
                        #Right-Most
                        downloadRanges.append((dataRanges[dataRangeIndex-1][1]+1, dataRanges[dataRangeIndex][0]-1))
                        if (dataRangeIndex == len(dataRanges)-1):
                            if (dataRanges[dataRangeIndex][1]+1 < firstStreamedKlineTS): downloadRanges.append((dataRanges[dataRangeIndex][1]+1, firstStreamedKlineTS-1))

            #Stream Data Disposal
            nStreamedKlines        = len(self.binance_streamedKlines[apiSymbol][intervalID])
            nStreamedKlines_ranges = len(self.binance_streamedKlines_ranges[apiSymbol][intervalID])
            if (0 < nStreamedKlines) or (0 < nStreamedKlines_ranges):
                self.binance_streamedKlines[apiSymbol][intervalID].clear()
                self.binance_streamedKlines_ranges[apiSymbol][intervalID].clear()
                self.binance_streamedKlines_nTotal -= nStreamedKlines
                self.binance_streamedKlines_existing.remove((apiSymbol, intervalID))

            #If there exist no data to download, send data preparation completion signal
            if (len(downloadRanges) == 0):
                self.ipcA[self.binance['marketAssets'][apiSymbol]['RTAAlloc']].sendFAR(functionID = 'DATAPREPCOMPLETE', functionParams = {'apiSymbol': apiSymbol, 'interval': KLINE_INTERVAL_BINANCEAPICORRESPONDENCES[intervalID]}, nMaxDispatch = 'INF')
            #If there exists data ranges to download, update the download queue
            else:
                if (apiSymbol in self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']]): self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']][apiSymbol][intervalID] = downloadRanges
                else:                                                                                                      self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']][apiSymbol]             = {intervalID: downloadRanges}

        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to calculate download ranges for {:s}_{:d}\n *".format(apiSymbol, intervalID), 'red'), termcolor.colored(e, 'red'))



    #<Market Registration Timestamp Related>
    #Process Any existing MrktRegTS Identification Queue
    def __processMrktRegTSCheckQueue(self):
        if (0 < len(self.binance['mrktRegTSCheckQueue'])):
            queue = self.binance['mrktRegTSCheckQueue'][-1]
            
            apiSymbol  = queue[0]
            intervalID = queue[1]

            #Check mrktRegTS once more in case DB connection was made after the queue appending
            mrktRegTS_corresponding = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID]

            if ((mrktRegTS_corresponding == None) and (self.__checkAPILimit_ReqWeight(self.__get_ExpectedRequestWeightToFindMrktRegTS(intervalID), reflectUponCheck = False)[0] == True)):
                #Try to find the mrktRegTS
                mrktRegTS = self.__get_MrktRegTS(apiSymbol, intervalID)

                #If the result was unsuccesful, move the queue to the end of the list
                if (mrktRegTS == None): print(termcolor.colored("Market Registration Timestamp for {:s}_{:d} Search Failed: Empty Fetched Klines, User Attention Needed".format(apiSymbol, intervalID), 'red'))
                else:
                    #Save the found mrktRegTS to DB
                    self.m_DataManagement.save_mrktRegistrationTS(apiSymbol, intervalID, mrktRegTS)

                    #Announce the found mrktRegTS
                    self.binance['marketAssets'][apiSymbol]['mrktRegTS'][intervalID] = mrktRegTS
                    self.ipcA['MAIN'].sendPRDEDIT(("MARKETASSETS", apiSymbol, 'mrktRegTS', intervalID), mrktRegTS, nMaxDispatch = 'INF')
                    self.ipcA['AUX'].sendPRDEDIT(("MARKETASSETS",  apiSymbol, 'mrktRegTS', intervalID), mrktRegTS, nMaxDispatch = 'INF')

                    #Reaching this point means the processing was successful, pop the queue from the list
                    self.binance['mrktRegTSCheckQueue'].pop(-1)
                    print(termcolor.colored("Market Registration Timestamp for {:s}_{:d} Search Successful:".format(apiSymbol, intervalID), 'green'),
                          termcolor.colored(datetime.utcfromtimestamp(mrktRegTS), 'green'),
                          termcolor.colored("<{:d} Remaining>".format(len(self.binance['mrktRegTSCheckQueue'])), 'green'))
                    
        #Return indicating whethere exists more mrktRegTS to check
        if (0 < len(self.binance['mrktRegTSCheckQueue'])): return True
        else:                                              return False


    
    #---Find MrktRegTS of the corresponding apiSymbol from the server
    # * This function assumed the mrktRegTS of the higher order interval is already identified <--- This must be considered when setting the 'mrktRegTSCheckQueue'
    def __get_MrktRegTS(self, apiSymbol, intervalID):
        try:
            clientSymbol = self.binance['marketAssets'][apiSymbol]['symbol']
            if (intervalID == KLINE_INTERVAL_ID_1M):
                t_beg = BINANCEFUTURES_STARTMONTH_TIMESTAMP
                t_end = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, t_beg, nTicks = 1000) - 1
                currentTS = int(time.time())
                if (currentTS < t_end): t_end = currentTS
                while (True):
                    calendar_t_beg = datetime.utcfromtimestamp(t_beg)
                    calendar_t_end = datetime.utcfromtimestamp(t_end)
                    delta_year  = calendar_t_end.year  - calendar_t_beg.year
                    delta_Month = calendar_t_end.month - calendar_t_beg.month
                    nMonths = delta_year*12 + delta_Month + 1
                    
                    klineFetch = self.__fetch_klines(clientSymbol = clientSymbol, interval = binance.Client.KLINE_INTERVAL_1MONTH, t_beg_s = t_beg, t_end_s = t_end, limit = nMonths)
                    if (0 < len(klineFetch)): break                                            #Break the loop if data exists within the range of (t_beg, t_end)
                    else:                     
                        t_beg = t_end+1
                        t_end = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, t_beg, nTicks = 1000) - 1
                        if (currentTS < t_end): t_end = currentTS

            elif (intervalID == KLINE_INTERVAL_ID_1W):
                mrktRegTS_1M = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_1M]
                if (mrktRegTS_1M == None):
                    self.binance['mrktRegTSCheckQueue'].insert(0, (apiSymbol, KLINE_INTERVAL_ID_1M))
                    return None
                t_beg = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, mrktRegTS_1M, nTicks = -1)     #First second of the previous      month
                t_end = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, mrktRegTS_1M, nTicks =  1) - 1 #Last  second of the corresponding month
                klineFetch = self.__fetch_klines(clientSymbol = clientSymbol, interval = binance.Client.KLINE_INTERVAL_1WEEK, t_beg_s = t_beg, t_end_s = t_end, limit = 99)

            elif (intervalID == KLINE_INTERVAL_ID_3d):
                mrktRegTS_1M = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_1M]
                if (mrktRegTS_1M == None):
                    self.binance['mrktRegTSCheckQueue'].insert(0, (apiSymbol, KLINE_INTERVAL_ID_1M))
                    return None
                t_beg = mrktRegTS_1M
                t_end = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, mrktRegTS_1M, nTicks = 1) - 1 #Last  second of the corresponding month
                klineFetch = self.__fetch_klines(clientSymbol = clientSymbol, interval = binance.Client.KLINE_INTERVAL_1DAY, t_beg_s = t_beg, t_end_s = t_end, limit = 99)

            elif (intervalID == KLINE_INTERVAL_ID_1d):
                mrktRegTS_3d = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_3d]
                if (mrktRegTS_3d == None):
                    self.binance['mrktRegTSCheckQueue'].insert(0, (apiSymbol, KLINE_INTERVAL_ID_3d))
                    return None
                return mrktRegTS_3d #This is a special case, mrktRegTS_1d is the same as mrktRegTS_3d by internal program definition

            elif ((intervalID == KLINE_INTERVAL_ID_12h) or (intervalID == KLINE_INTERVAL_ID_8h) or (intervalID == KLINE_INTERVAL_ID_6h) or (intervalID == KLINE_INTERVAL_ID_4h) or (intervalID == KLINE_INTERVAL_ID_2h) or (intervalID == KLINE_INTERVAL_ID_1h)):
                mrktRegTS_1d = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_1d]
                if (mrktRegTS_1d == None):
                    self.binance['mrktRegTSCheckQueue'].insert(0, (apiSymbol, KLINE_INTERVAL_ID_1d))
                    return None
                t_beg = mrktRegTS_1d
                t_end = t_beg + 86399
                klineFetch = self.__fetch_klines(clientSymbol = clientSymbol, interval = KLINE_INTERVAL_BINANCEAPICORRESPONDENCES[intervalID], t_beg_s = t_beg, t_end_s = t_end, limit = 99)

            elif ((intervalID == KLINE_INTERVAL_ID_30m) or (intervalID == KLINE_INTERVAL_ID_15m) or (intervalID == KLINE_INTERVAL_ID_5m) or (intervalID == KLINE_INTERVAL_ID_3m) or (intervalID == KLINE_INTERVAL_ID_1m)):
                mrktRegTS_1h = self.binance['marketAssets'][apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_1h]
                if (mrktRegTS_1h == None):
                    self.binance['mrktRegTSCheckQueue'].insert(0, (apiSymbol, KLINE_INTERVAL_ID_1h))
                    return None
                t_beg = mrktRegTS_1h
                t_end = t_beg + 3599
                klineFetch = self.__fetch_klines(clientSymbol = clientSymbol, interval = KLINE_INTERVAL_BINANCEAPICORRESPONDENCES[intervalID], t_beg_s = t_beg, t_end_s = t_end, limit = 99)
                
            #At this point, the first kline packet must have been fetched
            if (0 < len(klineFetch)): return int(klineFetch[0][0] / 1000)
            else: print(termcolor.colored("Empty Kline Packet Detected while attempting to find the market registration timestamp of {:s}_{:d}".format(apiSymbol, intervalID), 'light_red')); return None

        #If an error occurs, fill the apiLimit, report the error message, and return None
        except Exception as e:
            print(termcolor.colored("An error occurred while attempting to find the market registration timestamp of {:s}_{:d}\n *".format(apiSymbol, intervalID), 'light_red'), termcolor.colored(e, 'light_red'))
            return None



    #Return the expected request weight needed to find the market registration timestamp
    def __get_ExpectedRequestWeightToFindMrktRegTS(self, intervalID):
        if (intervalID == KLINE_INTERVAL_ID_1M):
            #Calculate how many months there were from the BINANCE FUTURES start month and the current month
            calendar_Now = datetime.utcnow()
            delta_year  = calendar_Now.year  - BINANCEFUTURES_STARTYEAR
            delta_Month = calendar_Now.month - BINANCEFUTURES_STARTMONTH
            nMonths = delta_year*12 + delta_Month + 1
            
            #With the number of months calcuated, compute the expected request weight consumption
            nPackets = int(nMonths/1000)
            lastPacketLength = nMonths % 1000
            if   ((  1 <= lastPacketLength) and (lastPacketLength <  100)): rwc_expected_fromLastPacket = 1
            elif ((100 <= lastPacketLength) and (lastPacketLength <  500)): rwc_expected_fromLastPacket = 2
            elif ((500 <= lastPacketLength) and (lastPacketLength < 1000)): rwc_expected_fromLastPacket = 5
            elif (lastPacketLength == 1000):                                rwc_expected_fromLastPacket = 10
            rwc_expected_total = nPackets*10+rwc_expected_fromLastPacket

            return rwc_expected_total + 1
        elif (intervalID == KLINE_INTERVAL_ID_1d): return 0  #Because mrktRegTS_1d = mrktRegTS_3d, no actual search is needed to be performed
        else:                                      return 1 + 1










    #<Klines Related>
    #---Process Any Existing Kline Download Queue
    def __processKlineDownloadQueue(self):
        if ((self.m_DataManagement.isDBAvailable() == True) and (self.m_DataManagement.isKlinesSaveAvailable() == True) and (self.binance['downloadTarget'] != None) and (self.__checkAPILimit_ReqWeight(10, reflectUponCheck = False)[0] == True)): #Check the server and request weight availability
            #Download Range Selection -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            try:
                #Select download range index
                downloadTarget_apiSymbol     = self.binance['downloadTarget'][0]
                downloadTarget_intervalID    = self.binance['downloadTarget'][1]
                downloadTarget_selectionCode = self.binance['downloadTarget'][2]
                downloadTarget_DRPriority    = self.binance['downloadTarget'][3]
                downloadRanges = self.binance['downloadRanges'][self.binance['marketAssets'][downloadTarget_apiSymbol]['RTAAllocMode']][downloadTarget_apiSymbol][downloadTarget_intervalID]

                if   (downloadTarget_DRPriority == 'LATEST'): downloadRangeIndex = len(downloadRanges)-1
                elif (downloadTarget_DRPriority == 'OLDEST'): downloadRangeIndex = 0
                elif (downloadTarget_DRPriority == 'RANDOM'): downloadRangeIndex = random.randint(0, len(downloadRanges)-1)
                downloadRange = downloadRanges[downloadRangeIndex]

                #Calculate the timestamp limit
                if (downloadTarget_intervalID == KLINE_INTERVAL_ID_3d): timestampLimit = getNextIntervalTickTimestamp(downloadTarget_intervalID, downloadRange[0], self.binance['marketAssets'][downloadTarget_apiSymbol]['mrktRegTS'][downloadTarget_intervalID], nTicks = 333)
                else:                                                   timestampLimit = getNextIntervalTickTimestamp(downloadTarget_intervalID, downloadRange[0], self.binance['marketAssets'][downloadTarget_apiSymbol]['mrktRegTS'][downloadTarget_intervalID], nTicks = 1000)

                #Set the effective download range based on the timestamp limit
                if (timestampLimit < downloadRange[1]): downloadRange_Effective = (downloadRange[0], timestampLimit-1); limitReached = True
                else:                                   downloadRange_Effective = (downloadRange[0], downloadRange[1]); limitReached = False
            except Exception as e:
                print(termcolor.colored("An error occured during a kline download process @DRC\n *", 'light_red'), termcolor.colored(e, 'light_red'))
                return False #Indication that kline download was aborted
            #Download Range Selection END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #Klines Fetch & Formatting ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            try:
                #Fetch Klines from the Binance Server
                """
                <Fetched Kline Contents>
                [0]:  Open Time
                [1]:  Open Price
                [2]:  High Price
                [3]:  Low Price
                [4]:  Close Price
                [5]:  Volume
                [6]:  Close Time
                [7]:  Quote Asset Volume
                [8]:  Number of Trades
                [9]:  Taker Buy Base Asset Volume
                [10]: Taker Buy Quote Asset Volume
                [11]: Ignore
                """
                targetClientSymbol = self.binance['marketAssets'][downloadTarget_apiSymbol]['symbol']

                #Fetch Klines from the Server
                if (downloadTarget_intervalID == KLINE_INTERVAL_ID_3d): 
                    fetchLimit = math.ceil(getNTicks_byRange(KLINE_INTERVAL_ID_1d, downloadRange_Effective[0],downloadRange_Effective[1],self.binance['marketAssets'][downloadTarget_apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_3d])*1.1)
                    if (1000 < fetchLimit): fetchLimit = 1000
                    fetchedKlines=self.__fetch_klines(clientSymbol=targetClientSymbol,interval=binance.Client.KLINE_INTERVAL_1DAY, t_beg_s=downloadRange_Effective[0],t_end_s=downloadRange_Effective[1],limit=fetchLimit)
                else:                      
                    fetchLimit = math.ceil(getNTicks_byRange(downloadTarget_intervalID,downloadRange_Effective[0],downloadRange_Effective[1],self.binance['marketAssets'][downloadTarget_apiSymbol]['mrktRegTS'][downloadTarget_intervalID])*1.1)
                    if (1000 < fetchLimit): fetchLimit = 1000                             
                    fetchedKlines=self.__fetch_klines(clientSymbol=targetClientSymbol,interval=KLINE_INTERVAL_BINANCEAPICORRESPONDENCES[downloadTarget_intervalID],t_beg_s=downloadRange_Effective[0],t_end_s=downloadRange_Effective[1],limit=fetchLimit)
            except Exception as e:
                self.__fillAPILimit_ReqWeight()
                print(termcolor.colored("An error occured during a kline download process for {:s}_{:d} @KF\n *".format(downloadTarget_apiSymbol, downloadTarget_intervalID), 'light_red'), termcolor.colored(e, 'light_red'))
                return False #Indication that kline download was aborted
            #Klines Fetch & Formatting END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #Klines Formatting & Saving -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            try:
                #Filter Fetched Klines
                if (0 < len(fetchedKlines)):
                    prec_Price    = self.binance['marketAssets'][downloadTarget_apiSymbol]['pricePrecision']
                    prec_Quantity = self.binance['marketAssets'][downloadTarget_apiSymbol]['quantityPrecision']
                    prec_Quote    = self.binance['marketAssets'][downloadTarget_apiSymbol]['quotePrecision']
                    coinIDIndexCode = self.m_DataManagement.get_coinIDIndex(downloadTarget_apiSymbol)*1e12
                    intervalIDCode  = downloadTarget_intervalID*1e10
                    #'3d' interval klines formatting
                    if (downloadTarget_intervalID == KLINE_INTERVAL_ID_3d):
                        klineBlocks_3d = dict()
                        targetMrktRegTS = self.binance['marketAssets'][downloadTarget_apiSymbol]['mrktRegTS'][KLINE_INTERVAL_ID_3d]

                        #Group '1d' klines into the corresponding '3d' timestamps
                        for kline in fetchedKlines:
                            klineTimestamp_open  = int(kline[0]/1000)

                            openTS_3d = int((klineTimestamp_open-targetMrktRegTS)/259200)*259200+targetMrktRegTS

                            #[0]: Open Price, [1]: High Price, [2]: Low Price, [3]: Close Price, [4]: nTrades, [5]: Base Asset Volume, [6]: Quote Asset Volume, [7]: Taker Buy Base Asset Volume, [8]: Taker Buy Quote Asset Volume
                            simplfiedKline_1d = (float(kline[1]), float(kline[2]), float(kline[3]), float(kline[4]), kline[8], float(kline[5]), float(kline[7]), float(kline[9]), float(kline[10]))

                            if (openTS_3d in klineBlocks_3d): klineBlocks_3d[openTS_3d].append(simplfiedKline_1d)
                            else:                             klineBlocks_3d[openTS_3d] = [simplfiedKline_1d]

                        #Generate '3d' Interval Klines from the grouped '1d' klines
                        fetchedKlines_filtered = list()
                        for tsIntervals_3d in klineBlocks_3d:
                            highPrice = 0; lowPrice = float('inf')
                            nTrades_Sum = 0; baVol_Sum = 0; qaVol_Sum = 0; tbbaVol_Sum = 0; tbqaVol_Sum = 0
                            for kline_1d in klineBlocks_3d[tsIntervals_3d]:
                                if (highPrice < kline_1d[1]): highPrice = kline_1d[1]
                                if (kline_1d[2] < lowPrice):  lowPrice  = kline_1d[2]
                                nTrades_Sum += kline_1d[4]
                                baVol_Sum   += kline_1d[5]
                                qaVol_Sum   += kline_1d[6]
                                tbbaVol_Sum += kline_1d[7]
                                tbqaVol_Sum += kline_1d[8]
                            openTS = int(coinIDIndexCode+intervalIDCode+tsIntervals_3d)
                            closeTS = tsIntervals_3d + KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d] - 1
                            fetchedKlines_filtered.append((openTS, closeTS,
                                                           round(klineBlocks_3d[tsIntervals_3d][0][0],prec_Price), round(highPrice,prec_Price), round(lowPrice,prec_Price), round(klineBlocks_3d[tsIntervals_3d][-1][3],prec_Price),
                                                           nTrades_Sum, round(baVol_Sum,prec_Quantity), round(qaVol_Sum,prec_Quote), round(tbbaVol_Sum,prec_Quantity), round(tbqaVol_Sum,prec_Quote), 13))

                    #Normal klines formatting
                    else:
                        #Relocate the klines into dict with key as the corresponding timestamp in seconds
                        fetchedKlines_dict = dict()
                        for kline in fetchedKlines:
                            klineTimestamp_open  = int(kline[0]/1000)
                            klineTimestamp_close = int(kline[6]/1000)
                            fetchedKlines_dict[klineTimestamp_open] = (int(coinIDIndexCode+intervalIDCode+klineTimestamp_open), klineTimestamp_close,
                                                                       round(float(kline[1]),prec_Price), round(float(kline[2]),prec_Price), round(float(kline[3]),prec_Price), round(float(kline[4]),prec_Price),
                                                                       kline[8], round(float(kline[5]),prec_Quantity), round(float(kline[7]),prec_Quote), round(float(kline[9]),prec_Quantity), round(float(kline[10]),prec_Quote))

                        fetchedKlineTimestamps = list(fetchedKlines_dict.keys())
                        #Analyze and fill in any expected and missing klines
                        fetchedKlines_filtered = list()
                        fillerKline = (0,0,0,0,0,0,0,0,0)
                        #'1M' interval filtering
                        if (downloadTarget_intervalID == KLINE_INTERVAL_ID_1M):
                            for index, klineTimestamp in enumerate(fetchedKlineTimestamps):
                                if (index == 0): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,))
                                else:
                                    timestampDelta = klineTimestamp - fetchedKlineTimestamps[index-1]
                                    timestampDelta_expected = getCurrentIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, klineTimestamp) - getCurrentIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, fetchedKlineTimestamps[index-1])
                                    if   (timestampDelta == timestampDelta_expected): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,)) #Expected Case
                                    elif (timestampDelta < timestampDelta_expected):  fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(11,)) #Unexpected kline exists
                                    else:                                                                                                                     #There exist some missing expected klines
                                        #Fill in any missing expected klines
                                        lastKlineTimestamp = fetchedKlineTimestamps[index-1]
                                        while (True):
                                            expectedKlineTimestamp = getNextIntervalTickTimestamp(KLINE_INTERVAL_ID_1M, lastKlineTimestamp, nTicks = 1)
                                            if (klineTimestamp <= expectedKlineTimestamp): break;
                                            else:                                          
                                                fetchedKlines_filtered.append((int(coinIDIndexCode+intervalIDCode+expectedKlineTimestamp), None)+fillerKline+(12,))
                                                lastKlineTimestamp = expectedKlineTimestamp
                                        #Append the kline fetched
                                        if (expectedKlineTimestamp == klineTimestamp): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,))
                                        else:                                          fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(11,))
                     
                        #Normal intervals filtering
                        else:
                            for index, klineTimestamp in enumerate(fetchedKlineTimestamps):
                                if (index == 0): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,));
                                else:
                                    timestampDelta = klineTimestamp - fetchedKlineTimestamps[index-1]
                                    if   (timestampDelta == KLINE_INTERVAL_SECs[downloadTarget_intervalID]): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,)) #Expected Case
                                    elif (timestampDelta < KLINE_INTERVAL_SECs[downloadTarget_intervalID]):  fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(11,)) #Unexpected kline exists
                                    else:                                                                                                                                            #There exist some missing expected klines
                                        #Fill in any missing expected klines
                                        lastKlineTimestamp = fetchedKlineTimestamps[index-1]
                                        while (True):
                                            expectedKlineTimestamp = lastKlineTimestamp+KLINE_INTERVAL_SECs[downloadTarget_intervalID]
                                            if (klineTimestamp <= expectedKlineTimestamp): break;
                                            else:
                                                fetchedKlines_filtered.append((int(coinIDIndexCode+intervalIDCode+expectedKlineTimestamp), None)+fillerKline+(12,))
                                                lastKlineTimestamp = expectedKlineTimestamp
                                        #Append the kline fetched
                                        if (expectedKlineTimestamp == klineTimestamp): fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(10,))
                                        else:                                          fetchedKlines_filtered.append(fetchedKlines_dict[klineTimestamp]+(11,))

                    if (False): #Print filtered klines
                        for index, kline in enumerate(fetchedKlines_filtered):
                            timestamp = kline[0] - coinIDIndexCode - intervalIDCode
                            print(index, datetime.fromtimestamp(timestamp, tz = timezone.utc), kline)

                    #Post Download & Formatting Process
                    #---Save Klines Data to the Database and Update Asset Data Availability
                    if (self.m_DataManagement.save_klineData(downloadTarget_apiSymbol, downloadTarget_intervalID, fetchedKlines_filtered) == True):
                        #Kline Subscription Handler
                        self.centralManager.klineSubscription_onKlineDownload(downloadTarget_apiSymbol, downloadTarget_intervalID, fetchedKlines_filtered)

                        #---Update the download range
                        if (limitReached == False):
                            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- [Scenario 1]: Klines data for the corresponding apiSymbol and interval has completed
                            if (len(downloadRanges) == 1):
                                #Remove the corresponding apiSymbol & intervalID from the download list
                                del self.binance['downloadRanges'][self.binance['marketAssets'][downloadTarget_apiSymbol]['RTAAllocMode']][downloadTarget_apiSymbol][downloadTarget_intervalID]
                            
                                #Send Data Preparation Completion Signal
                                self.ipcA[self.binance['marketAssets'][downloadTarget_apiSymbol]['RTAAlloc']].sendFAR(functionID = 'DATAPREPCOMPLETE', functionParams = {'apiSymbol': downloadTarget_apiSymbol, 'interval': KLINE_INTERVAL_BINANCEAPICORRESPONDENCES[downloadTarget_intervalID]}, nMaxDispatch = 'INF')

                                #Download Process Report
                                print(termcolor.colored("{:s}_{:d} Klines Preparation Complete! DR_E: [{:s} ~ {:s}]".format(downloadTarget_apiSymbol, downloadTarget_intervalID,
                                                                                                                            datetime.fromtimestamp(downloadRange_Effective[0], tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                            datetime.fromtimestamp(downloadRange_Effective[1], tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S")),
                                                        'light_green'))
                                #Download Process Report END

                                #Update the download target symbol and interval
                                if (len(self.binance['downloadRanges'][self.binance['marketAssets'][downloadTarget_apiSymbol]['RTAAllocMode']][downloadTarget_apiSymbol]) == 0): del self.binance['downloadRanges'][self.binance['marketAssets'][downloadTarget_apiSymbol]['RTAAllocMode']][downloadTarget_apiSymbol]
                                self.__selectDownloadTarget()

                            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- [Scenario 2]: There still exist more download ranges to process for the corresponding apiSymbol and interval
                            else:
                                #Remove the corresponding download range block from the download list
                                downloadRanges.pop(downloadRangeIndex)

                                #Download Process Report
                                print(termcolor.colored("{:s}_{:d} KDR_{:d} Completed! DR_E: [{:s} ~ {:s}]".format(downloadTarget_apiSymbol, downloadTarget_intervalID, downloadRangeIndex,
                                                                                                                   datetime.fromtimestamp(downloadRange_Effective[0],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                   datetime.fromtimestamp(downloadRange_Effective[1],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S")),
                                                        'green'))
                                if (downloadTarget_selectionCode == 'DARMERGEPRIORITY'): self.__selectDownloadTarget()
                                #Download Process Report END
                        else: # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- [Scenario 3]: There exist more klines data range to download for the corresponding download range
                            downloadRange_new = (int(fetchedKlines_filtered[-1][1]+1), downloadRange[1], False)
                            downloadRanges[downloadRangeIndex] = downloadRange_new
                            #Download Process Report
                            print(termcolor.colored("{:s}_{:d} KDR_{:d} Processed! DR_E: [{:s} ~ {:s}]\n * DR: [{:s} ~ {:s}] ---> [{:s} ~ {:s}]".format(downloadTarget_apiSymbol, downloadTarget_intervalID, downloadRangeIndex,
                                                                                                                                                        datetime.fromtimestamp(downloadRange_Effective[0],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                                                        datetime.fromtimestamp(downloadRange_Effective[1],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                                                        datetime.fromtimestamp(downloadRange[0],          tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                                                        datetime.fromtimestamp(downloadRange[1],          tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                                                        datetime.fromtimestamp(downloadRange_new[0],      tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"),
                                                                                                                                                        datetime.fromtimestamp(downloadRange_new[1],      tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S")), 
                                                    'green'))
                            #Download Process Report END

                        return True #Indication that kline download was processed with no error
                    else: return False
                else: # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ [Scenario 4]: Unexpected behavior, no fetched klines from the server
                    #Download Process Report
                    print(termcolor.colored("Klines fetch for {:s}_{:d} on range {:s} ~ {:s} was performed but no klines were fetched from the server".format(downloadTarget_apiSymbol, downloadTarget_intervalID, 
                                                                                                                                                              datetime.fromtimestamp(downloadRange_Effective[0],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S"), 
                                                                                                                                                              datetime.fromtimestamp(downloadRange_Effective[1],tz=timezone.utc).strftime("%Y/%m/%d_%H:%M:%S")), 
                                            'light_magenta'))
                    #Download Process Report END
            except Exception as e:
                print(termcolor.colored("An error occured during a kline download process for {:s}_{:d} @KFS\n *".format(downloadTarget_apiSymbol, downloadTarget_intervalID), 'light_red'), termcolor.colored(e, 'light_red'))
                return False #Indication that kline download was aborted
            #Klines Formatting & Saving END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        return True #Indication that kline download was processed with no error



    #---Select download targets
    def __selectDownloadTarget(self, apiSymbol = None, intervalID = None):
        try:
            #Record the previous download target
            downloadTarget_previous = self.binance['downloadTarget']

            #If there exists a user defined download target priority
            selectedFromUserDefined = False
            userDefined_removalList = list()
            for userDefinedTarget in self.binance['downloadTarget_userDefined']:
                if (userDefinedTarget[0] in self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']]):
                    if (0 < len(self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']][userDefinedTarget[0]])):
                        #Interval Not Defined
                        if (userDefinedTarget[1] == None):
                            intervalsInTargetSymbol = list(self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']][userDefinedTarget[0]].keys())
                            if (userDefinedTarget[3] == None): drPriority = self.binance['downloadTemporalPriority']
                            else:                              drPriority = userDefinedTarget[3]
                            if   (userDefinedTarget[2] == 'highest'): intervalsInTargetSymbol.sort(); self.binance['downloadTarget'] = [userDefinedTarget[0], intervalsInTargetSymbol[-1],                                                'USERDEFINED', drPriority]
                            elif (userDefinedTarget[2] == 'lowest'):  intervalsInTargetSymbol.sort(); self.binance['downloadTarget'] = [userDefinedTarget[0], intervalsInTargetSymbol[0],                                                 'USERDEFINED', drPriority]
                            elif (userDefinedTarget[2] == 'random'):                                  self.binance['downloadTarget'] = [userDefinedTarget[0], intervalsInTargetSymbol[random.randint(0, len(intervalsInTargetSymbol)-1)], 'USERDEFINED', drPriority]
                            selectedFromUserDefined = True
                            break
                        #Interval Defined
                        else:
                            #Defined Interval in the download list
                            if (userDefinedTarget[1] in self.binance['downloadRanges'][self.binance['marketAssets'][apiSymbol]['RTAAllocMode']][userDefinedTarget[0]]): 
                                if (userDefinedTarget[3] == None): drPriority = self.binance['downloadTemporalPriority']
                                else:                              drPriority = userDefinedTarget[3]
                                self.binance['downloadTarget'] = [userDefinedTarget[0], userDefinedTarget[1], 'USERDEFINED', drPriority]
                                selectedFromUserDefined = True
                                break
                            #Defined Interval not in the download list
                            else: userDefined_removalList.append(userDefinedTarget)
                    else: userDefined_removalList.append(userDefinedTarget)
                else: userDefined_removalList.append(userDefinedTarget)

            #Remove any non-valid user-defined download target
            for targetToRemove in userDefined_removalList: self.binance['downloadTarget_userDefined'].remove(targetToRemove)
            
            #Automatic download target selection by sorting method
            if (selectedFromUserDefined == False):
                selectedFromMergePriority = False
                #Select download target by checking the number of download ranges, if over 3, process first
                for allocMode in ('SA', 'SSO', 'SO'):
                    for apiSymbol in self.binance['downloadRanges'][allocMode]:
                        for intervalID in self.binance['downloadRanges'][allocMode][apiSymbol]:
                            if (1 < len(self.binance['downloadRanges'][allocMode][apiSymbol][intervalID])):
                                self.binance['downloadTarget'] = [apiSymbol, intervalID, 'DARMERGEPRIORITY', 'LATEST']
                                selectedFromMergePriority = True
                                break
                        if (selectedFromMergePriority == True): break
                    if (selectedFromMergePriority == True): break

                if (selectedFromMergePriority == False):
                    #Group Selection with priority 'SA' -> 'SSO' -> 'SO'
                    if   (0 < len(self.binance['downloadRanges']['SA'])):  targetGroup = 'SA'
                    elif (0 < len(self.binance['downloadRanges']['SSO'])): targetGroup = 'SSO'
                    elif (0 < len(self.binance['downloadRanges']['SO'])):  targetGroup = 'SO'
                    else:
                        self.binance['downloadTarget'] = None
                        return False #To indicate no download target exists

                    #Symbol Selection by list sorting
                    symbolsInTargetGroup = list(self.binance['downloadRanges'][targetGroup].keys())
                    symbolsInTargetGroup.sort()
                    symbol_firstOfTheSorted = symbolsInTargetGroup[0]

                    #Interval Selection by list sorting
                    intervalsInTargetSymbol = list(self.binance['downloadRanges'][targetGroup][symbol_firstOfTheSorted].keys())
                    intervalsInTargetSymbol.sort()

                    self.binance['downloadTarget'] = [symbol_firstOfTheSorted, intervalsInTargetSymbol[0], 'AUTOSELECT', self.binance['downloadTemporalPriority']]

            #Report the update on the download target
            #---[0]: None -> Existing
            if   ((downloadTarget_previous == None) and (self.binance['downloadTarget'] != None)): print(termcolor.colored("Klines Download Target Updated!: 'None' -> '{:s}_{:d}' <{:s}:{:s}>".format(self.binance['downloadTarget'][0], self.binance['downloadTarget'][1], self.binance['downloadTarget'][2], self.binance['downloadTarget'][3]), 'light_cyan'))
            #---[1]: Existing -> None
            elif ((downloadTarget_previous != None) and (self.binance['downloadTarget'] == None)): print(termcolor.colored("Klines Download Target Updated!: '{:s}_{:d} <{:s}:{:s}>' -> 'None'".format(downloadTarget_previous[0], downloadTarget_previous[1], downloadTarget_previous[2], downloadTarget_previous[3]), 'light_cyan'))
            #---[2]: Existing -> new Existing
            elif ((downloadTarget_previous != None) and (self.binance['downloadTarget'] != None)):
                if ((downloadTarget_previous[0] != self.binance['downloadTarget'][0]) or (downloadTarget_previous[1] != self.binance['downloadTarget'][1])):
                    print(termcolor.colored("Klines Download Target Updated!: '{:s}_{:d}' <{:s}:{:s}> -> '{:s}_{:d}' <{:s}:{:s}>".format(downloadTarget_previous[0], downloadTarget_previous[1], downloadTarget_previous[2], downloadTarget_previous[3], 
                                                                                                                                         self.binance['downloadTarget'][0], self.binance['downloadTarget'][1], self.binance['downloadTarget'][2], self.binance['downloadTarget'][3]), 'light_cyan'))
                    
            #Return True if a new download target is selected and False if there is no more target to download
            if (self.binance['downloadTarget'] == None): return False
            else:                                        return True

        except Exception as e: print(termcolor.colored("An error occured during a Download Target Selection with params (apiSymbol = {:s}, intervalID = {:s}):".format(str(apiSymbol), str(intervalID)), 'light_red'), termcolor.colored(e, 'light_red'))



    def __fetch_klines(self, clientSymbol, interval, t_beg_s, t_end_s, limit = 1000):
        if   ((  1 <= limit) and (limit <   100)): req_weight = 1;  limit_effective = 99
        elif ((100 <= limit) and (limit <   500)): req_weight = 2;  limit_effective = 499
        elif ((500 <= limit) and (limit <= 1000)): req_weight = 5;  limit_effective = 1000
        else:                                      req_weight = 10; limit_effective = limit
        #Check current weight limit availability, if not available, go to sleep until the next reset interval
        reqWeightAvailability = self.__checkAPILimit_ReqWeight(req_weight)
        while (reqWeightAvailability[0] != True):
            print(termcolor.colored("<<< REQUEST WEIGHT LIMIT REACHED, WAITING FOR {:d} SECONDS >>>>".format(reqWeightAvailability[1]), 'light_cyan'))
            time.sleep(reqWeightAvailability[1])
            reqWeightAvailability = self.__checkAPILimit_ReqWeight(req_weight)
        #Fetch Futures Historical Klines using default binance client
        fetchedKlines = self.binance['clients']['default']['client'].futures_historical_klines(symbol = clientSymbol, interval = interval, start_str = t_beg_s*1000, end_str = t_end_s*1000, limit = limit_effective, verifyFirstTS = False)
        nExtraFetchLaps = int(len(fetchedKlines)/limit_effective)
        self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'] += req_weight*nExtraFetchLaps
        return fetchedKlines



    #---Save Streamed Klines
    def __saveStreamedKlines(self, currentTime_ns = float('inf')):
        try:
            if ((0 < self.binance_streamedKlines_nTotal) and ((self.binance_streamedKlinesSaveInterval_ms <= currentTime_ns/1e6 - self.binance_streamedKlinesLastSaved_ms) or (100 < self.binance_streamedKlines_nTotal))):
                klines_collected = list()
                #Pause Closed Klines List Update For Data Copy
                for target in self.binance_streamedKlines_existing:
                    apiSymbol = target[0]; intervalID = target[1]
                    #Collect the klines
                    coinIDIndexCode = self.m_DataManagement.get_coinIDIndex(apiSymbol)*1e12; intervalIDCode = intervalID*1e10
                    klines_DBFormatted = list()
                    for kline in self.binance_streamedKlines[apiSymbol][intervalID]: klines_DBFormatted.append((int(coinIDIndexCode+intervalIDCode+kline[0]),) + kline[1:])
                    klines_collected += klines_DBFormatted

                #Attempt to save the streamed klines
                if (self.m_DataManagement.save_klineStreamData(klines_collected, self.binance_streamedKlines_ranges, self.binance_streamedKlines_existing) == True):
                    print(termcolor.colored("Successfully saved {:d} streamed klines!".format(self.binance_streamedKlines_nTotal), 'light_green'))
                    #If the save was successful, reset the control variables
                    for target in self.binance_streamedKlines_existing:
                        apiSymbol = target[0]; intervalID = target[1]
                        self.binance_streamedKlines[apiSymbol][intervalID].clear()
                        self.binance_streamedKlines_ranges[apiSymbol][intervalID].clear()
                    self.binance_streamedKlines_existing.clear()
                    self.binance_streamedKlines_nTotal = 0
                    self.binance_streamedKlinesLastSaved_ms = time.perf_counter_ns()/1e6
        except Exception as e: print(termcolor.colored("An unexpected error occured while attempting to prepare streamed klines for a save:", 'red'), termcolor.colored(e, 'red'))
        









    #<REST API Limit Related>
    #---Call before sending a request the Binance API in order to check if the current request weight used does not exceed the limit, if exceeded, return the amount of time to wait for the request weight reset, if not exceeded, add the weight to the tracker variable
    def __checkAPILimit_ReqWeight(self, reqWeight, reflectUponCheck = True):
        if (self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'] + reqWeight < int(self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit'])): #Multiplication by 0.95 is to only use up to 95% of the limit defined by the server
            if (reflectUponCheck == True): 
                self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'] += reqWeight
                print(termcolor.colored("Request Weight Consumed, {:d} / {:d}".format(self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'], self.binance['APIRateLimits']['usedByThisIP']['req_weight_min_LocalLimit']), 'light_yellow'))
            return (True, 0)
        else: #Calculate how many seconds are left until the next new minute
            currentSecond = int(time.time())
            nextMinute_s = (int(currentSecond / 60) + 1) * 60
            return (False, (nextMinute_s - currentSecond))
    #---Completely fill API Limit
    def __fillAPILimit_ReqWeight(self):
        self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'] = float('inf')
    #---Periodic Variable Updaters
    def __periodUpdater_10sec(self, **kwargs):
        self.binance['APIRateLimits']['usedByThisIP']['orders_sec'] = 0
    def __periodUpdater_min(self, **kwargs):
        self.binance['APIRateLimits']['usedByThisIP']['req_weight_min'] = 0
        self.binance['APIRateLimits']['usedByThisIP']['orders_min'] = 0
    #Internal Functions END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#Auxillary Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getAllIntervalTimestamps(marketRegTimestamp, timestamp_1min):
    mrktReg_firstDay = int(marketRegTimestamp/86400)*86400

    timestamp_dateTime = datetime.fromtimestamp(timestamp_1min, tz = timezone.utc)
    timestamp_ISOCalendar = timestamp_dateTime.isocalendar()
    
    timestamp_1m  = timestamp_1min
    timestamp_3m  = int(timestamp_1min/  180)*  180
    timestamp_5m  = int(timestamp_1min/  300)*  300
    timestamp_15m = int(timestamp_1min/  900)*  900
    timestamp_30m = int(timestamp_1min/ 1800)* 1800
    timestamp_1h  = int(timestamp_1min/ 3600)* 3600
    timestamp_2h  = int(timestamp_1min/ 7200)* 7200
    timestamp_4h  = int(timestamp_1min/14400)*14400
    timestamp_6h  = int(timestamp_1min/21600)*21600
    timestamp_8h  = int(timestamp_1min/28800)*28800
    timestamp_12h = int(timestamp_1min/43200)*43200
    timestamp_1d  = int(timestamp_1min/86400)*86400
    timestamp_3d  = int((timestamp_1d-mrktReg_firstDay)/259200)*259200+mrktReg_firstDay
    timestamp_1w  = int(datetime.fromisocalendar(year = timestamp_ISOCalendar.year, week = timestamp_ISOCalendar.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)
    timestamp_1M  = int(datetime(year = timestamp_dateTime.year, month = timestamp_dateTime.month, day = 1, tzinfo = timezone.utc).timestamp())

    return (timestamp_1m,  timestamp_3m, timestamp_5m, timestamp_15m, timestamp_30m,
            timestamp_1h,  timestamp_2h, timestamp_4h, timestamp_6h,  timestamp_8h,
            timestamp_12h, timestamp_1d, timestamp_3d, timestamp_1w,  timestamp_1M)



#Calculate and return the current interval tick timestamp
def getCurrentIntervalTickTimestamp(intervalID, timestamp_1m, mrktReg = None):
    if (intervalID == KLINE_INTERVAL_ID_1M):
        timestamp_dateTime = datetime.fromtimestamp(timestamp_1m, tz = timezone.utc)
        return int(datetime(year = timestamp_dateTime.year, month = timestamp_dateTime.month, day = 1, tzinfo = timezone.utc).timestamp())

    elif (intervalID == KLINE_INTERVAL_ID_1W):
        timestamp_ISOCalendar = datetime.fromtimestamp(timestamp_1m, tz = timezone.utc).isocalendar()
        return int(datetime.fromisocalendar(year = timestamp_ISOCalendar.year, week = timestamp_ISOCalendar.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)

    elif (intervalID == KLINE_INTERVAL_ID_3d):
        if (mrktReg == None): return (int(timestamp_1m/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]))*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
        else:
            mrktRegFirstDay = int(mrktReg     /86400)*86400
            timestamp_1d    = int(timestamp_1m/86400)*86400
            return (int((timestamp_1d-mrktRegFirstDay)/259200))*259200+mrktRegFirstDay

    else: return (int(timestamp_1m/KLINE_INTERVAL_SECs[intervalID]))*KLINE_INTERVAL_SECs[intervalID]



#Calculate and return the next interval tick timestamp
def getNextIntervalTickTimestamp(intervalID, timestamp, mrktReg = None, nTicks = 1):
    if (intervalID == KLINE_INTERVAL_ID_1M):
        timestamp_dateTime = datetime.fromtimestamp(timestamp, tz = timezone.utc)
        nextMonth = timestamp_dateTime.month+nTicks
        nextMonth_yearDeducted = nextMonth%12
        if (nextMonth_yearDeducted == 0): newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12) - 1; newMonthDate_month = 12
        else:                             newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12);     newMonthDate_month = nextMonth_yearDeducted
        return int(datetime(year = newMonthDate_year, month = newMonthDate_month, day = 1, tzinfo = timezone.utc).timestamp())

    elif (intervalID == KLINE_INTERVAL_ID_1W):
        timestamp_ISOCalendar = datetime.fromtimestamp(timestamp, tz = timezone.utc).isocalendar()
        return int(datetime.fromisocalendar(year = timestamp_ISOCalendar.year, week = timestamp_ISOCalendar.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC + KLINE_INTERVAL_SECs[intervalID]*nTicks)

    elif (intervalID == KLINE_INTERVAL_ID_3d):
        if (mrktReg == None): return (int(timestamp/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])+nTicks)*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
        else:
            mrktRegFirstDay = int(mrktReg  /86400)*86400
            timestamp_1d    = int(timestamp/86400)*86400
            return (int((timestamp_1d-mrktRegFirstDay)/259200)+nTicks)*259200+mrktRegFirstDay

    else: return (int(timestamp/KLINE_INTERVAL_SECs[intervalID])+nTicks)*KLINE_INTERVAL_SECs[intervalID]



#Return a list of timestamps for nTicks of interval
def getTimestampList_byNTicks(intervalID, timestamp, mrktReg = None, nTicks = 1):
    if (intervalID == KLINE_INTERVAL_ID_1M):
        timestamps = list()
        timestamp_dateTime = datetime.fromtimestamp(timestamp, tz = timezone.utc)
        for i in range (nTicks):
            nextMonth = timestamp_dateTime.month+i
            nextMonth_yearDeducted = nextMonth%12
            if (nextMonth_yearDeducted == 0): newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12) - 1; newMonthDate_month = 12
            else:                             newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12);     newMonthDate_month = nextMonth_yearDeducted
            timestamps.append(int(datetime(year = newMonthDate_year, month = newMonthDate_month, day = 1, tzinfo = timezone.utc).timestamp()))
        return timestamps

    elif (intervalID == KLINE_INTERVAL_ID_1W):
        timestamps = list()
        timestamp_ISOCalendar = datetime.fromtimestamp(timestamp, tz = timezone.utc).isocalendar()
        for i in range (nTicks): timestamps.append(int(datetime.fromisocalendar(year = timestamp_ISOCalendar.year, week = timestamp_ISOCalendar.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC + KLINE_INTERVAL_SECs[intervalID]*i))
        return timestamps

    elif (intervalID == KLINE_INTERVAL_ID_3d):
        if (mrktReg == None): 
            firstTickTS = int(timestamp/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
        else:
            mrktRegFirstDay = int(mrktReg  /86400)*86400
            timestamp_1d    = int(timestamp/86400)*86400
            firstTickTS = (int((timestamp_1d-mrktRegFirstDay)/259200))*259200+mrktRegFirstDay
        lastTickTS  = firstTickTS+KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]*nTicks
        return  list(range(firstTickTS, lastTickTS, KLINE_INTERVAL_SECs[intervalID]))

    else: 
        firstTickTS = int(timestamp/KLINE_INTERVAL_SECs[intervalID])*KLINE_INTERVAL_SECs[intervalID]
        lastTickTS  = firstTickTS+KLINE_INTERVAL_SECs[intervalID]*nTicks
        return list(range(firstTickTS, lastTickTS, KLINE_INTERVAL_SECs[intervalID]))



#Return a list of timestamps for nTicks of interval
def getTimestampList_byRange(intervalID, timestamp_beg, timestamp_end, mrktReg = None):
    try:
        if (intervalID == KLINE_INTERVAL_ID_1M):
            timestamps = list()
            timestamp_dateTime = datetime.fromtimestamp(timestamp_beg, tz = timezone.utc)
            while (True):
                nextMonth = timestamp_dateTime.month+len(timestamps)
                nextMonth_yearDeducted = nextMonth%12
                if (nextMonth_yearDeducted == 0): newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12) - 1; newMonthDate_month = 12
                else:                             newMonthDate_year = timestamp_dateTime.year + int(nextMonth/12);     newMonthDate_month = nextMonth_yearDeducted
                nextTimestamp = int(datetime(year = newMonthDate_year, month = newMonthDate_month, day = 1, tzinfo = timezone.utc).timestamp())
                if (nextTimestamp < timestamp_end): timestamps.append(nextTimestamp)
                else: break
            return timestamps

        elif (intervalID == KLINE_INTERVAL_ID_1W):
            timestamp_ISOCalendar_BEG = datetime.fromtimestamp(timestamp_beg, tz = timezone.utc).isocalendar()
            timestamp_ISOCalendar_END = datetime.fromtimestamp(timestamp_end, tz = timezone.utc).isocalendar()
            firstTickTS = int(datetime.fromisocalendar(year = timestamp_ISOCalendar_BEG.year, week = timestamp_ISOCalendar_BEG.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)
            lastTickTS  = int(datetime.fromisocalendar(year = timestamp_ISOCalendar_END.year, week = timestamp_ISOCalendar_END.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)
            return list(range(firstTickTS, lastTickTS, KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_1W]))

        elif (intervalID == KLINE_INTERVAL_ID_3d):
            if (mrktReg == None): 
                firstTickTS = int(timestamp_beg/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
            else:
                mrktRegFirstDay = int(mrktReg      /86400)*86400
                timestamp_1d    = int(timestamp_beg/86400)*86400
                firstTickTS = (int((timestamp_1d-mrktRegFirstDay)/259200))*259200+mrktRegFirstDay
            lastTickTS  = int(timestamp_end/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
            return list(range(firstTickTS, lastTickTS, KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]))

        else: 
            firstTickTS = int(timestamp_beg/KLINE_INTERVAL_SECs[intervalID])*KLINE_INTERVAL_SECs[intervalID]
            lastTickTS  = int(timestamp_end/KLINE_INTERVAL_SECs[intervalID])*KLINE_INTERVAL_SECs[intervalID]
            return list(range(firstTickTS, lastTickTS, KLINE_INTERVAL_SECs[intervalID]))
    except Exception as e: print(termcolor.colored("An error occured in 'getTimestampList_byRange' function:", 'light_red'), termcolor.colored(e, 'light_red'))



#Return number of ticks in a given range for the interval
def getNTicks_byRange(intervalID, timestamp_beg, timestamp_end, mrktReg = None):
    try:
        if (intervalID == KLINE_INTERVAL_ID_1M):
            dateTime_BEG = datetime.fromtimestamp(timestamp_beg, tz = timezone.utc)
            dateTime_END = datetime.fromtimestamp(timestamp_end, tz = timezone.utc)
            delta_Month = dateTime_END.month - dateTime_BEG.month
            delta_Year  = dateTime_END.year  - dateTime_BEG.year
            return delta_Year*12+delta_Month+1

        elif (intervalID == KLINE_INTERVAL_ID_1W):
            timestamp_ISOCalendar_BEG = datetime.fromtimestamp(timestamp_beg, tz = timezone.utc).isocalendar()
            timestamp_ISOCalendar_END = datetime.fromtimestamp(timestamp_end, tz = timezone.utc).isocalendar()
            firstTickTS = int(datetime.fromisocalendar(year = timestamp_ISOCalendar_BEG.year, week = timestamp_ISOCalendar_BEG.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)
            lastTickTS  = int(datetime.fromisocalendar(year = timestamp_ISOCalendar_END.year, week = timestamp_ISOCalendar_END.week, day = 1).timestamp() + TIMEZONE_DELTA_SEC)
            return int((lastTickTS-firstTickTS)/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_1W])+1

        elif (intervalID == KLINE_INTERVAL_ID_3d):
            if (mrktReg == None): 
                firstTickTS = int(timestamp_beg/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
            else:
                mrktRegFirstDay = int(mrktReg      /86400)*86400
                timestamp_1d    = int(timestamp_beg/86400)*86400
                firstTickTS = (int((timestamp_1d-mrktRegFirstDay)/259200))*259200+mrktRegFirstDay
            lastTickTS  = int(timestamp_end/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])*KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d]
            return int((lastTickTS-firstTickTS)/KLINE_INTERVAL_SECs[KLINE_INTERVAL_ID_3d])+1

        else: 
            firstTickTS = int(timestamp_beg/KLINE_INTERVAL_SECs[intervalID])*KLINE_INTERVAL_SECs[intervalID]
            lastTickTS  = int(timestamp_end/KLINE_INTERVAL_SECs[intervalID])*KLINE_INTERVAL_SECs[intervalID]
            return int((lastTickTS-firstTickTS)/KLINE_INTERVAL_SECs[intervalID])+1
    except Exception as e: print(termcolor.colored("An error occured in 'getNTicks_byRange' function:", 'light_red'), termcolor.colored(e, 'light_red'))

#Auxillary Functions END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------