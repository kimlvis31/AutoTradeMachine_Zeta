from multiprocessing import process
import ATM_Zeta_Auxillaries

from random import randint
import pyglet
import time
import os
import pprint
import termcolor
import binance
import math
import asyncio
import socket

STREAMINTERVALS = ('1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M')
MAXNSYMBOLS_PERCONN = int(150/(len(STREAMINTERVALS)-1)) #Recommended maximum number of streams per connection according to Binance WebSocket API is 200, in this program, it only utilizes 75% of that maximum recommended number

STREAMRESULTUPDATEINTERVAL_MILLISECONDS = 1000

STREAMPERIODICRESTARTINTERVAL_SECONDS = 3600 #Every 1 hour

INITIAL1DKLINEFETCH_MAXATTEMPT      = 5
INITIAL1DKLINEFETCH_ATTEMPTINTERVAL = 0.2

class RTA:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, ipcA, ipcAThread, rtaCode):
        self.rtaCode = rtaCode
        self.ipcA = ipcA
        self.ipcAThread = ipcAThread
        self.assets = dict()
        self.clientSymbolToAPISymbol = dict()

        self.sys_HostName = socket.gethostname()

        #Process Control
        self.eventHandlerPending = None
        self.process_terminate = False

        #Binance Server Access
        self.serverConnected = False

        self.binanceClient = None
        
        self.binanceTWM = None
        self.binanceTWM_Conns = list()
        self.klineStreamsBuffer = list(); self.klineStreamsBuffer_processing = False
        self.klineStreams_restart = False

        self.socketConnectionPermission = False
        self.socketConnectionPermissionRequestSent = False

        self.wsSymbolSubscriptionList = None
        
        #Database Access
        self.dbConnected = False
        self.dbDir = None
        
        #IPC Call Function Registration
        self.ipcA.addFARHandler("PROCCTRLFUNC_TERMINATE", self.far_RaiseTerminationFlag)

        self.ipcA.addFARHandler("SETWEBSOCKETSYMBOLSUBSCRIPTIONLIST",   self.farHandler_setWebSocketSymbolSubscriptionList)
        self.ipcA.addFARHandler("RECEIVEWEBSOCKETCONNECTIONPERMISSION", self.farHandler_WebSocketConnectionPermissionGiven)

        self.ipcA.addFARHandler("ONSERVERCONNECTION",    self.farHandler_OnServerConnection)
        self.ipcA.addFARHandler("ONSERVERDISCONNECTION", self.farHandler_OnServerDisconnection)
        self.ipcA.addFARHandler("ONDBCONNECTION",        self.farHandler_OnDBConnection)
        self.ipcA.addFARHandler("ONDBDISCONNECTION",     self.farHandler_OnDBDisconnection)

        self.ipcA.addFARHandler("DATAPREPCOMPLETE", self.farHandler_onDataPrepComplete)

    def postInitialization(self):
        self.ipcA.sendPRDEDIT("PROCSTATUS", "INITIALIZED", nMaxDispatch = 'INF')

        #These values of RTA are sent to ATM in order to share RTA's view of the current system status
        self.ipcA.sendPRDEDIT("SERVERCONNECTION", self.serverConnected, nMaxDispatch = 'INF')
        self.ipcA.sendPRDEDIT("DBCONNECTION",     self.dbConnected,     nMaxDispatch = 'INF')
        self.ipcA.sendPRDEDIT("DBDIR",            self.dbDir,           nMaxDispatch = 'INF')
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




    #Manager Process Loop ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self):
        self.ipcA.sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        while (self.process_terminate == False):
            currentTime_ns = time.perf_counter_ns()
            if (self.eventHandlerPending == None):
                if (self.serverConnected == True):
                    #Create any websocket connection if needed
                    self.__createWebSocketConnection()

                    #Check the existing WebSocket Connections for any needed renewal
                    self.__checkWebSocketConnectionRenewal()

                    #Process the kline stream buffer
                    self.__processKlineStreams()

                    #Perform assets process
                    for apiSymbol in self.assets: self.assets[apiSymbol].process(currentTime_ns)
            else:
                if   (self.eventHandlerPending == 'SERVERCONNECTION'):    self.__on_ServerConnection()
                elif (self.eventHandlerPending == 'SERVERDISCONNECTION'): self.__on_ServerDisconnection()
                elif (self.eventHandlerPending == 'DBCONNECTION'):        self.__on_DBConnection()
                elif (self.eventHandlerPending == 'DBDISCONNECTION'):     self.__on_DBDisconnection()
                self.eventHandlerPending = None
                
            #FAR/FARR Processing
            self.ipcA.processFARs()
            self.ipcA.processFARRs()

            time.sleep(0.001)

        #Termination Sequence
        self.ipcA.sendPRDEDIT("PROCSTATUS", "TERMINATED", nMaxDispatch = 'INF')
        self.ipcA.terminate()  #Set IPCA Termination Flag
        self.ipcAThread.join() #Wait until IPCA thread finishes
    #Manager Process Loop END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Manager Internal Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Handle WebSocket Connection Command from ATM
    def __createWebSocketConnection(self):
        if (self.wsSymbolSubscriptionList != None): #If there exists Symbol Subscription List to create
            if (self.socketConnectionPermission == True): #If socket connection permission is given, proceed and send WebSocket Connection Requests to the Binance Server
                apiSymbols = list(self.wsSymbolSubscriptionList.keys())
                #Create Kline Connections as needed
                streams_Conns = [{'streams': list(), 'apiSymbols': list()}]
                currentConnIndex = 0
                nSymbols_thisConn = 0
                
                for apiSymbol in apiSymbols:
                    clientSymbol = self.wsSymbolSubscriptionList[apiSymbol]['clientSymbol']
                        
                    #Stream Name Generation
                    for interval in STREAMINTERVALS:
                        if not(interval == '3d'): #'3d' Interval is calculated based on '1d' klines, so streaming for '3d' is skipped
                            streamName = "{:s}_perpetual@continuousKline_{:s}".format(clientSymbol.lower(), interval)
                            streams_Conns[currentConnIndex]['streams'].append(streamName)
                    streams_Conns[currentConnIndex]['apiSymbols'].append(apiSymbol)

                    #Connection Limit Handler
                    nSymbols_thisConn += 1
                    if (nSymbols_thisConn == MAXNSYMBOLS_PERCONN): streams_Conns.append({'streams': list(), 'apiSymbols': list()}); currentConnIndex += 1; nSymbols_thisConn = 0

                apiSymbols_streaming = list()
                for connIndex, streams_Conn in enumerate(streams_Conns):
                    if (0 < len(streams_Conn['streams'])):
                        #Successful WebSocket Connection Establishment
                        try:
                            self.binanceTWM_Conns.append({'connectionName': self.binanceTWM.start_futures_multiplex_socket(callback=self.__KlineStreamReceiver, streams=streams_Conn['streams']), 
                                                          'streamNames':    streams_Conn['streams'], 
                                                          'apiSymbols':     streams_Conn['apiSymbols'], 
                                                          'connectionTime': time.time()})
                            for apiSymbol in streams_Conn['apiSymbols']:
                                allocMode    = self.wsSymbolSubscriptionList[apiSymbol]['allocMode']
                                clientSymbol = self.wsSymbolSubscriptionList[apiSymbol]['clientSymbol']
                                mrktRegTS    = self.wsSymbolSubscriptionList[apiSymbol]['mrktRegTS']
                                precisions   = self.wsSymbolSubscriptionList[apiSymbol]['precisions']
                                self.assets[apiSymbol] = RTA_Asset(self.rtaCode, self.ipcA, self.binanceClient, connIndex, apiSymbol, clientSymbol, allocMode, mrktRegTS, precisions)
                                self.clientSymbolToAPISymbol[clientSymbol] = apiSymbol
                                apiSymbols_streaming.append(apiSymbol)
                        #Websocket Connection Establishment Failure
                        except Exception as e: print(termcolor.colored("[{:s}] An error occurred while attempting to start multiplex socket connection index {:d}\n *".format(self.rtaCode, connIndex), 'red'), termcolor.colored(e, 'red'))
                        time.sleep(1)

                #Reset control variables
                self.wsSymbolSubscriptionList   = None
                self.socketConnectionPermission = False
                self.klineStreams_restart       = False

                #Send WebSocket Connection Attempt Result
                self.ipcA.sendFAR(functionID = 'ONWEBSOCKETCONNECTIONCOMPLETION', functionParams = {'rtaCode': self.rtaCode, 'connectionCompletionTS': time.time(), 'streamingAPISymbols': apiSymbols_streaming}, nMaxDispatch = 'INF')

            else: #If no socket connection permission is given, send a permission request
                if (self.socketConnectionPermissionRequestSent == False):
                    self.ipcA.sendFAR(functionID = 'GETWEBSOCKETCONNECTIONPERMISSION', functionParams = {'rtaCode': self.rtaCode}, nMaxDispatch = 'INF') #Send a connection creation permission request to ATM
                    self.socketConnectionPermissionRequestSent = True
                


    #Check the connection times of the current WebSocket connections and restart the streaming if the connection time has reached a certain amount of time
    def __checkWebSocketConnectionRenewal(self):
        #If entire connections restart flag has been raised due to 'Queue overflow. Message not filled' error from the stream message
        if (self.klineStreams_restart == True):
            if (self.socketConnectionPermission == True):
                apiSymbols_streaming = list()
                for connIndex in range (len(self.binanceTWM_Conns)):
                    self.__restartWebSocketConnection(connIndex)
                    apiSymbols_streaming += self.binanceTWM_Conns[connIndex]['apiSymbols']
                    time.sleep(1)
                self.ipcA.sendFAR(functionID = 'ONWEBSOCKETCONNECTIONCOMPLETION', functionParams = {'rtaCode': self.rtaCode, 'connectionCompletionTS': time.time(), 'streamingAPISymbols': apiSymbols_streaming}, nMaxDispatch = 'INF')
                self.socketConnectionPermission = False
                self.klineStreams_restart = False
        #Periodic connection restart
        else:
            #Find connection indexes that need to be restarted
            restartNeededConnIndexes = list()
            for connIndex in range (len(self.binanceTWM_Conns)):
                if (STREAMPERIODICRESTARTINTERVAL_SECONDS < time.time() - self.binanceTWM_Conns[connIndex]['connectionTime']): restartNeededConnIndexes.append(connIndex)

            #If there exist any connection that needs to be restarted
            if (0 < len(restartNeededConnIndexes)):
                #If socket connection permission is given, restart the connections
                if (self.socketConnectionPermission == True):
                    apiSymbols_streaming = list()
                    for connIndex in restartNeededConnIndexes: self.__restartWebSocketConnection(connIndex); apiSymbols_streaming += self.binanceTWM_Conns[connIndex]['apiSymbols']; time.sleep(1)
                    self.ipcA.sendFAR(functionID = 'ONWEBSOCKETCONNECTIONCOMPLETION', functionParams = {'rtaCode': self.rtaCode, 'connectionCompletionTS': time.time(), 'streamingAPISymbols': apiSymbols_streaming}, nMaxDispatch = 'INF')
                    self.socketConnectionPermission = False
                #If the socket connection permission is not given and request is not sent yet, send request
                else:
                    if (self.socketConnectionPermissionRequestSent == False):
                        self.ipcA.sendFAR(functionID = 'GETWEBSOCKETCONNECTIONPERMISSION', functionParams = {'rtaCode': self.rtaCode}, nMaxDispatch = 'INF') #If no TWM exists, send a connection creation permission request to ATM
                        self.socketConnectionPermissionRequestSent = True



    #Restart the given index WebSocket connection
    def __restartWebSocketConnection(self, connectionIndex):
        try:
            connection = self.binanceTWM_Conns[connectionIndex]
            try: self.binanceTWM.stop_socket(connection['connectionName'])
            except Exception as e: print(termcolor.colored("[{:s}] WebSocket Connection {:d} Stop Failed\n *".format(self.rtaCode, connectionIndex), 'red'), termcolor.colored(e, 'red'))
            for apiSymbol in connection['apiSymbols']: self.assets[apiSymbol].on_StreamReconnection()
            newConnection = {'connectionName': self.binanceTWM.start_futures_multiplex_socket(callback=self.__KlineStreamReceiver, streams=connection['streamNames']),
                             'streamNames':    connection['streamNames'],
                             'apiSymbols':     connection['apiSymbols'],
                             'connectionTime': time.time()}
            self.binanceTWM_Conns[connectionIndex] = newConnection
            print(termcolor.colored("[{:s}] WebSocket connection {:d} successfully restarted!".format(self.rtaCode, connectionIndex), 'light_green'))
        except Exception as e: print(termcolor.colored("[{:s}] An error occurred while attempting to restart WebSocket Connection {:d}\n *".format(self.rtaCode, connectionIndex), 'red'), termcolor.colored(e, 'red'))



    #Handle Kline Stream Data from Threaded Binance WebSocket Manager
    def __KlineStreamReceiver(self, streamContents):
        #Expected Data Example
        #{'stream': 'dogeusdt_perpetual@continuousKline_6h', 
        # 'data':   {'e': 'continuous_kline', 
        #            'E': 1710435281932, 
        #            'ps': 'DOGEUSDT', 
        #            'ct': 'PERPETUAL', 
        #            'k': {'t': 1710417600000, 'T': 1710439199999, 'i': '6h', 'f': 4178342826779, 'L': 4180732271887, 'o': '0.183200', 'c': '0.177400', 'h': '0.189640', 'l': '0.169680', 'v': '6756780082', 'n': 2277398, 'x': False, 'q': '1211112589.376870', 'V': '3192382498', 'Q': '572467775.510730', 'B': '0'}}}
        try:
            if (self.serverConnected == True): #The reason for this check may not be so obvious; 'self.serverConnected' variable also indicates the RTA's readiness to process any incoming stream data
                if ('data' in streamContents):
                    streamName = streamContents['stream']
                    data       = streamContents['data']
                    if (data['e'] == 'continuous_kline'):
                        clientSymbol = data['ps']
                        if (clientSymbol in self.clientSymbolToAPISymbol): #Asset class may not have be initialized yet
                            apiSymbol = self.clientSymbolToAPISymbol[clientSymbol]
                            kline        = data['k']
                            eventTime    = data['E']
                            closed       = kline['x']
                            interval     = kline['i']
                            #Save the received stream data to the local buffer for later processing
                            if ((closed == True) or (STREAMRESULTUPDATEINTERVAL_MILLISECONDS <= eventTime - self.assets[apiSymbol].lastSentEventTimestmap_ms[interval])):
                                self.assets[apiSymbol].lastSentEventTimestmap_ms[interval] = eventTime
                                if (interval == '1d'): self.assets[apiSymbol].lastSentEventTimestmap_ms['3d'] = eventTime
                        
                                self.klineStreamsBuffer_processing = True
                                self.klineStreamsBuffer.append((apiSymbol, eventTime, kline))
                                self.klineStreamsBuffer_processing = False
                    else: print(termcolor.colored("[{:s}] Unexpected Stream Message Detected from Stream '{:s}'\n * {:s}".format(self.rtaCode, streamName, streamContents), 'light_red'))
                #Stream may return 'Queue overflow. Message not filled' error, not anymore sending any stream data. In this case, restart all of the existing connections
                elif (streamContents['e'] == 'error'):
                    if (streamContents['m'] == 'Queue overflow. Message not filled'):
                        if (self.klineStreams_restart == False):
                            print(termcolor.colored("[{:s}] Queue Overflow Occurred, all of the connections will soon restart!".format(self.rtaCode), 'light_yellow'))
                            self.klineStreams_restart = True
                            self.ipcA.sendFAR(functionID = 'GETWEBSOCKETCONNECTIONPERMISSION', functionParams = {'rtaCode': self.rtaCode}, nMaxDispatch = 'INF') #If no TWM exists, send a connection creation permission request to ATM
                            self.socketConnectionPermissionRequestSent = True
                else: print(termcolor.colored("[{:s}] Unexpected content received from WebSocket streams\n * {:s}".format(self.rtaCode, str(streamContents)), 'light_red'))
        except Exception as e: print(termcolor.colored("[{:s}] An error occurred while attempting to read Kline stream data\n * streamContents: {:s}\n Error Msg:".format(self.rtaCode, str(streamContents)), 'light_red'), termcolor.colored(e, 'light_red'))



    #Process any received Kline Stream Data from the buffer
    def __processKlineStreams(self):
        while ((0 < len(self.klineStreamsBuffer)) and (self.serverConnected == True)):
            """
            streamToProcess:
                [0]: apiSymbol
                [1]: eventTime
                [2]: kline
            """
            self.klineStreamsBuffer_processing = True
            streamToProcess = self.klineStreamsBuffer.pop(0)
            self.klineStreamsBuffer_processing = False
            self.assets[streamToProcess[0]].klineStreamHandler(eventTime = streamToProcess[1], kline = streamToProcess[2])



    #<Server Connection Related>
    def __on_ServerConnection(self):
        time.sleep(5)
        #If this is a first server connection since the prgram start, initialize the client and TWM
        if (self.binanceClient == None): self.binanceClient = binance.Client();
        if (self.binanceTWM == None):    self.binanceTWM    = binance.ThreadedWebsocketManager(); self.binanceTWM.start()

        #Reset connections
        for connectionIndex in range (len(self.binanceTWM_Conns)): 
            try: self.binanceTWM.stop_socket(self.binanceTWM_Conns[connectionIndex]['connectionName'])
            except Exception as e: print(termcolor.colored("[{:s}] WebSocket Connection {:d} Stop Failed\n *".format(self.rtaCode, connectionIndex), 'red'), termcolor.colored(e, 'red'))
        self.binanceTWM_Conns.clear()

        self.serverConnected = True
        self.ipcA.sendPRDEDIT("SERVERCONNECTION", self.serverConnected, nMaxDispatch = 'INF')

    def __on_ServerDisconnection(self):
        #Reset Stream Buffer
        while (self.klineStreamsBuffer_processing == True): pass
        self.klineStreamsBuffer_processing = True
        self.klineStreamsBuffer.clear()
        self.klineStreamsBuffer_processing = False

        #Clear Asset Data
        self.assets.clear()
        self.clientSymbolToAPISymbol.clear()

        #Clear now-unprocessable symbol subscription list
        self.wsSymbolSubscriptionList = None

        #Update process pespective of serverconnection via IPC
        self.ipcA.sendPRDEDIT("SERVERCONNECTION", self.serverConnected, nMaxDispatch = 'INF')


        
    #<DB Connection Related>
    def __on_DBConnection(self):
        self.ipcA.sendPRDEDIT("DBCONNECTION", self.dbConnected, nMaxDispatch = 'INF')
        self.ipcA.sendPRDEDIT("DBDIR",        self.dbDir,       nMaxDispatch = 'INF')



    def __on_DBDisconnection(self):
        self.dbDir = None

        for apiSymbol in self.assets: self.assets[apiSymbol].on_DBDisconnection()

        self.ipcA.sendPRDEDIT("DBCONNECTION", self.dbConnected, nMaxDispatch = 'INF')
        self.ipcA.sendPRDEDIT("DBDIR",        self.dbDir,       nMaxDispatch = 'INF')
    #Manager Internal Functions END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




    #FAR Hanlder Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Process Termination
    def far_RaiseTerminationFlag(self, functionParams): self.process_terminate = True



    #<Server Connection Related>
    #---Server Connection Handler
    def farHandler_OnServerConnection(self, functionParams):
        self.eventHandlerPending = "SERVERCONNECTION"
        
    #---Server Disconnection Handler
    def farHandler_OnServerDisconnection(self, functionParams):
        self.serverConnected = False
        self.eventHandlerPending = "SERVERDISCONNECTION"

    #<Database Connection Related>
    #---Database Connection Handler
    def farHandler_OnDBConnection(self, functionParams):
        self.dbConnected = True
        self.dbDir = functionParams['dbDir']
        self.eventHandlerPending = "DBCONNECTION"

    #---Database Disconnection Handler
    def farHandler_OnDBDisconnection(self, functionParams):
        self.dbConnected = False
        self.eventHandlerPending = "DBDISCONNECTION"





    #<WebSocket Connection Related>
    #---Receive WebSocket Connection Permission
    def farHandler_WebSocketConnectionPermissionGiven(self, functionParams):
        if (self.socketConnectionPermissionRequestSent == True):
            self.socketConnectionPermissionRequestSent = False
            self.socketConnectionPermission = functionParams['permissionGiven']



    #---Set the current RTA's WebSocket Symbol Subscription List
    def farHandler_setWebSocketSymbolSubscriptionList(self, functionParams):
        self.wsSymbolSubscriptionList = functionParams['symbolsData']



    #<Asset Control Related>
    #---Upon Data Preparation Completion
    def farHandler_onDataPrepComplete(self, functionParams):
        #Function Parameter Localization
        apiSymbol = functionParams['apiSymbol']
        interval  = functionParams['interval']

        #Load asset data from the database
        klines = 0
        
        self.assets[apiSymbol].on_DataPrepComplete(interval)
    #FAR Hanlder Functions END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RTA_Asset:
    def __init__(self, rtaCode, ipcA, binanceClient, webSocketConnectionIndex, apiSymbol, clientSymbol, allocMode, mrktRegTS, precisions):
        #Identification & Communication
        self.rtaCode       = rtaCode
        self.ipcA          = ipcA
        self.binanceClient = binanceClient

        self.webSocketConnectionIndex = webSocketConnectionIndex

        self.apiSymbol    = apiSymbol
        self.clientSymbol = clientSymbol
        self.allocMode    = allocMode
        self.mrktRegTS    = mrktRegTS

        self.prec_Price    = precisions['prec_Price']
        self.prec_Quantity = precisions['prec_Quantity']
        self.prec_Quote    = precisions['prec_Quote']

        #Data IO Control
        self.klines                    = dict(); self.klines_3dInterval_1dBlocks = [None, None, None]
        self.klines_lastClosedTS       = dict()
        self.klines_lastStreamedTS     = dict()
        self.firstClosedKlineReceived  = dict()
        self.lastSentEventTimestmap_ms = dict()

        self.firstStreamSinceDBConnection = dict()
        self.dataPrepCompletionCheckList  = dict()

        for interval in STREAMINTERVALS:
            self.klines[interval]                    = dict() #Closed Only
            self.klines_lastClosedTS[interval]       = None
            self.klines_lastStreamedTS[interval]     = None
            self.firstClosedKlineReceived[interval]  = False
            self.lastSentEventTimestmap_ms[interval] = 0

            self.firstStreamSinceDBConnection[interval] = False
            self.dataPrepCompletionCheckList[interval]  = False
            
        self.dataPrepared = False
        self.analyzing    = False

        #System Status Tracker
        self.dbConnected = True #Initialization of 'RTA_Asset' Implies connection to both DB and Binance Server
        


    #<General Processings>
    #---Perform asset process routine
    def process(self, currentTime_ns):
        pass



    #---Handle a kline stream
    def klineStreamHandler(self, eventTime, kline):
        """
        {'t': 1709110800000,      #Kline Start Time
         'T': 1709110859999,      #Kline End Time
         'i': '1m',               #Interval
         'f': 4056297037364,      #First Trade ID
         'L': 4056302579111,      #Last Trade ID
         'o': '59503.70',         #Open Price
         'c': '59387.20',         #Close Price
         'h': '59525.20',         #High Price
         'l': '59374.60',         #Low Price
         'v': '1075.580',         #Base Asset Volume
         'n': 10540,              #Number of Trades
         'x': False,              #Is this Kline Closed?
         'q': '63946507.44380',   #Quote Asset Volume
         'V': '358.026',          #Taker Buy Base Asset Volume
         'Q': '21286705.93250',   #Taker Buy Quote Asset Volume
         'B': '0'}                #Ignore
        }
        ->
        (
        [0]:  Open  Timestamp_second,
        [1]:  Close Timestamp_second,
        [2]:  Open  Price,
        [3]:  High  Price,
        [4]:  Low   Price,
        [5]:  Close Price,
        [6]:  nTrades,
        [7]:  Base  Asset Volume,
        [8]:  Quote Asset Volume,
        [9]:  Taker Buy Base Asset Volume,
        [10]: Taker Buy Quote Asset Volume,
        [11]: Condition,
        )
        """
        
        closed   = kline['x']
        interval = kline['i']

        openTS  = int(kline['t']/1000)
        closeTS = int(kline['T']/1000)

        formattedKline = (openTS, closeTS,                              #[0]:  Open Timestamp_second, [1]: Close Timestamp_second
                          round(float(kline['o']), self.prec_Price),    #[2]:  Open Price
                          round(float(kline['h']), self.prec_Price),    #[3]:  High Price
                          round(float(kline['l']), self.prec_Price),    #[4]:  Low Price
                          round(float(kline['c']), self.prec_Price),    #[5]:  Close Price
                          kline['n'],                                   #[6]:  nTrades
                          round(float(kline['v']), self.prec_Quantity), #[7]:  Base Asset Volume
                          round(float(kline['q']), self.prec_Quote),    #[8]:  Quote Asset Volume
                          round(float(kline['V']), self.prec_Quantity), #[9]:  Taker Buy Base Asset Volume
                          round(float(kline['Q']), self.prec_Quote),    #[10]: Taker Buy Quote Asset Volume
                          20)                                           #[11]: Condition

        if (interval == '1d'): self.__3dIntervalUpdater(formattedKline, closed, eventTime)

        #If this is a first stream to send via IPC since DB connection, send FAR 'ONFIRSTKLINESTREAM' via IPC
        if (self.firstStreamSinceDBConnection[interval] == False):
            self.ipcA.sendFAR(functionID = 'ONFIRSTKLINESTREAMRECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': interval, 'timestamp': openTS}, nMaxDispatch = 'INF')
            self.firstStreamSinceDBConnection[interval] = True

        #Update the internal Kline Data
        self.klines[interval][openTS]        = formattedKline
        self.klines_lastStreamedTS[interval] = openTS

        if (closed == True): self.klines_lastClosedTS[interval] = openTS

        #Send the kline via IPC
        if (closed == True): self.ipcA.sendFAR(functionID = 'ONKLINERECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': interval, 'Kline': formattedKline, 'closed': closed}, nMaxDispatch = 'INF')
        else:                self.ipcA.sendFAR(functionID = 'ONKLINERECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': interval, 'Kline': formattedKline, 'closed': closed}, nMaxDispatch = 1)

        if ((interval == '1d') and (self.analyzing == True)): self.__performKlineAnalysis(interval, closed)
        


    #---Unique function for special handling of '3d' interval
    def __3dIntervalUpdater(self, formattedKline_1d, closed, eventTime):
        openTS_1d = formattedKline_1d[0]

        openTS_3d = int((openTS_1d-self.mrktRegTS[12])/259200)*259200+self.mrktRegTS[12]
        blockIndex = int((openTS_1d-openTS_3d)/86400) #blockIndex of the received 1d interval kline [0, 1, 2]

        if ((self.firstStreamSinceDBConnection['3d'] == False) and (self.klines_lastStreamedTS['3d'] == None)):
            if (blockIndex != 0):
                #If this not the first block of the 3d interval block, try to fetch the previous 1d klines from the server
                nTry = 0
                while (True):
                    try: nTry += 1; previousBlocks = self.binanceClient.futures_historical_klines(symbol = self.clientSymbol, interval = '1d', start_str = openTS_3d*1000, end_str = (openTS_3d+blockIndex*86400-1)*1000, limit = 2); break
                    except Exception as e:
                        if (nTry == INITIAL1DKLINEFETCH_MAXATTEMPT): print(termcolor.colored("[{:s}] An error occured while attempting to fetch '1d' interval klines for '3d' interval block generation setup of {:s}, attempt limit reached [{:d} / {:d}]\n * ".format(self.rtaCode, self.apiSymbol, nTry, INITIAL1DKLINEFETCH_MAXATTEMPT), 'red'), termcolor.colored(e, 'red')); return 0
                        else:                                        time.sleep(INITIAL1DKLINEFETCH_ATTEMPTINTERVAL)

                #Check the fetched klines
                if (len(previousBlocks) < blockIndex):
                    nMissing = blockIndex - len(previousBlocks)
                    for i in range (nMissing): previousBlocks.append((0, 0, 0, 0, float('inf'), 0, 0, 0, 0, 0, 0))
                    print(termcolor.colored("[{:s}] A klines length mismatch occured during the '3d' interval block generation setup of {:s} and was filled with empty klines\n * Expected: {:d}, Received: {:d}".format(self.rtaCode, self.apiSymbol, blockIndex, len(previousBlocks)), 'yellow'))
                
                #Reformat and store the fetched klines
                for index, previousBlock in enumerate(previousBlocks):
                    self.klines_3dInterval_1dBlocks[index] = (int(previousBlock[0]/1000), int(previousBlock[0]/1000), #[0]:  Open Timestamp_second, [1]: Close Timestamp_second
                                                              round(float(previousBlock[1]), self.prec_Price),        #[2]:  Open Price
                                                              round(float(previousBlock[2]), self.prec_Price),        #[3]:  High Price
                                                              round(float(previousBlock[3]), self.prec_Price),        #[4]:  Low Price
                                                              round(float(previousBlock[4]), self.prec_Price),        #[5]:  Close Price
                                                              previousBlock[8],                                       #[6]:  nTrades
                                                              round(float(previousBlock[5]),  self.prec_Quantity),    #[7]:  Base Asset Volume
                                                              round(float(previousBlock[7]),  self.prec_Quote),       #[8]:  Quote Asset Volume
                                                              round(float(previousBlock[9]),  self.prec_Quantity),    #[9]:  Taker Buy Base Asset Volume
                                                              round(float(previousBlock[10]), self.prec_Quote))       #[10]: Taker Buy Quote Asset Volume

            self.ipcA.sendFAR(functionID = 'ONFIRSTKLINESTREAMRECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': '3d', 'timestamp': openTS_3d}, nMaxDispatch = 'INF')
            self.firstStreamSinceDBConnection['3d'] = True

        #Update the internal Kline Data
        self.klines_3dInterval_1dBlocks[blockIndex] = formattedKline_1d[:11]
        self.klines_lastStreamedTS['3d'] = openTS_3d

        #---Construct the 3d interval kline block from the 1d interval klines
        highPrice = 0; lowPrice = float('inf')
        nTrades_Sum = 0; baVol_Sum = 0; qaVol_Sum = 0; tbbaVol_Sum = 0; tbqaVol_Sum = 0
        for targetIndex in range(0, blockIndex+1):
            if (highPrice < self.klines_3dInterval_1dBlocks[targetIndex][3]): highPrice = self.klines_3dInterval_1dBlocks[targetIndex][3]
            if (self.klines_3dInterval_1dBlocks[targetIndex][4] < lowPrice):  lowPrice  = self.klines_3dInterval_1dBlocks[targetIndex][4]
            nTrades_Sum += self.klines_3dInterval_1dBlocks[targetIndex][6]
            baVol_Sum   += self.klines_3dInterval_1dBlocks[targetIndex][7]
            qaVol_Sum   += self.klines_3dInterval_1dBlocks[targetIndex][8]
            tbbaVol_Sum += self.klines_3dInterval_1dBlocks[targetIndex][9]
            tbqaVol_Sum += self.klines_3dInterval_1dBlocks[targetIndex][10]

        formattedKline_3d = (openTS_3d, openTS_3d+259200-1,
                             self.klines_3dInterval_1dBlocks[0][2],
                             highPrice,
                             lowPrice,
                             self.klines_3dInterval_1dBlocks[blockIndex][5],
                             nTrades_Sum,
                             baVol_Sum,
                             qaVol_Sum,
                             tbbaVol_Sum,
                             tbqaVol_Sum)

        #---Update the internal Kline Data
        self.klines['3d'][openTS_3d] = formattedKline_3d
        if ((closed == True) and (blockIndex == 2)): self.klines_lastClosedTS['3d'] = openTS_3d

        #Send the kline via IPC
        if (closed == True): self.ipcA.sendFAR(functionID = 'ONKLINERECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': '3d', 'Kline': formattedKline_3d, 'closed': closed}, nMaxDispatch = 'INF')
        else:                self.ipcA.sendFAR(functionID = 'ONKLINERECEIVAL', functionParams = {'apiSymbol': self.apiSymbol, 'interval': '3d', 'Kline': formattedKline_3d, 'closed': closed}, nMaxDispatch = 1)





    #<DB & Server Conneciton/Disconnection Handlers>
    #---Database Connection Handler
    def on_DBConnection(self):
        for interval in STREAMINTERVALS: self.firstStreamSinceDBConnection[interval] = False
        



    #---Database Disconnection Handler
    def on_DBDisconnection(self):
        pass



    def on_StreamReconnection(self):
        for interval in STREAMINTERVALS: self.firstStreamSinceDBConnection[interval] = False


    #<Asset Analysis Related>
    #Data Preparation Completion Handler
    def on_DataPrepComplete(self, interval):
        self.dataPrepCompletionCheckList[interval] = True

        #Check if klines of all intervals are prepared
        nPrepared = False
        for dataPrepCompletion in self.dataPrepCompletionCheckList:
            if (dataPrepCompletion == True): nPrepared += 1

        #If all of the raw klines are prepared, start analysis preparation
        if (nPrepared == len(self.dataPrepCompletionCheckList)):
            self.dataPrepared = True
            if (self.allocMode == 'SA'):
                self.analyzing = True
                self.ipcA.sendFAR(functionID = 'ONANALYSISBEGIN', functionParams = {'apiSymbol': self.apiSymbol})


                
    #Perform Analysis on the new kline
    def __performKlineAnalysis(self, updatedInterval, updateKlineClosed):
        pass
