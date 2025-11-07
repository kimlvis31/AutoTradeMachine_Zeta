from GUIs import ATM_Zeta_GUI_TextControl, ATM_Zeta_GUI_AdvancedPygletGroups, ATM_Zeta_GUIO_Generals, ATM_Zeta_GUIO_ChartDrawers

import ATM_Zeta_Auxillaries

import pyglet
import pprint
import termcolor
import time
import random

from datetime import datetime, timezone, tzinfo

KLINE_INTERVALS                    = ('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1W', '1M')
KLINE_INTERVALS_CORRESPONDINGIDs   = {'1m': 0, '3m': 1, '5m': 2, '15m': 3, '30m': 4, '1h': 5, '2h': 6, '4h': 7, '6h': 8, '8h': 9, '12h': 10, '1d': 11, '3d': 12, '1W': 13, '1M': 14}
KLINE_INTERVALS_CORRESPONDINGTEXTs = {0: '1m', 1: '3m', 2: '5m', 3: '15m', 4: '30m', 5: '1h', 6: '2h', 7: '4h', 8: '6h', 9: '8h', 10: '12h', 11: '1d', 12: '3d', 13: '1W', 14: '1M'}

def setupPage(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    initParams = {'pageInstance':        pageInstance,
                  'windowInstance':      windowInstance,
                  'systemFunctions':     systemFunctions,
                  'displaySpaceDefiner': displaySpaceDefiner,
                  'guioConfig':          guioConfig,
                  'imageManager':        imageManager,
                  'audioManager':        audioManager,
                  'visualManager':       visualManager,
                  'ipcA_MAIN_AUX':       ipcA_MAIN_AUX,
                  'ipcA_MAIN_ATM':       ipcA_MAIN_ATM}

    if   (pageInstance.pageName == "PROGRAMLOADING"):   __setup_PROGRAMLOADING(**initParams)
    elif (pageInstance.pageName == "DASHBOARD"):        __setup_DASHBOARD(**initParams)
    elif (pageInstance.pageName == "APIKEY"):           __setup_APIKEY(**initParams)
    elif (pageInstance.pageName == "ASSET"):            __setup_ASSET(**initParams)
    elif (pageInstance.pageName == "MARKET"):           __setup_MARKET(**initParams)
    elif (pageInstance.pageName == "SIMULATION"):       __setup_SIMULATION(**initParams)
    elif (pageInstance.pageName == "SIMULATIONRESULT"): __setup_SIMULATIONRESULT(**initParams)
    elif (pageInstance.pageName == "AUTOTRADE"):        __setup_AUTOTRADE(**initParams)
    elif (pageInstance.pageName == "SETTINGS"):         __setup_SETTINGS(**initParams)
    elif (pageInstance.pageName == "EXPERIMENT0"):      __setup_EXPERIMENT0(**initParams)
    elif (pageInstance.pageName == "EXPERIMENT1"):      __setup_EXPERIMENT1(**initParams)
    elif (pageInstance.pageName == "EXPERIMENT2"):      __setup_EXPERIMENT2(**initParams)
    elif (pageInstance.pageName == "EXPERIMENT3"):      __setup_EXPERIMENT3(**initParams)
    elif (pageInstance.pageName == "EXPERIMENT4"):      __setup_EXPERIMENT4(**initParams)
    




#PAGE-PROGRAMLOADING --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_PROGRAMLOADING(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL
    def ppf_PROGRAMLOADING(ppfVar, onLoad = False):
        initStep = ppfVar['INITSTEP']
        if (initStep == 'AUX'):
            if (ipcA_MAIN_AUX.getPRD('PROCSTATUS') == 'INITIALIZED'): 
                guios["INITSTATUS_TEXT"].updateText("INITIALIZING PROCESS CENTRAL")
                ppfVar['INITSTEP'] = 'CENTRAL'
                guios["INITSTATUS_GAUGEBAR"].updateGaugeValue(50)
        elif (initStep == 'CENTRAL'):
            if (ipcA_MAIN_ATM.getPRD('PROCSTATUS') == 'INITIALIZED'): 
                guios["INITSTATUS_TEXT"].updateText(visualManager.getTextPack('PROGRAMLOADING:CONTINUECOMMENT'))
                guios["INITSTATUS_GAUGEBAR"].updateGaugeValue(100)
                ppfVar['INITSTEP'] = 'COMPLETE'
                pageInstance.lastMouseInput = None
                pageInstance.lastKeyInput = None
                ipcA_MAIN_AUX.sendPRDEDIT("PROCCTRL_PROCGO", True, nMaxDispatch = 'INF')
                ipcA_MAIN_ATM.sendPRDEDIT("PROCCTRL_PROCGO", True, nMaxDispatch = 'INF')
        elif (initStep == 'COMPLETE'):
            if ((pageInstance.lastKeyInput != None) and (pageInstance.lastKeyInput['eType'] == 'PRESSED')): pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')

    pageInstance.pageProcessFunction = ppf_PROGRAMLOADING
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))
        
        guios["PROGRAMTITLE_TEXT"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,  groupOrder=1, xPos=100, yPos=4000, width=15800, height=1000, style=None, text="AUTO TRADE MACHINE ZETA",          fontSize = 300, textInteractable = False)
        guios["INITSTATUS_TEXT"]     = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,  groupOrder=1, xPos=100, yPos= 250, width=15800, height= 200, style=None, text="INITIALIZING PROCESS 'AUXILLARY'", fontSize = 120, textInteractable = False)
        guios["INITSTATUS_GAUGEBAR"] = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst, groupOrder=1, xPos=100, yPos= 100, width=15800, height= 100, style="styleB", align = 'horizontal', gaugeColor = (70, 150, 255, 255))

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-PROGRAMLOADING END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










