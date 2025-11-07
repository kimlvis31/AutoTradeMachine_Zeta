import ATM_Zeta_Auxillaries
import random
import time
import math
import termcolor
import numpy
import matplotlib.pyplot as plt
import pprint

KLINDEX_OPENTIME         =  0
KLINDEX_CLOSETIME        =  1
KLINDEX_OPENPRICE        =  2
KLINDEX_HIGHPRICE        =  3
KLINDEX_LOWPRICE         =  4
KLINDEX_CLOSEPRICE       =  5
KLINDEX_NTRADES          =  6
KLINDEX_VOLBASE          =  7
KLINDEX_VOLQUOTE         =  8
KLINDEX_VOLBASETAKERBUY  =  9
KLINDEX_VOLQUOTETAKERBUY = 10

def klineAnalyzer_tester(kline, klineIndex):
    expAnalysisData = list()
    for i in range (1000): expAnalysisData.append(round(random.randint(0, 2560)/10, 1))

    return (klineIndex, ) + kline[:11] + tuple(expAnalysisData)

def klineAnalyzer_getFormatter():
    formatter_base = ('id', 'ts_open', 'ts_close', 'p_open', 'p_high', 'p_low', 'p_close', 'nTrades', 'vol_base', 'vol_quote', 'vol_base_takerBuy', 'vol_quote_takerBuy')
    formatter_expAnalysisData = list()
    for i in range (1000): formatter_expAnalysisData.append("expData_{:d}".format(i))

    return formatter_base + tuple(formatter_expAnalysisData)

def klineAnalyzer_getTableFormat():
    formatter_base = "id INTEGER PRIMARY KEY, ts_open INTEGER, ts_close INTEGER, p_open REAL, p_high REAL, p_low REAL, p_close REAL, nTrades INTERGER, vol_base REAL, vol_quote REAL, vol_base_takerBuy REAL, vol_quote_takerBuy REAL"
    formatter_expAnalysisData = ""
    for i in range (1000): formatter_expAnalysisData += ", expData_{:d} REAL".format(i)
    return "(" + formatter_base + formatter_expAnalysisData + ")"





