import ATM_Zeta_Auxillaries

import time
import os
import pprint
import win32api
import shutil
import termcolor
import sqlite3
from datetime import datetime, timedelta, timezone

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

KLINE_INTERVAL_ID_1m  = 0
KLINE_INTERVAL_ID_3m  = 1
KLINE_INTERVAL_ID_5m  = 2
KLINE_INTERVAL_ID_15m = 3
KLINE_INTERVAL_ID_30m = 4
KLINE_INTERVAL_ID_1h  = 5
KLINE_INTERVAL_ID_2h  = 6
KLINE_INTERVAL_ID_4h  = 7
KLINE_INTERVAL_ID_6h  = 8
KLINE_INTERVAL_ID_8h  = 9
KLINE_INTERVAL_ID_12h = 10
KLINE_INTERVAL_ID_1d  = 11
KLINE_INTERVAL_ID_3d  = 12
KLINE_INTERVAL_ID_1W  = 13
KLINE_INTERVAL_ID_1M  = 14
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
                       KLINE_INTERVAL_ID_1W:  604800}

class manager_DataManagement:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, centralManager, ipcA):
        #Creating local instances of passed parameters
        self.centralManager = centralManager
        self.ipcA = ipcA

        #Manager Process Control Variables
        self.eventHandlerPending = None
        
        #Initialize Database Control Variables
        self.db_Status = {'connected': False, 'lastConnectionCheckTime': 0, 'driveDir': None, 'DBDir_klines': None, 'DBDir_analysis': None, 'DBDir_user': None,
                          'volume': {'total': None, 'used': None, 'free': None}, 'volume_classification': {'klines_class': None,   'klinesSaveAvailable': False,   'klines_allocated': None,   'klines_used': None, 
                                                                                                           'analysis_class': None, 'analysisSaveAvailable': False, 'analysis_allocated': None, 'analysis_used': None, 
                                                                                                           'user_class': None,     'userSaveAvailable': False,     'user_allocated': None,     'user_used': None},
                          'dbConnection_klines': None, 'dbConnection_analysis': None,
                          'dbCursor_klines':     None, 'dbCursor_analysis':     None,
                          'dbCursor_user':       None, 'dbCursor_user':         None}
        
        self.db_Contents = {'user':     dict(),
                            'analysis': dict(), 'analysisTables': list(),
                            'coinID':   dict()}
        self.existingCoinIDIndexes = list()

        #Initialization Completion Message
        print(termcolor.colored("Data Management", 'blue'), termcolor.colored("Manager Initialization Complete! ----------------------------------------------------------------------------------------", 'green'), termcolor.colored("\n>", 'dark_grey'))
    def postInitialization(self, fModifier, m_AutoTrader, m_BinanceAPI):
        self.fModifier = fModifier; self.m_AutoTrader = m_AutoTrader; self.m_BinanceAPI = m_BinanceAPI
        self.functionRepeaters = dict()
        
        prdAnnouncementForm_dbStatus = {'connected':               self.db_Status['connected'],
                                        'lastConnectionCheckTime': self.db_Status['lastConnectionCheckTime'],
                                        'driveDir':                self.db_Status['driveDir'],
                                        'DBDir_klines':            self.db_Status['DBDir_klines'],
                                        'DBDir_analysis':          self.db_Status['DBDir_analysis'],
                                        'volume':                  self.db_Status['volume'],
                                        'volume_classification':   self.db_Status['volume_classification']}
        
        self.ipcA['MAIN'].sendPRDEDIT("DBSTATUS", prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("DBSTATUS",  prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("ANALYSISSUMMARIES", self.db_Contents['analysis'], nMaxDispatch = 'INF')

        self.functionRepeaters['DBCONNECTIONCHECK'] = self.fModifier.addFixedRepeatedFunction(self.checkDBConnection, interval = 100, startUponInit = False)
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Process Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self):
        if (self.eventHandlerPending == None):
            pass
        else:
            if   (self.eventHandlerPending == 'DBCONNECTION'):    self.__on_DBConnection()
            elif (self.eventHandlerPending == 'DBDISCONNECTION'): self.__on_DBDisconnection()
            self.eventHandlerPending = None

    def terminate(self):
        pass
    #Process Functions END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Inter-Manager Call Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #<DB Status Related>
    #---Check Database Connection
    def checkDBConnection(self):
        lastConnectionStatus = self.db_Status['connected']
        currentTime = time.time()

        if (lastConnectionStatus == True):
            #Case: Connected -> Connected
            if ((os.path.exists(self.db_Status['DBDir_klines']) == True) and (os.path.exists(self.db_Status['DBDir_analysis']) == True) and (os.path.exists(self.db_Status['DBDir_user']) == True)):
                #Local Tracker Update
                self.db_Status['volume'] = self.__getDBVolume(); self.__classifyDBVolume()
                self.db_Status['lastConnectionCheckTime'] = currentTime

                #PRD Update
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'lastConnectionCheckTime'), self.db_Status['lastConnectionCheckTime'], nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'lastConnectionCheckTime'), self.db_Status['lastConnectionCheckTime'], nMaxDispatch = 'INF')

            #Case: Connected -> Disconnected
            else:
                #Local Tracker Update
                self.db_Status = {'connected': False, 'lastConnectionCheckTime': 0, 'driveDir': None, 'DBDir_klines': None, 'DBDir_analysis': None, 'DBDir_user': None,
                                  'volume': {'total': None, 'used': None, 'free': None}, 'volume_classification': {'klines_class': None,   'klinesSaveAvailable': False,   'klines_allocated': None,   'klines_used': None, 
                                                                                                                   'analysis_class': None, 'analysisSaveAvailable': False, 'analysis_allocated': None, 'analysis_used': None, 
                                                                                                                   'user_class': None,     'userSaveAvailable': False,     'user_allocated': None,     'user_used': None},
                                  'dbConnection_klines': None, 'dbConnection_analysis': None,
                                  'dbCursor_klines':     None, 'dbCursor_analysis':     None,
                                  'dbCursor_user':       None, 'dbCursor_user':         None}
                
                #PRD Update
                prdAnnouncementForm_dbStatus = {'connected':               self.db_Status['connected'],
                                                'lastConnectionCheckTime': self.db_Status['lastConnectionCheckTime'],
                                                'driveDir':                self.db_Status['driveDir'],
                                                'DBDir_klines':            self.db_Status['DBDir_klines'],
                                                'DBDir_analysis':          self.db_Status['DBDir_analysis'],
                                                'volume':                  self.db_Status['volume'],
                                                'volume_classification':   self.db_Status['volume_classification']}
                self.ipcA['MAIN'].sendPRDEDIT("DBSTATUS", prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT("DBSTATUS",  prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')

                #Event Handler Update
                self.eventHandlerPending = 'DBDISCONNECTION'
        else:
            result, driveName = self.__searchDBDrive()
            #Case: Disconnected -> Connected
            if (result == True):
                #Local Tracker Update
                self.db_Status['driveDir'] = driveName
                self.db_Status['DBDir_klines']   = os.path.join(driveName, 'ATM_ZETA_DB_klines.db')
                self.db_Status['DBDir_analysis'] = os.path.join(driveName, 'ATM_ZETA_DB_analysis.db')
                self.db_Status['DBDir_user']     = os.path.join(driveName, 'ATM_ZETA_DB_user.db')
                self.db_Status['lastConnectionCheckTime'] = currentTime

                #Event Handler Update
                self.eventHandlerPending = 'DBCONNECTION'
    
    #---Return if DB is available
    def isDBAvailable(self): return self.db_Status['connected']

    #---Return if Kline Data Save is available
    def isKlinesSaveAvailable(self): return self.db_Status['volume_classification']['klinesSaveAvailable']

    #---Return if Analysis Data Save is available
    def isAnalysisSaveAvailable(self): return self.db_Status['volume_classification']['analysisSaveAvailable']

    #---Return DB Directory
    def get_DBDir(self, dbType): 
        if   (dbType == 'klines'):   return self.db_Status['DBDir_klines']
        elif (dbType == 'analysis'): return self.db_Status['DBDir_analysis']
        elif (dbType == 'user'):     return self.db_Status['DBDir_user']

    #---Return DB Drive Directory
    def get_DriveDir(self): return self.db_Status['driveDir']










    #<Asset ID Related>
    #---Return whether the specified asset data exists in the connected DB or not
    def exists_asset(self, apiSymbol): return (apiSymbol in self.db_Contents['coinID'])



    #---Register the specified asset to the connected DB
    def register_asset(self, apiSymbol, mrktRegTSs):
        if (self.db_Status['connected'] == True):
            if (apiSymbol in self.db_Contents['coinID']): return self.db_Contents['coinID'][apiSymbol]['coinIDIndex']
            else:
                try:
                    #Find coinIDIndex that is not already issued
                    coinIDIndex = 0
                    while (coinIDIndex in self.existingCoinIDIndexes): coinIDIndex += 1
                    #Setup local and .db data for the new asset
                    self.db_Contents['coinID'][apiSymbol] = {'coinIDIndex': coinIDIndex, 'mrktRegTS': mrktRegTSs}
                    for intervalID in KLINE_INTERVAL_IDs: self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)] = list()
                    self.db_Status['dbCursor_klines'].execute("INSERT INTO coinID (id, coinName, mrktRegTS_0,mrktRegTS_1,mrktRegTS_2,mrktRegTS_3,mrktRegTS_4,mrktRegTS_5,mrktRegTS_6,mrktRegTS_7,mrktRegTS_8,mrktRegTS_9,mrktRegTS_10,mrktRegTS_11,mrktRegTS_12,mrktRegTS_13,mrktRegTS_14) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                                                              (coinIDIndex, apiSymbol, mrktRegTSs[0],mrktRegTSs[1],mrktRegTSs[2],mrktRegTSs[3],mrktRegTSs[4],mrktRegTSs[5],mrktRegTSs[6],mrktRegTSs[7],mrktRegTSs[8],mrktRegTSs[9],mrktRegTSs[10],mrktRegTSs[11],mrktRegTSs[12],mrktRegTSs[13],mrktRegTSs[14]))
                    self.db_Status['dbConnection_klines'].commit()
                    self.existingCoinIDIndexes.append(coinIDIndex)
                    return coinIDIndex
                except Exception as e: print(termcolor.colored("An unexpected error occurred during DB asset registration\n *", 'light_red'), termcolor.colored(e, 'light_red')); return None
        else: print(termcolor.colored("Asset registration for {:s} rejected: DB Not Connected".format(apiSymbol), 'light_red')); return None



    #---Return coinIDIndex of the specified asset
    def get_coinIDIndex(self, apiSymbol):
        if (apiSymbol in self.db_Contents['coinID']): return self.db_Contents['coinID'][apiSymbol]['coinIDIndex']
        else:                                         return None



    #---Return mrktRegTS of the specified asset and intervalID. If intervalID is not specified, return mrktRegTS for all intervasIDs
    def get_mrktRegistrationTS(self, apiSymbol, intervalID = None):
        if (apiSymbol in self.db_Contents['coinID']):
            if (intervalID == None): return self.db_Contents['coinID'][apiSymbol]['mrktRegTS']
            else:                    return self.db_Contents['coinID'][apiSymbol]['mrktRegTS'][intervalID]
        else:                        return None



    #---Save mrktRegTS for the specified asset and intervalID
    def save_mrktRegistrationTS(self, apiSymbol, intervalID, mrktRegTS):
        if (self.db_Status['connected'] == True):
            if (apiSymbol in self.db_Contents['coinID']):
                try:
                    self.db_Contents['coinID'][apiSymbol]['mrktRegTS'][intervalID] = mrktRegTS
                    self.db_Status['dbCursor_klines'].execute("UPDATE coinID SET mrktRegTS_{:d} = ? WHERE id = ?".format(intervalID), (mrktRegTS, self.db_Contents['coinID'][apiSymbol]['coinIDIndex']))
                    self.db_Status['dbConnection_klines'].commit()
                    return True
                except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to save MrktRegTS for {:s}_{:d}\n *".format(apiSymbol, intervalID), 'light_red'), termcolor.colored(e, 'light_red')); return False
            else: print(termcolor.colored("MrktRegTS save for {:s}_{:d} failed: apiSymbol not registered".format(apiSymbol, intervalID), 'light_red')); return False
        else: print(termcolor.colored("MrktRegTS save for {:s}_{:d} rejected: DB Not Connected".format(apiSymbol, intervalID), 'light_red')); return False
    









    #<Klines Management Related>
    #---Return Klines Data Availability of the specified asset and intervalID
    def get_DataAvailability(self, apiSymbol, intervalID):
        if ((apiSymbol in self.db_Contents['coinID']) and (intervalID in KLINE_INTERVAL_IDs)): 
            klineRanges = self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)]
            returnList = list()
            for klineRange in klineRanges: returnList.append(klineRange.copy())
            return returnList
        else: return None #No data exists for the corresponding apiSymbol and intervalID



    #---Return klines from the database, return None if no valid apiSymbol or ranges are passed
    def get_klines(self, apiSymbol, intervalID, rangeBeg, rangeEnd):
        try:
            if (apiSymbol in self.db_Contents['coinID']):
                coinIDIndexCode = self.db_Contents['coinID'][apiSymbol]['coinIDIndex']*1e12
                intervalIDCode  = intervalID*1e10
                #Confirm the ranges are within the limit
                if ((0 <= rangeBeg) and (rangeBeg <= 9999999999) and (0 <= rangeEnd) and (rangeEnd <= 9999999999) and (rangeBeg <= rangeEnd)):
                    #Read the klines from the database and return
                    self.db_Status['dbCursor_klines'].execute('SELECT * FROM klines WHERE ? <= id AND id <= ?', (coinIDIndexCode + intervalIDCode + rangeBeg, coinIDIndexCode + intervalIDCode + rangeEnd))
                    return self.db_Status['dbCursor_klines'].fetchall()
                else: return None
            else: return None
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to fetch klines from the database \n *", 'red'), termcolor.colored(e, 'red'))



    #---Save klines for the corresponding apiSymbol and intervalID
    def save_klineData(self, apiSymbol, intervalID, klines):
        try:
            if (self.db_Status['connected'] == True):
                if (self.db_Status['volume_classification']['klines_class'] != 3):
                    #Calculate and save the new klines data range
                    coinIDIndex = self.get_coinIDIndex(apiSymbol)
                    fetchedKlines_filtered_firstTS_OPEN = int(klines[0][0]-coinIDIndex*1e12-intervalID*1e10) #Open  timestamp of the first kline
                    fetchedKlines_filtered_lastTS_CLOSE = klines[-1][1]                                      #Close timestamp of the last  kline 

                    currentKlineRanges = self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)].copy()

                    #If no previous kline ranges exist, simply add the current range
                    if (len(currentKlineRanges) == 0): 
                        currentKlineRanges = [[fetchedKlines_filtered_firstTS_OPEN, fetchedKlines_filtered_lastTS_CLOSE]]

                    #If there exists any previous kline ranges, merge with them if possible, or insert at an appropriate position (It is assumed that no klines data overlap exists)
                    else:
                        #Find the position at which the the left edge of the fetched kline data range is greater than the right edge of the previous kline data range
                        insertionPosition = 0
                        overlapDetected = False
                        for index, currentKlineRange in enumerate(currentKlineRanges):
                            if (currentKlineRange[0] < fetchedKlines_filtered_firstTS_OPEN):
                                if (currentKlineRange[1] < fetchedKlines_filtered_firstTS_OPEN): insertionPosition += 1
                                else: overlapDetected = True; break;
                            else:
                                if (fetchedKlines_filtered_lastTS_CLOSE < currentKlineRange[0]): break;
                                else: overlapDetected = True; break;

                        #If Data Range Overlap is detected
                        if (overlapDetected == True):
                            print(termcolor.colored("Data Range Overlap detected while attempting to save fetched klines data for {:s}_{:d}\n * firstStreamedKlineTS: {:d}\n * Insertion Position: {:d}\n * Fetched Range: [{:d}~{:d}]\n * Overlapped Previous Range: [{:d}~{:d}]".format(apiSymbol, intervalID, 
                                                                                                                                                                                                                                                                                          self.m_BinanceAPI.get_firstStreamedKlineTS(apiSymbol, intervalID),
                                                                                                                                                                                                                                                                                          insertionPosition,
                                                                                                                                                                                                                                                                                          fetchedKlines_filtered_firstTS_OPEN, 
                                                                                                                                                                                                                                                                                          fetchedKlines_filtered_lastTS_CLOSE,
                                                                                                                                                                                                                                                                                          currentKlineRange[0], 
                                                                                                                                                                                                                                                                                          currentKlineRange[1]), 
                                                    'light_red'))
                            for index, currentKlineRange in enumerate(currentKlineRanges): print(termcolor.colored(" - Previous Data Range {:d}: [{:d}~{:d}]".format(index+1, currentKlineRange[0], currentKlineRange[1]), 'light_red'))
                            self.performKlineDeepRangeCheck(apiSymbol, intervalID, recalculateDownloadRanges = True)
                            return False

                        #Identify Mergible Adjacent Data Ranges
                        mergeL = False; mergeR = False
                        if (0 < insertionPosition):
                            if (currentKlineRanges[insertionPosition-1][1]+1 == fetchedKlines_filtered_firstTS_OPEN): mergeL = True
                        if (insertionPosition < len(currentKlineRanges)):
                            if (fetchedKlines_filtered_lastTS_CLOSE+1 == currentKlineRanges[insertionPosition][0]): mergeR = True

                        #Perform Data Ranges Merging
                        if (mergeL == True):
                            if (mergeR == True): #Merge with both sides
                                currentKlineRanges[insertionPosition-1] = [currentKlineRanges[insertionPosition-1][0], currentKlineRanges[insertionPosition][1]]
                                currentKlineRanges.pop(insertionPosition)
                            else: #Merge with left side only
                                currentKlineRanges[insertionPosition-1] = [currentKlineRanges[insertionPosition-1][0], fetchedKlines_filtered_lastTS_CLOSE] 
                        else:
                            if (mergeR == True): #Merge with right side only
                                currentKlineRanges[insertionPosition] = [fetchedKlines_filtered_firstTS_OPEN, currentKlineRanges[insertionPosition][1]]  
                            else: #Merge with none
                                currentKlineRanges.insert(insertionPosition, [fetchedKlines_filtered_firstTS_OPEN, fetchedKlines_filtered_lastTS_CLOSE])


                    #Save klines data to the .db file
                    self.db_Status['dbCursor_klines'].executemany("INSERT INTO klines (id, closeTS, p_open, p_high, p_low, p_close, nTrades, v, q, v_tb, q_tb, c) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",klines)

                    #Save update ranges data to the .db file
                    rangesInString = ""
                    for index, klineRange in enumerate(currentKlineRanges):
                        if (index < len(currentKlineRanges)-1): rangesInString += "{:d}_{:d}\n".format(klineRange[0], klineRange[1])
                        else:                                   rangesInString += "{:d}_{:d}".format(klineRange[0], klineRange[1])
                    self.db_Status['dbCursor_klines'].execute("UPDATE coinID SET klineRanges_{:d} = ? WHERE id = ?".format(intervalID), (rangesInString, coinIDIndex))

                    #Apply the changes to the .db file
                    self.db_Status['dbConnection_klines'].commit()

                    #Apply the changes to the current klines ranges after the successful .db commit
                    self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)] = currentKlineRanges
                    self.m_BinanceAPI.set_DataAvailability(apiSymbol, intervalID, currentKlineRanges)

                    #Return 'True' to indicate a successful data save
                    return True
                else: print(termcolor.colored("Fetched klines save request rejected: Available Volume Limit Reached", 'light_red')); return False
            else: print(termcolor.colored("Fetched klines save request rejected: DB Not Connected", 'light_red')); return False
        except Exception as e: 
            print(termcolor.colored("An unexpected error occured while attempting to save fetched klines data for {:s}_{:d}:".format(apiSymbol, intervalID), 'light_red'), termcolor.colored(e, 'light_red'));
            self.performKlineDeepRangeCheck(apiSymbol, intervalID, recalculateDownloadRanges = True)
            return False


    
    #---Save streamed klines for the corresponding apiSymbols and intervalIDs
    def save_klineStreamData(self, klines, klineRanges, existingTargets):
        if (self.db_Status['connected'] == True):
            if (self.db_Status['volume_classification']['klines_class'] != 3):
                try:
                    currentKlineRanges_All = dict()
                    for target in existingTargets:
                        apiSymbol = target[0]; intervalID = target[1]
                        #Edit the local instance of the kline ranges for the corresponding apiSymbol and indexID
                        streamedKlinesRanges = klineRanges[apiSymbol][intervalID]
                        currentKlineRanges = self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)].copy()
                        
                        #Overlap Detection & 
                        for streamedKlinesRange in streamedKlinesRanges:
                            if (len(currentKlineRanges) == 0): currentKlineRanges = [[streamedKlinesRange[0], streamedKlinesRange[1]]]                                      #[0]: No previously existing Data Availability
                            else:
                                if    (currentKlineRanges[-1][1]+1 == streamedKlinesRange[0]): currentKlineRanges[-1] = [currentKlineRanges[-1][0], streamedKlinesRange[1]] #[1]: Mergible existing Data Availability
                                else:                                                          currentKlineRanges.append([streamedKlinesRange[0], streamedKlinesRange[1]])  #[2]: Non-mergible existing Data Availability

                        #Generate string version of the current ranges for the corresponding apiSymbol and indexID
                        rangesInString = ""
                        for index, klineRange in enumerate(currentKlineRanges):
                            if (index < len(currentKlineRanges)-1): rangesInString += "{:d}_{:d}\n".format(klineRange[0], klineRange[1])
                            else:                                   rangesInString += "{:d}_{:d}".format(klineRange[0], klineRange[1])
                        self.db_Status['dbCursor_klines'].execute("UPDATE coinID SET klineRanges_{:d} = ? WHERE id = ?".format(intervalID), (rangesInString, self.get_coinIDIndex(apiSymbol)))
                    
                        if (apiSymbol in currentKlineRanges_All): currentKlineRanges_All[apiSymbol][intervalID] = currentKlineRanges
                        else:                                     currentKlineRanges_All[apiSymbol]             = {intervalID: currentKlineRanges}

                    #Save klines data to the .db file
                    self.db_Status['dbCursor_klines'].executemany("INSERT INTO klines (id, closeTS, p_open, p_high, p_low, p_close, nTrades, v, q, v_tb, q_tb, c) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",klines)

                    #Apply the changes to the .db file
                    self.db_Status['dbConnection_klines'].commit()
        
                    #Edit memory storage of the kline ranges
                    for apiSymbol in currentKlineRanges_All:
                        for intervalID in currentKlineRanges_All[apiSymbol]: 
                            self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)] = currentKlineRanges_All[apiSymbol][intervalID]
                            self.m_BinanceAPI.set_DataAvailability(apiSymbol, intervalID, currentKlineRanges_All[apiSymbol][intervalID])

                    #If the save process was performed with no error, return True to indicate successful processing
                    return True
                except Exception as e: 
                    print(termcolor.colored("An unexpected error occurred while attempting to save streamed klines\n *", 'red'), termcolor.colored(e, 'red'))
                    errorMsg_str = str(e)
                    if (errorMsg_str == "UNIQUE constraint failed: klines.id"): self.performKlineDeepRangeCheck(apiSymbol, intervalID, recalculateDownloadRanges = True)
                    return False
            else: print(termcolor.colored("Fetched klines save request rejected: Available Volume Limit Reached", 'light_red')); return False
        else: print(termcolor.colored("Streamed klines save request rejected: DB Not Connected", 'light_red')); return False



    #---Check Klines Data Range by Reading the actual klines and edit the range, this process may take even more than a minute, only perform when data overlap is detected
    def performKlineDeepRangeCheck(self, apiSymbol, intervalID, recalculateDownloadRanges = True):
        try:
            if (apiSymbol in self.db_Contents['coinID']):
                print(termcolor.colored("### Performing Klines Deep Range Check for {:s}_{:d}... ###".format(apiSymbol, intervalID), 'cyan'))

                coinIDIndexCode = self.db_Contents['coinID'][apiSymbol]['coinIDIndex']*1e12
                intervalIDCode  = intervalID*1e10

                print(termcolor.colored(" <Previous Data Ranges>", 'light_cyan'))
                for previousDataRange in self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)]: print(termcolor.colored("  * {:s}".format(str(previousDataRange)), 'light_cyan'))

                #Read the klines from the database
                print(termcolor.colored("### <Klines Deep Range Check - Executing SQL Command> ###", 'cyan'))
                self.db_Status['dbCursor_klines'].execute('SELECT * FROM klines WHERE ? <= id AND id <= ?', (coinIDIndexCode + intervalIDCode, coinIDIndexCode + intervalIDCode + 9999999999))
                print(termcolor.colored("### <Klines Deep Range Check - Fetching Data> ###", 'cyan'))
                klines_read = self.db_Status['dbCursor_klines'].fetchall()
            
                #Analyze the data ranges
                dataRanges = []
                print(termcolor.colored("### <Klines Deep Range Check - Analyzing Contents> ###", 'cyan'))
                for kline in klines_read:
                    ts_beg = int(kline[0]-coinIDIndexCode-intervalIDCode)
                    ts_end = int(kline[1])
                    if (len(dataRanges) == 0): dataRanges.append([ts_beg, ts_end])
                    else:
                        if (dataRanges[-1][1]+1 == ts_beg): dataRanges[-1][1] = ts_end
                        else:                               dataRanges.append([ts_beg, ts_end])

                #Create a string representation of the data ranges
                rangesInString = ""
                for index, dataRange in enumerate(dataRanges):
                    if (index < len(dataRanges)-1): rangesInString += "{:d}_{:d}\n".format(dataRange[0], dataRange[1])
                    else:                           rangesInString += "{:d}_{:d}".format(dataRange[0], dataRange[1])

                #Update the data range in 'coinID' table and commit
                print(termcolor.colored("### <Klines Deep Range Check - Saving New Data Ranges> ###", 'cyan'))
                self.db_Status['dbCursor_klines'].execute("UPDATE coinID SET klineRanges_{:d} = ? WHERE id = ?".format(intervalID), (rangesInString, coinIDIndexCode))
                self.db_Status['dbConnection_klines'].commit()

                self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)] = dataRanges
                if (recalculateDownloadRanges == True): self.m_BinanceAPI.recalculateDownloadRanges(apiSymbol, intervalID)
            
                print(termcolor.colored(" <New Data Ranges>", 'light_cyan'))
                for newDataRange in self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)]: print(termcolor.colored("  * {:s}".format(str(newDataRange)), 'light_cyan'))

                print(termcolor.colored("### Klines Deep Range Check Complete! ###", 'cyan'))
                return True
            else: return False
        except Exception as e: print(termcolor.colored("Unexpected error occurred during klines deep range check\n *", 'red'), termcolor.colored(e, 'red')); return False

    #---Add a Kline Deep Range Check Request Queue
    def requestKlineDeepRangeCheck(self, functionParams):
        try:
            apiSymbol                 = functionParams['apiSymbol']
            intervalID                = functionParams['intervalID']
            recalculateDownloadRanges = functionParams['recalculateDownloadRanges']
            return self.performKlineDeepRangeCheck(apiSymbol, intervalID, recalculateDownloadRanges)
        except Exception as e: print(termcolor.colored("Kline Deep Range Check Queue Appending Failed\n *", 'light_red'), termcolor.colored(e, 'light_red')); return False









    #<Analysis Management Related>
    def saveAnalysisResult(self, functionParams):
        #Create local instances of the function params
        try:
            saveRequestType = functionParams['saveRequestType']
            if (saveRequestType == 'summary'):
                result = functionParams['result']
                analysisType      = result['analysisType']
                analysisCode      = result['simulationCode']
                apiSymbol         = result['apiSymbol']
                simulationRangeBEG = result['simulationRangeBEG']
                simulationRangeEND = result['simulationRangeEND']
                simulatedRangeBEG  = result['simulatedRangeBEG']
                simulatedRangeEND  = result['simulatedRangeEND']
                resultType        = result['resultType']
                resultSummary_str = result['resultSummary_str']
                returnRecords = functionParams['returnRecords']
            elif (saveRequestType == 'analyzedKlines'):
                analysisCode            = functionParams['simulationCode']
                analyzedKlines          = functionParams['analyzedKlines']
                analyzedKlines_contents = functionParams['analyzedKlines_contents']
                blockIndex              = functionParams['blockIndex']
                isLastBlock             = functionParams['isLastBlock']
        except Exception as e:
            print(termcolor.colored("Analysis result save failed: check function parameters \n*", 'light_red'), termcolor.colored(e, 'light_red'))
            return {'saveResult': False, 'requestType': None, 'blockIndex': None}

        try:
            #Save 'summary' type analysis result
            if (saveRequestType == 'summary'):
                #Find lowest available analysisIndex
                targetAnalysisIndex = 0
                while (True):
                    doesNotExist = True
                    for existingAnalysisCode in self.db_Contents['analysis']:
                        if (targetAnalysisIndex == self.db_Contents['analysis'][existingAnalysisCode]['analysisIndex']): doesNotExist = False; break
                    if (doesNotExist == True): break
                    else: targetAnalysisIndex += 1
                analysisIndex = targetAnalysisIndex

                #Generate dbTableName
                if (resultType == "COMPLETE"): 
                    dbTableName = "arTable_{:s}".format(analysisCode.replace("/","").replace(":",""))
                    resultSaveComplete = 0
                else:                          
                    dbTableName = None
                    resultSaveComplete = 1

                #Save the result summary to the .db file
                self.db_Status['dbCursor_analysis'].execute("INSERT INTO analysisSummary (id, analysisType, analysisCode, apiSymbol, simulationRangeBEG, simulationRangeEND, simulatedRangeBEG, simulatedRangeEND, resultType, resultSummary, dbTableName, resultSaveComplete) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
                                                            (analysisIndex, analysisType, analysisCode, apiSymbol, simulationRangeBEG, simulationRangeEND, simulatedRangeBEG, simulatedRangeEND, resultType, resultSummary_str, dbTableName, resultSaveComplete))

                #If needed, create a .db table for the complete result
                if (dbTableName != None):
                    resultTableFormat = result['resultTableFormat']
                    self.db_Status['dbCursor_analysis'].execute("CREATE TABLE {:s} {:s}".format(dbTableName, resultTableFormat))
                    self.db_Contents['analysisTables'].append(dbTableName)
                    
                #Apply the changes to the .db file
                self.db_Status['dbConnection_analysis'].commit()

                #Update the local variable
                self.db_Contents['analysis'][analysisCode] = {'analysisIndex':      analysisIndex,
                                                              'analysisType':       analysisType,
                                                              'apiSymbol':          apiSymbol,
                                                              'simulationRangeBEG': simulationRangeBEG,
                                                              'simulationRangeEND': simulationRangeEND,
                                                              'simulatedRangeBEG':  simulatedRangeBEG,
                                                              'simulatedRangeEND':  simulatedRangeEND,
                                                              'resultType':         resultType,
                                                              'resultSummary':      resultSummary_str,
                                                              'dbTableName':        dbTableName}
                
                #Summary Record Announcement & Completion Signal Dispatch
                if (returnRecords == True): self.ipcA['AUX'].sendFAR(functionID = 'RECEIVEANALYSISSUMMARYRECORDS', functionParams = {'analysisSummaries': {analysisCode: self.db_Contents['analysis'][analysisCode]}}, nMaxDispatch = 'INF')
                return {'saveResult': True, 'requestType': saveRequestType, 'blockIndex': None}

            #Save 'analyzedKlines' type analysis result
            elif (saveRequestType == 'analyzedKlines'):
                dbTableName = self.db_Contents['analysis'][analysisCode]['dbTableName']
                #Save the analyzed klines to the .db file
                #---Generate Table Formatters
                formatter1 = ""
                formatter2 = ""
                for index, contentName in enumerate(analyzedKlines_contents):
                    if (index == (len(analyzedKlines_contents)-1)):
                        formatter1 += contentName
                        formatter2 += "?"
                    else:
                        formatter1 += contentName + ","
                        formatter2 += "?,"
                #---Execute SQL commands
                self.db_Status['dbCursor_analysis'].executemany("INSERT INTO {:s} ({:s}) VALUES ({:s})".format(dbTableName, formatter1, formatter2), analyzedKlines)

                #---If is the last block of the full analysis result, edit the 'resultSaveComplete' parameter to 1
                if (isLastBlock == True): self.db_Status['dbCursor_analysis'].execute("UPDATE analysisSummary SET resultSaveComplete = ? WHERE id = ?", (1, self.db_Contents['analysis'][analysisCode]['analysisIndex']))

                #Apply the changes to the .db file
                self.db_Status['dbConnection_analysis'].commit()
                
                #Summary Record Announcement & Completion Signal Dispatch
                if (isLastBlock == True): self.ipcA['AUX'].sendFAR(functionID = 'RECEIVEANALYSISSUMMARYRECORDS', functionParams = {'analysisSummaries': {analysisCode: self.db_Contents['analysis'][analysisCode]}}, nMaxDispatch = 'INF')
                return {'saveResult': True, 'requestType': saveRequestType, 'blockIndex': blockIndex}

        #Unexpected Error Handler
        except Exception as e:
            print(termcolor.colored("An unexpected error ocrrued while attempting to save analysis data for '{:s}'\n *".format(analysisCode), 'light_red'), termcolor.colored(e, 'light_red'))
            return {'saveResult': False, 'requestType': saveRequestType, 'blockIndex': None}



    def removeAnalysisResult(self, functionParams):
        try: analysisCode = functionParams['simulationCode']
        except: print(termcolor.colored("Analysis result removal failed: analysisCode not passed", 'light_red')); return (False, None)
        try:
            if (analysisCode in self.db_Contents['analysis']):
                analysisIndex = self.db_Contents['analysis'][analysisCode]['analysisIndex']
                tableName     = self.db_Contents['analysis'][analysisCode]['dbTableName']
                #Delete the corresponding analysis row from the table 'analysisSummary'
                self.db_Status['dbCursor_analysis'].execute("DELETE from analysisSummary WHERE id=?", (analysisIndex, ))
                #If a analysis table for the corresponding exists, delete it
                if (tableName in self.db_Contents['analysisTables']): 
                    self.db_Status['dbCursor_analysis'].execute("DROP TABLE {:s}".format(tableName))
                    self.db_Contents['analysisTables'].remove(tableName)
                #Apply the changes to the .db file
                self.db_Status['dbConnection_analysis'].commit()
                #Update the local dictionary
                del self.db_Contents['analysis'][analysisCode]
            return (True, analysisCode)
        except Exception as e:
            print(termcolor.colored("An unexpected error ocrrued while attempting to remove analysis data for '{:s}'\n *".format(analysisCode), 'light_red'), termcolor.colored(e, 'light_red'))
            return (False, analysisCode)



    def getAnalysisResult(self, functionParams):
        print(termcolor.colored("Analysis Result Request Received!\n", 'cyan'), functionParams)
    #Inter-Manager Call Functions END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Internal Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Search for a drive that has the drive name specified as 'self_dmConfig['driveName']'
    def __searchDBDrive(self):
        drives = win32api.GetLogicalDriveStrings().split("\000")[:-1]
        for i in range (len(drives)):
            driveName = win32api.GetVolumeInformation(drives[i])[0]
            if ('ATM_DATASTORAGE' == driveName): 
                diskUsage = shutil.disk_usage(drives[i])
                #The Total Volume of the drive must be more than 512 GBytes (or 549,755,813,888 Bytes)
                if (549755813888 <= diskUsage[0]): return (True, drives[i])
        return (False, None)



    #Analyze and return DB drive volume info
    def __getDBVolume(self):
        diskUsage = shutil.disk_usage(self.db_Status['driveDir'])
        return {'total': diskUsage[0], 'used': diskUsage[1], 'free': diskUsage[2]}

    def __classifyDBVolume(self):
        try:
            previousClassificaiton_klines   = self.db_Status['volume_classification']['klines_class']
            previousClassificaiton_analysis = self.db_Status['volume_classification']['analysis_class']
            previousClassificaiton_user     = self.db_Status['volume_classification']['user_class']
            
            """
            Classifications
            0: Stable                  (Less than 50% of the allocation used)
            1: Mild  Attention Advised (More than 50% and less than 70% of the allocation used)
            2: Heavy Attention Advised (More than 70% and less than 90% of the allocation used)
            3: Data Save Disabled      (More than 90% of the allocation used)
            """
            klinesUsed     = os.stat(self.db_Status['DBDir_klines']).st_size
            klinesUsedPerc = round((klinesUsed/self.db_Status['volume_classification']['klines_allocated'])*100,3)
            if   (klinesUsedPerc < 50): newClassification_klines = 0
            elif (klinesUsedPerc < 70): newClassification_klines = 1
            elif (klinesUsedPerc < 90): newClassification_klines = 2
            else:                       newClassification_klines = 3
            
            analysisUsed     = os.stat(self.db_Status['DBDir_analysis']).st_size
            analysisUsedPerc = round((analysisUsed/self.db_Status['volume_classification']['analysis_allocated'])*100,3)
            if   (analysisUsedPerc < 50): newClassification_analysis = 0
            elif (analysisUsedPerc < 70): newClassification_analysis = 1
            elif (analysisUsedPerc < 90): newClassification_analysis = 2
            else:                         newClassification_analysis = 3
            
            userUsed     = os.stat(self.db_Status['DBDir_user']).st_size
            userUsedPerc = round((userUsed/self.db_Status['volume_classification']['user_allocated'])*100,3)
            if   (userUsedPerc < 50): newClassification_user = 0
            elif (userUsedPerc < 70): newClassification_user = 1
            elif (userUsedPerc < 90): newClassification_user = 2
            else:                     newClassification_user = 3

            #Updated Contents Handling
            if (self.db_Status['volume_classification']['klines_used'] != klinesUsed):
                self.db_Status['volume_classification']['klines_used'] = klinesUsed
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'klines_used'), klinesUsed, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'klines_used'), klinesUsed, nMaxDispatch = 'INF')

            if (self.db_Status['volume_classification']['analysis_used'] != analysisUsed):
                self.db_Status['volume_classification']['analysis_used'] = analysisUsed
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'analysis_used'), analysisUsed, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'analysis_used'), analysisUsed, nMaxDispatch = 'INF')

            if (self.db_Status['volume_classification']['user_used'] != userUsed):
                self.db_Status['volume_classification']['user_used'] = userUsed
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'user_used'), userUsed, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'user_used'), userUsed, nMaxDispatch = 'INF')

            if (previousClassificaiton_klines != newClassification_klines):
                if (self.db_Status['volume_classification']['klines_class'] != None):
                    if   (newClassification_klines == 0): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Klines Volume Classification Updated {:d} -> {:d}: Volume Status Stable".format(self.db_Status['volume_classification']['klines_class'],    newClassification_klines), 'magenta'))
                    elif (newClassification_klines == 1): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Klines Volume Classification Updated {:d} -> {:d}: Mild Attention Advised".format(self.db_Status['volume_classification']['klines_class'],  newClassification_klines), 'magenta'))
                    elif (newClassification_klines == 2): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Klines Volume Classification Updated {:d} -> {:d}: Heavy Attention Advised".format(self.db_Status['volume_classification']['klines_class'], newClassification_klines), 'magenta'))
                    elif (newClassification_klines == 3): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Klines Volume Classification Updated {:d} -> {:d}: Data Save Disabled".format(self.db_Status['volume_classification']['klines_class'],      newClassification_klines), 'magenta'))
                self.db_Status['volume_classification']['klines_class'] = newClassification_klines
                if (newClassification_klines == 3): self.db_Status['volume_classification']['klinesSaveAvailable'] = False
                else:                               self.db_Status['volume_classification']['klinesSaveAvailable'] = True
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'klines_class'), newClassification_klines, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'klines_class'), newClassification_klines, nMaxDispatch = 'INF')
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'klinesSaveAvailable'), self.db_Status['volume_classification']['klinesSaveAvailable'], nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'klinesSaveAvailable'), self.db_Status['volume_classification']['klinesSaveAvailable'], nMaxDispatch = 'INF')

            if (previousClassificaiton_analysis != newClassification_analysis):
                if (self.db_Status['volume_classification']['analysis_class'] != None):
                    if   (newClassification_analysis == 0): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Analysis Volume Classification Updated {:d} -> {:d}: Volume Status Stable".format(self.db_Status['volume_classification']['analysis_class'],    newClassification_analysis), 'magenta'))
                    elif (newClassification_analysis == 1): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Analysis Volume Classification Updated {:d} -> {:d}: Mild Attention Advised".format(self.db_Status['volume_classification']['analysis_class'],  newClassification_analysis), 'magenta'))
                    elif (newClassification_analysis == 2): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Analysis Volume Classification Updated {:d} -> {:d}: Heavy Attention Advised".format(self.db_Status['volume_classification']['analysis_class'], newClassification_analysis), 'magenta'))
                    elif (newClassification_analysis == 3): print(termcolor.colored("<IMPORTANT DATABASE ALERT> Analysis Volume Classification Updated {:d} -> {:d}: Data Save Disabled".format(self.db_Status['volume_classification']['analysis_class'],      newClassification_analysis), 'magenta'))
                self.db_Status['volume_classification']['analysis_class'] = newClassification_analysis
                if (newClassification_analysis == 3): self.db_Status['volume_classification']['analysisSaveAvailable'] = False
                else:                                 self.db_Status['volume_classification']['analysisSaveAvailable'] = True
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'analysis_class'), newClassification_analysis, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'analysis_class'), newClassification_analysis, nMaxDispatch = 'INF')
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'analysisSaveAvailable'), self.db_Status['volume_classification']['klinesSaveAvailable'], nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'analysisSaveAvailable'), self.db_Status['volume_classification']['klinesSaveAvailable'], nMaxDispatch = 'INF')

            if (previousClassificaiton_user != newClassification_user):
                if (self.db_Status['volume_classification']['user_class'] != None):
                    if   (newClassification_user == 0): print(termcolor.colored("<IMPORTANT DATABASE ALERT> User Volume Classification Updated {:d} -> {:d}: Volume Status Stable".format(self.db_Status['volume_classification']['user_class'],    newClassification_user), 'magenta'))
                    elif (newClassification_user == 1): print(termcolor.colored("<IMPORTANT DATABASE ALERT> User Volume Classification Updated {:d} -> {:d}: Mild Attention Advised".format(self.db_Status['volume_classification']['user_class'],  newClassification_user), 'magenta'))
                    elif (newClassification_user == 2): print(termcolor.colored("<IMPORTANT DATABASE ALERT> User Volume Classification Updated {:d} -> {:d}: Heavy Attention Advised".format(self.db_Status['volume_classification']['user_class'], newClassification_user), 'magenta'))
                    elif (newClassification_user == 3): print(termcolor.colored("<IMPORTANT DATABASE ALERT> User Volume Classification Updated {:d} -> {:d}: Data Save Disabled".format(self.db_Status['volume_classification']['user_class'],      newClassification_user), 'magenta'))
                self.db_Status['volume_classification']['user_class'] = newClassification_user
                if (newClassification_user == 3): self.db_Status['volume_classification']['userSaveAvailable'] = False
                else:                             self.db_Status['volume_classification']['userSaveAvailable'] = True
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'user_class'), newClassification_user, nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'user_class'), newClassification_user, nMaxDispatch = 'INF')
                self.ipcA['MAIN'].sendPRDEDIT(("DBSTATUS", 'volume_classification', 'userSaveAvailable'), self.db_Status['volume_classification']['userSaveAvailable'], nMaxDispatch = 'INF')
                self.ipcA['AUX'].sendPRDEDIT(("DBSTATUS",  'volume_classification', 'userSaveAvailable'), self.db_Status['volume_classification']['userSaveAvailable'], nMaxDispatch = 'INF')

        except Exception as e: print(termcolor.colored("An unexpected error occurred during DB drive volume classification\n *", 'light_red'), termcolor.colored(e, 'light_red'))

    def __on_DBConnection(self):
        print(termcolor.colored("<ATM DATABASE FOUND!>", 'light_green'))
        
        #Check if .db file exists, create one if there is none, and create sqlite3 connection and cursor instances
        #---<Klines .db>
        if not(os.path.exists(self.db_Status['DBDir_klines'])): print(" Klines data file not found within the drive, will be created")
        self.db_Status['dbConnection_klines'] = sqlite3.connect(self.db_Status['DBDir_klines'])
        self.db_Status['dbCursor_klines'] = self.db_Status['dbConnection_klines'].cursor()
        
        #Get the tables list within the .db file and create any non-existing tables
        tableList = ('klines', 'coinID')
        self.db_Status['dbCursor_klines'].execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        fetchedTableList = self.db_Status['dbCursor_klines'].fetchall()
        tablesInDB = list()
        for fetchedElement in fetchedTableList: tablesInDB.append(fetchedElement[0])
        for tableName in tableList:
            if (tableName not in tablesInDB):
                if   (tableName == 'klines'): self.db_Status['dbCursor_klines'].execute("CREATE TABLE klines (id INTEGER PRIMARY KEY, closeTS INTEGER, p_open REAL, p_high REAL, p_low REAL, p_close REAL, nTrades INTEGER, v REAL, q REAL, v_tb REAL, q_tb REAL, c INTEGER)")
                elif (tableName == 'coinID'): self.db_Status['dbCursor_klines'].execute('''CREATE TABLE coinID (id INTEGER PRIMARY KEY, coinName TEXT,
                                                                                                                mrktRegTS_0  INTEGER, mrktRegTS_1  INTEGER, mrktRegTS_2  INTEGER, mrktRegTS_3  INTEGER, mrktRegTS_4  INTEGER,
                                                                                                                mrktRegTS_5  INTEGER, mrktRegTS_6  INTEGER, mrktRegTS_7  INTEGER, mrktRegTS_8  INTEGER, mrktRegTS_9  INTEGER,
                                                                                                                mrktRegTS_10 INTEGER, mrktRegTS_11 INTEGER, mrktRegTS_12 INTEGER, mrktRegTS_13 INTEGER, mrktRegTS_14 INTEGER,
                                                                                                                klineRanges_0 TEXT,  klineRanges_1 TEXT,  klineRanges_2 TEXT,  klineRanges_3 TEXT,  klineRanges_4 TEXT,
                                                                                                                klineRanges_5 TEXT,  klineRanges_6 TEXT,  klineRanges_7 TEXT,  klineRanges_8 TEXT,  klineRanges_9 TEXT,
                                                                                                                klineRanges_10 TEXT, klineRanges_11 TEXT, klineRanges_12 TEXT, klineRanges_13 TEXT, klineRanges_14 TEXT)''')
                
        #---<Analysis .db>
        if not(os.path.exists(self.db_Status['DBDir_analysis'])): print(" Analysis data file not found within the drive, will be created")
        self.db_Status['dbConnection_analysis'] = sqlite3.connect(self.db_Status['DBDir_analysis'])
        self.db_Status['dbCursor_analysis'] = self.db_Status['dbConnection_analysis'].cursor()
        tableList = ('analysisSummary',)
        self.db_Status['dbCursor_analysis'].execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        fetchedTableList = self.db_Status['dbCursor_analysis'].fetchall()
        tablesInDB = list()
        for fetchedElement in fetchedTableList: tablesInDB.append(fetchedElement[0])
        self.db_Contents['analysisTables'] = [table for table in tablesInDB if table != 'analysisSummary']
        for tableName in tableList:
            if (tableName not in tablesInDB):
                if (tableName == 'analysisSummary'): self.db_Status['dbCursor_analysis'].execute("CREATE TABLE analysisSummary (id INTEGER PRIMARY KEY, analysisType TEXT, analysisCode TEXT, apiSymbol TEXT, simulationRangeBEG INTEGER, simulationRangeEND INTEGER, simulatedRangeBEG INTEGER, simulatedRangeEND INTEGER, resultType TEXT, resultSummary TEXT, dbTableName TEXT, resultSaveComplete INTEGER)")
                
        #---<User .db>
        if not(os.path.exists(self.db_Status['DBDir_user'])): print(" User data file not found within the drive, will be created")
        self.db_Status['dbConnection_user'] = sqlite3.connect(self.db_Status['DBDir_user'])
        self.db_Status['dbCursor_user'] = self.db_Status['dbConnection_user'].cursor()
        
        #Get Drive Information
        self.db_Status['volume'] = self.__getDBVolume()
        self.db_Status['volume_classification']['klines_allocated']   = 274877906944 #256 GBytes
        self.db_Status['volume_classification']['user_allocated']     = 68719476736  #64 GBytes
        self.db_Status['volume_classification']['analysis_allocated'] = self.db_Status['volume']['total'] - self.db_Status['volume_classification']['klines_allocated'] - self.db_Status['volume_classification']['user_allocated'] - 68719476736 #DriveTotal - 256 GBytes (Klines) - 64 GBytes (User) - 64 GBytes (Auxillary); Minimum of 128 GBytes since 512 GBytes is the minimum required total volume of the DB drive
        self.__classifyDBVolume()

        print(" [DriveDir]:       {:s}".format(self.db_Status['driveDir']))
        print(" [DBDir_klines]:   {:s}".format(self.db_Status['DBDir_klines']))
        print(" [DBDir_analysis]: {:s}".format(self.db_Status['DBDir_analysis']))
        print(" [DBVolume_klines]:   <Allocated: {:s}, Used: {:s}, Free: {:s}>".format(ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['klines_allocated']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['klines_used']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['klines_allocated']-self.db_Status['volume_classification']['klines_used'])))
        print(" [DBVolume_analysis]: <Allocated: {:s}, Used: {:s}, Free: {:s}>".format(ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['analysis_allocated']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['analysis_used']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['analysis_allocated']-self.db_Status['volume_classification']['analysis_used'])))
        print(" [DBVolume_user]:     <Allocated: {:s}, Used: {:s}, Free: {:s}>".format(ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['user_allocated']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['user_used']),
                                                                                       ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume_classification']['user_allocated']-self.db_Status['volume_classification']['user_used'])))
        print(" [DBVolume_DRIVE]:    <Total: {:s}, Used: {:s}, Free: {:s}>".format(ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume']['total']),
                                                                                   ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume']['used']),
                                                                                   ATM_Zeta_Auxillaries.diskSpaceFormatter(self.db_Status['volume']['free'])))

        #Read DB Contents
        self.__readDBContents()

        #Raise connection flag after internal DBConnection protocol
        self.db_Status['connected'] = True

        #Call Central Manager's DB connection handler
        self.centralManager.on_DBConnection()

        #Post Connection Handling PRD Announcement
        prdAnnouncementForm_dbStatus = {'connected':               self.db_Status['connected'],
                                        'lastConnectionCheckTime': self.db_Status['lastConnectionCheckTime'],
                                        'driveDir':                self.db_Status['driveDir'],
                                        'DBDir_klines':            self.db_Status['DBDir_klines'],
                                        'DBDir_analysis':          self.db_Status['DBDir_analysis'],
                                        'volume':                  self.db_Status['volume'],
                                        'volume_classification':   self.db_Status['volume_classification']}
        
        self.ipcA['MAIN'].sendPRDEDIT("DBSTATUS", prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')
        self.ipcA['AUX'].sendPRDEDIT("DBSTATUS",  prdAnnouncementForm_dbStatus, nMaxDispatch = 'INF')
        
        self.ipcA['AUX'].sendFAR(functionID = 'RECEIVEANALYSISSUMMARYRECORDS', functionParams = {'analysisSummaries': self.db_Contents['analysis']}, nMaxDispatch = 'INF')

        print(termcolor.colored("<DATA BASE CONNECTION AND CONTENTS ANALYSIS COMPLETE!>", 'light_green'))
        
    def __on_DBDisconnection(self):
        print(termcolor.colored("<DISCONNECTED FROM ATM DATABASE!>", 'light_red'))
        
        #Reset DB Contents Data
        self.db_Contents['user'].clear()
        self.db_Contents['analysis'].clear()
        self.db_Contents['coinID'].clear()
        
        self.ipcA['AUX'].sendPRDEDIT("ANALYSISSUMMARIES", self.db_Contents['analysis'], nMaxDispatch = 'INF')

        self.centralManager.on_DBDisconnection()
        print(termcolor.colored("<ATM DATABASE DISCONNECTION HANDLING COMPLETE>", 'light_yellow'))
        
    def __readDBContents(self):
        try:
            print(" Reading DB Contents...!\n")
            #<Klines .db Contents Read>
            #Read the entire coinID table
            print(" [1/3] Reading Klines DB Contents...")
            self.db_Status['dbCursor_klines'].execute("SELECT * FROM coinID")
            dbTableData_coinID = self.db_Status['dbCursor_klines'].fetchall()
            for rowIndex, coinIDrow in enumerate(dbTableData_coinID):
                coinIDIndex = coinIDrow[0]; self.existingCoinIDIndexes.append(coinIDIndex)
                apiSymbol   = coinIDrow[1]
                #Read CoinIDIndex and MrktRegTS Data
                self.db_Contents['coinID'][apiSymbol] = {'coinIDIndex': coinIDIndex,
                                                         'mrktRegTS':   list(coinIDrow[2:17])}
                #Read Klines Range Data
                for index, intervalID in enumerate(KLINE_INTERVAL_IDs):
                    self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)] = list()
                    if (coinIDrow[index+17] != None):
                        klineRanges_text = coinIDrow[index+17].split("\n")
                        for klineRange in klineRanges_text:
                            beg_end = klineRange.split("_")
                            self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)].append([int(beg_end[0]), int(beg_end[1])])
                    #Look for any abnormalities
                    abnormalityDetected = False
                    for dataRangeIndex in range (len(self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)])):
                        currentDataRange = self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)][dataRangeIndex]
                        if (0 < dataRangeIndex):
                            previousDataRange = self.db_Contents['coinID'][apiSymbol]['klineRanges_'+str(intervalID)][dataRangeIndex-1]
                            if (currentDataRange[0] <= previousDataRange[1]): abnormalityDetected = True; break
                        if (currentDataRange[1] <= currentDataRange[0]): abnormalityDetected = True; break
                    if (abnormalityDetected == True):
                        print(termcolor.colored("Abnormal klines range detected for {:s}_{:d}, performing klines deep range check".format(apiSymbol, intervalID), 'light_magenta'))
                        self.performKlineDeepRangeCheck(apiSymbol, intervalID, recalculateDownloadRanges = False)
                print("  [{:d} / {:d}] {:s}: 'coinIDIndex': {:d}".format(rowIndex+1, len(dbTableData_coinID), apiSymbol, coinIDIndex))
            print(" [1/3] Klines DB Contents Read Complete!\n")

            #<Analysis .db Contents Read>
            print(" [2/3] Reading Analysis DB Contents...")
            self.db_Status['dbCursor_analysis'].execute("SELECT * FROM analysisSummary")
            dbTableData_analysisSummary = self.db_Status['dbCursor_analysis'].fetchall()
            for rowIndex, dbTableData_analysisSummaryRow in enumerate(dbTableData_analysisSummary):
                analysisIndex      = dbTableData_analysisSummaryRow[0]
                analysisType       = dbTableData_analysisSummaryRow[1]
                analysisCode       = dbTableData_analysisSummaryRow[2]
                apiSymbol          = dbTableData_analysisSummaryRow[3]
                simulationRangeBEG = dbTableData_analysisSummaryRow[4]
                simulationRangeEND = dbTableData_analysisSummaryRow[5]
                simulatedRangeBEG  = dbTableData_analysisSummaryRow[6]
                simulatedRangeEND  = dbTableData_analysisSummaryRow[7]
                resultType         = dbTableData_analysisSummaryRow[8]
                resultSummary      = dbTableData_analysisSummaryRow[9]
                dbTableName        = dbTableData_analysisSummaryRow[10]
                resultSaveComplete = dbTableData_analysisSummaryRow[11]

                self.db_Contents['analysis'][analysisCode] = {'analysisIndex':      analysisIndex,
                                                              'analysisType':       analysisType,
                                                              'apiSymbol':          apiSymbol,
                                                              'simulationRangeBEG': simulationRangeBEG,
                                                              'simulationRangeEND': simulationRangeEND,
                                                              'simulatedRangeBEG':  simulatedRangeBEG,
                                                              'simulatedRangeEND':  simulatedRangeEND,
                                                              'resultType':         resultType,
                                                              'resultSummary':      resultSummary,
                                                              'dbTableName':        dbTableName,
                                                              'resultSaveComplete': resultSaveComplete}
                print("  [{:d} / {:d}] <{:s}>\n   - analysisType:  {:s}\
                                             \n   - apiSymbol:     {:s}\
                                             \n   - simulationRange: ({:s}, {:s})\
                                             \n   - simulatedRange:  ({:s}, {:s})\
                                             \n   - resultType:    {:s}\
                                             \n   - resultSummary: {:s}\
                                             \n   - dbTableName:   {:s}".format(rowIndex+1, len(dbTableData_analysisSummary), analysisCode, analysisType, apiSymbol, str(simulationRangeBEG), str(simulationRangeEND), str(simulatedRangeBEG), str(simulatedRangeEND), resultType, resultSummary, str(dbTableName)))
            print(" [2/3] Analysis DB Contents Read Complete!")
            
            #<Analysis .db Contents Read>
            print(" [3/3] Reading User DB Contents...")
            print(" [3/3] User DB Contents Read Complete!")

            print(" DB Contents Read Complete!\n")
        except Exception as e: print(termcolor.colored("An unexpected error ocrrued while attempting to read DB contents\n *", 'light_red'), termcolor.colored(e, 'light_red'))
    #Internal Functions END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------