#PAGE-DASHBOARD -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_DASHBOARD(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_SETTINGS(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_SETTINGS
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_SETTINGS(objectInstance, **kwargs):         pageInstance.sysFunctions['LOADPAGE']('SETTINGS')
    def objFunc_pageMove_APIKEY(objectInstance, **kwargs):           pageInstance.sysFunctions['LOADPAGE']('APIKEY')
    def objFunc_pageMove_ASSET(objectInstance, **kwargs):            pageInstance.sysFunctions['LOADPAGE']('ASSET')
    def objFunc_pageMove_MARKET(objectInstance, **kwargs):           pageInstance.sysFunctions['LOADPAGE']('MARKET')
    def objFunc_pageMove_SIMULATION(objectInstance, **kwargs):       pageInstance.sysFunctions['LOADPAGE']('SIMULATION')
    def objFunc_pageMove_SIMULATIONRESULT(objectInstance, **kwargs): pageInstance.sysFunctions['LOADPAGE']('SIMULATIONRESULT')
    def objFunc_pageMove_AUTOTRADE(objectInstance, **kwargs):        pageInstance.sysFunctions['LOADPAGE']('AUTOTRADE')

    def objFunc_show_NavText_APIKEY(objectInstance, **kwargs):           guios["NAVIGATION_TEXT_APIKEY"].show()
    def objFunc_hide_NavText_APIKEY(objectInstance, **kwargs):           guios["NAVIGATION_TEXT_APIKEY"].hide()
    def objFunc_show_NavText_ASSET(objectInstance, **kwargs):            guios["NAVIGATION_TEXT_ASSET"].show()
    def objFunc_hide_NavText_ASSET(objectInstance, **kwargs):            guios["NAVIGATION_TEXT_ASSET"].hide()
    def objFunc_show_NavText_MARKET(objectInstance, **kwargs):           guios["NAVIGATION_TEXT_MARKET"].show()
    def objFunc_hide_NavText_MARKET(objectInstance, **kwargs):           guios["NAVIGATION_TEXT_MARKET"].hide()
    def objFunc_show_NavText_SIMULATION(objectInstance, **kwargs):       guios["NAVIGATION_TEXT_SIMULATION"].show()
    def objFunc_hide_NavText_SIMULATION(objectInstance, **kwargs):       guios["NAVIGATION_TEXT_SIMULATION"].hide()
    def objFunc_show_NavText_AUTOTRADE(objectInstance, **kwargs):        guios["NAVIGATION_TEXT_AUTOTRADE"].show()
    def objFunc_hide_NavText_AUTOTRADE(objectInstance, **kwargs):        guios["NAVIGATION_TEXT_AUTOTRADE"].hide()
    def objFunc_show_NavText_SIMULATIONRESULT(objectInstance, **kwargs): guios["NAVIGATION_TEXT_SIMULATIONRESULT"].show()
    def objFunc_hide_NavText_SIMULATIONRESULT(objectInstance, **kwargs): guios["NAVIGATION_TEXT_SIMULATIONRESULT"].hide()
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))
        
        guios["DASHBOARD_TITLETEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('DASHBOARD:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_SETTINGS"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst, groupOrder=2, xPos=50, yPos=8650, width=300, height=300, style="styleB", releaseFunction=objFunc_pageMove_SETTINGS, image = 'settingsIcon_512x512.png', imageSize = (250, 250), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))

        
        guios["NAVIGATION_TEXT_APIKEY"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=2200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('APIKEY:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_APIKEY"].hide()
        guios["NAVIGATION_BUTTON_APIKEY"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=2200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                                releaseFunction=objFunc_pageMove_APIKEY, hoverFunction = objFunc_show_NavText_APIKEY, hoverEscapeFunction = objFunc_hide_NavText_APIKEY,
                                                                                image = 'apikeyIcon_512x512.png', imageSize = (1400, 1400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        guios["NAVIGATION_TEXT_ASSET"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=4200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('ASSET:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_ASSET"].hide()
        guios["NAVIGATION_BUTTON_ASSET"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=4200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                               releaseFunction=objFunc_pageMove_ASSET, hoverFunction = objFunc_show_NavText_ASSET, hoverEscapeFunction = objFunc_hide_NavText_ASSET,
                                                                               image = 'assetIcon_512x512.png', imageSize = (1400, 1400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        guios["NAVIGATION_TEXT_MARKET"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=6200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('MARKET:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_MARKET"].hide()
        guios["NAVIGATION_BUTTON_MARKET"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=6200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                                releaseFunction=objFunc_pageMove_MARKET, hoverFunction = objFunc_show_NavText_MARKET, hoverEscapeFunction = objFunc_hide_NavText_MARKET,
                                                                                image = 'marketIcon_512x512.png', imageSize = (1300, 1300), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        guios["NAVIGATION_TEXT_SIMULATION"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=8200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('SIMULATION:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_SIMULATION"].hide()
        guios["NAVIGATION_BUTTON_SIMULATION"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=8200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                                    releaseFunction=objFunc_pageMove_SIMULATION, hoverFunction = objFunc_show_NavText_SIMULATION, hoverEscapeFunction = objFunc_hide_NavText_SIMULATION,
                                                                                    image = 'simulationIcon_512x512.png', imageSize = (1400, 1400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        guios["NAVIGATION_TEXT_SIMULATIONRESULT"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=10200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('SIMULATIONRESULT:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_SIMULATIONRESULT"].hide()
        guios["NAVIGATION_BUTTON_SIMULATIONRESULT"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=10200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                                   releaseFunction=objFunc_pageMove_SIMULATIONRESULT, hoverFunction = objFunc_show_NavText_SIMULATIONRESULT, hoverEscapeFunction = objFunc_hide_NavText_SIMULATIONRESULT,
                                                                                   image = 'simulationResultIcon_512x512.png', imageSize = (1400, 1400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        guios["NAVIGATION_TEXT_AUTOTRADE"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=12200, yPos=3750, width=1600, height= 250, style=None, text=visualManager.getTextPack('AUTOTRADE:TITLE'), fontSize = 100, textInteractable = False); guios["NAVIGATION_TEXT_AUTOTRADE"].hide()
        guios["NAVIGATION_BUTTON_AUTOTRADE"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=12200, yPos=4000, width=1600, height=1600, style="styleB",
                                                                                   releaseFunction=objFunc_pageMove_AUTOTRADE, hoverFunction = objFunc_show_NavText_AUTOTRADE, hoverEscapeFunction = objFunc_hide_NavText_AUTOTRADE,
                                                                                   image = 'autotradeIcon_512x512.png', imageSize = (1400, 1400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))


    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-DASHBOARD END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-APIKEY ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_APIKEY(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_APIKEY(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_APIKEY
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["APIKEY_TITLETEXT"]            = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('APIKEY:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD, image = 'dashboardIcon_512x512.png', imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-APIKEY END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-ASEET -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_ASSET(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_ASSET(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_ASSET
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["ASSET_TITLETEXT"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('ASSET:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD, image = 'dashboardIcon_512x512.png', imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-ASSET END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-MARKET ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_MARKET(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #Initial Page Variables
    pageInstance.ppfVariables['LOADED_ASSETLIST']           = None
    pageInstance.ppfVariables['LOADED_ASSETLIST_FORMATTED'] = None
    pageInstance.ppfVariables['SELECTED_ASSETNAME']  = None
    pageInstance.ppfVariables['SELECTED_INTERVALID'] = 0
    
    pageInstance.ppfVariables['SELECTEDASSETDATA_status']                = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAlloc']              = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAllocMode']          = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_mrktRegTS']             = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_firstStreamedKlineTSs'] = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges_perc']       = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges']            = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_analyzing']             = None 

    #Page Timers
    pageInstance.ppfVariables['PAGETIMER_LISTUPDATECHECKER_LASTUPDATED'] = 0
    pageInstance.ppfVariables['PAGETIMER_LISTUPDATECHECKER_INTERVAL_MS'] = 1000

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def ppf_MARKET(ppfVar, onLoad = False):
        currentTime_ms = time.perf_counter_ns()/1e6
        if ((ppfVar['PAGETIMER_LISTUPDATECHECKER_INTERVAL_MS'] < currentTime_ms-ppfVar['PAGETIMER_LISTUPDATECHECKER_LASTUPDATED']) or (onLoad == True)):
            #Load Market Asset Data
            marketAssets = ipcA_MAIN_ATM.getPRD('MARKETASSETS')
            if (marketAssets == "#DNF#"):
                guios["MARKET_SELECTIONBOX_CURRENCYLIST"].setSelectionList([])
                ppfVar['LOADED_ASSETLIST']           = None
                ppfVar['LOADED_ASSETLIST_FORMATTED'] = None
                ppfVar['SELECTED_ASSETNAME'] = None
                ppfVar['SELECTEDASSETDATA']  = None
            else:
                #Filter the Market Asset List and update the selecitonBox object
                currentMarketAssetsList = list(marketAssets.keys()); currentMarketAssetsList.sort()
                if ((ppfVar['LOADED_ASSETLIST'] == None) or ((len(currentMarketAssetsList) != len(ppfVar['LOADED_ASSETLIST'])) and (currentMarketAssetsList != ppfVar['LOADED_ASSETLIST']))):
                    ppfVar['LOADED_ASSETLIST'] = currentMarketAssetsList

                    ppfVar['LOADED_ASSETLIST_FORMATTED'] = dict()
                    for assetName in ppfVar['LOADED_ASSETLIST']:
                        assetStatus = marketAssets[assetName]['status']
                        nAssetName  = len(assetName)
                        nStatusText = len(assetStatus)
                        if   (assetStatus == 'TRADING'):  statusColor = 'GREEN_LIGHT'
                        elif (assetStatus == 'SETTLING'): statusColor = 'RED_LIGHT'
                        else:                             statusColor = 'ORANGE_LIGHT'
                        ppfVar['LOADED_ASSETLIST_FORMATTED'][assetName] = {'text': "{:s} <{:s}>".format(assetName, assetStatus), 'textStyles': [((0, nAssetName), 'DEFAULT'), ((nAssetName+1, nAssetName+1+nStatusText+2), statusColor)], 'textAnchor': 'W'}

                    guios["MARKET_SELECTIONBOX_CURRENCYLIST"].setSelectionList(selectionList = ppfVar['LOADED_ASSETLIST_FORMATTED'], displayTargets = 'all')
                    # If the selected symbol no longer exists, reset the selection
                    if (ppfVar['SELECTED_ASSETNAME'] not in ppfVar['LOADED_ASSETLIST']): pass

                #Detect Symbol Information Change
                selectedSymbol     = ppfVar['SELECTED_ASSETNAME']
                selectedIntervalID = ppfVar['SELECTED_INTERVALID']
                if (selectedSymbol in marketAssets):
                    selectedAssetData = marketAssets[selectedSymbol]
                    status               = selectedAssetData['status']
                    rtaAlloc             = selectedAssetData['RTAAlloc']
                    rtaAllocMode         = selectedAssetData['RTAAllocMode']
                    mrktRegTS            = selectedAssetData['mrktRegTS'][selectedIntervalID]
                    firstStreamedKlineTS = selectedAssetData['firstStreamedKlineTSs'][selectedIntervalID]
                    dataRanges_perc      = selectedAssetData['dataRanges_perc'][selectedIntervalID]
                    dataRanges_blocks    = selectedAssetData['dataRanges'][selectedIntervalID]
                    analyzing            = selectedAssetData['analyzing']

                    #Currency Status
                    if (status != ppfVar['SELECTEDASSETDATA_status']):
                        if   (status == 'TRADING'):  guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'GREEN_LIGHT')
                        elif (status == 'SETTLING'): guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'RED_LIGHT')
                        else:                        guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'ORANGE_LIGHT')
                        ppfVar['SELECTEDASSETDATA_status'] = status

                    #RTA Allocation
                    if ((rtaAlloc != ppfVar['SELECTEDASSETDATA_RTAAlloc']) or (rtaAllocMode != ppfVar['SELECTEDASSETDATA_RTAAllocMode'])):
                        guios["MARKET_SELECTEDCURRENCY_RTAALLOCCONTENT"].updateText("{:s} / {:s}".format(str(rtaAlloc), str(rtaAllocMode)))
                        ppfVar['SELECTEDASSETDATA_RTAAlloc']     = rtaAlloc
                        ppfVar['SELECTEDASSETDATA_RTAAllocMode'] = rtaAllocMode

                    #MrktRegTS
                    if (mrktRegTS != ppfVar['SELECTEDASSETDATA_mrktRegTS']):
                        if (mrktRegTS == None): guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText("N/A")
                        else:                   guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText(datetime.fromtimestamp(mrktRegTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                        ppfVar['SELECTEDASSETDATA_mrktRegTS'] = mrktRegTS
                        
                    #First Streamed Kline TS
                    if (firstStreamedKlineTS != ppfVar['SELECTEDASSETDATA_firstStreamedKlineTSs']):
                        if (firstStreamedKlineTS == None): guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText("N/A")
                        else:                              guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText(datetime.fromtimestamp(firstStreamedKlineTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                        ppfVar['SELECTEDASSETDATA_firstStreamedKlineTSs'] = firstStreamedKlineTS

                    #DA Perc
                    if (dataRanges_perc != ppfVar['SELECTEDASSETDATA_dataRanges_perc']):
                        if   (dataRanges_perc == None): guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("N/A",                              'GREY_DARK')
                        elif (dataRanges_perc == 100):  guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("100 %",                            'GREEN_LIGHT')
                        else:                           guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("{:.3f} %".format(dataRanges_perc), 'ORANGE_LIGHT')
                        ppfVar['SELECTEDASSETDATA_dataRanges_perc'] = dataRanges_perc
                        
                    #DA Blocks
                    if (dataRanges_blocks != ppfVar['SELECTEDASSETDATA_dataRanges']):
                        if (dataRanges_blocks == None): guios["MARKET_SELECTEDCURRENCY_DATARANGESCONTENT"].updateText("N/A")
                        else:
                            if (1 < len(dataRanges_blocks)):
                                dataRanges_blocks_str = ""
                                for dataRanges_block in dataRanges_blocks: dataRanges_blocks_str += "({:s} ~ {:s})".format(datetime.fromtimestamp(dataRanges_block[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_block[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                            elif (len(dataRanges_blocks) == 1):            dataRanges_blocks_str = "{:s} ~ {:s}".format(datetime.fromtimestamp(dataRanges_blocks[0][0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_blocks[0][1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                            else:                                          dataRanges_blocks_str = "-"
                            guios["MARKET_SELECTEDCURRENCY_DATARANGESCONTENT"].updateText(dataRanges_blocks_str)
                        ppfVar['SELECTEDASSETDATA_dataRanges'] = dataRanges_blocks
                    
                    #Analyzing
                    if (analyzing != ppfVar['SELECTEDASSETDATA_analyzing']):
                        if (analyzing == True): guios["MARKET_SELECTEDCURRENCY_ANALYZINGCONTENT"].updateText("TRUE",  'GREEN_LIGHT')
                        else:                   guios["MARKET_SELECTEDCURRENCY_ANALYZINGCONTENT"].updateText("FALSE", 'RED_LIGHT')
                        ppfVar['SELECTEDASSETDATA_analyzing'] = analyzing

                #SelectedSymbol no longer exists in the market data
                else:
                    ppfVar['SELECTEDASSETDATA_status']                = None
                    ppfVar['SELECTEDASSETDATA_RTAAlloc']              = None
                    ppfVar['SELECTEDASSETDATA_RTAAllocMode']          = None
                    ppfVar['SELECTEDASSETDATA_mrktRegTS']             = None
                    ppfVar['SELECTEDASSETDATA_firstStreamedKlineTSs'] = None
                    ppfVar['SELECTEDASSETDATA_dataRanges_perc']       = None
                    ppfVar['SELECTEDASSETDATA_dataRanges']            = None
                    ppfVar['SELECTEDASSETDATA_analyzing']             = None

                    #guios["MARKET_SELECTEDCURRENCY_CURRENCYNAMECONTENT"].updateText(selectedAssetName)
                    #guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText("TRUE")

            ppfVar['PAGETIMER_LISTUPDATECHECKER_LASTUPDATED'] = currentTime_ms

    pageInstance.pageProcessFunction = ppf_MARKET
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #PAGE LOAD FUNCTION ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def plf_MARKET(ppfVar):
        ppf_MARKET(ppfVar, onLoad = True)

    pageInstance.pageLoadFunction = plf_MARKET
    #PAGE LOAD FUNCTION END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')
        
        

    #Upon Currency Name Search Text Update
    def objFunc_currencyNameSearchTextUpdated(objectInstance, **kwargs):
        tibText = guios["MARKET_TEXTINPUTBOX_CURRENCYLIST"].getText()
        if (tibText == ""): filteredList = 'all'
        else:               filteredList = [asset for asset in pageInstance.ppfVariables['LOADED_ASSETLIST'] if tibText in asset]
        guios["MARKET_SELECTIONBOX_CURRENCYLIST"].setDisplayTargets(filteredList)


    #Upon New Currency Selection
    def objFunc_newCurrencySelected(objectInstance, **kwargs):
        selectedItems = objectInstance.getSelected()
        try:    selectedAssetName = selectedItems[0]
        except: selectedAssetName = None

        if (selectedAssetName != None): 
            #Read and update the selected currency name
            pageInstance.ppfVariables['SELECTED_ASSETNAME'] = selectedAssetName
            guios["MARKET_SELECTEDCURRENCY_CURRENCYNAMECONTENT"].updateText(selectedAssetName)
            
            marketAssetData = ipcA_MAIN_ATM.getPRD(('MARKETASSETS', selectedAssetName))
            pageInstance.ppfVariables['SELECTEDASSETDATA'] = marketAssetData
            status = marketAssetData['status']
            RTAAlloc = marketAssetData['RTAAlloc']; RTAAllocMode = marketAssetData['RTAAllocMode']
            mrktRegTS = marketAssetData['mrktRegTS'][pageInstance.ppfVariables['SELECTED_INTERVALID']]; firstStreamedKlineTS = marketAssetData['firstStreamedKlineTSs'][pageInstance.ppfVariables['SELECTED_INTERVALID']]
            analyzing = marketAssetData['analyzing']
            dataRanges_perc = marketAssetData['dataRanges_perc'][pageInstance.ppfVariables['SELECTED_INTERVALID']]
            
            #Update the Asset Data Texts
            guios["MARKET_SELECTEDCURRENCY_RTAALLOCCONTENT"].updateText("{:s} / {:s}".format(str(RTAAlloc), str(RTAAllocMode)))
            
            if   (status == 'TRADING'):  guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'GREEN_LIGHT')
            elif (status == 'SETTLING'): guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'RED_LIGHT')
            else:                        guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'ORANGE_LIGHT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_status'] = status

            if (mrktRegTS == None): guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText("N/A")
            else:                   guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText(datetime.fromtimestamp(mrktRegTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
            pageInstance.ppfVariables['SELECTEDASSETDATA_mrktRegTS'] = mrktRegTS
            
            if (firstStreamedKlineTS == None): guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText("N/A")
            else:                              guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText(datetime.fromtimestamp(firstStreamedKlineTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
            pageInstance.ppfVariables['SELECTEDASSETDATA_firstStreamedKlineTSs'] = firstStreamedKlineTS
            
            if   (dataRanges_perc == None): guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("N/A",                              'GREY_DARK')
            elif (dataRanges_perc == 100):  guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("100 %",                            'GREEN_LIGHT')
            else:                           guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("{:.3f} %".format(dataRanges_perc), 'ORANGE_LIGHT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges_perc'] = dataRanges_perc

            if (analyzing == True): guios["MARKET_SELECTEDCURRENCY_ANALYZINGCONTENT"].updateText("TRUE",  'GREEN_LIGHT')
            else:                   guios["MARKET_SELECTEDCURRENCY_ANALYZINGCONTENT"].updateText("FALSE", 'RED_LIGHT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_analyzing'] = analyzing

            pprint.pprint(marketAssetData)
            guios["MARKET_SELECTEDCURRENCY_KDRCHECKBUTTON"].activate()
            guios["MARKET_SELECTEDCURRENCY_LOADBUTTON"].activate()

    #Upon New Interval Selection
    def objFunc_newIntervalSelected(objectInstance, **kwargs):
        selectedIntervalID = objectInstance.getSelected()
        pageInstance.ppfVariables['SELECTED_INTERVALID'] = selectedIntervalID
        if (pageInstance.ppfVariables['SELECTED_ASSETNAME'] != None):
            #Get Asset Data via PRD
            marketAssetData = ipcA_MAIN_ATM.getPRD(('MARKETASSETS', pageInstance.ppfVariables['SELECTED_ASSETNAME']))
            pageInstance.ppfVariables['SELECTEDASSETDATA'] = marketAssetData
            RTAAlloc        = marketAssetData['RTAAlloc']; RTAAllocMode = marketAssetData['RTAAllocMode']
            mrktRegTS       = marketAssetData['mrktRegTS'][pageInstance.ppfVariables['SELECTED_INTERVALID']]; firstStreamedKlineTS = marketAssetData['firstStreamedKlineTSs'][pageInstance.ppfVariables['SELECTED_INTERVALID']]
            dataRanges_perc = marketAssetData['dataRanges_perc'][pageInstance.ppfVariables['SELECTED_INTERVALID']]
        
            #Update the Asset Data Texts
            guios["MARKET_SELECTEDCURRENCY_RTAALLOCCONTENT"].updateText("{:s} / {:s}".format(str(RTAAlloc), str(RTAAllocMode)))
            if (mrktRegTS == None): guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText("N/A")
            else:                   guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"].updateText(datetime.fromtimestamp(mrktRegTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
            
            if (firstStreamedKlineTS == None): guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText("N/A")
            else:                              guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"].updateText(datetime.fromtimestamp(firstStreamedKlineTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
            
            if (dataRanges_perc == None): guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("N/A")
            else:                         guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"].updateText("{:.3f} %".format(dataRanges_perc))

            

    #Upon Load Button Activation
    def objFunc_performKDRC_responseHandler(objectInstance, **kwargs):
        guios["MARKET_SELECTEDCURRENCY_KDRCHECKBUTTON"].activate()
        guios["MARKET_SELECTEDCURRENCY_LOADBUTTON"].activate()

    #Upon Load Button Activation
    def objFunc_performKDRC(objectInstance, **kwargs):
        selectedAssetName  = pageInstance.ppfVariables['SELECTED_ASSETNAME']
        selectedIntervalID = pageInstance.ppfVariables['SELECTED_INTERVALID']
        if ((selectedAssetName != None) and (selectedIntervalID != None)):
            ipcA_MAIN_ATM.sendFAR(functionID = "REQUESTKLINEDEEPRANGECHECK", 
                                  functionParams = {'apiSymbol':                 selectedAssetName,
                                                    'intervalID':                selectedIntervalID,
                                                    'recalculateDownloadRanges': True},
                                  FARRHandler = objFunc_performKDRC_responseHandler, nMaxDispatch = 'INF')
            guios["MARKET_SELECTEDCURRENCY_KDRCHECKBUTTON"].deactivate()
            guios["MARKET_SELECTEDCURRENCY_LOADBUTTON"].deactivate()

    #Upon Load Button Activation
    def objFunc_loadCurrenyKlines(objectInstance, **kwargs):
        selectedAssetName  = pageInstance.ppfVariables['SELECTED_ASSETNAME']
        selectedIntervalID = pageInstance.ppfVariables['SELECTED_INTERVALID']
        if ((selectedAssetName != None) and (selectedIntervalID != None)):
            guios["MARKET_CHARTDRAWER"].setTarget(apiSymbol = selectedAssetName, intervalID = selectedIntervalID)



    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["MARKET_TITLETEXT"]            = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('MARKET:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD, image = 'dashboardIcon_512x512.png', imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        #Currency List & Selection
        guios["MARKET_WRAPPER_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos= 100, yPos=8300, width=3200, height= 200, style="styleA", text = visualManager.getTextPack('MARKET:BINANCEUSDM'))
        guios["MARKET_TEXTBOX_CURRENCYSEARCH"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,           groupOrder=1, xPos= 100, yPos=8000, width= 800, height= 250, style="styleA", text=visualManager.getTextPack('MARKET:SEARCH'), textInteractable = True, fontSize = 80)
        guios["MARKET_TEXTINPUTBOX_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,      groupOrder=1, xPos=1000, yPos=8000, width=2300, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_currencyNameSearchTextUpdated)
        guios["MARKET_SELECTIONBOX_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos=3600, width=3200, height=4300, style="styleA", fontSize = 80, elementHeight = 250, multiSelect = False, singularSelect_allowRelease = False, showIndex = True, selectionUpdateFunction = objFunc_newCurrencySelected)
        
        #Currency Information
        #---Interval Selection
        guios["MARKET_SELECTEDCURRENCY_INTERVALTEXT"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos=3250, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:INTERVAL'), textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_INTERVALSELECTIONBOX"] = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst, groupOrder=2, xPos=1100, yPos=3250, width=2200, height=250, style="styleA", nDisplay = 5, selectionUpdateFunction = objFunc_newIntervalSelected, fontSize = 80)
        intervalSelectionList = { 0: {'text': '1m'},   1: {'text': '3m'},  2: {'text': '5m'},  3: {'text': '15m'}, 4: {'text': '30m'},
                                  5: {'text': '1h'},   6: {'text': '2h'},  7: {'text': '4h'},  8: {'text': '6h'},  9: {'text':  '8h'},
                                 10: {'text': '12h'}, 11: {'text': '1d'}, 12: {'text': '3d'}, 13: {'text': '1W'}, 14: {'text':  '1M'}}
        guios["MARKET_SELECTEDCURRENCY_INTERVALSELECTIONBOX"].setSelectionList(selectionList = intervalSelectionList, displayTargets = 'all')
        guios["MARKET_SELECTEDCURRENCY_INTERVALSELECTIONBOX"].setSelected(itemKey = pageInstance.ppfVariables['SELECTED_INTERVALID'], callSelectionUpdateFunction = False)
        #---Currency Name
        guios["MARKET_SELECTEDCURRENCY_CURRENCYNAME"]          = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=2900, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:CURRENCYNAME'),          textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_CURRENCYNAMECONTENT"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=2900, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Currency Name
        guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUS"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=2550, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:CURRENCYSTATUS'),        textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=2550, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---RTA Allocation
        guios["MARKET_SELECTEDCURRENCY_RTAALLOC"]              = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=2200, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:RTAALLOC'),              textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_RTAALLOCCONTENT"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=2200, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Market Registration Timestamp / Stream Begin Timestamp
        guios["MARKET_SELECTEDCURRENCY_MRKTREGTS"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1850, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:MRKTREGTS'),             textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_MRKTREGTSCONTENT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=1850, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Stream Begin Timestamp
        guios["MARKET_SELECTEDCURRENCY_STREAMBEGTS"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1500, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:STREAMBEGTS'),           textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_STREAMBEGTSCONTENT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=1500, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Analyzing
        guios["MARKET_SELECTEDCURRENCY_ANALYZING"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1150, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:ANALYZING'),             textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_ANALYZINGCONTENT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos=1150, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Data Status
        guios["MARKET_SELECTEDCURRENCY_DATASTATUS"]            = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos= 800, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:DATASTATUS'),            textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_DATASTATUSCONTENT"]     = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos= 800, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Data Ranges
        guios["MARKET_SELECTEDCURRENCY_DATARANGES"]            = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos= 450, width= 900, height=250, style="styleA", text=visualManager.getTextPack('MARKET:DATAAVAILABILITYRANGE'), textInteractable = True, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_DATARANGESCONTENT"]     = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1100, yPos= 450, width=2200, height=250, style="styleA", text="-",                                                       textInteractable = True, fontSize = 80)
        #---Perform KDRC (Klines Deep Range Check)
        guios["MARKET_SELECTEDCURRENCY_KDRCHECKBUTTON"]        = ATM_Zeta_GUIO_Generals.button_typeA(**inst,  groupOrder=1, xPos= 100, yPos= 100, width=1550, height=250, style="styleA", text=visualManager.getTextPack('MARKET:PERFORMKLINESDEEPRANGECHECK'), releaseFunction = objFunc_performKDRC, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_KDRCHECKBUTTON"].deactivate()
        #---Currency Load Button
        guios["MARKET_SELECTEDCURRENCY_LOADBUTTON"]            = ATM_Zeta_GUIO_Generals.button_typeA(**inst,  groupOrder=1, xPos=1750, yPos= 100, width=1550, height=250, style="styleA", text=visualManager.getTextPack('MARKET:LOAD'),                        releaseFunction = objFunc_loadCurrenyKlines, fontSize = 80)
        guios["MARKET_SELECTEDCURRENCY_LOADBUTTON"].deactivate()

        #Currency Chart View
        guios["MARKET_WRAPPER_CHARTVIEW"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos=3400, yPos=8300, width=12500, height=200, style="styleA", text = visualManager.getTextPack('MARKET:CHARTVIEW'))
        
        guios["MARKET_CHARTDRAWER"] = ATM_Zeta_GUIO_ChartDrawers.chartDrawer_typeA(**inst, groupOrder=1, xPos=3400, yPos=100, width=12500, height=8150, style="styleA", name = 'MARKETCHARTDRAWER')

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-MARKET END ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-SIMULATION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_SIMULATION(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #Initial Page Variables
    #---Currency List
    pageInstance.ppfVariables['DBCONNECTED'] = False

    pageInstance.ppfVariables['LOADED_ASSETLIST']   = None
    pageInstance.ppfVariables['SELECTED_ASSETNAME'] = None

    pageInstance.ppfVariables['SELECTEDASSETDATA_mrktRegTS']            = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges_perc']      = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges']           = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAlloc']             = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAllocMode']         = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_firstStreamedKlineTS'] = None
    pageInstance.ppfVariables['SELECTEDASSETDATA_status']               = None


    #---Simulator
    pageInstance.ppfVariables['LOADED_SIMULATIONLIST_PROCESSING'] = None
    pageInstance.ppfVariables['LOADED_SIMULATIONLIST_COMPLETED']  = None
    pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING'] = None
    pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED']  = None
    pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = None

    pageInstance.ppfVariables['SIMULATOR_CURRENTMSG']            = None
    pageInstance.ppfVariables['SIMULATOR_CURRENTANALYSISTARGET'] = None
    pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = None
    pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = None
    pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = None
    pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = None
    pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_RESULTTYPE']              = None
    
    pageInstance.ppfVariables['SIMULATIONADDREQUESTSENT'] = False
    pageInstance.ppfVariables['SIMULATIONCONFIGURATION'] = {'simulationCode':            None,
                                                            'simulationCodeAutoReplace': True,
                                                            'simulationRange_RealTime':  False,
                                                            'simulationRange':           (None, None),
                                                            'findVIPs':                  False,
                                                            'simulateTrading':           False,
                                                            'resultType':                None}
    pageInstance.ppfVariables['DB_ANALYSISSAVEAVAILABLE'] = False

    pageInstance.ppfVariables['SIMULATION_RUNNING'] = False
    
    #---Page Timers
    pageInstance.ppfVariables['PAGETIMER_DBCONNECTIONCHECKER_LASTUPDATED'] = 0
    pageInstance.ppfVariables['PAGETIMER_DBCONNECTIONCHECKER_INTERVAL_MS'] = 500

    pageInstance.ppfVariables['PAGETIMER_CURRENCYLISTUPDATECHECKER_LASTUPDATED'] = 0
    pageInstance.ppfVariables['PAGETIMER_CURRENCYLISTUPDATECHECKER_INTERVAL_MS'] = 1000
    
    pageInstance.ppfVariables['PAGETIMER_SIMULATIONLISTUPDATECHECKER_LASTUPDATED'] = 0
    pageInstance.ppfVariables['PAGETIMER_SIMULATIONLISTUPDATECHECKER_INTERVAL_MS'] = 20
    
    pageInstance.ppfVariables['PAGETIMER_SIMULATIONRUNNINGCHECK_LASTUPDATED'] = 0
    pageInstance.ppfVariables['PAGETIMER_SIMULATIONRUNNINGCHECK_INTERVAL_MS'] = 100

    #PAGE AUXILLARY FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def convertToTimestamp(formattedSimRange):
        try:
            if ((len(formattedSimRange) == 16) and (formattedSimRange[4] == '/') and (formattedSimRange[7] == '/') and (formattedSimRange[10] == ' ') and (formattedSimRange[13] == ':')):
                simRange_ts = datetime(year = int(formattedSimRange[0:4]), month = int(formattedSimRange[5:7]), day = int(formattedSimRange[8:10]), hour = int(formattedSimRange[11:13]), minute = int(formattedSimRange[14:16]), tzinfo = timezone.utc).timestamp()
                return int(simRange_ts)
        except: return None
    
    def onConfigurationUpdate(updatedConfig):
        if (updatedConfig == "DBCONNECTION"):
            pass
        
        elif (updatedConfig == "CURRENCY"):
            onConfigurationUpdate("SIMRANGE_REALTIME")

        elif (updatedConfig == "SIMRANGE_REALTIME"):
            switchStatus = guios["SIMULATION_SWITCH_REALTIMESIMULATION"].getStatus() 
            if (switchStatus == True):
                #Configuration Update & Object Setup
                pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationRange_RealTime'] = True
                guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE1"].deactivate()
            else:
                #Configuration Update & Object Setup
                pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationRange_RealTime'] = False
                guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE1"].activate()
            #Simulation Range Check
            onConfigurationUpdate("SIMRANGE")

        elif (updatedConfig == "SIMRANGE"):
            isRealTime = pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationRange_RealTime']
            if (isRealTime == True):
                simRange0_ts = convertToTimestamp(guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE0"].getText())
                if (simRange0_ts != None):
                    pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationRange'] = (simRange0_ts, None)
                    if (pageInstance.ppfVariables['SELECTED_ASSETNAME'] != None): guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].activate()
                else: guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].deactivate()
            else:
                simRange0_ts = convertToTimestamp(guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE0"].getText())
                simRange1_ts = convertToTimestamp(guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE1"].getText())
                if ((simRange0_ts != None) and (simRange1_ts != None) and (simRange0_ts < simRange1_ts)):
                    pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationRange'] = (simRange0_ts, simRange1_ts)
                    if (pageInstance.ppfVariables['SELECTED_ASSETNAME'] != None): guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].activate()
                else: guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].deactivate()

        elif (updatedConfig == "SIMCODE"):
            simCode = guios["SIMULATION_TEXTINPUTBOX_CUSTOMSIMULATIONCODECONTENT"].getText()
            if (simCode == ""): pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationCode'] = None
            else:               pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationCode'] = simCode

        elif (updatedConfig == "SIMCODE_AUTOREPLACE"):
            switchStatus = guios["SIMULATION_SWITCH_SIMULATIONCODEAUTOREPLACE"].getStatus() 
            if (switchStatus == True): pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationCodeAutoReplace'] = True
            else:                      pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationCodeAutoReplace'] = False

        elif (updatedConfig == "RESULTTYPE"):
            pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['resultType'] = guios["SIMULATION_SELECTIONBOX_RESULTTYPECONFIG"].getSelected()

        elif (updatedConfig == "FINDVIPS"):
            switchStatus = guios["SIMULATION_SWITCH_FINDVIPS"].getStatus()
            pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['findVIPs'] = switchStatus

        elif (updatedConfig == "SIMULATETRADING"):
            switchStatus = guios["SIMULATION_SWITCH_SIMULATETRADING"].getStatus() 
            pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulateTrading'] = switchStatus

    def onSimulatorMessageReceival(functionParams):
        guios["SIMULATION_TEXTBOX_SIMULATORMESSAGECONTENT"].updateText(functionParams['simulatorMsg'])

    def displaySimulationInfo(simulationCode, simulationStatus):
        if (simulationCode == None):
            pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = None
            pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = None
            pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = None
            pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = None
            pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_RESULTTYPE']              = None
            
            guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText("-")
            guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("-")
            guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("-")
            guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText("-")
            guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("-")
            guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText("-")
        else:
            if (simulationStatus == 'PROCESSING'):
                #Get Simulation Data via PRD
                simulationData = ipcA_MAIN_AUX.getPRD(('SIMULATIONS_PROCESSING', simulationCode))
                simulationRange             = simulationData['simulationRange']
                simulationRange_realTime    = simulationData['simulationRange_realTime']
                simulationProcess_perc      = simulationData['simulationProcess_perc']
                simulationProcess_percTotal = simulationData['simulationProcess_percTotal']
                simulationProcess           = simulationData['simulationProcess']
                estimatedCompletionTime     = simulationData['estimatedCompletionTime']
                resultType                  = simulationData['resultType']
                pprint.pprint(simulationData)

                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = simulationRange
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = simulationProcess_perc
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = simulationProcess
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = estimatedCompletionTime
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_RESULTTYPE']              = resultType

                #Update the Asset Simulation Data Texts
                #---Selected SimCode
                guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText(simulationCode)
                #---Simulation Range
                if (simulationRange_realTime == True): guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ ".format(datetime.fromtimestamp(simulationRange[0],  tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                else:                                  guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ {:s}".format(datetime.fromtimestamp(simulationRange[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(simulationRange[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                #---Simulation Completion Percentage
                if (simulationProcess_perc == None):
                    if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / - %")
                    else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / {:.1f} %".format(simulationProcess_percTotal))
                else:
                    if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / - %".format(simulationProcess_perc))
                    else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / {:.1f} %".format(simulationProcess_perc, simulationProcess_percTotal))
                #---Current Process
                guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText(simulationProcess)
                #---Estimated Completion Time
                if (estimatedCompletionTime == None): guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("N/A")
                else:                                 guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText(ATM_Zeta_Auxillaries.timeStringFormatter(int(estimatedCompletionTime/1e9)))
                #---Result Type
                guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText(resultType)

            elif (simulationStatus == 'COMPLETED'):
                #Get Simulation Data via PRD
                simulationData = ipcA_MAIN_AUX.getPRD(('SIMULATIONS_COMPLETED', simulationCode))
                simulationRange             = simulationData['simulationRange']
                simulationProcess_perc      = None
                simulationProcess_percTotal = None
                simulationProcess           = simulationData['resultSummary']
                estimatedCompletionTime     = None
                resultType                  = simulationData['resultType']
                pprint.pprint(simulationData)

                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = simulationRange
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = simulationProcess_perc
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = simulationProcess
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = estimatedCompletionTime
                pageInstance.ppfVariables['SELECTEDSIMULATIONDATA_RESULTTYPE']              = resultType
                
                #Update the Asset Simulation Data Texts
                #---Selected SimCode
                guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText(simulationCode)
                #---Simulation Range
                if (simulationRange[1] == None): guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ ".format(datetime.fromtimestamp(simulationRange[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                else:                            guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ {:s}".format(datetime.fromtimestamp(simulationRange[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(simulationRange[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                #---Simulation Completion Percentage
                guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("-")
                #---Current Process
                guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText(simulationProcess)
                #---Estimated Completion Time
                guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("-")
                #---Result Type
                guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText(resultType)


                
    #PAGE AUXILLARY FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_SIMULATION(ppfVar, onLoad = False):
        currentTime_ms = time.perf_counter_ns()/1e6
        #DB Connection Checker
        if ((ppfVar['PAGETIMER_DBCONNECTIONCHECKER_INTERVAL_MS'] < currentTime_ms-ppfVar['PAGETIMER_DBCONNECTIONCHECKER_LASTUPDATED']) or (onLoad == True)):
            if (ppfVar['DBCONNECTED'] == True):
                #Connected -> Connected (Do nothing)
                if (ipcA_MAIN_ATM.getPRD(("DBSTATUS", 'connected')) == True): pass
                #Connected -> Disconnected
                else:
                    ppfVar['DBCONNECTED'] = False
                    onConfigurationUpdate("DBCONNECTION")
            else:
                #Disconnected -> Connected
                if (ipcA_MAIN_ATM.getPRD(("DBSTATUS", 'connected')) == True):
                    ppfVar['DBCONNECTED'] = True
                    onConfigurationUpdate("DBCONNECTION")
                #Disconnected -> Disconnected (Do nothing)
                else: pass
                
            ppfVar['PAGETIMER_DBCONNECTIONCHECKER_LASTUPDATED'] = currentTime_ms

        #Currency List Update Checker
        if ((ppfVar['PAGETIMER_CURRENCYLISTUPDATECHECKER_INTERVAL_MS'] < currentTime_ms-ppfVar['PAGETIMER_CURRENCYLISTUPDATECHECKER_LASTUPDATED']) or (onLoad == True)):
            #Load Market Asset Data
            marketAssets = ipcA_MAIN_ATM.getPRD('MARKETASSETS')
            if (marketAssets == "#DNF#"):
                guios["MARKET_SELECTIONBOX_CURRENCYLIST"].updateSelectionList(list())
                ppfVar['LOADED_ASSETLIST']   = None
                ppfVar['SELECTED_ASSETNAME'] = None
                ppfVar['SELECTEDASSETDATA_mrktRegTS']            = None
                ppfVar['SELECTEDASSETDATA_dataRanges_perc']      = None
                ppfVar['SELECTEDASSETDATA_dataRanges']           = None
                ppfVar['SELECTEDASSETDATA_RTAAlloc']             = None
                ppfVar['SELECTEDASSETDATA_RTAAllocMode']         = None
                ppfVar['SELECTEDASSETDATA_firstStreamedKlineTS'] = None
            else:
                #Filter the Market Asset List and update the selecitonBox object
                currentMarketAssetsList = list(marketAssets.keys()); currentMarketAssetsList.sort()
                if ((ppfVar['LOADED_ASSETLIST'] == None) or ((len(currentMarketAssetsList) != len(ppfVar['LOADED_ASSETLIST'])) and (currentMarketAssetsList != ppfVar['LOADED_ASSETLIST']))):
                    ppfVar['LOADED_ASSETLIST'] = currentMarketAssetsList
                    #Compute display targets
                    searchText = guios["SIMULATION_TEXTINPUTBOX_CURRENCYLIST"].getText()
                    if (searchText == ""): displayTargets = 'all'
                    else:                  displayTargets = [sim for sim in ppfVar['LOADED_ASSETLIST'] if searchText in sim]
                    #Format selectionList
                    selectionListFormatted = dict()
                    for apiSymbol in ppfVar['LOADED_ASSETLIST']:
                        daPercentage = marketAssets[apiSymbol]['dataRanges_perc'][0]
                        if   (daPercentage == None): daPercentage_str = "< N/A >";                           percColor = 'GREY_DARK'
                        elif (daPercentage == 100):  daPercentage_str = "< 100 % >";                         percColor = 'GREEN_LIGHT'
                        else:                        daPercentage_str = "< {:.3f} % >".format(daPercentage); percColor = 'ORANGE_LIGHT'
                        nAssetName        = len(apiSymbol)
                        nDAPercentage_str = len(daPercentage_str)
                        selectionListFormatted[apiSymbol] = {'text': "{:s} {:s}".format(apiSymbol, daPercentage_str), 'textStyles': [((0, nAssetName), 'DEFAULT'), ((nAssetName+1, nAssetName+1+nDAPercentage_str), percColor)], 'textAnchor': 'W'}

                    #Update selectionList
                    guios["SIMULATION_SELECTIONBOX_CURRENCYLIST"].setSelectionList(selectionList = selectionListFormatted, displayTargets = displayTargets)
                    # If the selected symbol no longer exists, reset the selection
                    if (ppfVar['SELECTED_ASSETNAME'] not in ppfVar['LOADED_ASSETLIST']): pass
                else:
                    beg = time.perf_counter_ns()
                    for apiSymbol in marketAssets:
                        daPercentage = marketAssets[apiSymbol]['dataRanges_perc'][0]
                        if   (daPercentage == None): daPercentage_str = "< N/A >";                           percColor = 'GREY_DARK'
                        elif (daPercentage == 100):  daPercentage_str = "< 100 % >";                         percColor = 'GREEN_LIGHT'
                        else:                        daPercentage_str = "< {:.3f} % >".format(daPercentage); percColor = 'ORANGE_LIGHT'
                        effectiveText = "{:s} {:s}".format(apiSymbol, daPercentage_str)
                        if (effectiveText != guios["SIMULATION_SELECTIONBOX_CURRENCYLIST"].getSelectionListItemInfo(apiSymbol)['text']):
                            nAssetName        = len(apiSymbol)
                            nDAPercentage_str = len(daPercentage_str)
                            guios["SIMULATION_SELECTIONBOX_CURRENCYLIST"].editSelectionListItem(apiSymbol, {'text': effectiveText, 'textStyles': [((0, nAssetName), 'DEFAULT'), ((nAssetName+1, nAssetName+1+nDAPercentage_str), percColor)], 'textAnchor': 'W'})

                    end = time.perf_counter_ns()
                    print("{:.3f} us".format((end-beg)/1e3))

                #Detect Symbol Information Change
                selectedSymbol = ppfVar['SELECTED_ASSETNAME']
                if (selectedSymbol in marketAssets):
                    selectedAssetData = marketAssets[selectedSymbol]
                    #Update mrktRegTS
                    if (selectedAssetData['mrktRegTS'][0] != ppfVar['SELECTEDASSETDATA_mrktRegTS']):
                        mrktRegTS = selectedAssetData['mrktRegTS'][0]
                        if (mrktRegTS == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINECONTENT"].updateText("-")
                        else:                   guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINECONTENT"].updateText(datetime.fromtimestamp(mrktRegTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                        ppfVar['SELECTEDASSETDATA_mrktRegTS'] = mrktRegTS
                        
                    #Update Data Ranges Percentage
                    if (selectedAssetData['dataRanges_perc'][0] != ppfVar['SELECTEDASSETDATA_dataRanges_perc']):
                        dataRanges_perc = selectedAssetData['dataRanges_perc'][0]
                        if   (dataRanges_perc == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("N/A",                              'GREY_DARK')
                        elif (dataRanges_perc == 100):  guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("100 %",                            'GREEN_LIGHT')
                        else:                           guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("{:.3f} %".format(dataRanges_perc), 'ORANGE_LIGHT')
                        ppfVar['SELECTEDASSETDATA_dataRanges_perc'] = dataRanges_perc

                    #Update Data Ranges
                    dataRanges_ATM  = selectedAssetData['dataRanges'][0]
                    dataRanges_MAIN = ppfVar['SELECTEDASSETDATA_dataRanges']
                    if (dataRanges_ATM != dataRanges_MAIN):
                        if (dataRanges_ATM == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGESCONTENT"].updateText("N/A")
                        else:
                            if (1 < len(dataRanges_ATM)):
                                dataRanges_blocks_str = ""
                                for dataRanges_block in dataRanges_ATM: dataRanges_blocks_str += "({:s} ~ {:s})".format(datetime.fromtimestamp(dataRanges_block[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_block[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                            elif (len(dataRanges_ATM) == 1):            dataRanges_blocks_str = "{:s} ~ {:s}".format(datetime.fromtimestamp(dataRanges_ATM[0][0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_ATM[0][1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                            else:                                       dataRanges_blocks_str = "-"
                            guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGESCONTENT"].updateText(dataRanges_blocks_str)
                        ppfVar['SELECTEDASSETDATA_dataRanges'] = dataRanges_ATM.copy()

                    #Update RTA Allocation
                    if ((selectedAssetData['RTAAlloc'] != ppfVar['SELECTEDASSETDATA_RTAAlloc']) or (selectedAssetData['RTAAllocMode'] != ppfVar['SELECTEDASSETDATA_RTAAllocMode'])):
                        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_RTAALLOCCONTENT"].updateText("{:s} / {:s}".format(str(selectedAssetData['RTAAlloc']), str(selectedAssetData['RTAAllocMode'])))
                        ppfVar['SELECTEDASSETDATA_RTAAlloc']     = selectedAssetData['RTAAlloc']
                        ppfVar['SELECTEDASSETDATA_RTAAllocMode'] = selectedAssetData['RTAAllocMode']
                        
                    #Update Streaming
                    if (selectedAssetData['firstStreamedKlineTSs'][0] != ppfVar['SELECTEDASSETDATA_firstStreamedKlineTS']):
                        firstStreamedKlineTS = selectedAssetData['firstStreamedKlineTSs'][0]
                        if (firstStreamedKlineTS == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMINGCONTENT"].updateText("FALSE")
                        else:                              guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMINGCONTENT"].updateText(datetime.fromtimestamp(firstStreamedKlineTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                        ppfVar['SELECTEDASSETDATA_firstStreamedKlineTS'] = firstStreamedKlineTS

                    #Update Status
                    if (selectedAssetData['status'] != ppfVar['SELECTEDASSETDATA_status']):
                        status = selectedAssetData['status']
                        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status)
                        ppfVar['SELECTEDASSETDATA_status'] = status

                else:
                    ppfVar['SELECTEDASSETDATA_mrktRegTS']            = None
                    ppfVar['SELECTEDASSETDATA_dataRanges_perc']      = None
                    ppfVar['SELECTEDASSETDATA_dataRanges']           = None
                    ppfVar['SELECTEDASSETDATA_RTAAlloc']             = None
                    ppfVar['SELECTEDASSETDATA_RTAAllocMode']         = None
                    ppfVar['SELECTEDASSETDATA_firstStreamedKlineTS'] = None
                    ppfVar['SELECTEDASSETDATA_status'] = None

            ppfVar['PAGETIMER_CURRENCYLISTUPDATECHECKER_LASTUPDATED'] = currentTime_ms
            
        #Simulation List Update Checker
        if ((ppfVar['PAGETIMER_SIMULATIONLISTUPDATECHECKER_INTERVAL_MS'] < currentTime_ms-ppfVar['PAGETIMER_SIMULATIONLISTUPDATECHECKER_LASTUPDATED']) or (onLoad == True)):
            #Update Current Processing Target
            currentAnalysis = ipcA_MAIN_AUX.getPRD('CURRENTANALYSIS')
            if (ppfVar['SIMULATOR_CURRENTANALYSISTARGET'] != currentAnalysis):
                if ((currentAnalysis == None) or (currentAnalysis == '#DNF#')): guios["SIMULATION_TEXTBOX_CURRENTANALYZINGCONTENT"].updateText("-")
                else:                                                           guios["SIMULATION_TEXTBOX_CURRENTANALYZINGCONTENT"].updateText(currentAnalysis)
                ppfVar['SIMULATOR_CURRENTANALYSISTARGET'] = currentAnalysis

            #Update Processing Simulation List
            simulations_processing = ipcA_MAIN_AUX.getPRD('SIMULATIONS_PROCESSING')
            if (simulations_processing == "#DNF#"):
                guios["SIMULATION_SELECTIONBOX_PROCESSINGSIMULATIONLIST"].updateSelectionList(list())
                ppfVar['LOADED_SIMULATIONLIST_PROCESSING']   = None
                ppfVar['SELECTED_SIMULATIONCODE_PROCESSING'] = None
                ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = None
                ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = None
                ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = None
                ppfVar['SELECTEDSIMULATIONDATA_RESULTTYPE']              = None
            else:
                currentProcessingSimulationsList = list(simulations_processing.keys())
                if ((ppfVar['LOADED_SIMULATIONLIST_PROCESSING'] == None) or ((len(currentProcessingSimulationsList) != len(ppfVar['LOADED_SIMULATIONLIST_PROCESSING'])) and (currentProcessingSimulationsList != ppfVar['LOADED_SIMULATIONLIST_PROCESSING']))):
                    ppfVar['LOADED_SIMULATIONLIST_PROCESSING'] = currentProcessingSimulationsList
                    #Compute display targets
                    searchText = guios["SIMULATION_TEXTINPUTBOX_PROCESSINGSIMULATIONLIST"].getText()
                    if (searchText == ""): displayTargets = 'all'
                    else:                  displayTargets = [sim for sim in ppfVar['LOADED_SIMULATIONLIST_PROCESSING'] if searchText in sim]
                    #Format selectionList
                    selectionListFormatted = dict()
                    for simCode in ppfVar['LOADED_SIMULATIONLIST_PROCESSING']: selectionListFormatted[simCode] = {'text': simCode, 'textAnchor': 'W'}
                    #Update selectionList
                    guios["SIMULATION_SELECTIONBOX_PROCESSINGSIMULATIONLIST"].setSelectionList(selectionList = selectionListFormatted, displayTargets = displayTargets, keepSelected = True)
                    # If the selected simulation no longer exists, reset the selection
                    if (ppfVar['SELECTED_SIMULATIONCODE_PROCESSING'] not in ppfVar['LOADED_SIMULATIONLIST_PROCESSING']):
                        ppfVar['SELECTED_SIMULATIONCODE_PROCESSING'] = None
                        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].deactivate()
                        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].deactivate()
                    
            #Update Completed Simulation List
            simulations_completed = ipcA_MAIN_AUX.getPRD('SIMULATIONS_COMPLETED')
            if (simulations_completed == "#DNF#"):
                guios["SIMULATION_SELECTIONBOX_COMPLETEDSIMULATIONLIST"].updateSelectionList(list())
                ppfVar['LOADED_SIMULATIONLIST_COMPLETED']   = None
                ppfVar['SELECTED_SIMULATIONCODE_COMPLETED'] = None
            else:
                currentCompletedSimulationsList = list(simulations_completed.keys())
                if ((ppfVar['LOADED_SIMULATIONLIST_COMPLETED'] == None) or ((len(currentCompletedSimulationsList) != len(ppfVar['LOADED_SIMULATIONLIST_COMPLETED'])) and (currentCompletedSimulationsList != ppfVar['LOADED_SIMULATIONLIST_COMPLETED']))):
                    ppfVar['LOADED_SIMULATIONLIST_COMPLETED'] = currentCompletedSimulationsList
                    #Compute display targets
                    searchText = guios["SIMULATION_TEXTINPUTBOX_COMPLETEDSIMULATIONLIST"].getText()
                    if (searchText == ""): displayTargets = 'all'
                    else:                  displayTargets = [sim for sim in ppfVar['LOADED_SIMULATIONLIST_COMPLETED'] if searchText in sim]
                    #Format selectionList
                    selectionListFormatted = dict()
                    for simCode in ppfVar['LOADED_SIMULATIONLIST_COMPLETED']: selectionListFormatted[simCode] = {'text': simCode, 'textAnchor': 'W'}
                    #Update selectionList
                    guios["SIMULATION_SELECTIONBOX_COMPLETEDSIMULATIONLIST"].setSelectionList(selectionList = selectionListFormatted, displayTargets = displayTargets, keepSelected = True)
                    # If the selected simulation no longer exists, reset the selection
                    if (ppfVar['SELECTED_SIMULATIONCODE_COMPLETED'] not in ppfVar['LOADED_SIMULATIONLIST_COMPLETED']):
                        ppfVar['SELECTED_SIMULATIONCODE_COMPLETED'] = None
                        guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].deactivate()
                    
            #Selected Simulation Information
            if ((ppfVar['SELECTED_PROCESSINGORCOMPLETED'] == "PROCESSING") and (simulations_processing != "#DNF#")):
                selectedSimulationCode = ppfVar['SELECTED_SIMULATIONCODE_PROCESSING']
                #If the selected target is still in the list
                if (selectedSimulationCode in simulations_processing):
                    selectedSimulationData = simulations_processing[selectedSimulationCode]
                    #Update Current Completion
                    if (ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION'] != selectedSimulationData['simulationProcess_perc']):
                        simulationProcess_perc      = selectedSimulationData['simulationProcess_perc']
                        simulationProcess_percTotal = selectedSimulationData['simulationProcess_percTotal']
                        if (simulationProcess_perc == None):
                            if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / - %")
                            else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / {:.1f} %".format(simulationProcess_percTotal))
                        else:
                            if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / - %".format(simulationProcess_perc))
                            else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / {:.1f} %".format(simulationProcess_perc, simulationProcess_percTotal))
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION'] = simulationProcess_perc

                    #Update Current Process
                    if (ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS'] != selectedSimulationData['simulationProcess']):
                        currentProcess = selectedSimulationData['simulationProcess']
                        guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText(str(currentProcess))
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS'] = currentProcess

                    #Update Estimated Completion Time
                    if (ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] != selectedSimulationData['estimatedCompletionTime']):
                        ect = selectedSimulationData['estimatedCompletionTime']
                        if (ect == None): guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("N/A")
                        else:             guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText(ATM_Zeta_Auxillaries.timeStringFormatter(int(ect/1e9)))
                        ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = ect
                #If the selected target is no longer in the list
                else:
                    #If there exists another target in the list
                    if (0 < len(currentProcessingSimulationsList)):
                        nextSimulationCode = currentProcessingSimulationsList[0]
                        nextSimulationData = simulations_processing[nextSimulationCode]

                        guios["SIMULATION_SELECTIONBOX_PROCESSINGSIMULATIONLIST"].addSelectedByText(nextSimulationCode)
                        
                        simulationRange             = nextSimulationData['simulationRange']
                        simulationRange_realTime    = nextSimulationData['simulationRange_realTime']
                        simulationProcess_perc      = nextSimulationData['simulationProcess_perc']
                        simulationProcess_percTotal = nextSimulationData['simulationProcess_percTotal']
                        simulationProcess           = nextSimulationData['simulationProcess']
                        estimatedCompletionTime     = nextSimulationData['estimatedCompletionTime']
                        resultType                  = nextSimulationData['resultType']


                        ppfVar['SELECTED_SIMULATIONCODE_PROCESSING']             = nextSimulationCode
                        ppfVar['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = simulationRange
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = simulationProcess_perc
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = simulationProcess
                        ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = estimatedCompletionTime
                        ppfVar['SELECTEDSIMULATIONDATA_RESULTTYPE']              = resultType

                        guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText(nextSimulationCode)
                        if (simulationRange_realTime == True): guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ ".format(datetime.fromtimestamp(simulationRange[0],  tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                        else:                                  guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("{:s} ~ {:s}".format(datetime.fromtimestamp(simulationRange[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(simulationRange[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M")))
                        if (simulationProcess_perc == None):
                            if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / - %")
                            else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("- % / {:.1f} %".format(simulationProcess_percTotal))
                        else:
                            if (simulationProcess_percTotal == None): guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / - %".format(simulationProcess_perc))
                            else:                                     guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("{:.3f} % / {:.1f} %".format(simulationProcess_perc, simulationProcess_percTotal))
                        guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText(simulationProcess)
                        if (estimatedCompletionTime == None): guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("N/A")
                        else:                                 guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText(ATM_Zeta_Auxillaries.timeStringFormatter(estimatedCompletionTime))
                        guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText(resultType)
                        
                    #If the list is now empty
                    else:
                        ppfVar['SELECTED_SIMULATIONCODE_PROCESSING']             = None
                        ppfVar['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = None
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = None
                        ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = None
                        ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = None
                        ppfVar['SELECTEDSIMULATIONDATA_RESULTTYPE']              = None
                    
                        guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText("-")
                        guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("-")
                        guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("-")
                        guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText("-")
                        guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("-")
                        guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText("-")

            elif ((ppfVar['SELECTED_PROCESSINGORCOMPLETED'] == "COMPLETED") and (simulations_processing != "#DNF#")):
                selectedSimulationCode = ppfVar['SELECTED_SIMULATIONCODE_COMPLETED']
                if (selectedSimulationCode not in simulations_completed):
                    ppfVar['SELECTED_SIMULATIONCODE_COMPLETED']              = None
                    ppfVar['SELECTEDSIMULATIONDATA_SIMULATIONRANGE']         = None
                    ppfVar['SELECTEDSIMULATIONDATA_CURRENTCOMPLETION']       = None
                    ppfVar['SELECTEDSIMULATIONDATA_CURRENTPROCESS']          = None
                    ppfVar['SELECTEDSIMULATIONDATA_ESTIMATEDCOMPLETIONTIME'] = None
                    ppfVar['SELECTEDSIMULATIONDATA_RESULTTYPE']              = None
                    
                    guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"].updateText("-")
                    guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"].updateText("-")
                    guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"].updateText("-")
                    guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"].updateText("-")
                    guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"].updateText("-")
                    guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"].updateText("-")

            ppfVar['PAGETIMER_SIMULATIONLISTUPDATECHECKER_LASTUPDATED'] = currentTime_ms

        #Simulation Running Checker
        if ((ppfVar['PAGETIMER_SIMULATIONRUNNINGCHECK_INTERVAL_MS'] < currentTime_ms-ppfVar['PAGETIMER_SIMULATIONRUNNINGCHECK_LASTUPDATED']) or (onLoad == True)):
            if (ppfVar['SIMULATION_RUNNING'] == True):
                if (ipcA_MAIN_AUX.getPRD("SIMULATION_RUNNING") == False):
                    guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].activate()
                    guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].deactivate()
                    ppfVar['SIMULATION_RUNNING'] = False
            else:
                if (ipcA_MAIN_AUX.getPRD("SIMULATION_RUNNING") == True):
                    guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].deactivate()
                    guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].activate()
                    ppfVar['SIMULATION_RUNNING'] = True

    pageInstance.pageProcessFunction = ppf_SIMULATION
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #PAGE LOAD FUNCTION ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def plf_SIMULATION(ppfVar):
        ppf_SIMULATION(ppfVar, onLoad = True)
        ipcA_MAIN_AUX.addFARHandler("SIMULATORMESSAGE", onSimulatorMessageReceival)

    pageInstance.pageLoadFunction = plf_SIMULATION
    #PAGE LOAD FUNCTION END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')

    def objFunc_pageMove_SIMULATIONRESULT(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('SIMULATIONRESULT')
        
    #Upon Currency Name Search Text Update
    def objFunc_currencyNameSearchTextUpdated(objectInstance, **kwargs):
        tibText = guios["SIMULATION_TEXTINPUTBOX_CURRENCYLIST"].getText()
        if (tibText == ""): displayTargets = 'all'
        else:               displayTargets = [apiSymbol for apiSymbol in pageInstance.ppfVariables['LOADED_ASSETLIST'] if tibText in apiSymbol]
        guios["SIMULATION_SELECTIONBOX_CURRENCYLIST"].setDisplayTargets(displayTargets)
        
    #Upon New Currency Selection
    def objFunc_newCurrencySelected(objectInstance, **kwargs):
        selectedItems = objectInstance.getSelected()
        if (0 < len(selectedItems)):
            newSelectedCurrency = selectedItems[0]
            pageInstance.ppfVariables['SELECTED_ASSETNAME'] = newSelectedCurrency
            guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_NAMECONTENT"].updateText(newSelectedCurrency)
        
            #Get Asset Data via PRD
            marketAssetData = ipcA_MAIN_ATM.getPRD(('MARKETASSETS', newSelectedCurrency))
            mrktRegTS             = marketAssetData['mrktRegTS'][0]
            dataRanges_perc       = marketAssetData['dataRanges_perc'][0]
            dataRanges_blocks     = marketAssetData['dataRanges'][0]
            RTAAlloc              = marketAssetData['RTAAlloc']
            RTAAllocMode          = marketAssetData['RTAAllocMode']
            firstStreamedKlineTS  = marketAssetData['firstStreamedKlineTSs'][0]
            status                = marketAssetData['status']
        
            #Update mrktRegTS
            if (mrktRegTS == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINECONTENT"].updateText("-")
            else:                   guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINECONTENT"].updateText(datetime.fromtimestamp(mrktRegTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
            pageInstance.ppfVariables['SELECTEDASSETDATA_mrktRegTS'] = mrktRegTS
                        
            #Update Data Ranges Percentage
            if   (dataRanges_perc == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("N/A",                              'GREY_DARK')
            elif (dataRanges_perc == 100):  guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("100 %",                            'GREEN_LIGHT')
            else:                           guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"].updateText("{:.3f} %".format(dataRanges_perc), 'ORANGE_LIGHT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges_perc'] = dataRanges_perc

            #Update Data Ranges
            if (dataRanges_blocks == None):
                guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGESCONTENT"].updateText("N/A")
                pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges'] = None
            else:
                if (1 < len(dataRanges_blocks)):
                    dataRanges_blocks_str = ""
                    for dataRanges_block in dataRanges_blocks: dataRanges_blocks_str += "({:s} ~ {:s})".format(datetime.fromtimestamp(dataRanges_block[0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_block[1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                elif (len(dataRanges_blocks) == 1):            dataRanges_blocks_str = "{:s} ~ {:s}".format(datetime.fromtimestamp(dataRanges_blocks[0][0], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), datetime.fromtimestamp(dataRanges_blocks[0][1], tz=timezone.utc).strftime("%Y/%m/%d %H:%M"))
                else:                                          dataRanges_blocks_str = "-"
                guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGESCONTENT"].updateText(dataRanges_blocks_str)
                pageInstance.ppfVariables['SELECTEDASSETDATA_dataRanges'] = dataRanges_blocks

            #Update RTA Allocation
            guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_RTAALLOCCONTENT"].updateText("{:s} / {:s}".format(str(RTAAlloc), str(RTAAllocMode)))
            pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAlloc']     = RTAAlloc
            pageInstance.ppfVariables['SELECTEDASSETDATA_RTAAllocMode'] = RTAAllocMode
                        
            #Update Streaming
            if (firstStreamedKlineTS == None): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMINGCONTENT"].updateText("FALSE", 'RED_LIGHT')
            else:                              guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMINGCONTENT"].updateText(datetime.fromtimestamp(firstStreamedKlineTS, tz=timezone.utc).strftime("%Y/%m/%d %H:%M"), 'DEFAULT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_firstStreamedKlineTS'] = firstStreamedKlineTS

            #Update Status
            if   (status == 'TRADING'):  guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'GREEN_LIGHT')
            elif (status == 'SETTLING'): guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'RED_LIGHT')
            else:                        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"].updateText(status, 'ORANGE_LIGHT')
            pageInstance.ppfVariables['SELECTEDASSETDATA_status'] = status

            #Configuration Check
            onConfigurationUpdate("CURRENCY")
            
    #On Simulation Range Switch Toggling
    def objFunc_onSimulationRangeSwitchToggled(objectInstance, **kwargs): onConfigurationUpdate("SIMRANGE_REALTIME")
            
    #On Simulation Range Text Update
    def objFunc_onSimulationRangeTextUpdate(objectInstance, **kwargs): onConfigurationUpdate("SIMRANGE")
            
    #On Custom Simulation Code Text Update
    def objFunc_onCustomSimulationCodeUpdate(objectInstance, **kwargs): onConfigurationUpdate("SIMCODE")
    
    #On Simulation Code Auto Replace Switch Toggling
    def objFunc_onSimCodeAutoReplaceSwitchToggled(objectInstance, **kwargs): onConfigurationUpdate("SIMCODE_AUTOREPLACE")

    #Upon Result Type Selection
    def objFunc_onNewResultTypeSelection(objectInstance, **kwargs): onConfigurationUpdate("RESULTTYPE")

    #Send 'AddSimulationQueue' request to AUX
    def objFunc_addSimulationQueue_FARRHandler(functionResult):
        guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].activate()

    def objFunc_addSimulationQueue(objectInstance, **kwargs):
        apiSymbol = pageInstance.ppfVariables['SELECTED_ASSETNAME']
        ipcA_MAIN_AUX.sendFAR(functionID = "ADDSIMULATIONQUEUE", functionParams = {'apiSymbol': apiSymbol, 'simConfig': pageInstance.ppfVariables['SIMULATIONCONFIGURATION']}, FARRHandler = objFunc_addSimulationQueue_FARRHandler, nMaxDispatch = 'INF')
        pprint.pprint(pageInstance.ppfVariables['SIMULATIONCONFIGURATION'])
        guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].deactivate()

    #Upon Simulation Search Text Update
    def objFunc_processingSimulationSearchTextUpdated(objectInstance, **kwargs):
        tibText = guios["SIMULATION_TEXTINPUTBOX_PROCESSINGSIMULATIONLIST"].getText()
        if (tibText == ""): displayTargets = 'all'
        else:               displayTargets = [sim for sim in pageInstance.ppfVariables['LOADED_SIMULATIONLIST_PROCESSING'] if tibText in sim]
        guios["SIMULATION_SELECTIONBOX_PROCESSINGSIMULATIONLIST"].setDisplayTargets(displayTargets)

    #Upon New Simulation Selection
    def objFunc_newProcessingSimulationSelected(objectInstance, **kwargs):
        selectedItems = objectInstance.getSelected()
        #No Simulation Selected
        if (len(selectedItems) == 0):
            pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING'] = None
            if (pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED'] == None): 
                displaySimulationInfo(None, None)
                pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = None
            else:
                displaySimulationInfo(pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED'], 'COMPLETED')
                pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = 'COMPLETED'
            #Deactivate Simulation Control Buttons
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].deactivate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].deactivate()

        #A Simulation Selected
        else:
            selectedSimulation = selectedItems[0]
            pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING'] = selectedSimulation
            displaySimulationInfo(selectedSimulation, 'PROCESSING')
            #Activate Simulation Control Buttons
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].activate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].activate()
            #Update the current selected simulation type
            pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = "PROCESSING"

    #Upon Simulation Search Text Update
    def objFunc_completedSimulationSearchTextUpdated(objectInstance, **kwargs):
        tibText = guios["SIMULATION_TEXTINPUTBOX_COMPLETEDSIMULATIONLIST"].getText()
        if (tibText == ""): displayTargets = 'all'
        else:               displayTargets = [sim for sim in pageInstance.ppfVariables['LOADED_SIMULATIONLIST_COMPLETED'] if tibText in sim]
        guios["SIMULATION_SELECTIONBOX_COMPLETEDSIMULATIONLIST"].setDisplayTargets(displayTargets)

    #Upon New Simulation Selection
    def objFunc_newCompletedSimulationSelected(objectInstance, **kwargs):
        selectedItems = objectInstance.getSelected()
        #No Simulation Selected
        if (len(selectedItems) == 0):
            pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED'] = None
            if (pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING'] == None): 
                displaySimulationInfo(None, None)
                pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = None
            else:
                displaySimulationInfo(pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING'], 'PROCESSING')
                pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = 'PROCESSING'
            #Deactivate Simulation Control Buttons
            guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].deactivate()
        #A Simulation Selected
        else:
            selectedSimulation = selectedItems[0]
            pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED'] = selectedSimulation
            displaySimulationInfo(selectedSimulation, 'COMPLETED')
            #Activate Simulation Control Buttons
            guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].activate()
            #Update the current selected simulation type
            pageInstance.ppfVariables['SELECTED_PROCESSINGORCOMPLETED'] = "COMPLETED"
            
    #Upon Completed Simulation Removal Button Press
    def objFunc_removeSelectedProcessingSimulation_FARRHandler(functionResult):
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].activate()

    def objFunc_removeSelectedProcessingSimulation(objectInstance, **kwargs):
        selectedSimulationCode = pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING']
        if (selectedSimulationCode != None): 
            ipcA_MAIN_AUX.sendFAR(functionID = "REMOVESIMULATION", functionParams = {'simulationCode': selectedSimulationCode}, FARRHandler = objFunc_removeSelectedProcessingSimulation_FARRHandler, nMaxDispatch = 'INF')
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].deactivate()

    #Upon Completed Simulation Removal Button Press
    def objFunc_removeSelectedCompletedSimulation_FARRHandler(functionResult):
        guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].activate()

    def objFunc_removeSelectedCompletedSimulation(objectInstance, **kwargs):
        selectedSimulationCode = pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_COMPLETED']
        if (selectedSimulationCode != None): 
            ipcA_MAIN_AUX.sendFAR(functionID = "REMOVESIMULATION", functionParams = {'simulationCode': selectedSimulationCode}, FARRHandler = objFunc_removeSelectedCompletedSimulation_FARRHandler, nMaxDispatch = 'INF')
            guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].deactivate()

    #Resume Selected Processing Simulation
    def objFunc_resumeSimulation_FARRHandler(functionResult):
        if (functionResult == True):
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].deactivate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].activate()
        else:
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].activate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].deactivate()

    def objFunc_resumeSimulation(objectInstance, **kwargs):
        ipcA_MAIN_AUX.sendFAR(functionID = "RESUMESIMULATION", functionParams = None, FARRHandler = objFunc_resumeSimulation_FARRHandler, nMaxDispatch = 'INF')
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].deactivate()
        
    #Pause Selected Processing Simulation
    def objFunc_pauseSimulation_FARRHandler(functionResult):
        if (functionResult == True):
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].activate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].deactivate()
        else:
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"].deactivate()
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].activate()

    def objFunc_pauseSimulation(objectInstance, **kwargs):
        ipcA_MAIN_AUX.sendFAR(functionID = "PAUSESIMULATION", functionParams = None, FARRHandler = objFunc_pauseSimulation_FARRHandler, nMaxDispatch = 'INF')
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"].deactivate()

    #Terminate Selected Processing Simulation
    def objFunc_terminateSimulation_FARRHandler(functionResult):
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].activate()

    def objFunc_terminateSimulation(objectInstance, **kwargs):
        selectedSimulationCode = pageInstance.ppfVariables['SELECTED_SIMULATIONCODE_PROCESSING']
        if (selectedSimulationCode != None):
            ipcA_MAIN_AUX.sendFAR(functionID = "TERMINATESIMULATION", functionParams = {'simulationCode': selectedSimulationCode}, FARRHandler = objFunc_terminateSimulation_FARRHandler, nMaxDispatch = 'INF')
            guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].deactivate()

    def objFunc_onFindVIPsSwitchToggled(objectInstance, **kwargs):
        onConfigurationUpdate("FINDVIPS")

    def objFunc_onSimulateTradingSwitchToggled(objectInstance, **kwargs):
        onConfigurationUpdate("SIMULATETRADING")

    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["SIMULATION_TITLETEXT"]               = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('SIMULATION:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"]        = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD,        image = 'dashboardIcon_512x512.png',         imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        guios["NAVIGATION_BUTTON_SIMULATIONRESULT"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos= 400, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_SIMULATIONRESULT, image = 'simulationResultIcon2_512x512.png', imageSize = (250, 250), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        
        #Currency List & Selection
        guios["SIMULATION_WRAPPER_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos= 100, yPos=8300, width=3300, height= 200, style="styleA", text = visualManager.getTextPack('SIMULATION:BINANCEUSDM'))
        #---Currency List
        guios["SIMULATION_TEXTBOX_CURRENCYSEARCH"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,       groupOrder=1, xPos= 100, yPos=8000, width= 800, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SEARCH'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,  groupOrder=1, xPos=1000, yPos=8000, width=2400, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_currencyNameSearchTextUpdated)
        guios["SIMULATION_SELECTIONBOX_CURRENCYLIST"] = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst,  groupOrder=1, xPos= 100, yPos=2550, width=3300, height=5350, style="styleA", fontSize = 80, elementHeight = 250, multiSelect = False, singularSelect_allowRelease = False, showIndex = True, selectionUpdateFunction = objFunc_newCurrencySelected)
        #---Selected Currency Info
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_NAME"]                  = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=2200, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CURRENCYNAME'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_NAMECONTENT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos=2200, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUS"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1850, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CURRENCYSTATUS'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_CURRENCYSTATUSCONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos=1850, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINE"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1500, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:FIRST1MINKLINE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_FIRST1MINKLINECONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos=1500, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERC"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos=1150, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:DATAAVAILABILITYPERC'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DAPERCCONTENT"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos=1150, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGES"]              = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos= 800, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:DATAAVAILABILITYRANGE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_DARANGESCONTENT"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos= 800, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_RTAALLOC"]              = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos= 450, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:RTAALLOC'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_RTAALLOCCONTENT"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos= 450, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMING"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 100, yPos= 100, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:STREAMING'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SELECTEDCURRENCY_STREAMINGCONTENT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=1200, yPos= 100, width=2200, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)

        #Configuration
        guios["SIMULATION_WRAPPER_SIMULATIONCONFIG"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos= 3500, yPos=8300, width=9100, height= 200, style="styleA", text = visualManager.getTextPack('SIMULATION:SIMULATIONCONFIGURATION'))
        #---Simulation Range Configuration
        guios["SIMULATION_TEXTBOX_REALTIMESIMULATION"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 3500, yPos=8000, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:REALTIMESIMULATION'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_SWITCH_REALTIMESIMULATION"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,       groupOrder=1, xPos= 4700, yPos=8000, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=False, releaseFunction=objFunc_onSimulationRangeSwitchToggled)
        guios["SIMULATION_TEXTBOX_SIMULATIONRANGE0"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 5300, yPos=8000, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMULATIONRANGE0'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE0"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos= 6400, yPos=8000, width=1200, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_onSimulationRangeTextUpdate)
        guios["SIMULATION_TEXTBOX_SIMULATIONRANGE1"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 7700, yPos=8000, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMULATIONRANGE1'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_SIMULATIONRANGE1"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos= 8800, yPos=8000, width=1200, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_onSimulationRangeTextUpdate)
        guios["SIMULATION_TEXTBOX_DATEFORMAT"]            = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos=10100, yPos=8000, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:DATEFORMAT'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_DATEFORMATCONTENT"]     = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos=11200, yPos=8000, width=1400, height= 250, style="styleA", text='YYYY/MM/DD HH:MM', textInteractable = True, fontSize = 80)

        #---Custom Simulation Code
        guios["SIMULATION_TEXTBOX_CUSTOMSIMULATIONCODE"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 3500, yPos=7650, width=1700, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CUSTOMSIMCODE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_CUSTOMSIMULATIONCODECONTENT"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos= 5300, yPos=7650, width=2200, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_onCustomSimulationCodeUpdate)
        guios["SIMULATION_TEXTBOX_SIMULATIONCODEAUTOREPLACE"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 7600, yPos=7650, width=1600, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMCODEAUTOREPLACE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_SWITCH_SIMULATIONCODEAUTOREPLACE"]         = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,       groupOrder=1, xPos= 9300, yPos=7650, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulationCodeAutoReplace'], releaseFunction=objFunc_onSimCodeAutoReplaceSwitchToggled)

        #---Result Type
        guios["SIMULATION_TEXTBOX_RESULTTYPECONFIG"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 9900, yPos=7650, width=1000, height=250, style="styleA", text=visualManager.getTextPack('SIMULATION:RESULTTYPE'), textInteractable = True, fontSize = 80)
        availableResultTypes = {'COMPLETE': {'text': visualManager.getTextPack('SIMULATION:RESULTTYPE_COMPLETE')}, 'SUMMARY': {'text': visualManager.getTextPack('SIMULATION:RESULTTYPE_SUMMARY')}}
        guios["SIMULATION_SELECTIONBOX_RESULTTYPECONFIG"] = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst, groupOrder=1, xPos=11000, yPos=7650, width=1600, height=250, style="styleA", nDisplay = len(availableResultTypes), selectionUpdateFunction = objFunc_onNewResultTypeSelection, fontSize = 80)
        guios["SIMULATION_SELECTIONBOX_RESULTTYPECONFIG"].setSelectionList(selectionList = availableResultTypes, displayTargets = 'all')
        guios["SIMULATION_SELECTIONBOX_RESULTTYPECONFIG"].setSelected('COMPLETE')

        #---Simulator Message & Queue Add Button
        guios["SIMULATION_TEXTBOX_SIMULATORMESSAGE"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 3500, yPos= 100, width=1500, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMULATORMESSAGE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SIMULATORMESSAGECONTENT"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 5100, yPos= 100, width=5900, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"]               = ATM_Zeta_GUIO_Generals.button_typeA(**inst,  groupOrder=1, xPos=11100, yPos= 100, width=1500, height= 250, style="styleA", releaseFunction=objFunc_addSimulationQueue, text=visualManager.getTextPack('SIMULATION:ADDSIMULATIONQUEUE'), fontSize = 80)
        guios["SIMULATION_BUTTON_ADDSIMULATIONQUEUE"].deactivate()

        #---Find VIPs
        guios["SIMULATION_TEXTBOX_FINDVIPS"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 3500, yPos=7300, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:FINDVIPS'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_SWITCH_FINDVIPS"]  = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,  groupOrder=1, xPos= 4600, yPos=7300, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['findVIPs'], releaseFunction=objFunc_onFindVIPsSwitchToggled)
        
        #---Simulated Trades
        guios["SIMULATION_TEXTBOX_SIMULATETRADING"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos= 3500, yPos=5300, width=1000, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMULATETRADING'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_SWITCH_SIMULATETRADING"]  = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,  groupOrder=1, xPos= 4600, yPos=5300, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=pageInstance.ppfVariables['SIMULATIONCONFIGURATION']['simulateTrading'], releaseFunction=objFunc_onSimulateTradingSwitchToggled)

        #Simulation List & Selection
        #---Simulation List - Processing
        guios["SIMULATION_WRAPPER_SIMULATIONLIST_PROCESSING"]     = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos=12700, yPos=8300, width=3200, height= 200, style="styleA", text = visualManager.getTextPack('SIMULATION:SIMULATIONLIST_PROCESSING'))
        guios["SIMULATION_TEXTBOX_PROCESSINGSIMULATIONSEARCH"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=8000, width= 700, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SEARCH'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_PROCESSINGSIMULATIONLIST"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,           groupOrder=1, xPos=13500, yPos=8000, width=1700, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_processingSimulationSearchTextUpdated)
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"]    = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=1, xPos=15300, yPos=8000, width= 600, height= 250, style="styleA", releaseFunction=objFunc_removeSelectedProcessingSimulation, text=visualManager.getTextPack('SIMULATION:REMOVE'), fontSize = 80)
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONREMOVE"].deactivate()

        guios["SIMULATION_SELECTIONBOX_PROCESSINGSIMULATIONLIST"] = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst, groupOrder=1, xPos=12700, yPos=5650, width=3200, height=2250, style="styleA", fontSize = 80, elementHeight = 250, multiSelect = False, singularSelect_allowRelease = True, showIndex = True, selectionUpdateFunction = objFunc_newProcessingSimulationSelected)
        
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONRESUME"]    = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos=12700, yPos=5300, width=1100, height= 250, style="styleA", releaseFunction=objFunc_resumeSimulation,    text=visualManager.getTextPack('SIMULATION:RESUME'),    fontSize = 80)
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONPAUSE"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos=13900, yPos=5300, width= 950, height= 250, style="styleA", releaseFunction=objFunc_pauseSimulation,     text=visualManager.getTextPack('SIMULATION:PAUSE'),     fontSize = 80)
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos=14950, yPos=5300, width= 950, height= 250, style="styleA", releaseFunction=objFunc_terminateSimulation, text=visualManager.getTextPack('SIMULATION:TERMINATE'), fontSize = 80)
        guios["SIMULATION_BUTTON_PROCESSINGSIMULATIONTERMINATE"].deactivate()

        #---Simulation List - Completed
        guios["SIMULATION_WRAPPER_SIMULATIONLIST_COMPLETED"]     = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos=12700, yPos=5000, width=3200, height= 200, style="styleA", text = visualManager.getTextPack('SIMULATION:SIMULATIONLIST_COMPLETED'))
        guios["SIMULATION_TEXTBOX_COMPLETEDSIMULATIONSEARCH"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=4700, width= 700, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SEARCH'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTINPUTBOX_COMPLETEDSIMULATIONLIST"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,           groupOrder=1, xPos=13500, yPos=4700, width=1700, height= 250, style="styleA", text="", fontSize = 80, textUpdateFunction = objFunc_completedSimulationSearchTextUpdated)
        guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=1, xPos=15300, yPos=4700, width= 600, height= 250, style="styleA", releaseFunction=objFunc_removeSelectedCompletedSimulation, text=visualManager.getTextPack('SIMULATION:REMOVE'), fontSize = 80)
        guios["SIMULATION_BUTTON_COMPLETEDSIMULATIONREMOVE"].deactivate()

        guios["SIMULATION_SELECTIONBOX_COMPLETEDSIMULATIONLIST"] = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst, groupOrder=1, xPos=12700, yPos=2800, width=3200, height=1800, style="styleA", fontSize = 80, elementHeight = 250, multiSelect = False, singularSelect_allowRelease = True, showIndex = True, selectionUpdateFunction = objFunc_newCompletedSimulationSelected)

        #---Selected Simulation Info
        guios["SIMULATION_WRAPPER_SIMULATIONINFORMATION"]          = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos=12700, yPos=2500, width=3200, height= 200, style="styleA", text = visualManager.getTextPack('SIMULATION:SIMULATIONINFORMATION'))
        guios["SIMULATION_TEXTBOX_CURRENTANALYZING"]               = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=2200, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CURRENTANALYZING'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_CURRENTANALYZINGCONTENT"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos=2200, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_CURRENTTARGET"]                  = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=1850, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CURRENTTARGET'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_CURRENTTARGETCONTENT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos=1850, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SIMULATIONRANGE"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=1500, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:SIMULATIONRANGE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_SIMULATIONRANGECONTENT"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos=1500, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGE"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos=1150, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:COMPLETIONPERCENTAGE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_COMPLETIONPERCENTAGECONTENT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos=1150, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_CURRENTPROCESS"]                 = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos= 800, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:CURRENTPROCESS'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_CURRENTPROCESSCONTENT"]          = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos= 800, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIME"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos= 450, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:ESTIMATEDCOMPLETIONTIME'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_ESTIMATEDCOMPLETIONTIMECONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos= 450, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_RESULTTYPE"]                     = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=12700, yPos= 100, width=1100, height= 250, style="styleA", text=visualManager.getTextPack('SIMULATION:RESULTTYPE'), textInteractable = True, fontSize = 80)
        guios["SIMULATION_TEXTBOX_RESULTTYPECONTENT"]              = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=13900, yPos= 100, width=2000, height= 250, style="styleA", text="-", textInteractable = True, fontSize = 80)

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-SIMULATION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-SIMULATIONRESULT ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_SIMULATIONRESULT(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_SIMULATIONRESULT(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_SIMULATIONRESULT
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')
    def objFunc_pageMove_SIMULATION(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('SIMULATION')
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["SIMULATIONRESULT_TITLETEXT"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=6250, yPos=8550, width=3500, height=400, style=None, text=visualManager.getTextPack('SIMULATIONRESULT:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"]  = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD,  image = 'dashboardIcon_512x512.png',   imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        guios["NAVIGATION_BUTTON_SIMULATION"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos= 400, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_SIMULATION, image = 'simulationIcon2_512x512.png', imageSize = (250, 250), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))

        guios["SUBPAGEBOX0"] = ATM_Zeta_GUIO_Generals.subPageBox_typeA(**inst, groupOrder = 1, xPos = 2900, yPos = 50, width = 13000, height = 8450, style = None, useScrollBar_H = False, useScrollBar_V = True, name = 'tester')
        guios["SUBPAGEBOX0"].addGUIO("CHARTDRAWER",      ATM_Zeta_GUIO_ChartDrawers.chartDrawer_typeB, {'groupOrder': 0, 'xPos': 0, 'yPos': 10000, 'width': 12800, 'height': 8450, 'style': 'styleA', 'name': 'SIMULATIONRESULTCHARTDRAWER'})
        #guios["SUBPAGEBOX0"].addGUIO("BUTTONTYPEATEST1", ATM_Zeta_GUIO_Generals.button_typeA,          {'groupOrder': 0, 'xPos': 0, 'yPos':   100, 'width':  1000, 'height':   250, 'style': 'styleA', 'text': "button_typeA"})
        #guios["SUBPAGEBOX0"].addGUIO("BUTTONTYPEATEST2", ATM_Zeta_GUIO_Generals.button_typeA,          {'groupOrder': 0, 'xPos': 0, 'yPos': 30000, 'width':  1000, 'height':   250, 'style': 'styleA', 'text': "button_typeA"})


    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-SIMULATION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-AUTOTRADE -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_AUTOTRADE(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_AUTOTRADE(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_AUTOTRADE
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        guios["AUTOTRADE_TITLETEXT"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('AUTOTRADE:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD, image = 'dashboardIcon_512x512.png', imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-AUTOTRADE END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    




#PAGE-SETTINGS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_SETTINGS(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #PAGE PROCESS FUNCTION ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #pageInstance.ppfVariables['INITSTEP'] = 'AUX' #AUX -> CENTRAL -> RTAs
    def ppf_SETTINGS(ppfVar, onLoad = False):
        pass

    pageInstance.pageProcessFunction = ppf_SETTINGS
    #PAGE PROCESS FUNCTION END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #OBJECT FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_pageMove_DASHBOARD(objectInstance, **kwargs): 
        pageInstance.sysFunctions['LOADPAGE']('DASHBOARD')

    def objFunc_toggleProgramAudio(objectInstance, **kwargs):
        if (guios['AUDIOCONTROL_SWITCH_AUDIOPALY'].getStatus() == True):
            audioManager.setMute(False)
            guios["AUDIOCONTROL_SLIDER_AUDIOVOLUME"].activate()
        else:
            audioManager.setMute(True)
            guios["AUDIOCONTROL_SLIDER_AUDIOVOLUME"].deactivate()
        
    def objFunc_adjustProgramAudioVolume(objectInstance, **kwargs):
        audioManager.setVolume(guios["AUDIOCONTROL_SLIDER_AUDIOVOLUME"].getSliderValue())
        guios["AUDIOCONTROL_TEXT_AUDIOVOLUMEVALUE"].updateText("{:.1f}".format(audioManager.getVolume()))
        
    def objFunc_toggleFullScreen(objectInstance, **kwargs):
        systemFunctions["TOGGLE_FULLSCREEN"]()
        
    def objFunc_GUIThemeSelectionUpdate(objectInstance, **kwargs):
        selectedTheme = guios["GRAPHICSCONTROL_SELECTIONBOX_GUITHEME"].getSelected()
        systemFunctions['CHANGEGUITHEME'](selectedTheme)
        
    def objFunc_LanguageSelectionUpdate(objectInstance, **kwargs):
        selectedLanguage = guios["GRAPHICSCONTROL_SELECTIONBOX_LANGUAGE"].getSelected()
        systemFunctions['CHANGELANGUAGE'](selectedLanguage)
        
    def objFunc_SaveGUIConfig(objectInstance, **kwargs):
        systemFunctions['SAVEGUICONFIG']()
        
    #OBJECT FUNCTIONS END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        #Page Title
        guios["SETTINGS_TITLETEXT"]          = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=7000, yPos=8550, width=2000, height=400, style=None, text=visualManager.getTextPack('SETTINGS:TITLE'), fontSize = 220, textInteractable = False)
        guios["NAVIGATION_BUTTON_DASHBOARD"] = ATM_Zeta_GUIO_Generals.button_typeB(**inst,  groupOrder=2, xPos=  50, yPos=8650, width= 300, height=300, style="styleB", releaseFunction=objFunc_pageMove_DASHBOARD, image = 'dashboardIcon_512x512.png', imageSize = (225, 225), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        


        #Audio Menu
        guios["AUDIOCONTROL_WRAPPER"]               = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos= 100, yPos= 100, width=9850, height=4000, style="styleA", text=visualManager.getTextPack('SETTINGS:AUDIOWRAPPERTITLE'))
        #---Audio Play Switch
        guios["AUDIOCONTROL_TEXT_AUDIOPALY"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 200, yPos=3650, width=1500, height= 250, style="styleA", text=visualManager.getTextPack('SETTINGS:PLAYSOUND'))
        guios["AUDIOCONTROL_SWITCH_AUDIOPALY"]      = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=1800, yPos=3650, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=not(audioManager.ctrl_Mute), releaseFunction=objFunc_toggleProgramAudio)
        #---Volume Control Slider
        guios["AUDIOCONTROL_TEXT_AUDIOVOLUME"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2500, yPos=3650, width=1500, height= 250, style="styleA", text=visualManager.getTextPack('SETTINGS:MAINVOLUME'))
        guios["AUDIOCONTROL_SLIDER_AUDIOVOLUME"]    = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=2, xPos=4100, yPos=3650, width=4650, height= 250, align = 'horizontal', style="styleA", valueUpdateFunction = objFunc_adjustProgramAudioVolume, sliderValue=audioManager.getVolume())
        if (audioManager.ctrl_Mute == True): guios["AUDIOCONTROL_SLIDER_AUDIOVOLUME"].deactivate()
        guios["AUDIOCONTROL_TEXT_AUDIOVOLUMEVALUE"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=8850, yPos=3650, width=1000, height= 250, style="styleA", text="{:.1f}".format(audioManager.getVolume()))



        #Graphics Menu
        guios["GRAPHICSCONTROL_WRAPPER"]               = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos= 100, yPos=4200, width=9850, height=4350, style="styleA", text=visualManager.getTextPack('SETTINGS:GRAPHICSWRAPPERTITLE'))
        #---Audio Play Switch
        guios["GRAPHICSCONTROL_TEXT_FULLSCREEN"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 200, yPos=8100, width=2000, height= 250, style="styleA", text=visualManager.getTextPack('SETTINGS:FULLSCREEN'))
        guios["GRAPHICSCONTROL_SWITCH_FULLSCREEN"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=2300, yPos=8100, width= 500, height= 250, style="styleA", align='horizontal', switchStatus=systemFunctions["ISFULLSCREEN"](), releaseFunction=objFunc_toggleFullScreen)
        #---GUI Theme Selection
        guios["GRAPHICSCONTROL_TEXT_GUITHEME"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos= 200, yPos=7750, width=1250, height= 250, style="styleA", text=visualManager.getTextPack('SETTINGS:GUITHEME'))
        guiThemeSelectionList = {'LIGHT': {'text': visualManager.getTextPack('SETTINGS:LIGHTMODE')}, 'DARK': {'text': visualManager.getTextPack('SETTINGS:DARKMODE')}}
        guios["GRAPHICSCONTROL_SELECTIONBOX_GUITHEME"] = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst,           groupOrder=3, xPos=1550, yPos=7750, width=1250, height= 250, style="styleA", nDisplay = len(guiThemeSelectionList), selectionUpdateFunction = objFunc_GUIThemeSelectionUpdate)
        guios["GRAPHICSCONTROL_SELECTIONBOX_GUITHEME"].setSelectionList(selectionList = guiThemeSelectionList, displayTargets = 'all')
        guios["GRAPHICSCONTROL_SELECTIONBOX_GUITHEME"].setSelected(visualManager.getGUITheme(), callSelectionUpdateFunction = False)

        #---Language Selection
        guios["GRAPHICSCONTROL_TEXT_LANGUAGE"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos= 200, yPos=7400, width=1250, height= 250, style="styleA", text=visualManager.getTextPack('SETTINGS:LANGUAGE'))
        languageSelectionList = dict()
        for language in visualManager.getAvailableLanguages(): languageSelectionList[language] = {'text': visualManager.getTextPack('SETTINGS:'+language)}
        guios["GRAPHICSCONTROL_SELECTIONBOX_LANGUAGE"] = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst,           groupOrder=2, xPos=1550, yPos=7400, width=1250, height= 250, style="styleA", nDisplay = len(languageSelectionList), selectionUpdateFunction = objFunc_LanguageSelectionUpdate)
        guios["GRAPHICSCONTROL_SELECTIONBOX_LANGUAGE"].setSelectionList(selectionList = languageSelectionList, displayTargets = 'all')
        guios["GRAPHICSCONTROL_SELECTIONBOX_LANGUAGE"].setSelected(visualManager.getLanguage(), callSelectionUpdateFunction = False)



        #UserControl Menu
        guios["USERCONTROL_WRAPPER"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=10050, yPos=400, width=5850, height=8450, style="styleA", text = visualManager.getTextPack('SETTINGS:PREFERENCESWRAPPERTITLE'))

        #Configuration Management
        guios["BUTTONTEST0_BUTTON"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=10150, yPos=100, width=1800, height=250, style="styleA", releaseFunction=objFunc_SaveGUIConfig, text=visualManager.getTextPack('SETTINGS:SAVECHANGES'))

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-SETTINGS END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    









#PAGE-EXPERIMENT0 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_EXPERIMENT0(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND']    = pyglet.graphics.Group(order = 0)
    groups['OBJECTSLAYER0'] = pyglet.graphics.Group(order = 1)

    #OBJECT FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_ToggleTLs0(objectInstance, **kwargs):
        if (guios['DISPLAYSWITCH0'].getStatus() == True): 
            guios['TEXTELEMENTTESTER0_NW'].show();     guios['TEXTELEMENTTESTER0_NW1'].show()
            guios['TEXTELEMENTTESTER0_N'].show();      guios['TEXTELEMENTTESTER0_N1'].show()
            guios['TEXTELEMENTTESTER0_NE'].show();     guios['TEXTELEMENTTESTER0_NE1'].show()
            guios['TEXTELEMENTTESTER0_W'].show();      guios['TEXTELEMENTTESTER0_W1'].show()
            guios['TEXTELEMENTTESTER0_CENTER'].show(); guios['TEXTELEMENTTESTER0_CENTER1'].show()
            guios['TEXTELEMENTTESTER0_E'].show();      guios['TEXTELEMENTTESTER0_E1'].show()
            guios['TEXTELEMENTTESTER0_SW'].show();     guios['TEXTELEMENTTESTER0_SW1'].show()
            guios['TEXTELEMENTTESTER0_S'].show();      guios['TEXTELEMENTTESTER0_S1'].show()
            guios['TEXTELEMENTTESTER0_SE'].show();     guios['TEXTELEMENTTESTER0_SE1'].show()
        else:
            guios['TEXTELEMENTTESTER0_NW'].hide();     guios['TEXTELEMENTTESTER0_NW1'].hide()
            guios['TEXTELEMENTTESTER0_N'].hide();      guios['TEXTELEMENTTESTER0_N1'].hide()
            guios['TEXTELEMENTTESTER0_NE'].hide();     guios['TEXTELEMENTTESTER0_NE1'].hide()
            guios['TEXTELEMENTTESTER0_W'].hide();      guios['TEXTELEMENTTESTER0_W1'].hide()
            guios['TEXTELEMENTTESTER0_CENTER'].hide(); guios['TEXTELEMENTTESTER0_CENTER1'].hide()
            guios['TEXTELEMENTTESTER0_E'].hide();      guios['TEXTELEMENTTESTER0_E1'].hide()
            guios['TEXTELEMENTTESTER0_SW'].hide();     guios['TEXTELEMENTTESTER0_SW1'].hide()
            guios['TEXTELEMENTTESTER0_S'].hide();      guios['TEXTELEMENTTESTER0_S1'].hide()
            guios['TEXTELEMENTTESTER0_SE'].hide();     guios['TEXTELEMENTTESTER0_SE1'].hide()
    def objFunc_ToggleTLs1(objectInstance, **kwargs):
        if (guios['DISPLAYSWITCH1'].getStatus() == True): 
            guios['TEXTELEMENTTESTER1_NW'].show();     guios['TEXTELEMENTTESTER1_NW1'].show()
            guios['TEXTELEMENTTESTER1_N'].show();      guios['TEXTELEMENTTESTER1_N1'].show()
            guios['TEXTELEMENTTESTER1_NE'].show();     guios['TEXTELEMENTTESTER1_NE1'].show()
            guios['TEXTELEMENTTESTER1_W'].show();      guios['TEXTELEMENTTESTER1_W1'].show()
            guios['TEXTELEMENTTESTER1_CENTER'].show(); guios['TEXTELEMENTTESTER1_CENTER1'].show()
            guios['TEXTELEMENTTESTER1_E'].show();      guios['TEXTELEMENTTESTER1_E1'].show()
            guios['TEXTELEMENTTESTER1_SW'].show();     guios['TEXTELEMENTTESTER1_SW1'].show()
            guios['TEXTELEMENTTESTER1_S'].show();      guios['TEXTELEMENTTESTER1_S1'].show()
            guios['TEXTELEMENTTESTER1_SE'].show();     guios['TEXTELEMENTTESTER1_SE1'].show()
        else:
            guios['TEXTELEMENTTESTER1_NW'].hide();     guios['TEXTELEMENTTESTER1_NW1'].hide()
            guios['TEXTELEMENTTESTER1_N'].hide();      guios['TEXTELEMENTTESTER1_N1'].hide()
            guios['TEXTELEMENTTESTER1_NE'].hide();     guios['TEXTELEMENTTESTER1_NE1'].hide()
            guios['TEXTELEMENTTESTER1_W'].hide();      guios['TEXTELEMENTTESTER1_W1'].hide()
            guios['TEXTELEMENTTESTER1_CENTER'].hide(); guios['TEXTELEMENTTESTER1_CENTER1'].hide()
            guios['TEXTELEMENTTESTER1_E'].hide();      guios['TEXTELEMENTTESTER1_E1'].hide()
            guios['TEXTELEMENTTESTER1_SW'].hide();     guios['TEXTELEMENTTESTER1_SW1'].hide()
            guios['TEXTELEMENTTESTER1_S'].hide();      guios['TEXTELEMENTTESTER1_S1'].hide()
            guios['TEXTELEMENTTESTER1_SE'].hide();     guios['TEXTELEMENTTESTER1_SE1'].hide()
    def objFunc_ToggleTLs2(objectInstance, **kwargs):
        if (guios['DISPLAYSWITCH2'].getStatus() == True): 
            guios['TEXTELEMENTTESTER2_NW'].show();     guios['TEXTELEMENTTESTER2_NW1'].show()
            guios['TEXTELEMENTTESTER2_N'].show();      guios['TEXTELEMENTTESTER2_N1'].show()
            guios['TEXTELEMENTTESTER2_NE'].show();     guios['TEXTELEMENTTESTER2_NE1'].show()
            guios['TEXTELEMENTTESTER2_W'].show();      guios['TEXTELEMENTTESTER2_W1'].show()
            guios['TEXTELEMENTTESTER2_CENTER'].show(); guios['TEXTELEMENTTESTER2_CENTER1'].show()
            guios['TEXTELEMENTTESTER2_E'].show();      guios['TEXTELEMENTTESTER2_E1'].show()
            guios['TEXTELEMENTTESTER2_SW'].show();     guios['TEXTELEMENTTESTER2_SW1'].show()
            guios['TEXTELEMENTTESTER2_S'].show();      guios['TEXTELEMENTTESTER2_S1'].show()
            guios['TEXTELEMENTTESTER2_SE'].show();     guios['TEXTELEMENTTESTER2_SE1'].show()
        else:
            guios['TEXTELEMENTTESTER2_NW'].hide();     guios['TEXTELEMENTTESTER2_NW1'].hide()
            guios['TEXTELEMENTTESTER2_N'].hide();      guios['TEXTELEMENTTESTER2_N1'].hide()
            guios['TEXTELEMENTTESTER2_NE'].hide();     guios['TEXTELEMENTTESTER2_NE1'].hide()
            guios['TEXTELEMENTTESTER2_W'].hide();      guios['TEXTELEMENTTESTER2_W1'].hide()
            guios['TEXTELEMENTTESTER2_CENTER'].hide(); guios['TEXTELEMENTTESTER2_CENTER1'].hide()
            guios['TEXTELEMENTTESTER2_E'].hide();      guios['TEXTELEMENTTESTER2_E1'].hide()
            guios['TEXTELEMENTTESTER2_SW'].hide();     guios['TEXTELEMENTTESTER2_SW1'].hide()
            guios['TEXTELEMENTTESTER2_S'].hide();      guios['TEXTELEMENTTESTER2_S1'].hide()
            guios['TEXTELEMENTTESTER2_SE'].hide();     guios['TEXTELEMENTTESTER2_SE1'].hide()
    def objFunc_ToggleTheme(objectInstance, **kwargs):
        if (guios['GUITHEMESWITCH'].getStatus() == True): newTheme = 'LIGHT'
        else:                                             newTheme = 'DARK'
        guios["GUITHEMETEXT"].updateText(newTheme)
        systemFunctions['CHANGEGUITHEME'](newTheme)

    #OBJECT FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        textStyle = visualManager.getTextStyle('textBox_default')['DEFAULT']; textStyle['font_size'] = int(100*screenScaler)
        textObjectInst = {'scaler': screenScaler, 'batch': batch, 'group': groups['OBJECTSLAYER0'], 'defaultTextStyle': textStyle, 'showElementBox': True}

        guios["TEXTELEMENTTESTER0_NW"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER0_N"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER0_NE"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER0_W"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER0_CENTER"] = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER0_E"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER0_SW"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER0_S"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER0_SE"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SE')

        guios["TEXTELEMENTTESTER0_NW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER0_N1"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER0_NE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER0_W1"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER0_CENTER1"] = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER0_E1"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER0_SW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 100,  yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER0_S1"]      = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 1700, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER0_SE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 3300, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SE')



        guios["TEXTELEMENTTESTER1_NW"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER1_N"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER1_NE"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER1_W"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER1_CENTER"] = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER1_E"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER1_SW"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER1_S"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER1_SE"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SE')

        guios["TEXTELEMENTTESTER1_NW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER1_N1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER1_NE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER1_W1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER1_CENTER1"] = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER1_E1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER1_SW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 5000, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER1_S1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 6600, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER1_SE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_I(**textObjectInst, xPos = 8200, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SE')



        guios["TEXTELEMENTTESTER2_NW"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER2_N"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER2_NE"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 7900, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER2_W"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER2_CENTER"] = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER2_E"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 6800, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER2_SW"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER2_S"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER2_SE"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 5700, width = 1500, height = 1000, text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", anchor = 'SE')

        guios["TEXTELEMENTTESTER2_NW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NW')
        guios["TEXTELEMENTTESTER2_N1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER2_NE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 4500, width = 1500, height = 1000, text = "0123456789", anchor = 'NE')
        guios["TEXTELEMENTTESTER2_W1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'W')
        guios["TEXTELEMENTTESTER2_CENTER1"] = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'CENTER')
        guios["TEXTELEMENTTESTER2_E1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 3400, width = 1500, height = 1000, text = "0123456789", anchor = 'E')
        guios["TEXTELEMENTTESTER2_SW1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 9800,  yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SW')
        guios["TEXTELEMENTTESTER2_S1"]      = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 11400, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER2_SE1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 13000, yPos = 2300, width = 1500, height = 1000, text = "0123456789", anchor = 'SE')
        
        guios["TEXTELEMENTTESTER3_SPC0"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos =  100, yPos = 1000, width = 1500, height = 200, text = "0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER3_SPC1"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 1700, yPos = 1000, width = 1500, height = 80, text = "0123456789", anchor = 'S')
        guios["TEXTELEMENTTESTER3_SPC2"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 3300, yPos = 1000, width = 1500, height = 80, text = "0123456789", anchor = 'N')
        guios["TEXTELEMENTTESTER3_SPC3"]     = ATM_Zeta_GUI_TextControl.textObject_SL_IE(**textObjectInst, xPos = 4900, yPos = 1000, width = 1500, height = 80, text = "0123456789", anchor = 'CENTER')

        guios["DISPLAYSWITCH0"] = ATM_Zeta_GUIO_Generals.switch_typeB(**inst, groupOrder=1, xPos= 100, yPos=100, width= 500, height=250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleTLs0)
        guios["DISPLAYSWITCH1"] = ATM_Zeta_GUIO_Generals.switch_typeB(**inst, groupOrder=1, xPos= 700, yPos=100, width= 500, height=250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleTLs1)
        guios["DISPLAYSWITCH2"] = ATM_Zeta_GUIO_Generals.switch_typeB(**inst, groupOrder=1, xPos=1300, yPos=100, width= 500, height=250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleTLs2)

        if   (visualManager.getGUITheme() == 'LIGHT'): themeSwitchStatus = True
        elif (visualManager.getGUITheme() == 'DARK'):  themeSwitchStatus = False
        guios["GUITHEMESWITCH"] = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,  groupOrder=1, xPos=2000, yPos=100, width=500, height=250, style="styleA", align = 'horizontal', switchStatus = themeSwitchStatus, releaseFunction = objFunc_ToggleTheme)
        guios["GUITHEMETEXT"]   = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=1, xPos=2600, yPos=100, width=500, height=250, style="styleA", text=visualManager.getGUITheme())

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-EXPERIMENT0 END--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    


#PAGE-EXPERIMENT1 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_EXPERIMENT1(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND'] = pyglet.graphics.Group(order = 0)

    #OBJECT FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Button Test 0
    def objFunc_ToggleFullScreen(objectInstance, **kwargs):
        systemFunctions["TOGGLE_FULLSCREEN"]()
    def objFunc_ToggleActive_FullScreenButton(objectInstance, **kwargs):
        if (guios['BUTTONTEST0_BUTTONACTIVATIONSWITCH'].getStatus() == True): guios['BUTTONTEST0_BUTTON'].activate()
        else:                                                                 guios['BUTTONTEST0_BUTTON'].deactivate()
    def objFunc_ToggleDisplay_FullScreenButton(objectInstance, **kwargs):
        if (guios['BUTTONTEST0_BUTTONDISPLAYSWITCH'].getStatus() == True): guios['BUTTONTEST0_BUTTON'].show()
        else:                                                              guios['BUTTONTEST0_BUTTON'].hide()

    #Switch Type_A Test
    def objFunc_SwitchTypeATest(objectInstance, **kwargs):
        guios["SWITCHTEST0_SWITCHTEXT"].updateText(str(guios["SWITCHTEST0_SWITCH"].getStatus()))
    def objFunc_ToggleActive_SwitchTest0(objectInstance, **kwargs):
        if (guios['SWITCHTEST0_SWITCHACTIVATIONSWITCH'].getStatus() == True): guios['SWITCHTEST0_SWITCH'].activate()
        else:                                                                 guios['SWITCHTEST0_SWITCH'].deactivate()
    def objFunc_ToggleDisplay_SwitchTest0(objectInstance, **kwargs):
        if (guios['SWITCHTEST0_SWITCHDISPLAYSWITCH'].getStatus() == True): guios['SWITCHTEST0_SWITCH'].show()
        else:                                                              guios['SWITCHTEST0_SWITCH'].hide()

    #Switch Type_B Test
    def objFunc_SwitchTypeBTest(objectInstance, **kwargs):
        guios["SWITCHTEST1_SWITCHTEXT"].updateText(str(guios["SWITCHTEST1_SWITCH"].getStatus()))
    def objFunc_ToggleActive_SwitchTest1(objectInstance, **kwargs):
        if (guios['SWITCHTEST1_SWITCHACTIVATIONSWITCH'].getStatus() == True): guios['SWITCHTEST1_SWITCH'].activate()
        else:                                                                 guios['SWITCHTEST1_SWITCH'].deactivate()
    def objFunc_ToggleDisplay_SwitchTest1(objectInstance, **kwargs):
        if (guios['SWITCHTEST1_SWITCHDISPLAYSWITCH'].getStatus() == True): guios['SWITCHTEST1_SWITCH'].show()
        else:                                                              guios['SWITCHTEST1_SWITCH'].hide()

    #Slider Test 0
    def objFunc_SliderTest_Slider0(objectInstance, **kwargs): guios["SLIDERTEST0_SLIDERTEXT0"].updateText("H: {:f}".format(guios["SLIDERTEST0_SLIDERH"].getSliderValue()))
    def objFunc_SliderTest_Slider1(objectInstance, **kwargs): guios["SLIDERTEST0_SLIDERTEXT1"].updateText("V: {:f}".format(guios["SLIDERTEST0_SLIDERV"].getSliderValue()))
    def objFunc_ToggleActive_SliderTest0(objectInstance, **kwargs):
        if (guios['SLIDERTEST0_SLIDERACTIVATIONSWITCH'].getStatus() == True): guios['SLIDERTEST0_SLIDERH'].activate();   guios['SLIDERTEST0_SLIDERV'].activate()
        else:                                                                 guios['SLIDERTEST0_SLIDERH'].deactivate(); guios['SLIDERTEST0_SLIDERV'].deactivate()
    def objFunc_ToggleDisplay_SliderTest0(objectInstance, **kwargs):
        if (guios['SLIDERTEST0_SLIDERDISPLAYSWITCH'].getStatus() == True): guios['SLIDERTEST0_SLIDERH'].show(); guios['SLIDERTEST0_SLIDERV'].show()
        else:                                                              guios['SLIDERTEST0_SLIDERH'].hide(); guios['SLIDERTEST0_SLIDERV'].hide()

    #ScrollBar Test 0
    def objFunc_ScrollBarTest_ScrollBar0(objectInstance, **kwargs): guios["SCROLLBAR0_SCROLLBARTEXT0"].updateText("H: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARH"].getViewRange())))
    def objFunc_ScrollBarTest_ScrollBar1(objectInstance, **kwargs): guios["SCROLLBAR0_SCROLLBARTEXT1"].updateText("V: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARV"].getViewRange())))
    def objFunc_ToggleActive_ScrollBarTest0(objectInstance, **kwargs):
        if (guios['SCROLLBAR0_SCROLLBARACTIVATIONSWITCH'].getStatus() == True): guios['SCROLLBAR0_SCROLLBARH'].activate();   guios['SCROLLBAR0_SCROLLBARV'].activate()
        else:                                                                   guios['SCROLLBAR0_SCROLLBARH'].deactivate(); guios['SCROLLBAR0_SCROLLBARV'].deactivate()
    def objFunc_ToggleDisplay_ScrollBarTest0(objectInstance, **kwargs):
        if (guios['SCROLLBAR0_SCROLLBARDISPLAYSWITCH'].getStatus() == True): guios['SCROLLBAR0_SCROLLBARH'].show(); guios['SCROLLBAR0_SCROLLBARV'].show()
        else:                                                                guios['SCROLLBAR0_SCROLLBARH'].hide(); guios['SCROLLBAR0_SCROLLBARV'].hide()
    def objFunc_ScrollBarTest_ScrollBarWidthH(objectInstance, **kwargs):
        sliderVal = guios["SCROLLBAR0_SCROLLBARWIDTHSLIDERH"].getSliderValue()
        currentViewRangeH = guios["SCROLLBAR0_SCROLLBARH"].getViewRange(); centerValH = (currentViewRangeH[1] + currentViewRangeH[0]) / 2; newViewRangeH = [centerValH - (sliderVal / 2), centerValH + (sliderVal / 2)]
        if (newViewRangeH[0] < 0):   newViewRangeH[1] += 0 - newViewRangeH[0];   newViewRangeH[0] = 0
        if (100 < newViewRangeH[1]): newViewRangeH[0] -= newViewRangeH[1] - 100; newViewRangeH[1] = 100
        guios["SCROLLBAR0_SCROLLBARH"].editViewRange(newViewRangeH)
        guios["SCROLLBAR0_SCROLLBARTEXT0"].updateText("H: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARH"].getViewRange())))
    def objFunc_ScrollBarTest_ScrollBarWidthV(objectInstance, **kwargs):
        sliderVal = guios["SCROLLBAR0_SCROLLBARWIDTHSLIDERV"].getSliderValue()
        currentViewRangeV = guios["SCROLLBAR0_SCROLLBARV"].getViewRange(); centerValV = (currentViewRangeV[1] + currentViewRangeV[0]) / 2; newViewRangeV = [centerValV - (sliderVal / 2), centerValV + (sliderVal / 2)]
        if (newViewRangeV[0] < 0):   newViewRangeV[1] += 0 - newViewRangeV[0];   newViewRangeV[0] = 0
        if (100 < newViewRangeV[1]): newViewRangeV[0] -= newViewRangeV[1] - 100; newViewRangeV[1] = 100
        guios["SCROLLBAR0_SCROLLBARV"].editViewRange(newViewRangeV)
        guios["SCROLLBAR0_SCROLLBARTEXT1"].updateText("V: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARV"].getViewRange())))
        
    #LED Test 0
    def objFunc_LEDTest_Switch(objectInstance, **kwargs):
        guios["LEDTEST_LED0"].setMode(objectInstance.getStatus())
        guios["LEDTEST_LED1"].setMode(objectInstance.getStatus())
    def objFunc_ToggleDisplay_LEDTest0(objectInstance, **kwargs):
        if (objectInstance.getStatus() == True): guios['LEDTEST_LED0'].show(); guios['LEDTEST_LED1'].show()
        else:                                    guios['LEDTEST_LED0'].hide(); guios['LEDTEST_LED1'].hide()
    def objFunc_LED_ColorUpdateR(objectInstance, **kwargs):
        guios["LEDTEST_LED0"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_LED1"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_SLIDER_R_VALUETEXT"].updateText("{:d}".format(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55)))
    def objFunc_LED_ColorUpdateG(objectInstance, **kwargs):
        guios["LEDTEST_LED0"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_LED1"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_SLIDER_G_VALUETEXT"].updateText("{:d}".format(round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55)))
    def objFunc_LED_ColorUpdateB(objectInstance, **kwargs):
        guios["LEDTEST_LED0"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_LED1"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_SLIDER_B_VALUETEXT"].updateText("{:d}".format(round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55)))
    def objFunc_LED_ColorUpdateA(objectInstance, **kwargs):
        guios["LEDTEST_LED0"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_LED1"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_SLIDER_A_VALUETEXT"].updateText("{:d}".format(round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55)))
        
    #GaugeBar Test 0
    def objFunc_GaugeBarTest0_SliderHValUpdated(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARH0"].updateGaugeValue(guios["GAUGEBARTEST_GAUGEBARHSLIDER"].getSliderValue())
        guios["GAUGEBARTEST_GAUGEBARH1"].updateGaugeValue(guios["GAUGEBARTEST_GAUGEBARHSLIDER"].getSliderValue())
        guios["GAUGEBARTEST_GAUGEBARHSLIDER_VALUETEXT"].updateText("{:.3f}".format(guios["GAUGEBARTEST_GAUGEBARHSLIDER"].getSliderValue()))
    def objFunc_GaugeBarTest0_SliderVValUpdated(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARV0"].updateGaugeValue(guios["GAUGEBARTEST_GAUGEBARVSLIDER"].getSliderValue())
        guios["GAUGEBARTEST_GAUGEBARV1"].updateGaugeValue(guios["GAUGEBARTEST_GAUGEBARVSLIDER"].getSliderValue())
        guios["GAUGEBARTEST_GAUGEBARVSLIDER_VALUETEXT"].updateText("{:.3f}".format(guios["GAUGEBARTEST_GAUGEBARVSLIDER"].getSliderValue()))
    def objFunc_GAUGEBARTEST_ColorUpdateR(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARH0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARH1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_SLIDER_R_VALUETEXT"].updateText("{:d}".format(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55)))
    def objFunc_GAUGEBARTEST_ColorUpdateG(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARH0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARH1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_SLIDER_G_VALUETEXT"].updateText("{:d}".format(round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55)))
    def objFunc_GAUGEBARTEST_ColorUpdateB(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARH0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARH1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_SLIDER_B_VALUETEXT"].updateText("{:d}".format(round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55)))
    def objFunc_GAUGEBARTEST_ColorUpdateA(objectInstance, **kwargs):
        guios["GAUGEBARTEST_GAUGEBARH0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARH1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV0"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_GAUGEBARV1"].updateGaugeColor(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["GAUGEBARTEST_SLIDER_A_VALUETEXT"].updateText("{:d}".format(round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55)))
    def objFunc_ToggleDisplay_GAUGEBARTEST(objectInstance, **kwargs):
        if (guios['GAUGEBARTEST_GAUGEBARDISPLAYSWITCH'].getStatus() == True): guios['GAUGEBARTEST_GAUGEBARH0'].show(); guios['GAUGEBARTEST_GAUGEBARH1'].show(); guios['GAUGEBARTEST_GAUGEBARV0'].show(); guios['GAUGEBARTEST_GAUGEBARV1'].show()
        else:                                                                 guios['GAUGEBARTEST_GAUGEBARH0'].hide(); guios['GAUGEBARTEST_GAUGEBARH1'].hide(); guios['GAUGEBARTEST_GAUGEBARV0'].hide(); guios['GAUGEBARTEST_GAUGEBARV1'].hide()
        
    #TextInputBox Test 0
    def objFunc_ToggleActive_TextInputBox(objectInstance, **kwargs):
        if (guios['TEXTINPUTBOXTEST_TEXTINPUTBOXACTIVATIONSWITCH'].getStatus() == True): guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].activate()
        else:                                                                            guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].deactivate()
    def objFunc_ToggleDisplay_TextInputBox(objectInstance, **kwargs):
        if (guios['TEXTINPUTBOXTEST_TEXTINPUTBOXDISPLAYSWITCH'].getStatus() == True): guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].show()
        else:                                                                         guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].hide()
    def objFunc_CopyText_TextInputBox(objectInstance, **kwargs):
        guios["TEXTINPUTBOXTEST_TEXTCOPYBOX"].updateText(guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].getText())
    def objFunc_CopyText_TextInputBox1(objectInstance, **kwargs):
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX1"].updateText(guios['TEXTINPUTBOXTEST_TEXTINPUTBOX'].getText())
        
    #Audio Control Test 0
    def objFunc_AudioControlTest_AudioMute(objectInstance, **kwargs):
        if (guios['AUDIOCONTROLTEST_AUDIOMUTESWITCH'].getStatus() == True): audioManager.setMute(True)
        else:                                                               audioManager.setMute(False)

    def objFunc_AudioControlTest_AdjustVolume(objectInstance, **kwargs):
        audioManager.setVolume(guios["AUDIOCONTROLTEST_VOLUMESLIDER"].getSliderValue())
        guios["AUDIOCONTROLTEST_VOLUMEVALUE"].updateText("{:.1f}".format(audioManager.getVolume()))

    #Passive Graphics Test0
    def objFunc_ToggleDisplay_PG_Wrapper(objectInstance, **kwargs):
        if (guios['PASSIVEGRAPHICSTEST_WRAPPEROBJECT0_DISPLAYSWITCH'].getStatus() == True): 
            guios['PASSIVEGRAPHICSTEST_WRAPPEROBJECT0'].show()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX0'].show()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX1'].show()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX2'].show()
        else:                                                                               
            guios['PASSIVEGRAPHICSTEST_WRAPPEROBJECT0'].hide()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX0'].hide()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX1'].hide()
            guios['PASSIVEGRAPHICSTEST_IMAGEBOX2'].hide()
            
    #Button Test 1
    def objFunc_ToggleActive_FullScreenButton1(objectInstance, **kwargs):
        if (guios['BUTTONTEST1_BUTTONACTIVATIONSWITCH'].getStatus() == True): guios['BUTTONTEST1_BUTTON0'].activate()
        else:                                                                 guios['BUTTONTEST1_BUTTON0'].deactivate()
    def objFunc_ToggleDisplay_FullScreenButton1(objectInstance, **kwargs):
        if (guios['BUTTONTEST1_BUTTONDISPLAYSWITCH'].getStatus() == True): guios['BUTTONTEST1_BUTTON0'].show()
        else:                                                              guios['BUTTONTEST1_BUTTON0'].hide()

    #SelectionBox Test
    def objFunc_SelectionBoxTest_SelectionUpdateFunction(objectInstance, **kwargs):
        print(objectInstance.getSelected())
    def objFunc_ToggleActive_SelectionBox(objectInstance, **kwargs):
        if (guios['SELECTIONBOXTEST0_SELECTIONBOXACTIVATIONSWITCH'].getStatus() == True): guios['SELECTIONBOXTEST0_SELECTIONBOX'].activate()
        else:                                                                             guios['SELECTIONBOXTEST0_SELECTIONBOX'].deactivate()
    def objFunc_ToggleDisplay_SelectionBox(objectInstance, **kwargs):
        if (guios['SELECTIONBOXTEST0_SELECTIONBOXDISPLAYSWITCH'].getStatus() == True): guios['SELECTIONBOXTEST0_SELECTIONBOX'].show()
        else:                                                                          guios['SELECTIONBOXTEST0_SELECTIONBOX'].hide()

    #Theme/Language
    def objFunc_ToggleTheme(objectInstance, **kwargs):
        if (guios['GUITHEMESWITCH'].getStatus() == True): newTheme = 'LIGHT'
        else:                                             newTheme = 'DARK'
        guios["GUITHEMETEXT"].updateText(newTheme)
        systemFunctions['CHANGEGUITHEME'](newTheme)
        
    def objFunc_ToggleLanguage(objectInstance, **kwargs):
        if (guios['LANGUAGESWITCH'].getStatus() == True): newLanguage = 'KOR'
        else:                                             newLanguage = 'ENG'
        guios["LANGUAGETEXT"].updateText(newLanguage)
        systemFunctions['CHANGELANGUAGE'](newLanguage)
        
    def objFunc_ToggleActive_SelectionBox1(objectInstance, **kwargs):
        if (guios['SELECTIONBOXTEST1_SELECTIONBOXACTIVATIONSWITCH'].getStatus() == True): guios['SELECTIONBOXTEST1_SELECTIONBOX'].activate()
        else:                                                                             guios['SELECTIONBOXTEST1_SELECTIONBOX'].deactivate()
    def objFunc_ToggleDisplay_SelectionBox1(objectInstance, **kwargs):
        if (guios['SELECTIONBOXTEST1_SELECTIONBOXDISPLAYSWITCH'].getStatus() == True): guios['SELECTIONBOXTEST1_SELECTIONBOX'].show()
        else:                                                                          guios['SELECTIONBOXTEST1_SELECTIONBOX'].hide()

    def objFunc_ClearSelectionBox0(objectInstance, **kwargs):
        guios["SELECTIONBOXTEST0_SELECTIONBOX"].clearSelectionList()

    def objFunc_SetSelectionBox0(objectInstance, **kwargs):
        strList = ['SELECTION', 'CHOICE', 'TESTER', 'CLEARED']
        strToUse = strList[random.randint(0,0)]
        selectionList = dict()
        for i in range (500): 
            itemKey = strToUse+str(i)
            selectionList[itemKey] = {'text': itemKey}
        guios["SELECTIONBOXTEST0_SELECTIONBOX"].setSelectionList(selectionList = selectionList, displayTargets = 'all', keepSelected = True)

    #OBJECT FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))
        
        guios["BUTTONTEST0_WRAPPER"]                    = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=100, yPos=7750, width=2000, height=1150, style="styleA", text = "BUTTON TEST")
        guios["BUTTONTEST0_BUTTON"]                     = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=2, xPos=200, yPos=8450, width=1800, height= 250, style="styleA", releaseFunction=objFunc_ToggleFullScreen, text=visualManager.getTextPack('EXPERIMENT0:FULLSCREEN'))
        guios["BUTTONTEST0_BUTTONACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=200, yPos=8150, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_FullScreenButton)
        guios["BUTTONTEST0_BUTTONACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=750, yPos=8150, width=1250, height= 250, style="styleA", text="ACTIVATION")
        guios["BUTTONTEST0_BUTTONDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=200, yPos=7850, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_FullScreenButton)
        guios["BUTTONTEST0_BUTTONDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=750, yPos=7850, width=1250, height= 250, style="styleA", text="DISPLAY")
        
        guios["SWITCHTEST0_WRAPPER"]                    = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=2200, yPos=7750, width=2000, height=1150, style="styleA", text = "SWITCH TypeA TEST");
        guios["SWITCHTEST0_SWITCH"]                     = ATM_Zeta_GUIO_Generals.switch_typeA(**inst,                 groupOrder=1, xPos=2300, yPos=8450, width= 500, height= 250, style="styleA", releaseFunction = objFunc_SwitchTypeATest)
        guios["SWITCHTEST0_SWITCHTEXT"]                 = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2850, yPos=8450, width=1250, height= 250, style="styleA", text=str(guios["SWITCHTEST0_SWITCH"].getStatus()))
        guios["SWITCHTEST0_SWITCHACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=2300, yPos=8150, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_SwitchTest0)
        guios["SWITCHTEST0_SWITCHACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2850, yPos=8150, width=1250, height= 250, style="styleA", text="ACTIVATION")
        guios["SWITCHTEST0_SWITCHDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=2300, yPos=7850, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_SwitchTest0)
        guios["SWITCHTEST0_SWITCHDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2850, yPos=7850, width=1250, height= 250, style="styleA", text="DISPLAY")
        
        guios["SWITCHTEST1_WRAPPER"]                    = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=4300, yPos=7750, width=2000, height=1150, style="styleA", text = "SWITCH TypeB TEST");
        guios["SWITCHTEST1_SWITCH"]                     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=1, xPos=4400, yPos=8450, width= 500, height= 250, style="styleA", releaseFunction = objFunc_SwitchTypeBTest)
        guios["SWITCHTEST1_SWITCHTEXT"]                 = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4950, yPos=8450, width=1250, height= 250, style="styleA", text=str(guios["SWITCHTEST1_SWITCH"].getStatus()))
        guios["SWITCHTEST1_SWITCHACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=4400, yPos=8150, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_SwitchTest1)
        guios["SWITCHTEST1_SWITCHACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4950, yPos=8150, width=1250, height= 250, style="styleA", text="ACTIVATION")
        guios["SWITCHTEST1_SWITCHDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=4400, yPos=7850, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_SwitchTest1)
        guios["SWITCHTEST1_SWITCHDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4950, yPos=7850, width=1250, height= 250, style="styleA", text="DISPLAY")
        
        guios["SLIDERTEST0_WRAPPER"]                    = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=6400, yPos=6600, width=2000, height=2300, style="styleA", text = "SLIDER TEST");
        guios["SLIDERTEST0_SLIDERH"]                    = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=6500, yPos=8550, width=1800, height= 200, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_SliderTest_Slider0);
        guios["SLIDERTEST0_SLIDERV"]                    = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=6500, yPos=6700, width=1800, height= 200, style="styleA", align = 'vertical',   valueUpdateFunction = objFunc_SliderTest_Slider1);
        guios["SLIDERTEST0_SLIDERTEXT0"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=6800, yPos=8300, width=1500, height= 200, style="styleA", text="H: {:f}".format(guios["SLIDERTEST0_SLIDERH"].getSliderValue()))
        guios["SLIDERTEST0_SLIDERTEXT1"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=6800, yPos=8050, width=1500, height= 200, style="styleA", text="V: {:f}".format(guios["SLIDERTEST0_SLIDERV"].getSliderValue()))
        guios["SLIDERTEST0_SLIDERACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=6800, yPos=7750, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_SliderTest0)
        guios["SLIDERTEST0_SLIDERACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=7350, yPos=7750, width= 950, height= 250, style="styleA", text="ACTIVATION")
        guios["SLIDERTEST0_SLIDERDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=6800, yPos=7450, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_SliderTest0)
        guios["SLIDERTEST0_SLIDERDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=7350, yPos=7450, width= 950, height= 250, style="styleA", text="DISPLAY")
        
        guios["SCROLLBAR0_WRAPPER"]                       = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=8500, yPos=6600, width=2000, height=2300, style="styleA", text = "SCROLLBAR TEST");
        guios["SCROLLBAR0_SCROLLBARH"]                    = ATM_Zeta_GUIO_Generals.scrollBar_typeA(**inst,              groupOrder=1, xPos=8600, yPos=8600, width=1800, height= 100, style="styleA", align = 'horizontal', viewRangeUpdateFunction = objFunc_ScrollBarTest_ScrollBar0);
        guios["SCROLLBAR0_SCROLLBARV"]                    = ATM_Zeta_GUIO_Generals.scrollBar_typeA(**inst,              groupOrder=1, xPos=8600, yPos=6750, width=1800, height= 100, style="styleA", align = 'vertical',   viewRangeUpdateFunction = objFunc_ScrollBarTest_ScrollBar1);
        guios["SCROLLBAR0_SCROLLBARTEXT0"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=8800, yPos=8300, width=1600, height= 200, style="styleA", text="H: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARH"].getViewRange())))
        guios["SCROLLBAR0_SCROLLBARTEXT1"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=8800, yPos=8050, width=1600, height= 200, style="styleA", text="V: {:s}".format(str(guios["SCROLLBAR0_SCROLLBARV"].getViewRange())))
        guios["SCROLLBAR0_SCROLLBARACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=8800, yPos=7750, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_ScrollBarTest0)
        guios["SCROLLBAR0_SCROLLBARACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=9350, yPos=7750, width=1050, height= 250, style="styleA", text="ACTIVATION")
        guios["SCROLLBAR0_SCROLLBARDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=8800, yPos=7450, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_ScrollBarTest0)
        guios["SCROLLBAR0_SCROLLBARDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=9350, yPos=7450, width=1050, height= 250, style="styleA", text="DISPLAY")
        guios["SCROLLBAR0_SCROLLBARWIDTHSLIDERH"]         = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=8800, yPos=7200, width=1600, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_ScrollBarTest_ScrollBarWidthH);
        guios["SCROLLBAR0_SCROLLBARWIDTHSLIDERV"]         = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=8800, yPos=7000, width=1600, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_ScrollBarTest_ScrollBarWidthV);
        
        guios["LEDTEST_WRAPPER"]                 = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=10600, yPos=6600, width=2000, height=2300, style="styleA", text = "LED TEST");
        guios["LEDTEST_LED0"]                    = ATM_Zeta_GUIO_Generals.LED_typeA(**inst,                    groupOrder=1, xPos=10700, yPos=8500, width=1800, height= 200, style="styleA")
        guios["LEDTEST_LED1"]                    = ATM_Zeta_GUIO_Generals.LED_typeA(**inst,                    groupOrder=1, xPos=10700, yPos=8250, width=1800, height= 200, style="styleB")
        guios["LEDTEST_LEDPOWERSWITCH"]          = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=10700, yPos=7950, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_LEDTest_Switch)
        guios["LEDTEST_LEDPOWERSWITCHTEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=11250, yPos=7950, width=1250, height= 250, style="styleA", text="LED POWER")
        guios["LEDTEST_SWITCHDISPLAYSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=10700, yPos=7650, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_LEDTest0)
        guios["LEDTEST_SWITCHDISPLAYSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=11250, yPos=7650, width=1250, height= 250, style="styleA", text="DISPLAY")
        guios["LEDTEST_SLIDER_R_TEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=10700, yPos=7400, width= 100, height= 150, style=None,     text="R")
        guios["LEDTEST_SLIDER_G_TEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=10700, yPos=7200, width= 100, height= 150, style=None,     text="G")
        guios["LEDTEST_SLIDER_B_TEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=10700, yPos=7000, width= 100, height= 150, style=None,     text="B")
        guios["LEDTEST_SLIDER_A_TEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=10700, yPos=6800, width= 100, height= 150, style=None,     text="A")
        guios["LEDTEST_SLIDER_R"]                = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=10850, yPos=7400, width=1300, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_LED_ColorUpdateR);
        guios["LEDTEST_SLIDER_G"]                = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=10850, yPos=7200, width=1300, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_LED_ColorUpdateG);
        guios["LEDTEST_SLIDER_B"]                = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=10850, yPos=7000, width=1300, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_LED_ColorUpdateB);
        guios["LEDTEST_SLIDER_A"]                = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=10850, yPos=6800, width=1300, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_LED_ColorUpdateA);
        guios["LEDTEST_SLIDER_R_VALUETEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=12200, yPos=7400, width= 300, height= 150, style=None,     text="{:d}".format(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55)))
        guios["LEDTEST_SLIDER_G_VALUETEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=12200, yPos=7200, width= 300, height= 150, style=None,     text="{:d}".format(round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55)))
        guios["LEDTEST_SLIDER_B_VALUETEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=12200, yPos=7000, width= 300, height= 150, style=None,     text="{:d}".format(round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55)))
        guios["LEDTEST_SLIDER_A_VALUETEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=12200, yPos=6800, width= 300, height= 150, style=None,     text="{:d}".format(round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55)))
        guios["LEDTEST_LED0"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        guios["LEDTEST_LED1"].updateColor(round(guios["LEDTEST_SLIDER_R"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_G"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_B"].getSliderValue()*2.55),round(guios["LEDTEST_SLIDER_A"].getSliderValue()*2.55))
        
        guios["GAUGEBARTEST_WRAPPER"]                   = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=12700, yPos=6600, width=3200, height=2300, style="styleA", text = "GAUGEBAR TEST");
        guios["GAUGEBARTEST_GAUGEBARH0"]                = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos=13300, yPos=8500, width=2500, height= 200, style="styleA", align = 'horizontal')
        guios["GAUGEBARTEST_GAUGEBARH1"]                = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos=13300, yPos=8250, width=2500, height= 200, style="styleB", align = 'horizontal')
        guios["GAUGEBARTEST_GAUGEBARV0"]                = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos=12800, yPos=6750, width=1950, height= 200, style="styleB", align = 'vertical')
        guios["GAUGEBARTEST_GAUGEBARV1"]                = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos=13050, yPos=6750, width=1950, height= 200, style="styleA", align = 'vertical')
        guios["GAUGEBARTEST_GAUGEBARHSLIDER_TEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=8000, width= 100, height= 150, style=None,     text="H")
        guios["GAUGEBARTEST_GAUGEBARHSLIDER"]           = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=8000, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GaugeBarTest0_SliderHValUpdated);
        guios["GAUGEBARTEST_GAUGEBARHSLIDER_VALUETEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=8000, width= 500, height= 150, style=None,     text="{:.3f}".format(guios["GAUGEBARTEST_GAUGEBARHSLIDER"].getSliderValue()))
        guios["GAUGEBARTEST_GAUGEBARVSLIDER_TEXT"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=7800, width= 100, height= 150, style=None,     text="V")
        guios["GAUGEBARTEST_GAUGEBARVSLIDER"]           = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=7800, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GaugeBarTest0_SliderVValUpdated);
        guios["GAUGEBARTEST_GAUGEBARVSLIDER_VALUETEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=7800, width= 500, height= 150, style=None,     text="{:.3f}".format(guios["GAUGEBARTEST_GAUGEBARVSLIDER"].getSliderValue()))
        guios["GAUGEBARTEST_SLIDER_R_TEXT"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=7600, width= 100, height= 150, style=None,     text="R")
        guios["GAUGEBARTEST_SLIDER_G_TEXT"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=7400, width= 100, height= 150, style=None,     text="G")
        guios["GAUGEBARTEST_SLIDER_B_TEXT"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=7200, width= 100, height= 150, style=None,     text="B")
        guios["GAUGEBARTEST_SLIDER_A_TEXT"]             = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=13300, yPos=7000, width= 100, height= 150, style=None,     text="A")
        guios["GAUGEBARTEST_SLIDER_R"]                  = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=7600, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GAUGEBARTEST_ColorUpdateR);
        guios["GAUGEBARTEST_SLIDER_G"]                  = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=7400, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GAUGEBARTEST_ColorUpdateG);
        guios["GAUGEBARTEST_SLIDER_B"]                  = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=7200, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GAUGEBARTEST_ColorUpdateB);
        guios["GAUGEBARTEST_SLIDER_A"]                  = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=13500, yPos=7000, width=1700, height= 150, style="styleA", align = 'horizontal', valueUpdateFunction = objFunc_GAUGEBARTEST_ColorUpdateA);
        guios["GAUGEBARTEST_SLIDER_R_VALUETEXT"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=7600, width= 500, height= 150, style=None,     text="{:d}".format(round(guios["GAUGEBARTEST_SLIDER_R"].getSliderValue()*2.55)))
        guios["GAUGEBARTEST_SLIDER_G_VALUETEXT"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=7400, width= 500, height= 150, style=None,     text="{:d}".format(round(guios["GAUGEBARTEST_SLIDER_G"].getSliderValue()*2.55)))
        guios["GAUGEBARTEST_SLIDER_B_VALUETEXT"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=7200, width= 500, height= 150, style=None,     text="{:d}".format(round(guios["GAUGEBARTEST_SLIDER_B"].getSliderValue()*2.55)))
        guios["GAUGEBARTEST_SLIDER_A_VALUETEXT"]        = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=15300, yPos=7000, width= 500, height= 150, style=None,     text="{:d}".format(round(guios["GAUGEBARTEST_SLIDER_A"].getSliderValue()*2.55)))
        objFunc_GAUGEBARTEST_ColorUpdateR(None); objFunc_GAUGEBARTEST_ColorUpdateG(None); objFunc_GAUGEBARTEST_ColorUpdateB(None); objFunc_GAUGEBARTEST_ColorUpdateA(None)
        guios["GAUGEBARTEST_GAUGEBARDISPLAYSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=13500, yPos=6700, width= 500, height= 200, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_GAUGEBARTEST)
        guios["GAUGEBARTEST_GAUGEBARDISPLAYSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=14100, yPos=6700, width= 950, height= 200, style="styleA", text="DISPLAY")
        
        guios["TEXTINPUTBOXTEST_WRAPPER"]                          = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos= 100, yPos=5400, width=6200, height=2250, style="styleA", text = "TEXTINPUTBOX TEST")
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"]                     = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,           groupOrder=2, xPos= 200, yPos=6950, width=6000, height= 500, style="styleA", text="", fontSize = 200)
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOXACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos= 200, yPos=6650, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_TextInputBox)
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOXACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 750, yPos=6650, width=1250, height= 250, style="styleA", text="ACTIVATION")
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOXDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos= 200, yPos=6350, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_TextInputBox)
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOXDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 750, yPos=6350, width=1250, height= 250, style="styleA", text="DISPLAY")
        guios["TEXTINPUTBOXTEST_TEXTCOPYBOX"]                      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2050, yPos=6650, width=4150, height= 250, style="styleA", text="")
        guios["TEXTINPUTBOXTEST_TEXTCOPYBUTTON"]                   = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=2, xPos=2050, yPos=6350, width=4150, height= 250, style="styleA", releaseFunction=objFunc_CopyText_TextInputBox,  text="COPY TEXT FROM TEXTINPUTBOX")
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX1"]                    = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,           groupOrder=2, xPos= 200, yPos=5850, width=5950, height= 500, style=None,     text="", fontSize = 200)
        guios["TEXTINPUTBOXTEST_TEXTCOPYBUTTON1"]                  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=2, xPos= 200, yPos=5550, width=5950, height= 250, style="styleA", releaseFunction=objFunc_CopyText_TextInputBox1, text="COPY TEXT FROM TEXTINPUTBOX")
        testTextStyle1 = {'bold': True, 'italic': False, 'color': (100, 255, 150, 255), 'anchor_x': 'center', 'anchor_y': 'center', 'selectionColor': (30, 30, 30, 255), 'selectionBackgroundColor': (30, 30, 30, 255), 'caretColor': (255, 255, 100, 255)}
        testTextStyle2 = {'bold': True, 'italic': False, 'color': (100, 150, 255, 255), 'anchor_x': 'center', 'anchor_y': 'center', 'selectionColor': (30, 30, 30, 255), 'selectionBackgroundColor': (30, 30, 30, 255), 'caretColor': (255, 255, 100, 255)}
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"].textElement.addTextStyle('GREEN', testTextStyle1)
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"].textElement.addTextStyle('BLUE', testTextStyle2)
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"].textElement.insertText('ABCDEFG', 0, textStyle = 'GREEN')
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"].textElement.insertText('012345', 3, textStyle = 'BLUE')
        guios["TEXTINPUTBOXTEST_TEXTINPUTBOX"].textElement.insertText('XYZ', 12)

        guios["AUDIOCONTROLTEST_WRAPPER"]             = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos= 100, yPos=3300, width=3200, height=2000, style="styleA", text = "AUDIO CONTROL TEST")
        guios["AUDIOCONTROLTEST_AUDIOMUTESWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos= 200, yPos=4850, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = audioManager.isMuted(), releaseFunction = objFunc_AudioControlTest_AudioMute)
        guios["AUDIOCONTROLTEST_AUDIOMUTESWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 750, yPos=4850, width=1250, height= 250, style="styleA", text="AUDIO MUTE")
        guios["AUDIOCONTROLTEST_VOLUMESLIDERTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos= 200, yPos=4500, width= 700, height= 250, style="styleA", text="VOLUME")
        guios["AUDIOCONTROLTEST_VOLUMESLIDER"]        = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=1000, yPos=4500, width=1400, height= 250, style="styleA", align ='horizontal', valueUpdateFunction = objFunc_AudioControlTest_AdjustVolume, sliderValue = audioManager.getVolume())
        guios["AUDIOCONTROLTEST_VOLUMEVALUE"]         = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2500, yPos=4500, width= 700, height= 250, style="styleA", text="{:.1f}".format(audioManager.getVolume()))
        
        guios["PASSIVEGRAPHICSTEST_WRAPPER"]                          = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=6400, yPos= 100, width=9500, height=6400, style="styleA", text = "PASSIVE GRAPHICS TEST")
        guios["PASSIVEGRAPHICSTEST_WRAPPEROBJECT0"]                   = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=2, xPos=6500, yPos=5400, width=2000, height=1000, style="styleA", text = "PG_WRAPPER", fontSize = 100)
        guios["PASSIVEGRAPHICSTEST_WRAPPEROBJECT0_DISPLAYSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=8600, yPos=6050, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_PG_Wrapper)
        guios["PASSIVEGRAPHICSTEST_WRAPPEROBJECT0_DISPLAYSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=9150, yPos=6050, width=1250, height= 250, style="styleA", text="DISPLAY")
        guios["PASSIVEGRAPHICSTEST_IMAGEBOX0"]                        = ATM_Zeta_GUIO_Generals.imageBox_typeA(**inst,               groupOrder=2, xPos=6500, yPos=4800, width= 500, height= 500, style="styleA", image = 'binanceIcon_512x512.png')
        guios["PASSIVEGRAPHICSTEST_IMAGEBOX1"]                        = ATM_Zeta_GUIO_Generals.imageBox_typeA(**inst,               groupOrder=2, xPos=7050, yPos=4800, width= 500, height= 500, style="styleA", image = None)
        guios["PASSIVEGRAPHICSTEST_IMAGEBOX2"]                        = ATM_Zeta_GUIO_Generals.imageBox_typeA(**inst,               groupOrder=2, xPos=7600, yPos=4800, width= 500, height= 500, style=None,     image = 'binanceIcon_512x512.png')

        guios["BUTTONTEST1_WRAPPER"]                    = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=3400, yPos=4400, width=2900, height=900, style="styleA", text = "BUTTON TEST")
        guios["BUTTONTEST1_BUTTON0"]                    = ATM_Zeta_GUIO_Generals.button_typeB(**inst,                 groupOrder=2, xPos=3500, yPos=4500, width= 550, height=550, style="styleB", releaseFunction=objFunc_ToggleFullScreen, image = 'fullscreenIcon_512x512.png', imageSize = (400, 400), imageRGBA = visualManager.getFromColorTable('ICON_COLORING'))
        guios["BUTTONTEST1_BUTTONACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=4150, yPos=4800, width= 500, height=250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_FullScreenButton1)
        guios["BUTTONTEST1_BUTTONACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4700, yPos=4800, width=1500, height=250, style="styleA", text="ACTIVATION")
        guios["BUTTONTEST1_BUTTONDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=4150, yPos=4500, width= 500, height=250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_FullScreenButton1)
        guios["BUTTONTEST1_BUTTONDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4700, yPos=4500, width=1500, height=250, style="styleA", text="DISPLAY")
        
        guios["SELECTIONBOXTEST0_WRAPPER"]                          = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos= 100, yPos= 100, width=3200, height=3100, style="styleA", text = "SELECTION BOX TEST 0")
        guios["SELECTIONBOXTEST0_SELECTIONBOX"]                     = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst,           groupOrder=1, xPos= 200, yPos= 200, width=1200, height=2800, style="styleA", multiSelect = True, selectionUpdateFunction = objFunc_SelectionBoxTest_SelectionUpdateFunction, elementHeight = 250, fontSize = 80)
        guios["SELECTIONBOXTEST0_SELECTIONBOX"].setSelectionList(selectionList = ['TEST'+str(i) for i in range (500)], displayTargets = 'all', callSelectionUpdateFunction = False)
        guios["SELECTIONBOXTEST0_SELECTIONBOXACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=1450, yPos=2750, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_SelectionBox)
        guios["SELECTIONBOXTEST0_SELECTIONBOXACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2000, yPos=2750, width=1200, height= 250, style="styleA", text="ACTIVATION")
        guios["SELECTIONBOXTEST0_SELECTIONBOXDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=1450, yPos=2450, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_SelectionBox)
        guios["SELECTIONBOXTEST0_SELECTIONBOXDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=2000, yPos=2450, width=1200, height= 250, style="styleA", text="DISPLAY")
        guios["SELECTIONBOXTEST0_CLEARSELECTIONLIST"]               = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=2, xPos=1450, yPos=2150, width=1750, height= 250, style="styleA", releaseFunction=objFunc_ClearSelectionBox0,  text="CLEAR SELECTIONBOX")
        guios["SELECTIONBOXTEST0_SETSELECTIONLIST"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=2, xPos=1450, yPos=1850, width=1750, height= 250, style="styleA", releaseFunction=objFunc_SetSelectionBox0,  text="SET SELECTIONBOX")

        guios["THEME/LANGUAGE_WRAPPER"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=3400, yPos=100, width=2900, height=550, style="styleA", text = "THEME/LANAUGAGE")
        if   (visualManager.getGUITheme() == 'LIGHT'): themeSwitchStatus = True
        elif (visualManager.getGUITheme() == 'DARK'):  themeSwitchStatus = False
        guios["GUITHEMESWITCH"]         = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=1, xPos=3500, yPos=200, width=500, height=250, style="styleA", align = 'horizontal', switchStatus = themeSwitchStatus, releaseFunction = objFunc_ToggleTheme)
        guios["GUITHEMETEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=4100, yPos=200, width=500, height=250, style="styleA", text=visualManager.getGUITheme())
        if   (visualManager.getLanguage() == 'KOR'): themeSwitchStatus = True
        elif (visualManager.getLanguage() == 'ENG'): themeSwitchStatus = False
        guios["LANGUAGESWITCH"]         = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=1, xPos=5100, yPos=200, width=500, height=250, style="styleA", align = 'horizontal', switchStatus = themeSwitchStatus, releaseFunction = objFunc_ToggleLanguage)
        guios["LANGUAGETEXT"]           = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=5700, yPos=200, width=500, height=250, style="styleA", text=visualManager.getLanguage())

        guios["SELECTIONBOXTEST1_WRAPPER"]                          = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=3400, yPos= 750, width=2900, height=3600, style="styleA", text = "SELECTION BOX TEST 1")
        guios["SELECTIONBOXTEST1_SELECTIONBOX"]                     = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst,           groupOrder=1, xPos=3500, yPos=3800, width=2700, height= 300, style="styleA", elementHeight = 250, showIndex = True, fontSize = 80)
        selections = dict()
        selections[0] = {'text': 'SELECTION_0', 'textAnchor': 'NW'}
        selections[1] = {'text': 'SELECTION_1', 'textAnchor': 'N'}
        selections[2] = {'text': 'SELECTION_2', 'textAnchor': 'NE'}
        selections[3] = {'text': 'SELECTION_3', 'textAnchor': 'W'}
        selections[4] = {'text': 'SELECTION_4', 'textAnchor': 'CENTER'}
        selections[5] = {'text': 'SELECTION_5', 'textAnchor': 'E'}
        selections[6] = {'text': 'SELECTION_6', 'textAnchor': 'SW'}
        selections[7] = {'text': 'SELECTION_7', 'textAnchor': 'S'}
        selections[8] = {'text': 'SELECTION_8', 'textAnchor': 'SE'}
        selections[9]  = {'text': 'SELECTION_9',  'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'RED_DARK')]}
        selections[10] = {'text': 'SELECTION_10', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'RED')]}
        selections[11] = {'text': 'SELECTION_11', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'RED_LIGHT')]}
        selections[12] = {'text': 'SELECTION_12', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'ORANGE_DARK')]}
        selections[13] = {'text': 'SELECTION_13', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'ORANGE')]}
        selections[14] = {'text': 'SELECTION_14', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'ORANGE_LIGHT')]}
        selections[15] = {'text': 'SELECTION_15', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'YELLOW_DARK')]}
        selections[16] = {'text': 'SELECTION_16', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'YELLOW')]}
        selections[17] = {'text': 'SELECTION_17', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'YELLOW_LIGHT')]}
        selections[18] = {'text': 'SELECTION_18', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREEN_DARK')]}
        selections[19] = {'text': 'SELECTION_19', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREEN')]}
        selections[20] = {'text': 'SELECTION_20', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREEN_LIGHT')]}
        selections[21] = {'text': 'SELECTION_21', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'BLUE_DARK')]}
        selections[22] = {'text': 'SELECTION_22', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'BLUE')]}
        selections[23] = {'text': 'SELECTION_23', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'BLUE_LIGHT')]}
        selections[24] = {'text': 'SELECTION_24', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'VIOLET_DARK')]}
        selections[25] = {'text': 'SELECTION_25', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'VIOLET')]}
        selections[26] = {'text': 'SELECTION_26', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'VIOLET_LIGHT')]}
        selections[27] = {'text': 'SELECTION_27', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'CYAN_DARK')]}
        selections[28] = {'text': 'SELECTION_28', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'CYAN')]}
        selections[29] = {'text': 'SELECTION_29', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'CYAN_LIGHT')]}
        selections[30] = {'text': 'SELECTION_30', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREY_DARK')]}
        selections[31] = {'text': 'SELECTION_31', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREY')]}
        selections[32] = {'text': 'SELECTION_32', 'textAnchor': 'CENTER', 'textStyles': [((0, 9), 'GREY_LIGHT')]}
        selections[33] = {'text': visualManager.getTextPack('EXPERIMENT1:SELECTIONBOXLUPDATETESTTEXT')}
        guios["SELECTIONBOXTEST1_SELECTIONBOX"].setSelectionList(selectionList = selections, displayTargets = 'all')

        guios["SELECTIONBOXTEST1_SELECTIONBOXACTIVATIONSWITCH"]     = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=3500, yPos=1150, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleActive_SelectionBox1)
        guios["SELECTIONBOXTEST1_SELECTIONBOXACTIVATIONSWITCHTEXT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4100, yPos=1150, width=1500, height= 250, style="styleA", text="ACTIVATION")
        guios["SELECTIONBOXTEST1_SELECTIONBOXDISPLAYSWITCH"]        = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=2, xPos=3500, yPos= 850, width= 500, height= 250, style="styleA", align = 'horizontal', switchStatus = True, releaseFunction = objFunc_ToggleDisplay_SelectionBox1)
        guios["SELECTIONBOXTEST1_SELECTIONBOXDISPLAYSWITCHTEXT"]    = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=2, xPos=4100, yPos= 850, width=1500, height= 250, style="styleA", text="DISPLAY")

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-EXPERIMENT1 END--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    