def analysisGenerator_EVENTS(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        analysisEvents = list()
        for analysisCode in klineAccess:
            if ((analysisCode != 'raw') and (analysisCode != 'EVENT')):
                if ((timestamp in klineAccess[analysisCode]) and (type(klineAccess[analysisCode][timestamp]) == dict) and ('EVENTS' in klineAccess[analysisCode][timestamp])): analysisEvents += klineAccess[analysisCode][timestamp]['EVENTS']

        #Save analysisEvents
        try:    klineAccess['EVENTS'][timestamp] = analysisEvents
        except: klineAccess['EVENTS'] = {timestamp: analysisEvents}

        #Return True to indicate successful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to collect EVENTS at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_SMA(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        nSamples = analysisParams['nSamples']
        analysisCode = 'SMA_{:d}'.format(nSamples)
        timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)
        
        #Calculate SMA
        #[1]: Previous SMA exists
        if ((analysisCode in klineAccess) and (timestamp_previous in klineAccess[analysisCode])): 
            timestamp_expired = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -nSamples)
            previousPriceSum = klineAccess[analysisCode][timestamp_previous]*nSamples
            newPriceSum      = previousPriceSum - klineAccess['raw'][timestamp_expired][KLINDEX_CLOSEPRICE] + klineAccess['raw'][timestamp][KLINDEX_CLOSEPRICE]
            sma = round(newPriceSum / nSamples, precisions['price'])
        #[2]: Previous SMA does not exist
        else:
            timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples, direction = False, mrktReg = mrktRegTS)
            priceSum = 0
            for i in range (nSamples): priceSum += klineAccess['raw'][timestampsList[i]][KLINDEX_CLOSEPRICE]
            sma = round(priceSum / nSamples, precisions['price'])
            
        #Save SMA
        try:    klineAccess[analysisCode][timestamp] = sma
        except: klineAccess[analysisCode] = {timestamp: sma}

        #Return True to indicate successful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate SMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_WMA(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        nSamples = analysisParams['nSamples']
        analysisCode = 'WMA_{:d}'.format(nSamples)
        timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples+1, direction = False, mrktReg = mrktRegTS)
    
        #Calculate WMA (WMA cannot gain any processing speed improvement by refering to the previous WMA)
        baseSum = nSamples*(nSamples+1)/2
        weightedSum = 0
        for index, ts in enumerate(timestampsList): weightedSum += klineAccess['raw'][ts][KLINDEX_CLOSEPRICE]*(nSamples-index)
        wma = round(weightedSum/baseSum, precisions['price'])
    
        #Save WMA
        try:    klineAccess[analysisCode][timestamp] = wma
        except: klineAccess[analysisCode] = {timestamp: wma}
        
        #Return True to indicate succesfful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate WMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_EMA(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        nSamples = analysisParams['nSamples']
        kValue   = 2/(nSamples+1)
        analysisCode = 'EMA_{:d}'.format(nSamples)
        timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)

        #Calculate EMA
        if ((analysisCode in klineAccess) and (timestamp_previous in klineAccess[analysisCode])): ema = round((klineAccess['raw'][timestamp][KLINDEX_CLOSEPRICE]*kValue) + (klineAccess[analysisCode][timestamp_previous]             *(1-kValue)), precisions['price']) #[1]: Previous EMA exists
        else:                                                                                     ema = round((klineAccess['raw'][timestamp][KLINDEX_CLOSEPRICE]*kValue) + (klineAccess['raw'][timestamp_previous][KLINDEX_CLOSEPRICE]*(1-kValue)), precisions['price']) #[2]: Previous EMA does not exist

        #Save EMA
        try:    klineAccess[analysisCode][timestamp] = ema
        except: klineAccess[analysisCode] = {timestamp: ema}

        #Return True to indicate succesfful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate EMA analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_PSAR(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        psar_start        = analysisParams['start']
        psar_acceleration = analysisParams['acceleration']
        psar_maximum      = analysisParams['maximum']
        analysisCode = 'PSAR_{:.3f}_{:.3f}_{:.3f}'.format(psar_start, psar_acceleration, psar_maximum)
        timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)
    
        #Calculate PSAR
        #[1]: Previous PSAR exists
        if ((analysisCode in klineAccess) and (timestamp_previous in klineAccess[analysisCode])):
            psar_previous = klineAccess[analysisCode][timestamp_previous]
            #[1-1]: Previous PSAR value does not exist (PSAR Index 3)
            if (psar_previous['PSAR'] == None):
                timestamp_previous2 = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -2)
                kline_previous1 = klineAccess['raw'][timestamp_previous]
                kline_previous2 = klineAccess['raw'][timestamp_previous2]
                if (psar_previous['PD'] == True): 
                    psar = max([kline_previous1[KLINDEX_HIGHPRICE], kline_previous2[KLINDEX_HIGHPRICE]])
                    ep   = min([kline_previous1[KLINDEX_LOWPRICE],  kline_previous2[KLINDEX_LOWPRICE]])
                else:        
                    psar = min([kline_previous1[KLINDEX_LOWPRICE],  kline_previous2[KLINDEX_LOWPRICE]])
                    ep   = max([kline_previous1[KLINDEX_HIGHPRICE], kline_previous2[KLINDEX_HIGHPRICE]])                     
                af = psar_start
                pd = psar_previous['PD']
                pd_reversed = False

            #[1-2]: Previous PSAR value exists (PSAR Index 3 <)
            else:
                timestamp_previous2 = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -2)
                kline_current = klineAccess['raw'][timestamp]
                kline_previous1 = klineAccess['raw'][timestamp_previous]
                kline_previous2 = klineAccess['raw'][timestamp_previous2]
            
                psar_ = psar_previous['PSAR'] + psar_previous['AF']*(psar_previous['EP']-psar_previous['PSAR'])
                if (psar_previous['PD'] == True):
                    #Reverse Detect
                    pd_reversed = (kline_current[KLINDEX_LOWPRICE] < psar_)
                
                    #AF Update
                    if (psar_previous['EP'] < kline_current[KLINDEX_HIGHPRICE]):
                        ep = kline_current[KLINDEX_HIGHPRICE]
                        af = psar_previous['AF'] + psar_acceleration
                        if (psar_maximum < af): af = psar_maximum
                    else: 
                        ep = psar_previous['EP']
                        af = psar_previous['AF']

                    psar_ = min([psar_, kline_previous1[KLINDEX_LOWPRICE], kline_previous2[KLINDEX_LOWPRICE]])
                else:
                    #Reverse Detect
                    pd_reversed = (psar_ < kline_current[KLINDEX_HIGHPRICE])

                    #AF Update
                    if (kline_current[KLINDEX_LOWPRICE] < psar_previous['EP']):
                        ep = kline_current[KLINDEX_LOWPRICE]
                        af = psar_previous['AF'] + psar_acceleration
                        if (psar_maximum < af): af = psar_maximum
                    else: 
                        ep = psar_previous['EP']
                        af = psar_previous['AF']

                    psar_ = max([psar_, kline_previous1[KLINDEX_HIGHPRICE], kline_previous2[KLINDEX_HIGHPRICE]])

                #PD Reversal Handling
                if (pd_reversed == True):
                    psar_ = ep
                    af = psar_start
                    pd = not(psar_previous['PD'])
                    if (pd == True): ep = kline_current[KLINDEX_HIGHPRICE]
                    else:            ep = kline_current[KLINDEX_LOWPRICE]
                else: pd = psar_previous['PD']

                psar = psar_

        #[2]: Previous PSAR does not exist 
        else:
            #[2-1]: Previous Kline exists (PSAR Index 2)
            if (timestamp_previous in klineAccess['raw']):
                #Determine progression direction
                kline_previous = klineAccess['raw'][timestamp_previous]
                kline_current = klineAccess['raw'][timestamp]
            
                p_high_previous = kline_previous[KLINDEX_HIGHPRICE]
                p_high_current  = kline_current[KLINDEX_HIGHPRICE]
                if (p_high_previous <= p_high_current): p_high_delta = p_high_current-p_high_previous
                else:                                   p_high_delta = 0
                p_low_previous = kline_previous[KLINDEX_LOWPRICE]
                p_low_current  = kline_current[KLINDEX_LOWPRICE]
                if (p_low_current <= p_low_previous): p_low_delta = p_low_previous-p_low_current
                else:                                 p_low_delta = 0

                if (p_low_delta <= p_high_delta): pd = False
                else:                             pd = True
                af   = None
                ep   = None
                psar = None
                pd_reversed = False

            #[2-2]: Previous Kline does not exist
            else: return None
            
        #Prepare Major Events to Report
        eventsReport = list()
        if (pd_reversed == True):
            if (pd == True): eventsReport.append("{:s} <REV_INCREMENTAL>".format(analysisCode))
            else:            eventsReport.append("{:s} <REV_DECREMENTAL>".format(analysisCode))

        #PD:   Progression Direction (True: Incremental, False: Decremental)
        #AF:   Acceleration Factor
        #EP:   Extreme Point
        #PSAR: PSAR Value
        psarResult = {'PD': pd, 'PDReversed': pd_reversed, 'AF': af, 'EP': ep, 'PSAR': psar, 'EVENTS': eventsReport}

        #Save PSAR
        try:    klineAccess[analysisCode][timestamp] = psarResult
        except: klineAccess[analysisCode] = {timestamp: psarResult}

        #Return True to indicate succesfful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate PSAR analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_BOL(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        nSamples  = analysisParams['nSamples']
        maType    = analysisParams['maType']
        bandWidth = analysisParams['bandWidth']
        analysisCode = 'BOL_{:d}_{:.1f}'.format(nSamples, bandWidth)
        timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples+1, direction = False, mrktReg = mrktRegTS)

        #Get, or Calculate and Save MA
        maCode = "{:s}_{:d}".format(maType, nSamples)
        #If MA for the current timestamp does not exist or the analysis mode is 1, compute the MA
        if (not((maCode in klineAccess) and (timestamp in klineAccess[maCode])) or (analysisMode == 1)):
            analysisParams_MA = {'nSamples': nSamples}
            if   (maType == 'SMA'): analysisGenerator_SMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
            elif (maType == 'WMA'): analysisGenerator_WMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
            elif (maType == 'EMA'): analysisGenerator_EMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
        ma = klineAccess[maCode][timestamp]

        #Calculate BOL
        deviationSquaredSum = 0
        for i in range (nSamples): deviationSquaredSum += math.pow((klineAccess['raw'][timestampsList[i]][KLINDEX_CLOSEPRICE])-ma, 2)
        sd = math.sqrt(deviationSquaredSum/nSamples)
        bol = (round(ma-sd*bandWidth, precisions['price']), 
                ma, 
                round(ma+sd*bandWidth, precisions['price']))
        
        #Save BOL
        try:    klineAccess[analysisCode][timestamp] = bol
        except: klineAccess[analysisCode] = {timestamp: bol}

        #Return True to indicate successful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate BOL analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_IVP(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        analysisCode = 'IVP'
        timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)

        targetKline = klineAccess['raw'][timestamp]
        targetKline_closePrice = targetKline[KLINDEX_CLOSEPRICE]
        targetKline_highPrice  = targetKline[KLINDEX_HIGHPRICE]
        targetKline_lowPrice   = targetKline[KLINDEX_LOWPRICE]
        targetKline_vol        = targetKline[KLINDEX_VOLBASE]
    
        nSamples             = analysisParams['nSamples']
        useBLE               = analysisParams['useBLE']
        gammaFactor_userMin  = analysisParams['minGammaFactor']
        useAGF               = analysisParams['useAGF']
        AGFRefLen            = analysisParams['AGFRefLen']
        AGFMAType            = analysisParams['AGFMAType']
        clusteringRange      = analysisParams['clusteringRange']
        EXISTENCECOUNTER_MIN = analysisParams['existenceCounter_min']
        EXISTENCECOUNTER_MAX = analysisParams['existenceCounter_max']
        CSACCELERATIONFACTOR = analysisParams['csAccelerationFactor']
        ANCHORRANGERFACTOR   = analysisParams['anchorRangerFactor']

        previousAnalysisExists = (('IVP' in klineAccess) and (timestamp_previous in klineAccess['IVP']))

        #Active Beta Factor Computation
        betaFactor_userMin = round(targetKline_closePrice*gammaFactor_userMin, precisions['price'])
        if (useAGF == True):
            #Collect Prices Data
            targetTimestamps = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = AGFRefLen+1, direction = False, mrktReg = mrktRegTS)
            priceCollection  = numpy.array([klineAccess['raw'][ts] for ts in targetTimestamps[:-1] if ts in klineAccess['raw']])[:, KLINDEX_CLOSEPRICE]
            priceCollection_filtered = numpy.zeros(AGFRefLen)

            #Generate Filtered Price Collection Data
            lastExtrema = None; lastDirection = None; lastDirectionUpdateIndex = None
            for index in range (1, AGFRefLen):
                newDirection = (0 <= priceCollection[index]-priceCollection[index-1])
                if (lastDirection != newDirection):
                    if (lastDirection == None): 
                        lastDirection = newDirection
                        lastDirectionUpdateIndex = index
                    else:
                        if (lastExtrema == None):
                            lastExtrema = priceCollection[index-1]
                            for i in range (0, index+1): priceCollection_filtered[i] = lastExtrema
                            lastDirection = newDirection
                            lastDirectionUpdateIndex = index
                        else:
                            if (betaFactor_userMin <= abs(lastExtrema-priceCollection[index-1])):
                                lastExtrema = priceCollection[index-1]
                                lastDirection = newDirection
                                lastDirectionUpdateIndex = index
                            priceCollection_filtered[index-1] = lastExtrema
                else:
                    if (lastExtrema != None):
                        if (newDirection == True) and (lastExtrema < priceCollection[index]):
                            lastExtrema = priceCollection[index]
                            for i in range (lastDirectionUpdateIndex-1, index): priceCollection_filtered[i] = lastExtrema
                        elif (newDirection == False) and (priceCollection[index] < lastExtrema):
                            lastExtrema = priceCollection[index]
                            for i in range (lastDirectionUpdateIndex-1, index): priceCollection_filtered[i] = lastExtrema
                        else: priceCollection_filtered[index-1] = lastExtrema
            priceCollection_filtered[-1] = priceCollection_filtered[-2]

            #Find price level deltas
            priceDeltas = list()
            lastPriceLevel = priceCollection_filtered[0]
            for price_filtered in priceCollection_filtered:
                if (price_filtered != lastPriceLevel):
                    priceDeltas.append(abs(lastPriceLevel-price_filtered))
                    lastPriceLevel = price_filtered
                
            nPriceDeltas = len(priceDeltas)
            #Find SMA of price level deltas
            if (AGFMAType == 'SMA'):
                priceDeltaSum = sum(priceDeltas)
                priceDeltaMA = priceDeltaSum/nPriceDeltas
            #Find WMA of price level deltas
            elif (AGFMAType == 'WMA'):
                baseSum = nPriceDeltas*(nPriceDeltas+1)/2
                weightedSum = 0
                for index, priceDelta in enumerate(priceDeltas): weightedSum += priceDelta*(1+index)
                weightedDeltaAverage = weightedSum/baseSum
                priceDeltaMA = weightedDeltaAverage
            #Find EMA of price level deltas
            elif (AGFMAType == 'EMA'):
                priceDelta_kValue = 2/(nPriceDeltas+1)
                priceDelta_lastEMA = priceDeltas[0]
                for priceDelta in priceDeltas[1:]: priceDelta_lastEMA = (priceDelta*priceDelta_kValue) + (priceDelta_lastEMA*(1-priceDelta_kValue))
                priceDeltaMA = priceDelta_lastEMA
                        
            #Set betaFactor value
            if (previousAnalysisExists == True):
                previousIVP_betaFactor_effective = klineAccess['IVP'][timestamp_previous]['betaFactor_effective']
                betaFactor_effective = round((previousIVP_betaFactor_effective+priceDeltaMA)/2, precisions['price'])
            else: betaFactor_effective = round(priceDeltaMA, precisions['price'])
        else: betaFactor_effective = betaFactor_userMin

        #DivisionHeight & nDivisions Determination
        #---divisionCeiling determination
        p_max = klineAccess['raw_status'][timestamp]['p_max']
        p_max_OOM = math.floor(math.log(p_max, 10))
        p_max_MSD = int(p_max/pow(10, p_max_OOM))
        if (p_max_MSD == 10): p_max_MSD = 1; p_max_OOM += 1
        dCeiling_MSD = (int(p_max_MSD/1)+1)*1
        if (dCeiling_MSD == 10): dCeiling_MSD = 1;            dCeiling_OOM = p_max_OOM+1
        else:                    dCeiling_MSD = dCeiling_MSD; dCeiling_OOM = p_max_OOM
        dCeiling = dCeiling_MSD*pow(10, dCeiling_OOM)
        
        #---divisionHeight determination
        divisionHeight_min = betaFactor_effective/10
        divisionHeight_min_OOM = math.floor(math.log(divisionHeight_min, 10))
        divisionHeight_min_MSD = int(divisionHeight_min/pow(10, divisionHeight_min_OOM))
        if (divisionHeight_min_MSD == 10): divisionHeight_min_MSD = 1; divisionHeight_min_OOM += 1
        divisionHeight_MSD = int(divisionHeight_min_MSD/5)*5
        if (divisionHeight_MSD == 0): divisionHeight_MSD = 1;                  divisionHeight_OOM = divisionHeight_min_OOM
        else:                         divisionHeight_MSD = divisionHeight_MSD; divisionHeight_OOM = divisionHeight_min_OOM
        divisionHeight = divisionHeight_MSD*pow(10, divisionHeight_OOM)

        #---If divisionHeight of the previous IVP is smaller than that of the current IVP, use the previous divisionHeight
        if (previousAnalysisExists == True):
            previousIVP_divisionHeight = klineAccess['IVP'][timestamp_previous]['divisionHeight']
            if (previousIVP_divisionHeight < divisionHeight): divisionHeight = previousIVP_divisionHeight

        nDivisions = int(dCeiling/divisionHeight)

        #IVP Computation
        if (previousAnalysisExists == True):
            #Get previous IVP
            previousIVP = klineAccess['IVP'][timestamp_previous]
            previousIVP_ivpRaw     = numpy.copy(previousIVP['ivp_raw'])
            previousIVP_nDivisions = len(previousIVP_ivpRaw)
            previousIVP_divisionHeight = previousIVP['divisionHeight']
            #Transfer the previous IVP to the current IVP
            if ((previousIVP_divisionHeight == divisionHeight) and (previousIVP_nDivisions == nDivisions)): ivp = previousIVP_ivpRaw
            else:
                ivp = numpy.zeros(nDivisions)
                for divisionIndex_previousIVP in range (previousIVP_nDivisions):
                    division_p_low  = previousIVP_divisionHeight*divisionIndex_previousIVP
                    division_p_high = previousIVP_divisionHeight*(divisionIndex_previousIVP+1)
                    d_f = int((division_p_low) /divisionHeight)
                    d_c = int((division_p_high)/divisionHeight)
                    if (d_f == d_c):
                        ivp[d_f] += previousIVP_ivpRaw[divisionIndex_previousIVP]
                    elif (d_f + 1 == d_c):
                        volumeDensity = previousIVP_ivpRaw[divisionIndex_previousIVP]/previousIVP_divisionHeight
                        p_d_c = divisionHeight*d_c
                        if (d_c < nDivisions): ivp[d_c] += (division_p_high-p_d_c)*volumeDensity
                        ivp[d_f] += (p_d_c-division_p_low) *volumeDensity
                    else:
                        volumeDensity = previousIVP_ivpRaw[divisionIndex_previousIVP]/previousIVP_divisionHeight
                        if (d_c < nDivisions): ivp[d_c] += (division_p_high-divisionHeight*d_c)*volumeDensity
                        ivp[d_f] += (divisionHeight*(d_f+1)-division_p_low)*volumeDensity
                        volAllocation_Full = divisionHeight*volumeDensity
                        for divisionIndex in range (d_f+1,d_c): ivp[divisionIndex] += volAllocation_Full
                    
            #Remove the expired kline VP from the constructed IVP
            timestamp_expired = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -nSamples)
            expiredKline = klineAccess['raw'][timestamp_expired]
            expiredKline_highPrice = expiredKline[KLINDEX_HIGHPRICE]
            expiredKline_lowPrice  = expiredKline[KLINDEX_LOWPRICE]
            expiredKline_vol       = expiredKline[KLINDEX_VOLBASE]
            d_c = int((expiredKline_highPrice)/divisionHeight)
            d_f = int((expiredKline_lowPrice) /divisionHeight)
            if (d_f == d_c):
                ivp[d_f] -= expiredKline_vol
            elif (d_f + 1 == d_c):
                volumeDensity = expiredKline_vol / (expiredKline_highPrice-expiredKline_lowPrice)
                p_d_c = divisionHeight*d_c
                ivp[d_c] -= (expiredKline_highPrice-p_d_c)*volumeDensity
                ivp[d_f] -= (p_d_c-expiredKline_lowPrice) *volumeDensity
            else:
                volumeDensity = expiredKline_vol / (expiredKline_highPrice-expiredKline_lowPrice)
                ivp[d_c]       -= (expiredKline_highPrice-divisionHeight*d_c)   *volumeDensity
                ivp[d_f]       -= (divisionHeight*(d_f+1)-expiredKline_lowPrice)*volumeDensity
                ivp[d_f+1:d_c] -= divisionHeight*volumeDensity

            #Add the current kline VP to the constructed IVP
            d_c = int((targetKline_highPrice)/divisionHeight)
            d_f = int((targetKline_lowPrice) /divisionHeight)
            if (d_f == d_c):
                ivp[d_f] += targetKline_vol
            elif (d_f + 1 == d_c):
                volumeDensity = targetKline_vol / (targetKline_highPrice-targetKline_lowPrice)
                p_d_c = divisionHeight*d_c
                ivp[d_c] += (targetKline_highPrice-p_d_c)*volumeDensity
                ivp[d_f] += (p_d_c-targetKline_lowPrice) *volumeDensity
            else:
                volumeDensity = targetKline_vol / (targetKline_highPrice-targetKline_lowPrice)
                ivp[d_c]       += (targetKline_highPrice-divisionHeight*d_c)   *volumeDensity
                ivp[d_f]       += (divisionHeight*(d_f+1)-targetKline_lowPrice)*volumeDensity
                ivp[d_f+1:d_c] += divisionHeight*volumeDensity
        else:
            ivp = numpy.zeros(nDivisions)
            timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples, direction = False, mrktReg = mrktRegTS)
            for ts in timestampsList:
                kline_p_high = klineAccess['raw'][ts][KLINDEX_HIGHPRICE]
                kline_p_low  = klineAccess['raw'][ts][KLINDEX_LOWPRICE]
                kline_vol    = klineAccess['raw'][ts][KLINDEX_VOLBASE]
                d_c = int((kline_p_high)/divisionHeight)
                d_f = int((kline_p_low)/ divisionHeight)
                if (d_f == d_c):
                    ivp[d_f] += kline_vol
                elif (d_f + 1 == d_c):
                    volumeDensity = kline_vol / (kline_p_high-kline_p_low)
                    p_d_c = divisionHeight*d_c
                    ivp[d_c] += (kline_p_high-p_d_c)*volumeDensity
                    ivp[d_f] += (p_d_c-kline_p_low) *volumeDensity
                else:
                    volumeDensity = kline_vol / (kline_p_high-kline_p_low)
                    ivp[d_c]       += (kline_p_high-(divisionHeight*d_c))   *volumeDensity
                    ivp[d_f]       += ((divisionHeight*(d_f+1))-kline_p_low)*volumeDensity
                    ivp[d_f+1:d_c] += divisionHeight*volumeDensity
        ivp_rawMax = numpy.max(ivp)

        #IVP Clustering
        #---Compute clustering index range
        pClusteringRange_beg = targetKline_closePrice*(100-clusteringRange)/100
        pClusteringRange_end = targetKline_closePrice*(100+clusteringRange)/100
        dIndex_clusteringRange_beg = int(pClusteringRange_beg/divisionHeight)
        dIndex_clusteringRange_end = int(pClusteringRange_end/divisionHeight)+1
        if (nDivisions < dIndex_clusteringRange_end): dIndex_clusteringRange_end = nDivisions

        #---Find Local Extremas within the clustering range
        localMinimas = list(); localMaximas = list()
        lastDirection = None
        for dIndex in range (dIndex_clusteringRange_beg, dIndex_clusteringRange_end):
            delta = ivp[dIndex+1]-ivp[dIndex]
            if   (delta < 0):  newDirection = False
            elif (0 < delta):  newDirection = True
            elif (delta == 0): newDirection = None
            if   ((lastDirection == False) and (newDirection == True)):  localMinimas.append((ivp[dIndex], dIndex, round((dIndex+0.5)*divisionHeight, precisions['price']))); lastDirection = True  #Local Minima
            elif ((lastDirection == True)  and (newDirection == False)): localMaximas.append((ivp[dIndex], dIndex, round((dIndex+0.5)*divisionHeight, precisions['price']))); lastDirection = False #Local Maxima
            elif (lastDirection == None): lastDirection = newDirection

        #---Sort Extremas to determine priority based on the corresponding ivp value
        localMinimas.sort()
        localMaximas.sort(reverse = True)

        #---Local Extrema Filtering
        ivp_clusterSources = list() #List of Tuples <[0]: ivp Value (Indicates Extrema Strength), [1]: divisionIndex, [2]: Extrema Value>
        ivp_clusterSources_occupiedRegions = list()
        if   (0 < len(localMaximas)): extremaTypeToAdd = True
        elif (0 < len(localMinimas)): extremaTypeToAdd = False
        else:                         extremaTypeToAdd = None
        while (extremaTypeToAdd != None):
            if (extremaTypeToAdd == True):
                extrema = localMaximas.pop(0)
                isInOccupiedRegion = False
                for occupiedRegion in ivp_clusterSources_occupiedRegions:
                    if (occupiedRegion[0] < extrema[2]) and (extrema[2] < occupiedRegion[1]): isInOccupiedRegion = True; break
                if (isInOccupiedRegion == True):
                    if   (0 < len(localMaximas)): extremaTypeToAdd = True
                    elif (0 < len(localMinimas)): extremaTypeToAdd = False
                    else:                         extremaTypeToAdd = None
                else:
                    ivp_clusterSources.append(extrema[2])
                    ivp_clusterSources_occupiedRegions.append((extrema[2]-betaFactor_effective, extrema[2]+betaFactor_effective))
                    if   (0 < len(localMinimas)): extremaTypeToAdd = False
                    elif (0 < len(localMaximas)): extremaTypeToAdd = True
                    else:                         extremaTypeToAdd = None

            if (extremaTypeToAdd == False):
                extrema = localMinimas.pop(0)
                isInOccupiedRegion = False
                for occupiedRegion in ivp_clusterSources_occupiedRegions:
                    if (occupiedRegion[0] < extrema[2]) and (extrema[2] < occupiedRegion[1]): isInOccupiedRegion = True; break
                if (isInOccupiedRegion == True):
                    if   (0 < len(localMinimas)): extremaTypeToAdd = False
                    elif (0 < len(localMaximas)): extremaTypeToAdd = True
                    else:                         extremaTypeToAdd = None
                else:
                    ivp_clusterSources.append(extrema[2])
                    ivp_clusterSources_occupiedRegions.append((extrema[2]-betaFactor_effective, extrema[2]+betaFactor_effective))
                    if   (0 < len(localMaximas)): extremaTypeToAdd = True
                    elif (0 < len(localMinimas)): extremaTypeToAdd = False
                    else:                         extremaTypeToAdd = None

        #---Cluster Sources Collection
        ivp_clusterSources.sort()
        nClusterSources = len(ivp_clusterSources)

        #Cluster Construction and Events Detection
        #--- ivpCluster Format
        # 'cs':  Cluster Source
        # 'ec':  Existence Counter
        # 'cuc': Cluster Unique Color
        ivp_historicalClusters    = list()
        ivp_filteredClusters      = list()
        ivp_filteredClusterEvents = list()
    
        if (previousAnalysisExists == True):
            ivp_historicalClusters_prev = klineAccess['IVP'][timestamp_previous]['ivp_historicalClusters']
            nHistoricalClusters_prev = len(ivp_historicalClusters_prev)

            #[1]: Construct historical cluster sources
            csIndex_current = 0
            for csIndex_prev in range (nHistoricalClusters_prev):
                #Cluster Region
                if (csIndex_prev == 0):
                    if (nHistoricalClusters_prev == 1):            clusterRegion = (0,                                                                                                                           dCeiling)
                    else:                                          clusterRegion = (0,                                                                                                                           round((ivp_historicalClusters_prev[csIndex_prev][0]+ivp_historicalClusters_prev[csIndex_prev+1][0])/2, precisions['price']))
                elif (csIndex_prev == nHistoricalClusters_prev-1): clusterRegion = (round((ivp_historicalClusters_prev[csIndex_prev-1][0]+ivp_historicalClusters_prev[csIndex_prev][0])/2, precisions['price']), dCeiling)
                else:                                              clusterRegion = (round((ivp_historicalClusters_prev[csIndex_prev-1][0]+ivp_historicalClusters_prev[csIndex_prev][0])/2, precisions['price']), round((ivp_historicalClusters_prev[csIndex_prev][0]+ivp_historicalClusters_prev[csIndex_prev+1][0])/2, precisions['price']))
            
                #Current Clusters within the corresponding previous Cluster
                currentClusterSourcesWithin = list()
                while (csIndex_current < nClusterSources):
                    cs = ivp_clusterSources[csIndex_current]
                    if ((clusterRegion[0] <= cs) and (cs < clusterRegion[1])): #The current cluster source is within the previous cluster region
                        currentClusterSourcesWithin.append(csIndex_current)
                        csIndex_current += 1
                    else: break
                nCurrentClusterSourcesWithin = len(currentClusterSourcesWithin)
            
                if (nCurrentClusterSourcesWithin == 0): 
                    if (1 < ivp_historicalClusters_prev[csIndex_prev][1]): ivp_historicalClusters.append((ivp_historicalClusters_prev[csIndex_prev][0], ivp_historicalClusters_prev[csIndex_prev][1]-1))
                elif (nCurrentClusterSourcesWithin == 1): 
                    ecEffective = ivp_historicalClusters_prev[csIndex_prev][1]+1
                    if (EXISTENCECOUNTER_MAX < ecEffective): ecEffective = EXISTENCECOUNTER_MAX
                    ivp_historicalClusters.append((ivp_historicalClusters_prev[csIndex_prev][0], ecEffective))
                elif (1 < nCurrentClusterSourcesWithin):
                    nearestCSIndex = None
                    minDistance = float('inf')
                    for csIndex in currentClusterSourcesWithin:
                        distance = abs(ivp_historicalClusters_prev[csIndex_prev][0] - ivp_clusterSources[csIndex])
                        if (distance < minDistance): minDistance = distance; nearestCSIndex = csIndex
                    for csIndex in currentClusterSourcesWithin:
                        if (csIndex == nearestCSIndex): 
                            ecEffective = ivp_historicalClusters_prev[csIndex_prev][1]+1
                            if (EXISTENCECOUNTER_MAX < ecEffective): ecEffective = EXISTENCECOUNTER_MAX
                            ivp_historicalClusters.append((ivp_clusterSources[csIndex], ecEffective))
                        else: ivp_historicalClusters.append((ivp_clusterSources[csIndex], 1))
        
            #[2]: Construct un-identified filtered clusters
            ivp_filteredClusters = [{'cs': historicalCluster[0], 'cuc': None, 'ct': 'ivp'} for historicalCluster in ivp_historicalClusters if EXISTENCECOUNTER_MIN <= historicalCluster[1]]
            #--- BLE (Bollinger Enhancement)
            if (useBLE == True):
                for bolCode in [analysisCode for analysisCode in klineAccess if analysisCode[:3] == 'BOL']:
                    for bolLineValue in klineAccess[bolCode][timestamp]: ivp_filteredClusters.append({'cs': bolLineValue, 'cuc': None, 'ct': 'ble'})
            #--- Sort the constructed un-identified filtered clusters
            ivp_filteredClusters.sort(key = lambda x: x['cs'])
            nFilteredClusters = len(ivp_filteredClusters)

            #[3]: Determine filteredCluster Events and assign cuc (cluster unique color)
            ivp_filteredClusters_prev = klineAccess['IVP'][timestamp_previous]['ivp_filteredClusters']
            nFilteredClusters_prev = len(ivp_filteredClusters_prev)
            if (0 < nFilteredClusters_prev):
                fcIndex_current = 0
                for fcIndex_prev in range (nFilteredClusters_prev):
                    #Cluster Region
                    if (fcIndex_prev == 0):
                        if (nFilteredClusters_prev == 1):            clusterRegion = (0,                                                                                                                             dCeiling)
                        else:                                        clusterRegion = (0,                                                                                                                             round((ivp_filteredClusters_prev[fcIndex_prev]['cs']+ivp_filteredClusters_prev[fcIndex_prev+1]['cs'])/2, precisions['price']))
                    elif (fcIndex_prev == nFilteredClusters_prev-1): clusterRegion = (round((ivp_filteredClusters_prev[fcIndex_prev-1]['cs']+ivp_filteredClusters_prev[fcIndex_prev]['cs'])/2, precisions['price']), dCeiling)
                    else:                                            clusterRegion = (round((ivp_filteredClusters_prev[fcIndex_prev-1]['cs']+ivp_filteredClusters_prev[fcIndex_prev]['cs'])/2, precisions['price']), round((ivp_filteredClusters_prev[fcIndex_prev]['cs']+ivp_filteredClusters_prev[fcIndex_prev+1]['cs'])/2, precisions['price']))

                    #Current filteredClusters within the corresponding previous filtered cluster
                    currentFilteredClustersWithin = list()
                    while (fcIndex_current < nFilteredClusters):
                        cs = ivp_filteredClusters[fcIndex_current]['cs']
                        if ((clusterRegion[0] <= cs) and (cs < clusterRegion[1])): #The current cluster source is within the previous cluster region
                            currentFilteredClustersWithin.append(fcIndex_current)
                            fcIndex_current += 1
                        else: break
                    nCurrentFilteredClustersWithin = len(currentFilteredClustersWithin)
            
                    #Case 1: Previous Cluster Disappeared
                    if (nCurrentFilteredClustersWithin == 0):
                        nextClusterIndex = None

                        #If the destoryed cluster source was above the current close price
                        if (targetKline_closePrice <= ivp_filteredClusters_prev[fcIndex_prev]['cs']):
                            fcIndex = nFilteredClusters-1
                            while ((0 <= fcIndex) and (targetKline_closePrice < ivp_filteredClusters[fcIndex]['cs'])): fcIndex -= 1
                            nextClusterIndex = fcIndex+1
                        #If the destoryed cluster source was below the current close price
                        else:
                            fcIndex = 0
                            while ((fcIndex < nFilteredClusters) and (ivp_filteredClusters[fcIndex]['cs'] < targetKline_closePrice)): fcIndex += 1
                            nextClusterIndex = fcIndex-1

                        if ((nextClusterIndex < 0) or (nFilteredClusters <= nextClusterIndex)): nextClusterIndex = None
                        ivp_filteredClusterEvents.append(('DESTROYED', fcIndex_prev, nextClusterIndex))

                    #Case 2: Previous Cluster Still Existing Singularly
                    elif (nCurrentFilteredClustersWithin == 1):
                        fcIndexWithin = currentFilteredClustersWithin[0]
                        fcWithin_cs = ivp_filteredClusters[fcIndexWithin]['cs']
                        fcWithin_ct = ivp_filteredClusters[fcIndexWithin]['ct']
                        if (fcWithin_ct == 'ivp'):
                            csEffective = round((fcWithin_cs*CSACCELERATIONFACTOR)+(ivp_filteredClusters_prev[fcIndex_prev]['cs']*(1-CSACCELERATIONFACTOR)), precisions['price'])
                            if   (fcIndex_prev != fcIndexWithin):                                ivp_filteredClusterEvents.append(('INDEXUPDATED', fcIndex_prev, fcIndexWithin))
                            elif (ivp_filteredClusters_prev[fcIndex_prev]['cs'] != csEffective): ivp_filteredClusterEvents.append(('VALUEUPDATED', fcIndex_prev, csEffective))
                            ivp_filteredClusters[fcIndexWithin]['cs']  = csEffective
                            ivp_filteredClusters[fcIndexWithin]['cuc'] = ivp_filteredClusters_prev[fcIndex_prev]['cuc']
                        elif (fcWithin_ct == 'ble'):
                            if   (fcIndex_prev != fcIndexWithin):                                ivp_filteredClusterEvents.append(('INDEXUPDATED', fcIndex_prev, fcIndexWithin))
                            elif (ivp_filteredClusters_prev[fcIndex_prev]['cs'] != fcWithin_cs): ivp_filteredClusterEvents.append(('VALUEUPDATED', fcIndex_prev, fcWithin_cs))
                            ivp_filteredClusters[fcIndexWithin]['cuc'] = ivp_filteredClusters_prev[fcIndex_prev]['cuc']

                    #Case 3: Previous Cluster Splitted
                    elif (1 < nCurrentFilteredClustersWithin):
                        nearestFCIndex = None
                        minDistance = float('inf')
                        for fcIndex in currentFilteredClustersWithin:
                            distance = abs(ivp_filteredClusters_prev[fcIndex_prev]['cs'] - ivp_filteredClusters[fcIndex]['cs'])
                            if (distance < minDistance): minDistance = distance; nearestFCIndex = fcIndex
                        for fcIndex in currentFilteredClustersWithin:
                            if (fcIndex == nearestFCIndex):
                                fcTarget_cs = ivp_filteredClusters[fcIndex]['cs']
                                fcTarget_ct = ivp_filteredClusters[fcIndex]['ct']
                                if (fcTarget_ct == 'ivp'):
                                    csEffective = round((fcTarget_cs*CSACCELERATIONFACTOR)+(ivp_filteredClusters_prev[fcIndex_prev]['cs']*(1-CSACCELERATIONFACTOR)), precisions['price'])
                                    ivp_filteredClusters[fcIndex]['cs']  = ivp_filteredClusters_prev[fcIndex_prev]['cs']
                                    ivp_filteredClusters[fcIndex]['cuc'] = ivp_filteredClusters_prev[fcIndex_prev]['cuc']
                                elif (fcTarget_ct == 'ble'): ivp_filteredClusters[fcIndex]['cuc'] = ivp_filteredClusters_prev[fcIndex_prev]['cuc']
                            else: ivp_filteredClusters[fcIndex]['cuc'] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                        ivp_filteredClusterEvents.append(('SPLITED', fcIndex_prev, nearestFCIndex, currentFilteredClustersWithin))
            else:
                for fcIndex in range (nFilteredClusters):
                    ivp_filteredClusters[fcIndex]['cuc'] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    ivp_filteredClusterEvents.append(('CREATED', fcIndex))
        else:
            #[1]: Construct historical cluster sources
            for csIndex in range (nClusterSources): ivp_historicalClusters = [(csValue, 1) for csValue in ivp_clusterSources]

            #[2]: Construct un-identified filtered clusters
            ivp_filteredClusters = [{'cs': historicalCluster[0], 'cuc': None, 'ct': 'ivp'} for historicalCluster in ivp_historicalClusters]
            #--- BLE (Bollinger Enhancement)
            if (useBLE == True):
                for bolCode in [analysisCode for analysisCode in klineAccess if analysisCode[:3] == 'BOL']:
                    for bolLineValue in klineAccess[bolCode][timestamp]: ivp_filteredClusters.append({'cs': bolLineValue, 'cuc': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), 'ct': 'ble'})
            #--- Sort the constructed un-identified filtered clusters
            ivp_filteredClusters.sort(key = lambda x: x['cs'])
            nFilteredClusters = len(ivp_filteredClusters)

            #[3]: Determine filteredCluster Events and assign cuc (cluster unique color)
            for fcIndex in range (nFilteredClusters):
                ivp_filteredClusters[fcIndex]['cuc'] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                ivp_filteredClusterEvents.append(('CREATED', fcIndex))
        
        #Determine Anchor Cluster
        #---Determine currently contacted cluster
        klinePriceRanger = (targetKline_lowPrice, targetKline_highPrice)
        contactedClusterIndex      = None
        firstContactedClusterFound = False
        nFilteredClusters = len(ivp_filteredClusters)
        for fcIndex, cluster in enumerate(ivp_filteredClusters):
            clusterSource = cluster['cs']
            if (fcIndex == 0):
                if (nFilteredClusters == 1):       clusterRegion = (0,                                                                                                         dCeiling)
                else:                              clusterRegion = (0,                                                                                                         round((ivp_filteredClusters[fcIndex]['cs']+ivp_filteredClusters[fcIndex+1]['cs'])/2, precisions['price']))
            elif (fcIndex == nFilteredClusters-1): clusterRegion = (round((ivp_filteredClusters[fcIndex-1]['cs']+ivp_filteredClusters[fcIndex]['cs'])/2, precisions['price']), dCeiling)
            else:                                  clusterRegion = (round((ivp_filteredClusters[fcIndex-1]['cs']+ivp_filteredClusters[fcIndex]['cs'])/2, precisions['price']), round((ivp_filteredClusters[fcIndex]['cs']+ivp_filteredClusters[fcIndex+1]['cs'])/2, precisions['price']))
        
            d_ToBottom = clusterSource-clusterRegion[0]
            d_ToTop    = clusterRegion[1]-clusterSource

            clusterSourceRanger = (round(clusterSource-d_ToBottom*ANCHORRANGERFACTOR, precisions['price']), round(clusterSource+d_ToTop*ANCHORRANGERFACTOR, precisions['price']))
            #Check for overlap
            overlapClassification = 0
            if (0 <= clusterSourceRanger[0]-klinePriceRanger[0]): overlapClassification += 0b1000
            if (0 <= clusterSourceRanger[0]-klinePriceRanger[1]): overlapClassification += 0b0100
            if (0 <  clusterSourceRanger[1]-klinePriceRanger[0]): overlapClassification += 0b0010
            if (0 <  clusterSourceRanger[1]-klinePriceRanger[1]): overlapClassification += 0b0001
            if ((overlapClassification != 0b0000) and (overlapClassification != 0b1111)): #Overlap Detected
                contactedClusterIndex = fcIndex
                if (firstContactedClusterFound == False): firstContactedClusterFound = True
                else:                                     break

        #---Determine what happened to the previous anchor cluster, if existed
        previousIVP_anchorClusterIndex      = None
        previousIVP_anchorClusterIndex_prev = None
        if (previousAnalysisExists == True):
            previousIVP_anchorClusterIndex      = klineAccess['IVP'][timestamp_previous]['anchorClusterIndex']
            previousIVP_anchorClusterIndex_prev = klineAccess['IVP'][timestamp_previous]['anchorClusterIndex_prev']
            #Cluster Events
            #('CREATED',      newClusterIndex)                                              #New cluster created
            #('DESTROYED',    previousClusterIndex, nextClusterIndex)                       #Previously existing cluster destroyed
            #('INDEXUPDATED', previousClusterIndex, newClusterIndex)                        #ClusterNumber updated
            #('VALUEUPDATED', previousClusterIndex, newClusterExtrema)                      #ClusterSource position updated
            #('SPLITED',      previousClusterIndex, nearestClusterIndex, newClusterNumbers) #Cluster Splitted, previousClusterIndex, nearestNewClusterIndex to the previous source, and all of newly generated cluster numbers
            if (previousIVP_anchorClusterIndex != None):
                for clusterEvent in ivp_filteredClusterEvents:
                    if (clusterEvent[1] == previousIVP_anchorClusterIndex):
                        eventType = clusterEvent[0] #What happened to the previous anchor cluster
                        if ((eventType == 'DESTROYED') or (eventType == 'INDEXUPDATED') or (eventType == 'SPLITED')): previousIVP_anchorClusterIndex = clusterEvent[2]
                        break
            if (previousIVP_anchorClusterIndex_prev != None):
                for clusterEvent in ivp_filteredClusterEvents:
                    if (clusterEvent[1] == previousIVP_anchorClusterIndex_prev):
                        eventType = clusterEvent[0] #What happened to the previous anchor cluster
                        if ((eventType == 'DESTROYED') or (eventType == 'INDEXUPDATED') or (eventType == 'SPLITED')): previousIVP_anchorClusterIndex_prev = clusterEvent[2]
                        break
                
        #Anchor Cluster Events
        #0: Anchor Cluster Same
        #1: Anchor Cluster Updated
        if (contactedClusterIndex == None):
            if (previousIVP_anchorClusterIndex == None): anchorClusterIndex = None;                           anchorClusterIndex_prev = None                                #None     -> None
            else:                                        anchorClusterIndex = previousIVP_anchorClusterIndex; anchorClusterIndex_prev = previousIVP_anchorClusterIndex_prev #Not None -> None (Use Previous)
            anchorClusterUpdated = False
        else:
            if   (previousIVP_anchorClusterIndex == None):                  anchorClusterUpdated = True;  anchorClusterIndex_prev = None                                    #None -> Not None (New Anchor Found)
            elif (contactedClusterIndex == previousIVP_anchorClusterIndex): anchorClusterUpdated = False; anchorClusterIndex_prev = previousIVP_anchorClusterIndex_prev     #Same Anchor Cluster
            else:                                                           anchorClusterUpdated = True;  anchorClusterIndex_prev = previousIVP_anchorClusterIndex          #New  Anchor Cluster
            anchorClusterIndex = contactedClusterIndex

        #Prepare Major Events to Report
        eventsReport = list()
        if (anchorClusterUpdated == True): eventsReport.append("UPDATED_AC")

        #Save IVP Result
        if (analysisMode == 0):
            #Record & Reference Only
            gammaFactor_effective = round(betaFactor_effective/targetKline_closePrice, 4)
            #Result Formatting & Save
            ivpResult = {'ivp_raw': ivp, 'ivp_raw_max': ivp_rawMax, 'divisionHeight': divisionHeight, 'gammaFactor_effective': gammaFactor_effective, 'betaFactor_effective': betaFactor_effective,
                            'ivp_clusteringIndex_beg': dIndex_clusteringRange_beg, 'ivp_clusteringIndex_end': dIndex_clusteringRange_end,
                            'ivp_historicalClusters': ivp_historicalClusters, 'ivp_filteredClusters': ivp_filteredClusters, 'ivp_filteredClusterEvents': ivp_filteredClusterEvents, 
                            'anchorClusterIndex': anchorClusterIndex, 'anchorClusterIndex_prev': anchorClusterIndex_prev, 'anchorClusterUpdated': anchorClusterUpdated,
                            'EVENTS': eventsReport}
            try:    klineAccess[analysisCode][timestamp] = ivpResult
            except: klineAccess[analysisCode] = {timestamp: ivpResult}
        elif (analysisMode == 1): klineAccess[analysisCode][timestamp]['ivp_filteredClusterEvents'] = ivp_filteredClusterEvents

        #Return True to indicate successful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate IVP analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))
    