#PAGE-EXPERIMENT2 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_EXPERIMENT2(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND']    = pyglet.graphics.Group(order = 0)
    groups['OBJECTSLAYER0'] = pyglet.graphics.Group(order = 1)

    nTests = 1

    #OBJECT FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_anchorNW(objectInstance, **kwargs):
        anchor = 'NW'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorN(objectInstance, **kwargs):
        anchor = 'N'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorNE(objectInstance, **kwargs):
        anchor = 'NE'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorW(objectInstance, **kwargs):
        anchor = 'W'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorCENTER(objectInstance, **kwargs):
        anchor = 'CENTER'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorE(objectInstance, **kwargs):
        anchor = 'E'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorSW(objectInstance, **kwargs):
        anchor = 'SW'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorS(objectInstance, **kwargs):
        anchor = 'S'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_anchorSE(objectInstance, **kwargs):
        anchor = 'SE'
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setAnchor(anchor); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setAnchor(anchor); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_changeX(objectInstance, **kwargs):
        xCoord = float(guios["COORDX_VALUE"].getText())
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].moveTo(x = xCoord); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].moveTo(x = xCoord); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_changeY(objectInstance, **kwargs):
        yCoord = float(guios["COORDX_VALUE"].getText())
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].moveTo(y = yCoord); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].moveTo(y = yCoord); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    def objFunc_changeXY(objectInstance, **kwargs):
        xCoord = float(guios["COORDX_VALUE"].getText())
        yCoord = float(guios["COORDX_VALUE"].getText())
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].moveTo(x = xCoord, y = yCoord); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].moveTo(x = xCoord, y = yCoord); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_COORDCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))
        
    def objFunc_updateText(objectInstance, **kwargs):
        text = guios["TEXT_VALUE"].getText()
        tester1pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER1"].setText(text); end = time.perf_counter_ns(); tester1pTimes.append(end-beg)
        guios["PTIME_TEXTCHANGE_TESTER1_CONTENT"].updateText("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3))
        tester2pTimes = list()
        for i in range (nTests): beg = time.perf_counter_ns(); guios["TEXTELEMENTTESTER2"].setText(text); end = time.perf_counter_ns(); tester2pTimes.append(end-beg)
        guios["PTIME_TEXTCHANGE_TESTER2_CONTENT"].updateText("{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

        print("{:.3f} us".format(sum(tester1pTimes)/len(tester1pTimes)/1e3), "{:.3f} us".format(sum(tester2pTimes)/len(tester2pTimes)/1e3))

    #OBJECT FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))
        
        initialText = "A"

        textStyle1 = visualManager.getTextStyle('textBox_default')['DEFAULT']; textStyle1['font_size'] = 16
        textObjectInst = {'scaler': screenScaler, 'batch': batch, 'group': groups['OBJECTSLAYER0'], 'defaultTextStyle': textStyle1, 'showElementBox': True}
        guios["TEXTELEMENTTESTER1"] = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 7000, yPos = 5000, width = 2000, height = 1000, text = initialText, anchor = 'NW')
        
        textStyle2 = visualManager.getTextStyle('textBox_default')['DEFAULT']; textStyle2['font_size'] = 16.135
        textObjectInst = {'scaler': screenScaler, 'batch': batch, 'group': groups['OBJECTSLAYER0'], 'defaultTextStyle': textStyle2, 'showElementBox': True}
        guios["TEXTELEMENTTESTER2"] = ATM_Zeta_GUI_TextControl.textObject_SL(**textObjectInst, xPos = 7000, yPos = 3000, width = 2000, height = 1000, text = initialText, anchor = 'NW')

        guios["BUTTON_ANCHOR_NW"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos= 500, yPos=4800, width=600, height=400, style="styleA", text='NW',     fontSize = 80, releaseFunction=objFunc_anchorNW)
        guios["BUTTON_ANCHOR_N"]      = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1200, yPos=4800, width=600, height=400, style="styleA", text='N',      fontSize = 80, releaseFunction=objFunc_anchorN)
        guios["BUTTON_ANCHOR_NE"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1900, yPos=4800, width=600, height=400, style="styleA", text='NE',     fontSize = 80, releaseFunction=objFunc_anchorNE)
        guios["BUTTON_ANCHOR_W"]      = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos= 500, yPos=4300, width=600, height=400, style="styleA", text='W',      fontSize = 80, releaseFunction=objFunc_anchorW)
        guios["BUTTON_ANCHOR_CENTER"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1200, yPos=4300, width=600, height=400, style="styleA", text='CENTER', fontSize = 80, releaseFunction=objFunc_anchorCENTER)
        guios["BUTTON_ANCHOR_E"]      = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1900, yPos=4300, width=600, height=400, style="styleA", text='E',      fontSize = 80, releaseFunction=objFunc_anchorE)
        guios["BUTTON_ANCHOR_SW"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos= 500, yPos=3800, width=600, height=400, style="styleA", text='SW',     fontSize = 80, releaseFunction=objFunc_anchorSW)
        guios["BUTTON_ANCHOR_S"]      = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1200, yPos=3800, width=600, height=400, style="styleA", text='S',      fontSize = 80, releaseFunction=objFunc_anchorS)
        guios["BUTTON_ANCHOR_SE"]     = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=2, xPos=1900, yPos=3800, width=600, height=400, style="styleA", text='SE',     fontSize = 80, releaseFunction=objFunc_anchorSE)

        guios["PTIME_ANCHORCHANGE_TESTER1_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos= 500, yPos=3250, width= 700, height= 250, style="styleA", text="TESTER1", fontSize = 80)
        guios["PTIME_ANCHORCHANGE_TESTER1_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=1300, yPos=3250, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)
        guios["PTIME_ANCHORCHANGE_TESTER2_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos= 500, yPos=2900, width =700, height= 250, style="styleA", text="TESTER2", fontSize = 80)
        guios["PTIME_ANCHORCHANGE_TESTER2_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=1300, yPos=2900, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)
        
        guios["COORDX_NAMETAG"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=2, xPos= 500, yPos=2450, width =700, height=250, style="styleA", text="COORD X",   fontSize = 80)
        guios["COORDX_VALUE"]         = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1300, yPos=2450, width=1700, height=250, style="styleA", text="",          fontSize = 80, textUpdateFunction = None)
        guios["COORDX_CHANGEBUTTON"]  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=2, xPos=3100, yPos=2450, width=1000, height=250, style="styleA", text='CHANGE X',  fontSize = 80, releaseFunction=objFunc_changeX)
        guios["COORDY_NAMETAG"]       = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=2, xPos= 500, yPos=2100, width =700, height=250, style="styleA", text="COORD Y",   fontSize = 80)
        guios["COORDY_VALUE"]         = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1300, yPos=2100, width=1700, height=250, style="styleA", text="",          fontSize = 80, textUpdateFunction = None)
        guios["COORDY_CHANGEBUTTON"]  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=2, xPos=3100, yPos=2100, width=1000, height=250, style="styleA", text='CHANGE Y',  fontSize = 80, releaseFunction=objFunc_changeY)
        guios["COORDXY_CHANGEBUTTON"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=2, xPos=4200, yPos=2100, width=1000, height=600, style="styleA", text='CHANGE XY', fontSize = 80, releaseFunction=objFunc_changeXY)
        
        guios["PTIME_COORDCHANGE_TESTER1_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=5300, yPos=2450, width= 700, height= 250, style="styleA", text="TESTER1", fontSize = 80)
        guios["PTIME_COORDCHANGE_TESTER1_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=6100, yPos=2450, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)
        guios["PTIME_COORDCHANGE_TESTER2_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=5300, yPos=2100, width =700, height= 250, style="styleA", text="TESTER2", fontSize = 80)
        guios["PTIME_COORDCHANGE_TESTER2_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=6100, yPos=2100, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)
        
        guios["TEXT_NAMETAG"]      = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=2, xPos= 500, yPos=1650, width =700, height=250, style="styleA", text="TEXT",        fontSize = 80)
        guios["TEXT_VALUE"]        = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1300, yPos=1650, width=2000, height=250, style="styleA", text="",            fontSize = 80, textUpdateFunction = None)
        guios["TEXT_CHANGEBUTTON"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=2, xPos=3400, yPos=1650, width=1000, height=250, style="styleA", text='UPDATE TEXT', fontSize = 80, releaseFunction=objFunc_updateText)
        
        guios["PTIME_TEXTCHANGE_TESTER1_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos= 500, yPos=1300, width= 700, height= 250, style="styleA", text="TESTER1", fontSize = 80)
        guios["PTIME_TEXTCHANGE_TESTER1_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=1300, yPos=1300, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)
        guios["PTIME_TEXTCHANGE_TESTER2_NAMETAG"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos= 500, yPos= 950, width =700, height= 250, style="styleA", text="TESTER2", fontSize = 80)
        guios["PTIME_TEXTCHANGE_TESTER2_CONTENT"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst, groupOrder=2, xPos=1300, yPos= 950, width=1200, height= 250, style="styleA", text="-",       fontSize = 80)

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-EXPERIMENT2 END--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    


#PAGE-EXPERIMENT3 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_EXPERIMENT3(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND']    = pyglet.graphics.Group(order = 0)
    groups['OBJECTSLAYER0'] = pyglet.graphics.Group(order = 1)

    #OBJECT FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_onCoordinateUpdateButtonClick(objectInstance, **kwargs):
        try:
            targetName = guios["targetValue"].getText()
            xCoord = float(guios["xCoordValue"].getText())
            yCoord = float(guios["yCoordValue"].getText())
            guios[targetName].moveTo(xCoord, yCoord)
            print(termcolor.colored("COORDINATE UPDATED FOR {:s}:".format(targetName), 'light_green'), xCoord, yCoord)
        except Exception as e: print(termcolor.colored(e, 'light_red'))

    def objFunc_onSizeUpdateButtonClick(objectInstance, **kwargs):
        try:
            targetName = guios["targetValue"].getText()
            width  = float(guios["widthValue"].getText())
            height = float(guios["heightValue"].getText())
            guios[targetName].resize(width, height)
            print(termcolor.colored("SIZE UPDATED FOR {:s}:".format(targetName), 'light_green'), width, height)
        except Exception as e: print(termcolor.colored(e, 'light_red'))

    def objFunc_onQuickSetButtonClick(objectInstance, **kwargs):
        targetName = objectInstance.getName()
        xCoord = guios[targetName].xPos
        yCoord = guios[targetName].yPos
        width  = guios[targetName].width
        height = guios[targetName].height

        guios["targetValue"].updateText(targetName)
        guios["xCoordValue"].updateText(str(xCoord))
        guios["yCoordValue"].updateText(str(yCoord))
        guios["widthValue"].updateText(str(width))
        guios["heightValue"].updateText(str(height))
        if (guios[targetName].hidden == True):
            guios["showTarget"].activate()
            guios["hideTarget"].deactivate()
        else:
            guios["showTarget"].deactivate()
            guios["hideTarget"].activate()

    def objFunc_deactivateAll(objectInstance, **kwargs):
        guios["button_typeA"].deactivate()
        guios["button_typeB"].deactivate()
        guios["switch_typeA"].deactivate()
        guios["switch_typeB"].deactivate()
        guios["switch_typeC"].deactivate()
        guios["slider_typeA_V"].deactivate()
        guios["slider_typeA_H"].deactivate()
        guios["scrollBar_typeA_V"].deactivate()
        guios["scrollBar_typeA_H"].deactivate()
        guios["textInputBox_typeA"].deactivate()
        guios["selectionBox_typeA"].deactivate()
        guios["selectionBox_typeB"].deactivate()
        guios["deactivateAll"].deactivate()
        guios["activateAll"].activate()

    def objFunc_activateAll(objectInstance, **kwargs):
        guios["button_typeA"].activate()
        guios["button_typeB"].activate()
        guios["switch_typeA"].activate()
        guios["switch_typeB"].activate()
        guios["switch_typeC"].activate()
        guios["slider_typeA_V"].activate()
        guios["slider_typeA_H"].activate()
        guios["scrollBar_typeA_V"].activate()
        guios["scrollBar_typeA_H"].activate()
        guios["textInputBox_typeA"].activate()
        guios["selectionBox_typeA"].activate()
        guios["selectionBox_typeB"].activate()
        guios["deactivateAll"].activate()
        guios["activateAll"].deactivate()
        
    def objFunc_showTarget(objectInstance, **kwargs):
        guios[guios["targetValue"].getText()].show()
        guios["showTarget"].deactivate()
        guios["hideTarget"].activate()

    def objFunc_hideTarget(objectInstance, **kwargs):
        guios[guios["targetValue"].getText()].hide()
        guios["showTarget"].activate()
        guios["hideTarget"].deactivate()

    #OBJECT FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))

        #Test Targets
        guios["passiveGraphics_wrapperTypeA"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA(**inst, groupOrder=1, xPos=  100, yPos=8400, width=5000, height= 500, style="styleA", text="passiveGraphics_wrapperTypeA")
        guios["passiveGraphics_wrapperTypeB"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB(**inst, groupOrder=1, xPos= 5200, yPos=8400, width=5000, height= 500, style="styleA", text="passiveGraphics_wrapperTypeA")
        guios["passiveGraphics_wrapperTypeC"] = ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC(**inst, groupOrder=1, xPos=10300, yPos=8400, width=5000, height= 500, style="styleA", text="passiveGraphics_wrapperTypeA")
        guios["textBox_typeA"]                = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,                groupOrder=1, xPos=  100, yPos=7550, width=1500, height= 250, style="styleA", text="textBox_typeA")
        guios["imageBox_typeA"]               = ATM_Zeta_GUIO_Generals.imageBox_typeA(**inst,               groupOrder=1, xPos=  100, yPos=6450, width=1000, height=1000, style="styleA", image='binanceIcon_512x512.png')
        guios["button_typeA"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst,                 groupOrder=1, xPos=  100, yPos=6100, width=1500, height= 250, style="styleA", text="button_typeA")
        guios["button_typeB"]                 = ATM_Zeta_GUIO_Generals.button_typeB(**inst,                 groupOrder=1, xPos=  100, yPos=5750, width=1500, height= 250, style="styleA", image='settingsIcon_512x512.png', imageSize=(150, 150), imageRGBA=visualManager.getFromColorTable('ICON_COLORING'))
        guios["switch_typeA"]                 = ATM_Zeta_GUIO_Generals.switch_typeA(**inst,                 groupOrder=1, xPos=  100, yPos=5400, width=1000, height= 250, style="styleA")
        guios["switch_typeB"]                 = ATM_Zeta_GUIO_Generals.switch_typeB(**inst,                 groupOrder=1, xPos=  100, yPos=5050, width=1000, height= 250, style="styleA")
        guios["switch_typeC"]                 = ATM_Zeta_GUIO_Generals.switch_typeC(**inst,                 groupOrder=1, xPos=  100, yPos=4700, width=1000, height= 250, style="styleA", text="switch_typeC")
        guios["slider_typeA_V"]               = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=  100, yPos=2600, width=2000, height= 200, style="styleA", align='vertical')
        guios["slider_typeA_H"]               = ATM_Zeta_GUIO_Generals.slider_typeA(**inst,                 groupOrder=1, xPos=  400, yPos=4400, width=2000, height= 200, style="styleA", align='horizontal')
        guios["scrollBar_typeA_V"]            = ATM_Zeta_GUIO_Generals.scrollBar_typeA(**inst,              groupOrder=1, xPos= 1700, yPos=5450, width=2000, height= 200, style="styleA", align='vertical')
        guios["scrollBar_typeA_H"]            = ATM_Zeta_GUIO_Generals.scrollBar_typeA(**inst,              groupOrder=1, xPos= 2000, yPos=7250, width=2000, height= 200, style="styleA", align='horizontal')
        guios["textInputBox_typeA"]           = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst,           groupOrder=1, xPos= 5200, yPos=7550, width=3000, height= 250, style="styleA", text="textInputBox_typeA")
        guios["LED_typeA"]                    = ATM_Zeta_GUIO_Generals.LED_typeA(**inst,                    groupOrder=1, xPos= 5200, yPos=7200, width=3000, height= 250, style="styleA", mode = True)
        guios["gaugeBar_typeA_V"]             = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos= 8300, yPos=3750, width=3000, height= 250, style="styleA", align='vertical')
        guios["gaugeBar_typeA_H"]             = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(**inst,               groupOrder=1, xPos= 5200, yPos=6850, width=3000, height= 250, style="styleA", align='horizontal')
        guios["selectionBox_typeA"]           = ATM_Zeta_GUIO_Generals.selectionBox_typeA(**inst,           groupOrder=1, xPos= 5200, yPos=3750, width=3000, height=3000, style="styleA", elementHeight = 250)
        guios["selectionBox_typeB"]           = ATM_Zeta_GUIO_Generals.selectionBox_typeB(**inst,           groupOrder=1, xPos= 8300, yPos=6850, width=3000, height= 250, style="styleA", nDisplay = 10)
        #guios["chartDrawer_typeA"]            = ATM_Zeta_GUIO_ChartDrawers.chartDrawer_typeA(**inst,        groupOrder=1, xPos= 5200, yPos= 100, width=5000, height=3500, style="styleA")
        guios["subPage_typeA"]                = ATM_Zeta_GUIO_Generals.subPageBox_typeA(**inst,             groupOrder=1, xPos=10300, yPos= 100, width=3000, height=3000, style = 'styleA', useScrollBar_H = True, useScrollBar_V = True, name = 'level0')

        guios["subPage_typeA"].addGUIO("SELECITONBOXTYPEATEST",  ATM_Zeta_GUIO_Generals.selectionBox_typeA, {'groupOrder': 0, 'xPos': 20000, 'yPos':  100, 'width': 1000, 'height': 1000, 'style': 'styleA'})
        guios["subPage_typeA"].addGUIO("SELECITONBOXTYPEBTEST",  ATM_Zeta_GUIO_Generals.selectionBox_typeB, {'groupOrder': 0, 'xPos': 14200, 'yPos': 2000, 'width': 1000, 'height':  250, 'style': 'styleA', 'nDisplay': 5})
        guios["subPage_typeA"].addGUIO("BUTTONTYPEATEST",        ATM_Zeta_GUIO_Generals.button_typeA,       {'groupOrder': 0, 'xPos': 20000, 'yPos': 1200, 'width': 3000, 'height':  250, 'style': 'styleA', 'text': "button_typeA"})

        #Test Targets Setting
        guios["LED_typeA"].updateColor(120, 255, 30, 255)
        guios["selectionBox_typeA"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9", "ITEM10", "ITEM11", "ITEM12", "ITEM13", "ITEM14", "ITEM15", "ITEM16", "ITEM17", "ITEM18", "ITEM19"], displayTargets = 'all')
        guios["selectionBox_typeB"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9", "ITEM10", "ITEM11", "ITEM12", "ITEM13", "ITEM14", "ITEM15", "ITEM16", "ITEM17", "ITEM18", "ITEM19"], displayTargets = 'all')
        guios["subPage_typeA"].GUIOs["SELECITONBOXTYPEATEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')
        guios["subPage_typeA"].GUIOs["SELECITONBOXTYPEBTEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')

        #Target
        guios["targetTitle"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos=2200, width= 800, height=250, style="styleA", text="TARGET",  fontSize = 80)
        guios["targetValue"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1000, yPos=2200, width=2500, height=250, style="styleA", text="",        fontSize = 80)

        #Coordinate
        guios["xCoordTitle"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos=1850, width= 800, height=250, style="styleA", text="COORD X", fontSize = 80)
        guios["xCoordValue"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1000, yPos=1850, width=2500, height=250, style="styleA", text="",        fontSize = 80)
        guios["yCoordTitle"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos=1500, width= 800, height=250, style="styleA", text="COORD Y", fontSize = 80)
        guios["yCoordValue"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1000, yPos=1500, width=2500, height=250, style="styleA", text="",        fontSize = 80)
        guios["updateCoord"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos= 100, yPos=1150, width=3400, height=250, style="styleB", text='UPDATE COORDINATE', fontSize = 80, releaseFunction=objFunc_onCoordinateUpdateButtonClick)

        #Size
        guios["widthTitle"]  = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos= 800, width= 800, height=250, style="styleA", text="WIDTH",  fontSize = 80)
        guios["widthValue"]  = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1000, yPos= 800, width=2500, height=250, style="styleA", text="",       fontSize = 80)
        guios["heightTitle"] = ATM_Zeta_GUIO_Generals.textBox_typeA(**inst,      groupOrder=1, xPos= 100, yPos= 450, width= 800, height=250, style="styleA", text="HEIGHT", fontSize = 80)
        guios["heightValue"] = ATM_Zeta_GUIO_Generals.textInputBox_typeA(**inst, groupOrder=1, xPos=1000, yPos= 450, width=2500, height=250, style="styleA", text="",       fontSize = 80)
        guios["updateSize"]  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos= 100, yPos= 100, width=3400, height=250, style="styleB", text='UPDATE SIZE', fontSize = 80, releaseFunction=objFunc_onSizeUpdateButtonClick)

        #Hide/Show
        guios["showTarget"]  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos=3600, yPos= 450, width=700, height=250, style="styleB", text='SHOW', fontSize = 80, releaseFunction=objFunc_showTarget)
        guios["hideTarget"]  = ATM_Zeta_GUIO_Generals.button_typeA(**inst,       groupOrder=1, xPos=3600, yPos= 100, width=700, height=250, style="styleB", text='HIDE', fontSize = 80, releaseFunction=objFunc_hideTarget)
        guios["showTarget"].deactivate()
        guios["hideTarget"].deactivate()

        #Quick-Set Buttons
        guios["qsb_passiveGraphics_wrapperTypeA"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos= 100, width=2500, height=250, style="styleB", text='passiveGraphics_wrapperTypeA', name = 'passiveGraphics_wrapperTypeA', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_passiveGraphics_wrapperTypeB"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos= 450, width=2500, height=250, style="styleB", text='passiveGraphics_wrapperTypeB', name = 'passiveGraphics_wrapperTypeB', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_passiveGraphics_wrapperTypeC"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos= 800, width=2500, height=250, style="styleB", text='passiveGraphics_wrapperTypeC', name = 'passiveGraphics_wrapperTypeC', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_textBox_typeA"]                = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=1150, width=2500, height=250, style="styleB", text='textBox_typeA',      name = 'textBox_typeA',      fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_imageBox_typeA"]               = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=1500, width=2500, height=250, style="styleB", text='imageBox_typeA',     name = 'imageBox_typeA',     fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_button_typeA"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=1850, width=2500, height=250, style="styleB", text='button_typeA',       name = 'button_typeA',       fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_button_typeB"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=2200, width=2500, height=250, style="styleB", text='button_typeB',       name = 'button_typeB',       fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_switch_typeA"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=2550, width=2500, height=250, style="styleB", text='switch_typeA',       name = 'switch_typeA',       fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_switch_typeB"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=2900, width=2500, height=250, style="styleB", text='switch_typeB',       name = 'switch_typeB',       fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_switch_typeC"]                 = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=3250, width=2500, height=250, style="styleB", text='switch_typeC',       name = 'switch_typeC',       fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_slider_typeA_V"]               = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=3600, width=2500, height=250, style="styleB", text='slider_typeA_V',     name = 'slider_typeA_V',     fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_slider_typeA_H"]               = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=3950, width=2500, height=250, style="styleB", text='slider_typeA_H',     name = 'slider_typeA_H',     fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_scrollBar_typeA_V"]            = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=4300, width=2500, height=250, style="styleB", text='scrollBar_typeA_V',  name = 'scrollBar_typeA_V',  fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_scrollBar_typeA_H"]            = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=4650, width=2500, height=250, style="styleB", text='scrollBar_typeA_H',  name = 'scrollBar_typeA_H',  fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_textInputBox_typeA"]           = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=5000, width=2500, height=250, style="styleB", text='textInputBox_typeA', name = 'textInputBox_typeA', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_LED_typeA"]                    = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=5350, width=2500, height=250, style="styleB", text='LED_typeA',          name = 'LED_typeA',          fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_gaugeBar_typeA_V"]             = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=5700, width=2500, height=250, style="styleB", text='gaugeBar_typeA_V',   name = 'gaugeBar_typeA_V',   fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_gaugeBar_typeA=H"]             = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=6050, width=2500, height=250, style="styleB", text='gaugeBar_typeA_H',   name = 'gaugeBar_typeA_H',   fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_selectionBox_typeA"]           = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=6400, width=2500, height=250, style="styleB", text='selectionBox_typeA', name = 'selectionBox_typeA', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_selectionBox_typeB"]           = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=6750, width=2500, height=250, style="styleB", text='selectionBox_typeB', name = 'selectionBox_typeB', fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_chartDrawer_typeA"]            = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=7100, width=2500, height=250, style="styleB", text='chartDrawer_typeA',  name = 'chartDrawer_typeA',  fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["qsb_subPage_typeA"]                = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=7450, width=2500, height=250, style="styleB", text='subPage_typeA',      name = 'subPage_typeA',      fontSize = 80, releaseFunction=objFunc_onQuickSetButtonClick)
        guios["activateAll"]   = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 13400, yPos=7800, width=1200, height=250, style="styleB", text='ACTIVATE',   fontSize = 80, releaseFunction=objFunc_activateAll)
        guios["deactivateAll"] = ATM_Zeta_GUIO_Generals.button_typeA(**inst, groupOrder=1, xPos= 14700, yPos=7800, width=1200, height=250, style="styleB", text='DEACTIVATE', fontSize = 80, releaseFunction=objFunc_deactivateAll)
        guios["activateAll"].deactivate()

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-EXPERIMENT3 END--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    