def analysisGenerator_PIP(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    PIP_REFERREDANALYSISTYPES = set(['PSAR', 'IVP', 'MMACD'])
    PIP_DECISIONMAKERREGIONFACTOR = 0.2
    PIP_MINPOTENTIALPROFIT = 0.005
    
    #try:
    analysisCode = 'PIP'
    timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)
    previousAnalysisExists = (('PIP' in klineAccess) and (timestamp_previous in klineAccess['PIP']))
    
    #Result data instantiation
    pip_type          = None
    pip_entrancePoint = None
    pip_exitPoint     = None
    
    targetKline = klineAccess['raw'][timestamp]
    targetKline_closePrice = targetKline[KLINDEX_CLOSEPRICE]

    #Get Existing Analysis List
    referredAnalysisCodes = dict()
    for existingAnalysisCode in klineAccess:
        analysisType = existingAnalysisCode.split("_")[0]
        if (analysisType in PIP_REFERREDANALYSISTYPES):
            if (analysisType in referredAnalysisCodes): referredAnalysisCodes[analysisType].append(existingAnalysisCode)
            else:                                       referredAnalysisCodes[analysisType] = [existingAnalysisCode]
    
    if ('IVP' in referredAnalysisCodes):
        #If anchorCluster exists, check if the current price is within the decisionMakerRegion
        ivp_filteredClusters     = klineAccess['IVP'][timestamp]['ivp_filteredClusters']
        ivp_anchorClusterIndex   = klineAccess['IVP'][timestamp]['anchorClusterIndex']
        if (ivp_anchorClusterIndex != None):
            if ((0 < ivp_anchorClusterIndex) and (ivp_anchorClusterIndex < len(ivp_filteredClusters)-1)):
                cs_anchor   = ivp_filteredClusters[ivp_anchorClusterIndex]['cs']
                cs_upward   = ivp_filteredClusters[ivp_anchorClusterIndex+1]['cs']
                cs_downward = ivp_filteredClusters[ivp_anchorClusterIndex-1]['cs']
                decisionMakerRegion = (cs_anchor-(cs_anchor-cs_downward)*PIP_DECISIONMAKERREGIONFACTOR, cs_anchor+(cs_upward-cs_anchor)*PIP_DECISIONMAKERREGIONFACTOR)
                if ((decisionMakerRegion[0] <= targetKline_closePrice) and (targetKline_closePrice <= decisionMakerRegion[1])):
                    ca_directivityPoint = 0

                    #PSAR Voting
                    if ('PSAR' in referredAnalysisCodes):
                        for psarCode in referredAnalysisCodes['PSAR']:
                            if (klineAccess[psarCode][timestamp]['PDReversed'] == True):
                                if (klineAccess[psarCode][timestamp]['PD'] == True): ca_directivityPoint += 1
                                else:                                                ca_directivityPoint -= 1
                
                    #MMACD Voting
                    if ('MMACD' in referredAnalysisCodes):
                        if (klineAccess['MMACD'][timestamp]['polarityReversed'] == True):
                            if (klineAccess['MMACD'][timestamp]['msDeltaMAMomentum_polarity'] == True): ca_directivityPoint += 1
                            else:                                                                       ca_directivityPoint -= 1

                    #DirectivityPoint Evaluation
                    if (1 <= ca_directivityPoint):
                        pip_type = 'buy'
                        pip_entrancePoint = ivp_filteredClusters[ivp_anchorClusterIndex]['cs']
                        pip_exitPoint     = ivp_filteredClusters[ivp_anchorClusterIndex+1]['cs']

                    elif (ca_directivityPoint <= -1):
                        pip_type = 'sell'
                        pip_entrancePoint = ivp_filteredClusters[ivp_anchorClusterIndex]['cs']
                        pip_exitPoint     = ivp_filteredClusters[ivp_anchorClusterIndex-1]['cs']

    if ((pip_type == None) and (previousAnalysisExists == True)):
        if (('IVP' in referredAnalysisCodes) and (klineAccess['IVP'][timestamp]['anchorClusterUpdated'] == False)):
            pip_type = klineAccess['PIP'][timestamp_previous]['type']
            pip_entrancePoint = klineAccess['PIP'][timestamp_previous]['entrancePoint']
            pip_exitPoint     = klineAccess['PIP'][timestamp_previous]['exitPoint']

    #Analysis Result Formatting
    pipResult = {'type': pip_type, 'entrancePoint': pip_entrancePoint, 'exitPoint': pip_exitPoint}

    #Save PIP
    try:    klineAccess[analysisCode][timestamp] = pipResult
    except: klineAccess[analysisCode] = {timestamp: pipResult}

    #Return True to indicate successful analysis generation
    return True
    #except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate VIP analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red')); return False