#PAGE-EXPERIMENT5 -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def __setup_EXPERIMENT4(pageInstance, windowInstance, systemFunctions, displaySpaceDefiner, guioConfig, imageManager, audioManager, visualManager, ipcA_MAIN_AUX, ipcA_MAIN_ATM):
    #Batch and GUIO Variable Instances Localization
    batch = pageInstance.batch; groups = pageInstance.groups
    guios = pageInstance.GUIOs; screenRatio = displaySpaceDefiner['ratio']; screenScaler = displaySpaceDefiner['scaler']
    inst = {'windowInstance': windowInstance, 'displaySpaceDefiner': displaySpaceDefiner, 'guioConfig': guioConfig, 'batch': batch, 'scaler': screenScaler, 'imageManager': imageManager, 'audioManager': audioManager, 'visualManager': visualManager, 'sysFunctions': systemFunctions, 'ipcA_MAIN_AUX': ipcA_MAIN_AUX, 'ipcA_MAIN_ATM': ipcA_MAIN_ATM}

    #Setup the Groups for layered drawing
    groups['BACKGROUND']    = pyglet.graphics.Group(order = 0)
    groups['OBJECTSLAYER0'] = pyglet.graphics.Group(order = 1)

    #OBJECT FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def objFunc_ToggleTheme(objectInstance, **kwargs):
        if (guios['subPageBox1'].GUIOs["GUITHEMESWITCH"].getStatus() == True): newTheme = 'LIGHT'
        else:                                                                  newTheme = 'DARK'
        systemFunctions['CHANGEGUITHEME'](newTheme)
        
    def objFunc_ToggleLanguage(objectInstance, **kwargs):
        if (guios['subPageBox1'].GUIOs['LANGUAGESWITCH'].getStatus() == True): newLanguage = 'KOR'
        else:                                                                  newLanguage = 'ENG'
        systemFunctions['CHANGELANGUAGE'](newLanguage)

    #OBJECT FUNCTIONS END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #GUIO Initializations
    if (screenRatio == '16:9H'):
        pageInstance.backgroundShape = pyglet.shapes.Rectangle(batch = batch, group = groups['BACKGROUND'], x = 0, y = 0, width = 16000, height = 9000, color = visualManager.getFromColorTable('PAGEBACKGROUND'))
        
        guios["subPageBox1"] = ATM_Zeta_GUIO_Generals.subPageBox_typeA(**inst, groupOrder = 1, xPos = 100, yPos = 100, width =15800, height = 8800, style = 'styleA', useScrollBar_H = True, useScrollBar_V = True, name = 'level0')
        guios["subPageBox1"].addGUIO("subPageBox1_level1",     ATM_Zeta_GUIO_Generals.subPageBox_typeA,   {'groupOrder': 10, 'xPos':   100, 'yPos':   100, 'width': 14000, 'height': 8000, 'useScrollBar_H': True, 'useScrollBar_V': True, 'name': 'level1'})

        guios["subPageBox1"].addGUIO("SELECITONBOXTYPEATEST", ATM_Zeta_GUIO_Generals.selectionBox_typeA, {'groupOrder': 0, 'xPos': 20000, 'yPos':  100, 'width': 1000, 'height': 1000, 'style': 'styleA'})
        guios["subPageBox1"].GUIOs["SELECITONBOXTYPEATEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')
        guios["subPageBox1"].addGUIO("BUTTONTYPEATEST",        ATM_Zeta_GUIO_Generals.button_typeA,       {'groupOrder': 0, 'xPos': 20000, 'yPos': 1200, 'width': 3000, 'height':  250, 'style': 'styleA', 'text': "button_typeA"})
        guios["subPageBox1"].addGUIO("SELECITONBOXTYPEBTEST",  ATM_Zeta_GUIO_Generals.selectionBox_typeB, {'groupOrder': 0, 'xPos': 14200, 'yPos': 2000, 'width': 1000, 'height':  250, 'style': 'styleA', 'nDisplay': 5})
        guios["subPageBox1"].GUIOs["SELECITONBOXTYPEBTEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')
        guios["subPageBox1"].addGUIO("GUITHEMESWITCH",  ATM_Zeta_GUIO_Generals.switch_typeB, {'groupOrder': 0, 'xPos': 14200, 'yPos': 3500, 'width': 500, 'height': 250, 'style': 'styleA', 'releaseFunction': objFunc_ToggleTheme})
        guios["subPageBox1"].addGUIO("LANGUAGESWITCH",  ATM_Zeta_GUIO_Generals.switch_typeB, {'groupOrder': 0, 'xPos': 14200, 'yPos': 3850, 'width': 500, 'height': 250, 'style': 'styleA', 'releaseFunction': objFunc_ToggleLanguage})

        guios["subPageBox1"].GUIOs['subPageBox1_level1'].addGUIO("subPageBox1_level2", ATM_Zeta_GUIO_Generals.subPageBox_typeA, {'groupOrder': 10, 'xPos':   100, 'yPos': 100, 'width': 12000, 'height': 7000, 'useScrollBar_H': True, 'useScrollBar_V': True, 'name': 'level2'})
        guios["subPageBox1"].GUIOs['subPageBox1_level1'].addGUIO("BUTTONTYPEATEST",    ATM_Zeta_GUIO_Generals.button_typeA,     {'groupOrder':  0, 'xPos': 20000, 'yPos': 100, 'width':  1000, 'height':  250, 'style': 'styleA', 'text': "button_typeA"})

        guios["subPageBox1"].GUIOs['subPageBox1_level1'].GUIOs['subPageBox1_level2'].addGUIO("subPageBox1_level3", ATM_Zeta_GUIO_Generals.subPageBox_typeA, {'groupOrder': 10, 'xPos':   100, 'yPos': 100, 'width': 8000, 'height': 6000, 'useScrollBar_H': True, 'useScrollBar_V': True, 'name': 'level3'})
        guios["subPageBox1"].GUIOs['subPageBox1_level1'].GUIOs['subPageBox1_level2'].addGUIO("BUTTONTYPEATEST",    ATM_Zeta_GUIO_Generals.button_typeA,     {'groupOrder':  0, 'xPos': 20000, 'yPos': 100, 'width': 1000, 'height':  250, 'style': 'styleA', 'text': "button_typeA"})

        target = guios["subPageBox1"].GUIOs['subPageBox1_level1'].GUIOs['subPageBox1_level2'].GUIOs['subPageBox1_level3']
        target.addGUIO("BUTTONTYPEATEST1",      ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos':   100, 'yPos':   100, 'width': 1000, 'height': 250, 'style': 'styleA', 'text': "button_typeA"})
        target.addGUIO("BUTTONTYPEATEST2",      ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 20000, 'yPos':   100, 'width': 1000, 'height': 250, 'style': 'styleA', 'text': "button_typeA"})
        target.addGUIO("BUTTONTYPEATEST3",      ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 20000, 'yPos': 10000, 'width': 1000, 'height': 250, 'style': 'styleA', 'text': "button_typeA"})
        target.addGUIO("BUTTONTYPEATEST4",      ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos':   100, 'yPos': 10000, 'width': 1000, 'height': 250, 'style': 'styleA', 'text': "button_typeA"})
        target.addGUIO("SELECITONBOXTYPEATEST", ATM_Zeta_GUIO_Generals.selectionBox_typeA, {'groupOrder': 0, 'xPos': 1500, 'yPos': 3000, 'width': 2000, 'height': 2000, 'elementHeight': 250, 'style': 'styleA'})
        target.addGUIO("SELECITONBOXTYPEBTEST", ATM_Zeta_GUIO_Generals.selectionBox_typeB, {'groupOrder': 0, 'xPos': 3600, 'yPos': 3000, 'width': 2000, 'height':  250, 'nDisplay': 5,       'style': 'styleA'})
        target.GUIOs["SELECITONBOXTYPEATEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')
        target.GUIOs["SELECITONBOXTYPEBTEST"].setSelectionList(["ITEM0", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7", "ITEM8", "ITEM9"], displayTargets = 'all')
        target.addGUIO("SLIDERTPEATEST",        ATM_Zeta_GUIO_Generals.slider_typeA,       {'groupOrder': 0, 'xPos': 6000, 'yPos': 3000, 'width': 2000, 'height': 150, 'align': 'vertical', 'style': 'styleA'})
        target.addGUIO("SCROLLBARTYPEATEST",    ATM_Zeta_GUIO_Generals.scrollBar_typeA,    {'groupOrder': 0, 'xPos': 6300, 'yPos': 3000, 'width': 2000, 'height': 150, 'align': 'vertical', 'style': 'styleA'})
        target.addGUIO("TEXTINPUTBOXTYPEATEST", ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 6600, 'yPos': 3000, 'width': 2000, 'height': 250, 'style': 'styleA', 'fontSize': 80})
        target.addGUIO("PASSIVEGRAPHICSWRAPPERTYPEA", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeA, {'groupOrder': 0, 'xPos': 3000, 'yPos': 5000, 'width': 3000, 'height': 2000, 'style': 'styleA', 'fontSize': 80, 'text': visualManager.getTextPack('SETTINGS:GRAPHICSWRAPPERTITLE')})
        target.addGUIO("PASSIVEGRAPHICSWRAPPERTYPEB", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB, {'groupOrder': 0, 'xPos': 3000, 'yPos': 7100, 'width': 3000, 'height':  200, 'style': 'styleA', 'fontSize': 80, 'text': visualManager.getTextPack('SETTINGS:GRAPHICSWRAPPERTITLE')})
        target.addGUIO("PASSIVEGRAPHICSWRAPPERTYPEC", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 3000, 'yPos': 7300, 'width': 3000, 'height':  200, 'style': 'styleA', 'fontSize': 80, 'text': visualManager.getTextPack('SETTINGS:GRAPHICSWRAPPERTITLE')})

    elif (screenRatio == '21:9H'): pass
    elif (screenRatio == '32:9H'): pass
#PAGE-EXPERIMENT4 END--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------