def analysisGenerator_VOL(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        valueType = analysisParams['valueType']
        volType   = analysisParams['volType']
        if   (volType == 'BASE'):    volAccessIndex = KLINDEX_VOLBASE;          effectivePrecision = precisions['quantity']
        elif (volType == 'QUOTE'):   volAccessIndex = KLINDEX_VOLQUOTE;         effectivePrecision = precisions['quote']
        elif (volType == 'BASETB'):  volAccessIndex = KLINDEX_VOLBASETAKERBUY;  effectivePrecision = precisions['quantity']
        elif (volType == 'QUOTETB'): volAccessIndex = KLINDEX_VOLQUOTETAKERBUY; effectivePrecision = precisions['quote']

        if (valueType == 0):
            analysisCode = 'VOL'
            kline = klineAccess['raw'][timestamp]
            volResult = {'valueType': 0, 'value': kline[volAccessIndex]}

            #Save VOL
            try:    klineAccess[analysisCode][timestamp] = volResult
            except: klineAccess[analysisCode] = {timestamp: volResult}
            #Return True to indicate successful analysis generation
            return True

        elif (valueType == 'SMA'):
            nSamples = analysisParams['nSamples']
            analysisCode = 'VOL_SMA_{:d}'.format(nSamples)
            timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)

            #Calculate SMA
            #[1]: Previous SMA exists
            if ((analysisCode in klineAccess) and (timestamp_previous in klineAccess[analysisCode])):
                timestamp_expired = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -nSamples)
                previousVolSum = klineAccess[analysisCode][timestamp_previous]['value']*nSamples
                newVolSum      = previousVolSum - klineAccess['raw'][timestamp_expired][volAccessIndex] + klineAccess['raw'][timestamp][volAccessIndex]
                sma = round(newVolSum / nSamples, effectivePrecision)
            #[2]: Previous SMA does not exist
            else:
                timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples, direction = False, mrktReg = mrktRegTS)
                volSum = 0
                for ts in timestampsList: volSum += klineAccess['raw'][ts][volAccessIndex]
                sma = round(volSum / nSamples, effectivePrecision)

            #Save volMAResult
            volMAResult = {'valueType': 1, 'value': sma}
            try:    klineAccess[analysisCode][timestamp] = volMAResult
            except: klineAccess[analysisCode] = {timestamp: volMAResult}
            #Return True to indicate successful analysis generation
            return True

        elif (valueType == 'WMA'):
            nSamples = analysisParams['nSamples']
            analysisCode = 'VOL_WMA_{:d}'.format(nSamples)
            timestampsList = ATM_Zeta_Auxillaries.getTimestampList_byNTicks(intervalID = intervalID, timestamp = timestamp, nTicks = nSamples+1, direction = False, mrktReg = mrktRegTS)
        
            #Calculate WMA (WMA cannot gain any processing speed improvement by refering to the previous WMA)
            baseSum = nSamples*(nSamples+1)/2
            weightedSum = 0
            for index, ts in enumerate(timestampsList): weightedSum += klineAccess['raw'][ts][volAccessIndex]*(nSamples-index)
            wma = round(weightedSum/baseSum, effectivePrecision)
    
            #Save volMAResult
            volMAResult = {'valueType': 1, 'value': wma}
            try:    klineAccess[analysisCode][timestamp] = volMAResult
            except: klineAccess[analysisCode] = {timestamp: volMAResult}
            #Return True to indicate succesfful analysis generation
            return True

        elif (valueType == 'EMA'):
            nSamples = analysisParams['nSamples']
            kValue   = 2/(nSamples+1)
            analysisCode = 'VOL_EMA_{:d}'.format(nSamples)
            timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)

            #Calculate EMA
            #[1]: Previous EMA exists
            if ((analysisCode in klineAccess) and (timestamp_previous in klineAccess[analysisCode])): ema = round((klineAccess['raw'][timestamp][volAccessIndex]*kValue) + (klineAccess[analysisCode][timestamp_previous]['value']*(1-kValue)), effectivePrecision)
            #[2]: Previous EMA does not Exist
            else:
                smaCode = 'VOL_SMA_{:d}'.format(nSamples)
            #[2-1]: Previous SMA does exist
                if ((smaCode in klineAccess) and (timestamp_previous in klineAccess[smaCode])): ema = round((klineAccess['raw'][timestamp][volAccessIndex]*kValue) + (klineAccess[smaCode][timestamp_previous]['value']*(1-kValue)), precisions['price'])
            #[2-2]: Previous SMA does not exist
                else:
                    analysisParams_VOLSMA = {'valueType': 'SMA', 'volType': volType, 'nSamples': nSamples}
                    analysisGenerator_VOL(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp_previous, **analysisParams_VOLSMA)
                    ema = round((klineAccess['raw'][timestamp][volAccessIndex]*kValue) + (klineAccess[smaCode][timestamp_previous]['value']*(1-kValue)), precisions['price'])

            #Save EMA
            volMAResult = {'valueType': 1, 'value': ema}
            try:    klineAccess[analysisCode][timestamp] = volMAResult
            except: klineAccess[analysisCode] = {timestamp: volMAResult}
            #Return True to indicate succesfful analysis generation
            return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate VOL analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

def analysisGenerator_MMACD(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        signal_nSamples = analysisParams['signal_nSamples']
        signal_kValue   = 2/(signal_nSamples+1)

        msDeltaMA_nSamples = analysisParams['msDeltaMA_nSamples']
        msDeltaMA_kValue   = 2/(msDeltaMA_nSamples+1)

        activatedMAs     = analysisParams['activatedMAs']
        activatedMACodes = analysisParams['activatedMACodes']
        nActivatedMAs = len(activatedMAs)

        analysisCode = 'MMACD'
        timestamp_previous = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = intervalID, timestamp = timestamp, mrktReg = mrktRegTS, nTicks = -1)
        previousAnalysisExists = (('MMACD' in klineAccess) and (timestamp_previous in klineAccess['MMACD']))
        
        #Sort Activated MA Intervals and generate maPairs
        maPairs = list()
        for maPairTargetIndex_short in range (0, nActivatedMAs-1):
            for maPairTargetIndex_long in range (maPairTargetIndex_short+1, nActivatedMAs):
                maPairs.append((maPairTargetIndex_short, maPairTargetIndex_long))

        #Check MA result existences and generate any non-existing
        for maIndex in range (nActivatedMAs):
            maCode = activatedMACodes[maIndex]
            if (not((maCode in klineAccess) and (timestamp in klineAccess[maCode])) or (analysisMode == 1)):
                analysisParams_MA = {'nSamples': activatedMAs[maIndex]}
                analysisGenerator_EMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)

        #Compute current mmacd (Sum of maPair Deltas)
        maPairDeltaSum = 0
        for maPair in maPairs: maPairDeltaSum += klineAccess[activatedMACodes[maPair[0]]][timestamp] - klineAccess[activatedMACodes[maPair[1]]][timestamp]
        mmacd = round(maPairDeltaSum, precisions['price'])

        #Compute signal, msDeltaMA, msDeltaMAMomentum, and msDeltaMAMomentum_polarity
        if (previousAnalysisExists == True): 
            mmacd_prev = klineAccess['MMACD'][timestamp_previous]

            signal    = round((mmacd*signal_kValue) + (mmacd_prev['mmacd']*(1-signal_kValue)), precisions['price'])
            msDeltaMA = round(((mmacd-signal)*msDeltaMA_kValue) + (mmacd_prev['msDeltaMA']*(1-msDeltaMA_kValue)), precisions['price'])
            msDeltaMAMomentum = round(msDeltaMA-mmacd_prev['msDeltaMA'], precisions['price'])

            #[1]: msDeltaMAMomentum Polarity has not been determined yet
            if (mmacd_prev['msDeltaMAMomentum_polarity'] == None):
                if (0 <= msDeltaMAMomentum): msDeltaMAMomentum_polarity = True
                else:                        msDeltaMAMomentum_polarity = False
                prRefValue                 = msDeltaMAMomentum
                polarityReversed           = False
            #[2]: msDeltaMAMomentum Polarity has been determined, check for the rawPolarity of the current msDeltaMAMomentum
            else:
                msDeltaMAMomentum_rawPolarity = (0 <= msDeltaMAMomentum)
                #[2-1]: Polarity of the previous msDeltaMAMomentum and the rawPolarity of the current msDeltaMAMomentum are the same
                if (msDeltaMAMomentum_rawPolarity == mmacd_prev['msDeltaMAMomentum_polarity']):
                    msDeltaMAMomentum_polarity = mmacd_prev['msDeltaMAMomentum_polarity']
                    prRefValue                 = msDeltaMAMomentum
                    polarityReversed           = False
                #[2-2]: Polarity of the previous msDeltaMAMomentum and the rawPolarity of the current msDeltaMAMomentum are different, check for polarity reversal
                else:
                    if (mmacd_prev['msDeltaMAMomentum_polarity'] == True):
                        #[2-2-1]: Polarity Reversal Occurred (Positive -> Negative)
                        if (msDeltaMAMomentum <= -mmacd_prev['prRefValue']*0.3):
                            msDeltaMAMomentum_polarity = False
                            prRefValue                 = msDeltaMAMomentum
                            polarityReversed           = True
                        #[2-2-2]: Polarity Reversal Not Occurred (Positive -> Positive)
                        else:
                            msDeltaMAMomentum_polarity = mmacd_prev['msDeltaMAMomentum_polarity']
                            prRefValue                 = mmacd_prev['prRefValue']
                            polarityReversed           = False
                    else:
                        #[2-2-3]: Polarity Reversal Occurred (Negative -> Positive)
                        if (-mmacd_prev['prRefValue']*0.3 <= msDeltaMAMomentum):
                            msDeltaMAMomentum_polarity = True
                            prRefValue                 = msDeltaMAMomentum
                            polarityReversed           = True
                        #[2-2-4]: Polarity Reversal Not Occurred (Negative -> Negative)
                        else:
                            msDeltaMAMomentum_polarity = mmacd_prev['msDeltaMAMomentum_polarity']
                            prRefValue                 = mmacd_prev['prRefValue']
                            polarityReversed           = False
        else:                                
            signal    = round(mmacd, precisions['price'])
            msDeltaMA = round(mmacd-signal, precisions['price'])
            msDeltaMAMomentum          = 0
            msDeltaMAMomentum_polarity = None
            prRefValue                 = None
            polarityReversed           = False
        
        #Prepare Major Events to Report
        eventsReport = list()
        if (polarityReversed == True):
            if (msDeltaMAMomentum_polarity == True): eventsReport.append("MMACD <REV_INCREMENTAL>")
            else:                                    eventsReport.append("MMACD <REV_DECREMENTAL>")

        #Analysis Result Formatting
        mmacdResult = {'mmacd': mmacd, 'signal': signal, 'msDeltaMA': msDeltaMA, 'msDeltaMAMomentum': msDeltaMAMomentum, 'msDeltaMAMomentum_polarity': msDeltaMAMomentum_polarity, 'prRefValue': prRefValue, 'polarityReversed': polarityReversed, 'EVENTS': eventsReport}
            
        #Save SMA
        try:    klineAccess[analysisCode][timestamp] = mmacdResult
        except: klineAccess[analysisCode] = {timestamp: mmacdResult}

        #Return True to indicate successful analysis generation
        return True
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate MMACD analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))
    
def analysisGenerator_DMIxADX(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        #Return True to indicate successful analysis generation
        return None
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate SMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))
    
def analysisGenerator_MFI(analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
    try:
        #Return True to indicate successful analysis generation
        return None
    except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate SMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))