#'chartDrawer_typeA' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_TIMELIMIT_KLINESPROCESS_NS = 10e6
class chartDrawer_typeA:
    #Initialization -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        #Default Graphics Parameters
        self.window = kwargs['windowInstance']
        self.scaler = kwargs['scaler']; self.batch = kwargs['batch']
        
        groupOrder = kwargs.get('groupOrder', None)
        if (groupOrder == None):
            self.group_0 = kwargs['group_0']
            self.group_1 = kwargs['group_1']
            self.group_2 = kwargs['group_2']
            self.group_3 = kwargs['group_3']
            self.group_4 = kwargs['group_4']
            self.group_5 = kwargs['group_5']
            #Hovered Descriptor
            self.group_hd0 = kwargs['group_20']
            #For Settings Subpage
            self.group_ss0 = kwargs['group_21']
            self.group_ss1 = kwargs['group_22']
            self.group_ss2 = kwargs['group_23']
            self.group_ss3 = kwargs['group_24']
            self.groupOrder = self.group_0.order
            self.parentCameraGroup = self.group_0
        else:
            self.groupOrder = groupOrder
            self.group_0 = pyglet.graphics.Group(order = self.groupOrder)
            self.group_1 = pyglet.graphics.Group(order = self.groupOrder+1)
            self.group_2 = pyglet.graphics.Group(order = self.groupOrder+2)
            self.group_3 = pyglet.graphics.Group(order = self.groupOrder+3)
            self.group_4 = pyglet.graphics.Group(order = self.groupOrder+4)
            self.group_5 = pyglet.graphics.Group(order = self.groupOrder+5)
            #Hovered Descriptor
            self.group_hd0 = pyglet.graphics.Group(order = self.groupOrder+20)
            #For Settings Subpage
            self.group_ss_order = self.groupOrder+21
            self.parentCameraGroup = None
        
        self.imageManager  = kwargs['imageManager']
        self.audioManager  = kwargs['audioManager']
        self.visualManager = kwargs['visualManager']
        self.currentGUITheme = self.visualManager.getGUITheme()
        self.ipcA_AUX = kwargs['ipcA_MAIN_AUX']
        self.ipcA_ATM = kwargs['ipcA_MAIN_ATM']
        
        self.name = kwargs.get('name', None)
        if (self.name == None): self.objectConfig_preset = None
        else:                   self.objectConfig_preset = kwargs['guioConfig'].get(self.name, None)
        self.xPos = kwargs.get('xPos', 0); self.yPos = kwargs.get('yPos', 0)
        self.width = kwargs.get('width', 0); self.height = kwargs.get('height', 0)
        self.style = kwargs.get('style', 'styleA')
        
        self.textStyle = kwargs.get('textStyle', 'default')
        self.effectiveTextStyle = self.visualManager.getTextStyle('chartDrawer_'+self.textStyle)
        for textStyleCode in self.effectiveTextStyle: self.effectiveTextStyle[textStyleCode]['font_size'] = 80*self.scaler

        #DisplayBox Dimension Standards & Interaction Control Variables
        self.hitBox = dict()
        self.hitBox_Object = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(self.xPos, self.yPos, self.width, self.height)
        self.images = dict()
        self.frameSprites = dict()

        if (self.width  < _GD_OBJECT_MINWIDTH):  self.width  = _GD_OBJECT_MINWIDTH  
        if (self.height < _GD_OBJECT_MINHEIGHT): self.height = _GD_OBJECT_MINHEIGHT 

        #---Information Displayers, priority goes: KLINESVOLUME -> AUXILLARYBAR -> SIVIEWERS
        self.usableSIViewers = min([int((self.height-_GD_OBJECT_MINHEIGHT-(_GD_DISPLAYBOX_AUXILLARYBAR_HEIGHT+_GD_DISPLAYBOX_GOFFSET))/(_GD_DISPLAYBOX_SIVIEWER_HEIGHT+_GD_DISPLAYBOX_GOFFSET)), len(_SITYPES)])
        
        self.displayBox = {'AUXILLARYBAR': None,
                           'KLINESPRICE':       None, 'MAINGRID_KLINESPRICE': None,
                           'MAINGRID_TEMPORAL': None, 'SETTINGSBUTTONFRAME':  None}
        for siViewerIndex in range (len(_SITYPES)):
            self.displayBox['SIVIEWER'+str(siViewerIndex+1)]          = None
            self.displayBox['MAINGRID_SIVIEWER'+str(siViewerIndex+1)] = None
        
        self.displayBox_graphics = dict()
        for displayBoxName in self.displayBox: self.displayBox_graphics[displayBoxName] = dict()
        self.displayBox_graphics_visibleSIViewers = set()

        self.displayBox_VerticalSection_Order = list()
        self.displayBox_VisibleBoxes = list()
        
        #---Kline Loading Display Elements
        self.images['KLINELOADINGCOVER'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_klinesLoadingCover", self.width*self.scaler, self.height*self.scaler)
        self.frameSprites['KLINELOADINGCOVER'] = pyglet.sprite.Sprite(x = self.xPos*self.scaler, y = self.yPos*self.scaler, img = self.images['KLINELOADINGCOVER'][0], batch = self.batch, group = self.group_1)
        self.frameSprites['KLINELOADINGCOVER'].visible = False
        self.klinesLoadingGaugeBar = ATM_Zeta_GUIO_Generals.gaugeBar_typeA(windowInstance = self.window, batch = self.batch, scaler = self.scaler, imageManager = self.imageManager, audioManager = self.audioManager, visualManager = self.visualManager,
                                                                           xPos = self.xPos, yPos = self.yPos, width = 100, height = _GD_KLINESLOADINGGAUGEBAR_HEIGHT,
                                                                           style = 'styleA', align = 'horizontal', group_0 = self.group_2, group_1 = self.group_3, value = 0)
        self.klinesLoadingTextBox_perc = ATM_Zeta_GUIO_Generals.textBox_typeA(windowInstance = self.window, batch = self.batch, scaler = self.scaler, imageManager = self.imageManager, audioManager = self.audioManager, visualManager = self.visualManager,
                                                                              xPos = self.xPos, yPos = self.yPos, width = 100, height = _GD_KLINESLOADINGGAUGEBAR_HEIGHT,
                                                                              style = None, group_0 = self.group_4, group_1 = self.group_5, text = '', fontSize = 60)
        self.klinesLoadingTextBox = ATM_Zeta_GUIO_Generals.textBox_typeA(windowInstance = self.window, batch = self.batch, scaler = self.scaler, imageManager = self.imageManager, audioManager = self.audioManager, visualManager = self.visualManager,
                                                                         xPos = self.xPos, yPos = self.yPos, width = 100, height = 200,
                                                                         style = None, group_0 = self.group_2, group_1 = self.group_3, text = "", fontSize = 80)
        self.klinesLoadingGaugeBar.hide()
        self.klinesLoadingTextBox_perc.hide()
        self.klinesLoadingTextBox.hide()

        #Mouse Control Variables
        self.mouse_lastHoveredSection  = None; self.mouse_lastSelectedSection = None
        self.mouse_Dragged  = False; self.mouse_DragDX   = dict(); self.mouse_DragDY   = dict()
        self.mouse_Scrolled = False; self.mouse_ScrollDX = dict(); self.mouse_ScrollDY = dict(); self.mouse_lastScrolled_ns = 0
        self.mouse_Event_lastRead    = None
        self.mouse_Event_lastPressed = None
        self.mouse_Event_currentlyPressed = False
        self.mouse_Event_lastInterpreted_ns = 0
        
        #Kline & Analysis Control Variables
        self.apiSymbol    = None
        self.intervalID   = None
        self.mrktRegTS    = None
        self.currencyInfo = None

        self.klines = {'raw': dict(), 'raw_status': dict(), 'events': dict()}
        self.klines_analysisParams         = dict()
        self.klines_analysisTargets        = dict()
        self.klines_analysisTargets_keySet = set()
        self.klines_fetchComplete = False
        self.klines_fetching      = False
        self.klines_toProcess = dict(); self.klines_processed = dict()
        self.klines_drawQueue = dict(); self.klines_drawn     = dict()
        self.klines_drawRemovalQueue = set()
        
        self.klines_analysisReferers = dict()
        
        self.__klines_analysisGenerationOrder = ('SMA', 'WMA', 'EMA', 'PSAR', 'BOL', 'VOL', 'IVP', 'MMACD', 'DMIxADX', 'MFI', 'PIP')
        self.__klines_analysisGenerators = {'EVENTS':  self.__analysisGenerator_EVENTS,
                                            'SMA':     self.__analysisGenerator_SMA,
                                            'WMA':     self.__analysisGenerator_WMA,
                                            'EMA':     self.__analysisGenerator_EMA,
                                            'PSAR':    self.__analysisGenerator_PSAR,
                                            'BOL':     self.__analysisGenerator_BOL,
                                            'IVP':     self.__analysisGenerator_IVP,
                                            'PIP':     self.__analysisGenerator_PIP,
                                            'VOL':     self.__analysisGenerator_VOL,
                                            'MMACD':   self.__analysisGenerator_MMACD,
                                            'DMIxADX': self.__analysisGenerator_DMIxADX,
                                            'MFI':     self.__analysisGenerator_MFI}
        
        self.__klines_PAPs = {'SMA':     None,
                              'WMA':     None,
                              'EMA':     self.__PAP_EMA,
                              'PSAR':    self.__PAP_PSAR,
                              'BOL':     self.__PAP_BOL,
                              'IVP':     self.__PAP_IVP,
                              'PIP':     self.__PAP_PIP,
                              'VOL':     self.__PAP_VOL,
                              'MMACD':   self.__PAP_MMACD,
                              'DMIxADX': self.__PAP_DMIxADX,
                              'MFI':     self.__PAP_MFI}

        self.__klines_drawerFunctions = {'KLINE':  self.__klineDrawer_KLINE,
                                         'EVENTS': self.__klineDrawer_EVENTS,
                                         'SMA':     self.__klineDrawer_SMA,
                                         'WMA':     self.__klineDrawer_WMA,
                                         'EMA':     self.__klineDrawer_EMA,
                                         'PSAR':    self.__klineDrawer_PSAR,
                                         'BOL':     self.__klineDrawer_BOL,
                                         'IVP':     self.__klineDrawer_IVP,
                                         'PIP':     self.__klineDrawer_PIP,
                                         'VOL':     self.__klineDrawer_VOL,
                                         'MMACD':   self.__klineDrawer_MMACD,
                                         'DMIxADX': self.__klineDrawer_DMIxADX,
                                         'MFI':     self.__klineDrawer_MFI}
        
        self.siTypes_siViewerAlloc = dict.fromkeys(_SITYPES, None) #Allocated SIViewer Number for the corresponding SI Type
        self.siTypes_analysisCodes = dict.fromkeys(_SITYPES, None) #Allocated Analysis Codes for the corresponding SI type
        
        #Settings Sub Page Setup
        self.settingsSubPages = dict()
        settingsSubPageList = ('MAIN',) + _MITYPES + _SITYPES
        self.settingsSubPage_Current = settingsSubPageList[0]
        self.settingsSubPage_Opened = False
        self.settingsButtonStatus = 'DEFAULT'
        
        if (groupOrder == None):
            for subPageName in settingsSubPageList:
                self.settingsSubPages[subPageName] = ATM_Zeta_GUIO_Generals.subPageBox_typeA(windowInstance = self.window, batch = self.batch, scaler = self.scaler, guioConfig = kwargs['guioConfig'], sysFunctions = kwargs['sysFunctions'], imageManager = self.imageManager, audioManager = self.audioManager, visualManager = self.visualManager, ipcA_MAIN_AUX = self.ipcA_AUX, ipcA_MAIN_ATM = self.ipcA_ATM,
                                                                                             xPos = self.xPos+50, yPos = self.yPos+50, width = 3700, height = self.height-100, useScrollBar_V = True, useScrollBar_H = False,
                                                                                             group_0 = self.group_ss0, group_1 = self.group_ss1, group_2 = self.group_ss2, group_3 = self.group_ss3)
                self.settingsSubPages[subPageName].hide()
        else:
            for subPageName in settingsSubPageList:
                self.settingsSubPages[subPageName] = ATM_Zeta_GUIO_Generals.subPageBox_typeA(windowInstance = self.window, batch = self.batch, scaler = self.scaler, guioConfig = kwargs['guioConfig'], sysFunctions = kwargs['sysFunctions'], imageManager = self.imageManager, audioManager = self.audioManager, visualManager = self.visualManager, ipcA_MAIN_AUX = self.ipcA_AUX, ipcA_MAIN_ATM = self.ipcA_ATM,
                                                                                             xPos = self.xPos+50, yPos = self.yPos+50, width = 3700, height = self.height-100, useScrollBar_V = True, useScrollBar_H = False,
                                                                                             groupOrder = self.group_ss_order)
                self.settingsSubPages[subPageName].hide()
        self.__configureSettingsSubPageObjects()
            
        #Object Configuration Setup
        self.sysFunc_editGUIOConfig = kwargs['sysFunctions']['EDITGUIOCONFIG']
        self.objectConfig = dict()
        self.__initializeObjectConfig()

        #ViewRange & Grid Control
        self.gridColor       = self.visualManager.getFromColorTable('CHARTDRAWER_GRID')
        self.gridColor_Heavy = self.visualManager.getFromColorTable('CHARTDRAWER_GRIDHEAVY')
        self.guideColor      = self.visualManager.getFromColorTable('CHARTDRAWER_GUIDECONTENT')
        self.posHighlightColor_hovered  = self.visualManager.getFromColorTable('CHARTDRAWER_POSHOVERED')
        self.posHighlightColor_selected = self.visualManager.getFromColorTable('CHARTDRAWER_POSSELECTED')

        #<Horizontal ViewRange & Vertical Grid>
        #---Horizontal ViewRange
        self.expectedKlineTemporalWidth = 60
        self.horizontalViewRangeWidth_min = None; self.horizontalViewRangeWidth_max = None
        self.horizontalViewRangeWidth_m = None;   self.horizontalViewRangeWidth_b = None
        self.horizontalViewRange = [None, None]
        self.horizontalViewRange_backwardBufferSamples = 0
        self.horizontalViewRange_backwardBufferFactor  = 2
        self.horizontalViewRange_forwardBufferFactor   = 1
        self.horizontalViewRange_timestampsInViewRange  = set()
        self.horizontalViewRange_timestampsInBufferZone = set()
        self.checkVerticalExtremas_SIs = {'VOL':     self.__checkVerticalExtremas_VOL,
                                          'MMACD':   self.__checkVerticalExtremas_MMACD,
                                          'DMIxADX': self.__checkVerticalExtremas_DMIxADX,
                                          'MFI':     self.__checkVerticalExtremas_MFI}

        #---Horizontal Position Highlighter
        self.posHighlight_hoveredPos       = (None, None, None, None)
        self.posHighlight_updatedPositions = None
        self.posHighlight_selectedPos      = None
        self.posHighlight_lastUpdated_ns   = 0

        #---Vertical Grid
        self.verticalGrid_intervalID = 0
        self.verticalGrid_intervals = list()
        self.nMaxVerticalGridLines = None

        #Timezone Setup
        objectConfig_timeZone = self.objectConfig['TimeZone']
        if   (objectConfig_timeZone     == 'LOCAL'): self.timezoneDelta = -time.timezone
        elif (objectConfig_timeZone[:3] == 'UTC'):   self.timezoneDelta = int(objectConfig_timeZone.split("+")[1])*3600
        
        #<Vertical ViewRange & Horizontal Grid>
        #---Vertical ViewRange
        self.verticalViewRange_magnification = dict()
        self.verticalValue_min = dict()
        self.verticalValue_max = dict()
        self.verticalValue_loaded = dict()
        self.verticalViewRange = dict()
        self.verticalViewRange_precision = dict()
        
        self.verticalViewRange_magnification['KLINESPRICE'] = 100
        self.verticalValue_min['KLINESPRICE'] = 0
        self.verticalValue_max['KLINESPRICE'] = 100000
        self.verticalViewRange['KLINESPRICE'] = [self.verticalValue_min['KLINESPRICE'], self.verticalValue_max['KLINESPRICE']]
        self.verticalViewRange_precision['KLINESPRICE'] = 3
        for siViewerIndex in range (len(_SITYPES)):
            siViewerCode = 'SIVIEWER'+str(siViewerIndex+1)
            self.verticalViewRange_magnification[siViewerCode] = 100
            self.verticalValue_min[siViewerCode] = 0
            self.verticalValue_max[siViewerCode] = 1
            self.verticalValue_loaded[siViewerCode] = False
            self.verticalViewRange[siViewerCode] = [self.verticalValue_min[siViewerCode], self.verticalValue_max[siViewerCode]]
            self.verticalViewRange_precision[siViewerCode] = 3

        #---Horizontal Grid
        self.horizontalGridIntervals      = dict()
        self.horizontalGridIntervalHeight = dict()
        self.nMaxHorizontalGridLines = dict()
        
        self.horizontalGridIntervals['KLINESPRICE']      = list()
        self.horizontalGridIntervalHeight['KLINESPRICE'] = None
        self.nMaxHorizontalGridLines['KLINESPRICE']      = None
        for siViewerIndex in range (len(_SITYPES)):
            siViewerCode = 'SIVIEWER'+str(siViewerIndex+1)
            self.horizontalGridIntervals[siViewerCode]      = list()
            self.horizontalGridIntervalHeight[siViewerCode] = None
            self.nMaxHorizontalGridLines[siViewerCode]      = int((_GD_DISPLAYBOX_SIVIEWER_HEIGHT-_GD_DISPLAYBOX_GOFFSET*2)*self.scaler/_GD_DISPLAYBOX_GRID_HORIZONTALLINEPIXELINTERVAL_SIVIEWER)
        
        #Object Status
        self.status = "DEFAULT"
        self.hidden = False
        
        #Configuration Data Read & GUIO Configuration Matching
        self.__readObjectConfig()
        self.__matchGUIOsToConfig()

        #Post Initialization Act
        self.__configureDisplayBoxes(onInit = True)

        #Analysis Parameters Configuration
        for miType in _MITYPES: self.__configureAnalysisParams(miType)
        for siType in _SITYPES: self.__configureAnalysisParams(siType)
        self.__configureAnalysisParams('EVENTS')

        #Initialize Currency Target
        self.setTarget(apiSymbol = None, intervalID = None)
    #Initialization END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




    #Object Configuration & GUIO Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __initializeObjectConfig(self):
        #---Default Object Configuration
        self.objectConfig = dict()
        #--- MAIN Config
        for analysisType in (_MITYPES+_SITYPES): self.objectConfig['{:s}Compute'.format(analysisType)] = False
        for siViewerIndex in range (len(_SITYPES)): self.objectConfig['SIVIEWER{:d}Display'.format(siViewerIndex+1)] = False; self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerIndex+1)] = _SITYPES[siViewerIndex]
        self.objectConfig['UseAuxBar']      = True
        self.objectConfig['DisplayEvents']  = True
        self.objectConfig['TimeZone']       = 'LOCAL'
        self.objectConfig['KlineColorType'] = 1
        #--- SMA Config
        for lineIndex in range (_NMAXLINES['SMA']):
            lineNumber = lineIndex+1
            self.objectConfig['SMA{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['SMA{:d}nSamples'.format(lineNumber)] = 0
            self.objectConfig['SMA{:d}Width'.format(lineNumber)] = 1
            self.objectConfig['SMA{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['SMA{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['SMA{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['SMA{:d}colorA%DARK'.format(lineNumber)] =255
            self.objectConfig['SMA{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['SMA{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['SMA{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['SMA{:d}colorA%LIGHT'.format(lineNumber)]=255
            self.objectConfig['SMA{:d}Display'.format(lineNumber)] = True

        #--- WMA Config
        for lineIndex in range (_NMAXLINES['WMA']):
            lineNumber = lineIndex+1
            self.objectConfig['WMA{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['WMA{:d}nSamples'.format(lineNumber)] = 0
            self.objectConfig['WMA{:d}Width'.format(lineNumber)] = 1
            self.objectConfig['WMA{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['WMA{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['WMA{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['WMA{:d}colorA%DARK'.format(lineNumber)] =255
            self.objectConfig['WMA{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['WMA{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['WMA{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['WMA{:d}colorA%LIGHT'.format(lineNumber)]=255
            self.objectConfig['WMA{:d}Display'.format(lineNumber)] = True

        #--- EMA Config
        for lineIndex in range (_NMAXLINES['EMA']):
            lineNumber = lineIndex+1
            self.objectConfig['EMA{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['EMA{:d}nSamples'.format(lineNumber)] = 0
            self.objectConfig['EMA{:d}Width'.format(lineNumber)] = 1
            self.objectConfig['EMA{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['EMA{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['EMA{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['EMA{:d}colorA%DARK'.format(lineNumber)] =255
            self.objectConfig['EMA{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['EMA{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['EMA{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['EMA{:d}colorA%LIGHT'.format(lineNumber)]=255
            self.objectConfig['EMA{:d}Display'.format(lineNumber)] = True

        #--- PSAR Config
        for lineIndex in range (_NMAXLINES['PSAR']):
            lineNumber = lineIndex+1
            self.objectConfig['PSAR{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['PSAR{:d}start'.format(lineNumber)]        = 0.020
            self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)] = 0.020
            self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]      = 0.200
            self.objectConfig['PSAR{:d}Size'.format(lineNumber)] = 1
            self.objectConfig['PSAR{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['PSAR{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['PSAR{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['PSAR{:d}colorA%DARK'.format(lineNumber)] =255
            self.objectConfig['PSAR{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['PSAR{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['PSAR{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['PSAR{:d}colorA%LIGHT'.format(lineNumber)]=255
            self.objectConfig['PSAR{:d}Display'.format(lineNumber)] = True

        #--- BOL Config
        for lineIndex in range (_NMAXLINES['BOL']):
            lineNumber = lineIndex+1
            self.objectConfig['BOL{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['BOL{:d}nSamples'.format(lineNumber)] = 1; self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)] = 2.0
            self.objectConfig['BOL{:d}Width'.format(lineNumber)] = 1
            self.objectConfig['BOL{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['BOL{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['BOL{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['BOL{:d}colorA%DARK'.format(lineNumber)] =30
            self.objectConfig['BOL{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['BOL{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['BOL{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['BOL{:d}colorA%LIGHT'.format(lineNumber)]=30
            self.objectConfig['BOL{:d}Display'.format(lineNumber)] = True
        self.objectConfig['BOLMAType'] = 'SMA'
        self.objectConfig['BOLdisplayCenterLine'] = True
        self.objectConfig['BOLdisplayBand']       = True

        #--- IVP Config
        self.objectConfig['IVPRAWDisplay']      = True
        self.objectConfig['IVPRAWcolorR%DARK']  = random.randint(64,255); self.objectConfig['IVPRAWcolorG%DARK']  = random.randint(64,255); self.objectConfig['IVPRAWcolorB%DARK']  = random.randint(64,255); self.objectConfig['IVPRAWcolorA%DARK']  = 30
        self.objectConfig['IVPRAWcolorR%LIGHT'] = random.randint(64,255); self.objectConfig['IVPRAWcolorG%LIGHT'] = random.randint(64,255); self.objectConfig['IVPRAWcolorB%LIGHT'] = random.randint(64,255); self.objectConfig['IVPRAWcolorA%LIGHT'] = 30
        self.objectConfig['IVPCCURRENTANCHORDisplay']      = True
        self.objectConfig['IVPCCURRENTANCHORcolorR%DARK']  = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorG%DARK']  = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorB%DARK']  = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorA%DARK']  = 30
        self.objectConfig['IVPCCURRENTANCHORcolorR%LIGHT'] = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorG%LIGHT'] = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorB%LIGHT'] = random.randint(64,255); self.objectConfig['IVPCCURRENTANCHORcolorA%LIGHT'] = 30
        self.objectConfig['IVPCPREVANCHORDisplay']         = True
        self.objectConfig['IVPCPREVANCHORcolorR%DARK']     = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorG%DARK']  = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorB%DARK']  = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorA%DARK']  = 30
        self.objectConfig['IVPCPREVANCHORcolorR%LIGHT']    = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorG%LIGHT'] = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorB%LIGHT'] = random.randint(64,255); self.objectConfig['IVPCPREVANCHORcolorA%LIGHT'] = 30
        self.objectConfig['IVPRAWDisplayWidth'] = 0.2
        self.objectConfig['IVPnSamples']        = 500
        self.objectConfig['IVPUseBLE']          = False
        self.objectConfig['IVPMinGammaFactorPerc'] = 1.0
        self.objectConfig['IVPUseAGF']             = True
        self.objectConfig['IVPAGFRefLen']          = 120
        self.objectConfig['IVPAGFMAType']          = 'SMA'
        self.objectConfig['IVPCExtension']  = True
        self.objectConfig['IVPCPositional'] = False
        self.objectConfig['IVPClusteringRange']       = 5.0
        self.objectConfig['IVPCExistenceCounterMin']  = 10
        self.objectConfig['IVPCExistenceCounterMax']  = 200
        self.objectConfig['IVPCCSAccelerationFactor'] = 0.2
        self.objectConfig['IVPCAnchorRangerFactor']   = 0.25

        #---PIP Config
        self.objectConfig['PIPBUYPOScolorR%DARK']   = random.randint(64,255); self.objectConfig['PIPBUYPOScolorG%DARK']   = random.randint(64,255); self.objectConfig['PIPBUYPOScolorB%DARK']   = random.randint(64,255); self.objectConfig['PIPBUYPOScolorA%DARK']   = 150
        self.objectConfig['PIPBUYPOScolorR%LIGHT']  = random.randint(64,255); self.objectConfig['PIPBUYPOScolorG%LIGHT']  = random.randint(64,255); self.objectConfig['PIPBUYPOScolorB%LIGHT']  = random.randint(64,255); self.objectConfig['PIPBUYPOScolorA%LIGHT']  = 150
        self.objectConfig['PIPSELLPOScolorR%DARK']  = random.randint(64,255); self.objectConfig['PIPSELLPOScolorG%DARK']  = random.randint(64,255); self.objectConfig['PIPSELLPOScolorB%DARK']  = random.randint(64,255); self.objectConfig['PIPSELLPOScolorA%DARK']  = 150
        self.objectConfig['PIPSELLPOScolorR%LIGHT'] = random.randint(64,255); self.objectConfig['PIPSELLPOScolorG%LIGHT'] = random.randint(64,255); self.objectConfig['PIPSELLPOScolorB%LIGHT'] = random.randint(64,255); self.objectConfig['PIPSELLPOScolorA%LIGHT'] = 150


        #---VOL Config
        self.objectConfig['VOLType']   = 'BASE'
        self.objectConfig['VOLMAType'] = 'SMA'
        for lineIndex in range (_NMAXLINES['VOL']):
            lineNumber = lineIndex+1
            self.objectConfig['VOL{:d}Compute'.format(lineNumber)] = False
            self.objectConfig['VOL{:d}nSamples'.format(lineNumber)] = 1
            self.objectConfig['VOL{:d}Width'.format(lineNumber)] = 1
            self.objectConfig['VOL{:d}colorR%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['VOL{:d}colorG%DARK'.format(lineNumber)] =random.randint(64,255); self.objectConfig['VOL{:d}colorB%DARK'.format(lineNumber)] =random.randint(64, 255); self.objectConfig['VOL{:d}colorA%DARK'.format(lineNumber)] =255
            self.objectConfig['VOL{:d}colorR%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['VOL{:d}colorG%LIGHT'.format(lineNumber)]=random.randint(64,255); self.objectConfig['VOL{:d}colorB%LIGHT'.format(lineNumber)]=random.randint(64, 255); self.objectConfig['VOL{:d}colorA%LIGHT'.format(lineNumber)]=255
            self.objectConfig['VOL{:d}Display'.format(lineNumber)] = True

        #---MMACD Config
        self.objectConfig['MMACDMMACDDisplay']     = True
        self.objectConfig['MMACDSIGNALDisplay']    = True
        self.objectConfig['MMACDHISTOGRAMDisplay'] = True
        self.objectConfig['MMACDMMACDcolorR%DARK']       = random.randint(64,255); self.objectConfig['MMACDMMACDcolorG%DARK']       = random.randint(64,255); self.objectConfig['MMACDMMACDcolorB%DARK']       = random.randint(64,255); self.objectConfig['MMACDMMACDcolorA%DARK']       = 255
        self.objectConfig['MMACDMMACDcolorR%LIGHT']      = random.randint(64,255); self.objectConfig['MMACDMMACDcolorG%LIGHT']      = random.randint(64,255); self.objectConfig['MMACDMMACDcolorB%LIGHT']      = random.randint(64,255); self.objectConfig['MMACDMMACDcolorA%LIGHT']      = 255
        self.objectConfig['MMACDSIGNALcolorR%DARK']      = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorG%DARK']      = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorB%DARK']      = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorA%DARK']      = 255
        self.objectConfig['MMACDSIGNALcolorR%LIGHT']     = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorG%LIGHT']     = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorB%LIGHT']     = random.randint(64,255); self.objectConfig['MMACDSIGNALcolorA%LIGHT']     = 255
        self.objectConfig['MMACDHISTOGRAM+colorR%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorG%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorB%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorA%DARK']  = 255
        self.objectConfig['MMACDHISTOGRAM+colorR%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorG%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorB%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM+colorA%LIGHT'] = 255
        self.objectConfig['MMACDHISTOGRAM-colorR%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorG%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorB%DARK']  = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorA%DARK']  = 255
        self.objectConfig['MMACDHISTOGRAM-colorR%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorG%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorB%LIGHT'] = random.randint(64,255); self.objectConfig['MMACDHISTOGRAM-colorA%LIGHT'] = 255
        self.objectConfig['MMACDSignalInterval']        = 10
        self.objectConfig['MMACDSignalDeltaMAInterval'] = 5
        for lineIndex in range (_NMAXLINES['MMACD']):
            lineNumber = lineIndex+1
            self.objectConfig['MMACD{:d}Compute'.format(lineNumber)]  = False
            self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)] = 1

    def __configureSettingsSubPageObjects(self):
        subPageViewSpaceWidth = 3450
        #<MAIN>
        if (True):
            yPos_beg = 20000
            #Title
            self.settingsSubPages['MAIN'].addGUIO("TITLE_MAIN", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeB, {'groupOrder': 0, 'xPos': 0, 'yPos': yPos_beg, 'width': subPageViewSpaceWidth, 'height': 200, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_CHARTSETTINGS')})
                
            #Main Indicators
            yPosPoint0 = yPos_beg-200
            self.settingsSubPages['MAIN'].addGUIO("TITLE_MAININDICATORS", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0, 'width': subPageViewSpaceWidth, 'height': 200, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MAININDICATORS'), 'fontSize': 80})
            for i, miType in enumerate(_MITYPES):
                self.settingsSubPages['MAIN'].addGUIO("MAININDICATOR_{:s}".format(miType),      ATM_Zeta_GUIO_Generals.switch_typeC,  {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint0-350-350*i, 'width': 2950, 'height': 250, 'style': 'styleB', 'name': 'MAIN_INDICATORSWITCH_{:s}'.format(miType), 'text': miType, 'fontSize': 80, 'releaseFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MAIN'].addGUIO("MAININDICATORSETUP_{:s}".format(miType), ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 3050, 'yPos': yPosPoint0-350-350*i, 'width':  400, 'height': 250, 'style': 'styleA', 'text': ">".format(miType), 'fontSize': 80, 'name': 'navButton_MI_{:s}'.format(miType), 'releaseFunction': self.__onSettingsNavButtonClick})
                
            #Sub Indicators
            yPosPoint1 = yPosPoint0-300-350*len(_MITYPES)
            self.settingsSubPages['MAIN'].addGUIO("TITLE_SUBINDICATORS", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint1, 'width': subPageViewSpaceWidth, 'height': 200, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SUBINDICATORS'), 'fontSize': 80})
            for i, siType in enumerate(_SITYPES):
                self.settingsSubPages['MAIN'].addGUIO("SUBINDICATOR_{:s}".format(siType),      ATM_Zeta_GUIO_Generals.switch_typeC, {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint1-350-350*i, 'width': 2950, 'height': 250, 'style': 'styleB', 'name': 'MAIN_INDICATORSWITCH_{:s}'.format(siType), 'text': siType, 'fontSize': 80, 'releaseFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MAIN'].addGUIO("SUBINDICATORSETUP_{:s}".format(siType), ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 3050, 'yPos': yPosPoint1-350-350*i, 'width':  400, 'height': 250, 'style': 'styleA', 'text': ">", 'fontSize': 80, 'name': 'navButton_SI_{:s}'.format(siType), 'releaseFunction': self.__onSettingsNavButtonClick})
            
            #Sub Indicators Display
            yPosPoint2 = yPosPoint1-300-350*len(_SITYPES)
            self.settingsSubPages['MAIN'].addGUIO("TITLE_SUBINDICATORSDISPLAY", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint2, 'width': subPageViewSpaceWidth, 'height': 200, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SUBINDICATORDISPLAY'), 'fontSize': 80})
            siSelection = dict()
            for siType in _SITYPES: siSelection[siType] = {'text': siType}
            for i in range (len(_SITYPES)):
                siViewerNumber = i+1
                self.settingsSubPages['MAIN'].addGUIO("SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber),    ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint2-350-350*i, 'width': 1100, 'height': 250, 'style': 'styleB', 'name': 'MAIN_SIVIEWERDISPLAYSWITCH_{:d}'.format(siViewerNumber),    'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDICATOR{:d}'.format(siViewerNumber)), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MAIN'].addGUIO("SUBINDICATOR_DISPLAYSELECTION{:d}".format(siViewerNumber), ATM_Zeta_GUIO_Generals.selectionBox_typeB, {'groupOrder': 0, 'xPos': 1200, 'yPos': yPosPoint2-350-350*i, 'width': 2250, 'height': 250, 'style': 'styleA', 'name': 'MAIN_SIVIEWERDISPLAYSELECTION_{:d}'.format(siViewerNumber), 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSELECTION{:d}".format(siViewerNumber)].setSelectionList(selectionList = siSelection, displayTargets = 'all')
                
            #Aux Settings
            yPosPoint3 = yPosPoint2-300-350*len(_SITYPES)
            self.settingsSubPages['MAIN'].addGUIO("TITLE_AUX",                       ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos':  yPosPoint3,      'width': subPageViewSpaceWidth, 'height': 200, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_AUX'), 'fontSize': 80})
            self.settingsSubPages['MAIN'].addGUIO("AUX_SHOWAUXBAR_TEXT",             ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos':  yPosPoint3- 350, 'width': 2850,                  'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:SHOWAUXBAR'), 'fontSize': 80})
            self.settingsSubPages['MAIN'].addGUIO("AUX_SHOWAUXBAR_SWITCH",           ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos':  yPosPoint3- 350, 'width':  500,                  'height': 250, 'style': 'styleA', 'name': 'MAIN_SHOWAUXBAR_SWITCH', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MAIN'].addGUIO("AUX_DISPLAYEVENTS_TEXT",          ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos':  yPosPoint3- 700, 'width': 2850,                  'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAYEVENTS'), 'fontSize': 80})
            self.settingsSubPages['MAIN'].addGUIO("AUX_DISPLAYEVENTS_SWITCH",        ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos':  yPosPoint3- 700, 'width':  500,                  'height': 250, 'style': 'styleA', 'name': 'MAIN_DISPLAYEVENTS_SWITCH', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MAIN'].addGUIO("AUX_KLINECOLORTYPE_TEXT",         ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos':  yPosPoint3-1050, 'width': 1200,                  'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:KLINECOLORTYPE'), 'fontSize': 80})
            self.settingsSubPages['MAIN'].addGUIO("AUX_KLINECOLORTYPE_SELECTIONBOX", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 1, 'xPos': 1300, 'yPos':  yPosPoint3-1050, 'width': 2150,                  'height': 250, 'style': 'styleA', 'name': 'MAIN_KLINECOLORTYPE_SELECTION', 'nDisplay': 5, 'fontSize': 80, 'expansionDir': 1, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MAIN'].addGUIO("AUX_TIMEZONE_TEXT",               ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos':  yPosPoint3-1400, 'width': 1200,                  'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TIMEZONE'), 'fontSize': 80})
            self.settingsSubPages['MAIN'].addGUIO("AUX_TIMEZONE_SELECTIONBOX",       ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos': 1300, 'yPos':  yPosPoint3-1400, 'width': 2150,                  'height': 250, 'style': 'styleA', 'name': 'MAIN_TIMEZONE_SELECTION', 'nDisplay': 10, 'fontSize': 80, 'expansionDir': 1, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MAIN'].addGUIO("AUX_SAVECONFIGURATION",           ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 0,    'yPos':  yPosPoint3-1750, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:SAVECONFIG'), 'fontSize': 80, 'name': 'MAIN_SAVECONFIG', 'releaseFunction': self._onSettingsContentUpdate})

            #GUIO Setup
            self.settingsSubPages['MAIN'].GUIOs["AUX_KLINECOLORTYPE_SELECTIONBOX"].setSelectionList({1: {'text': 'TYPE1'}, 2: {'text': 'TYPE2'}}, displayTargets = 'all')
            timeZoneSelections = {'LOCAL': {'text': 'LOCAL'}}
            for hour in range (24): timeZoneSelections['UTC+{:d}'.format(hour)] = {'text': 'UTC+{:d}'.format(hour)}
            self.settingsSubPages['MAIN'].GUIOs["AUX_TIMEZONE_SELECTIONBOX"].setSelectionList(timeZoneSelections, displayTargets = 'all')

        #<SMA & WMA & EMA Settings>
        if (True):
            for miType in ('SMA', 'WMA', 'EMA'):
                self.settingsSubPages[miType].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MI_{:s}'.format(miType)), 'fontSize': 100})
                self.settingsSubPages[miType].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width':                   400, 'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width': 600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  700, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'name': '{:s}_LineSelectionBox'.format(miType), 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 1750, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'mode': True})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2800, 'yPos': 9300, 'width': 650, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': '{:s}_ApplyColor'.format(miType), 'releaseFunction': self._onSettingsContentUpdate})
                for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                    self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                    self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': '{:s}_Color_{:s}'.format(miType,componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                    self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
                self.settingsSubPages[miType].addGUIO("INDICATORINDEX_COLUMNTITLE",    ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': 800, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),    'fontSize': 90, 'anchor': 'SW'})
                self.settingsSubPages[miType].addGUIO("INDICATORINTERVAL_COLUMNTITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':  900, 'yPos': 7550, 'width': 550, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVAL'), 'fontSize': 90, 'anchor': 'SW'})
                self.settingsSubPages[miType].addGUIO("INDICATORWIDTH_COLUMNTITLE",    ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1550, 'yPos': 7550, 'width': 550, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:WIDTH'),    'fontSize': 90, 'anchor': 'SW'})
                self.settingsSubPages[miType].addGUIO("INDICATORCOLOR_COLUMNTITLE",    ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2200, 'yPos': 7550, 'width': 650, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'),    'fontSize': 90, 'anchor': 'SW'})
                self.settingsSubPages[miType].addGUIO("INDICATORDISPLAY_COLUMNTITLE",  ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2950, 'yPos': 7550, 'width': 500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAY'),  'fontSize': 90, 'anchor': 'SW'})
                maList = dict()
                for i in range (_NMAXLINES[miType]):
                    lineNumber = i+1
                    self.settingsSubPages[miType].addGUIO("INDICATOR_{:s}{:d}".format(miType,lineNumber),               ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos':    0, 'yPos': 7200-350*i, 'width': 800, 'height': 250, 'style': 'styleB', 'name': '{:s}_LineActivationSwitch_{:d}'.format(miType,lineNumber), 'text': '{:s} {:d}'.format(miType,lineNumber), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                    self.settingsSubPages[miType].addGUIO("INDICATOR_{:s}{:d}_INTERVALINPUT".format(miType,lineNumber), ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos':  900, 'yPos': 7200-350*i, 'width': 550, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': '{:s}_IntervalTextInputBox_{:d}'.format(miType,lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                    self.settingsSubPages[miType].addGUIO("INDICATOR_{:s}{:d}_WIDTHINPUT".format(miType,lineNumber),    ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1550, 'yPos': 7200-350*i, 'width': 550, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': '{:s}_WidthTextInputBox_{:d}'.format(miType,lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                    self.settingsSubPages[miType].addGUIO("INDICATOR_{:s}{:d}_LINECOLOR".format(miType,lineNumber),     ATM_Zeta_GUIO_Generals.LED_typeA,          {'groupOrder': 0, 'xPos': 2200, 'yPos': 7200-350*i, 'width': 650, 'height': 250, 'style': 'styleA', 'mode': True})
                    self.settingsSubPages[miType].addGUIO("INDICATOR_{:s}{:d}_DISPLAY".format(miType,lineNumber),       ATM_Zeta_GUIO_Generals.switch_typeB,       {'groupOrder': 0, 'xPos': 2950, 'yPos': 7200-350*i, 'width': 500, 'height': 250, 'style': 'styleA', 'name': '{:s}_DisplaySwitch_{:d}'.format(miType,lineNumber), 'releaseFunction': self._onSettingsContentUpdate})
                    maList[str(lineNumber)] = {'text': "{:s} {:d}".format(miType, lineNumber)}
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = maList, displayTargets = 'all')

                self.settingsSubPages[miType].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': 7200-350*(_NMAXLINES[miType]-1)-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': '{:s}_ApplySettings'.format(miType), 'releaseFunction': self._onSettingsContentUpdate})
            
        #<BOL Settings>
        if (True):
            self.settingsSubPages['BOL'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MI_BOL'), 'fontSize': 100})
            self.settingsSubPages['BOL'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width': 600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  700, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'name': 'BOL_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 1750, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2800, 'yPos': 9300, 'width': 650, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'BOL_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'BOL_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_BLOCKTITLE_MATYPE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_MATYPETEXT",        ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 7200, 'width':                  1200, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE'), 'fontSize': 80})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_MATYPESELECTION",   ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos': 1300, 'yPos': 7200, 'width':                  2150, 'height': 250, 'style': 'styleA', 'name': 'BOL_MATypeSelectionBox', 'nDisplay': 3, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            maTypes = {'SMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_SMA')},
                        'WMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_WMA')},
                        'EMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_EMA')}}
            self.settingsSubPages['BOL'].GUIOs["INDICATOR_MATYPESELECTION"].setSelectionList(selectionList = maTypes, displayTargets = 'all')
            self.settingsSubPages['BOL'].addGUIO("INDICATORINDEX_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 6850, 'width': 600, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),         'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORINTERVAL_COLUMNTITLE",  ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':  700, 'yPos': 6850, 'width': 500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVALSHORT'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORBANDWIDTH_COLUMNTITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1300, 'yPos': 6850, 'width': 450, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:BANDWIDTH'),     'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORWIDTH_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1850, 'yPos': 6850, 'width': 450, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:WIDTH'),         'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORCOLOR_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2400, 'yPos': 6850, 'width': 450, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'),         'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATORDISPLAY_COLUMNTITLE",   ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2950, 'yPos': 6850, 'width': 500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAY'),       'fontSize': 90, 'anchor': 'SW'})
            bolList = dict()
            for i in range (_NMAXLINES['BOL']):
                lineNumber = i+1
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}".format(lineNumber),                ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos':    0, 'yPos': 6500-350*i, 'width': 600, 'height': 250, 'style': 'styleB', 'name': 'BOL_LineActivationSwitch_{:d}'.format(lineNumber), 'text': 'BOL {:d}'.format(lineNumber), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}_INTERVALINPUT".format(lineNumber),  ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos':  700, 'yPos': 6500-350*i, 'width': 500, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'BOL_IntervalTextInputBox_{:d}'.format(lineNumber),  'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}_BANDWIDTHINPUT".format(lineNumber), ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1300, 'yPos': 6500-350*i, 'width': 450, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'BOL_BandWidthTextInputBox_{:d}'.format(lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}_WIDTHINPUT".format(lineNumber),     ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1850, 'yPos': 6500-350*i, 'width': 450, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'BOL_WidthTextInputBox_{:d}'.format(lineNumber),     'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}_LINECOLOR".format(lineNumber),      ATM_Zeta_GUIO_Generals.LED_typeA,          {'groupOrder': 0, 'xPos': 2400, 'yPos': 6500-350*i, 'width': 450, 'height': 250, 'style': 'styleA', 'mode': True})
                self.settingsSubPages['BOL'].addGUIO("INDICATOR_BOL{:d}_DISPLAY".format(lineNumber),        ATM_Zeta_GUIO_Generals.switch_typeB,       {'groupOrder': 0, 'xPos': 2950, 'yPos': 6500-350*i, 'width': 500, 'height': 250, 'style': 'styleA', 'name': 'BOL_DisplaySwitch_{:d}'.format(lineNumber), 'releaseFunction': self._onSettingsContentUpdate})
                bolList[str(lineNumber)] = {'text': "BOL {:d}".format(lineNumber)}
            yPosPoint0 = 6500-350*(_NMAXLINES['BOL']-1)
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_BLOCKTITLE_DISPLAYCONTENTS",      ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint0- 350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAYCONTENTS'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_DISPLAYCONTENTS_BOLCENTERTEXT",   ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint0- 700, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAYBOLCENTER'), 'fontSize': 80})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_DISPLAYCONTENTS_BOLCENTERSWITCH", ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': yPosPoint0- 700, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'BOL_DisplayContentsSwitch_BolCenter', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_DISPLAYCONTENTS_BOLBANDTEXT",     ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': yPosPoint0-1050, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAYBOLBAND'), 'fontSize': 80})
            self.settingsSubPages['BOL'].addGUIO("INDICATOR_DISPLAYCONTENTS_BOLBANDSWITCH",   ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': yPosPoint0-1050, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'BOL_DisplayContentsSwitch_BolBand', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['BOL'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-1400, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'BOL_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = bolList, displayTargets = 'all')
                
        #<PSAR Settings>
        if (True):
            self.settingsSubPages['PSAR'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MI_PSAR'), 'fontSize': 100})
            self.settingsSubPages['PSAR'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width': 600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  700, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'name': 'PSAR_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 1750, 'yPos': 9300, 'width': 950, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2800, 'yPos': 9300, 'width': 650, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'PSAR_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'PSAR_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORINDEX_COLUMNTITLE",        ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': 500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),            'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORSTART_COLUMNTITLE",        ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':  600, 'yPos': 7550, 'width': 400, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PSARSTART'),        'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORACCELERATION_COLUMNTITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1100, 'yPos': 7550, 'width': 400, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PSARACCELERATION'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORMAXIMUM_COLUMNTITLE",      ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1600, 'yPos': 7550, 'width': 400, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PSARMAXIMUM'),      'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORSIZE_COLUMNTITLE",         ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2100, 'yPos': 7550, 'width': 300, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:SIZE'),             'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORCOLOR_COLUMNTITLE",        ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2500, 'yPos': 7550, 'width': 350, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'),            'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PSAR'].addGUIO("INDICATORDISPLAY_COLUMNTITLE",      ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2950, 'yPos': 7550, 'width': 500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAY'),          'fontSize': 90, 'anchor': 'SW'})
            psarList = dict()
            for i in range (_NMAXLINES['PSAR']):
                lineNumber = i+1
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}".format(lineNumber),                   ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos':    0, 'yPos': 7200-350*i, 'width': 500, 'height': 250, 'style': 'styleB', 'name': 'PSAR_LineActivationSwitch_{:d}'.format(lineNumber), 'text': 'PSAR {:d}'.format(lineNumber), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_STARTINPUT".format(lineNumber),        ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos':  600, 'yPos': 7200-350*i, 'width': 400, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'PSAR_StartTextInputBox_{:d}'.format(lineNumber),        'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_ACCELERATIONINPUT".format(lineNumber), ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1100, 'yPos': 7200-350*i, 'width': 400, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'PSAR_AccelerationTextInputBox_{:d}'.format(lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_MAXIMUMINPUT".format(lineNumber),      ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1600, 'yPos': 7200-350*i, 'width': 400, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'PSAR_MaximumTextInputBox_{:d}'.format(lineNumber),      'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_SIZEINPUT".format(lineNumber),         ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 2100, 'yPos': 7200-350*i, 'width': 300, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'PSAR_SizeTextInputBox_{:d}'.format(lineNumber),         'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_LINECOLOR".format(lineNumber),         ATM_Zeta_GUIO_Generals.LED_typeA,          {'groupOrder': 0, 'xPos': 2500, 'yPos': 7200-350*i, 'width': 350, 'height': 250, 'style': 'styleA', 'mode': True})
                self.settingsSubPages['PSAR'].addGUIO("INDICATOR_PSAR{:d}_DISPLAY".format(lineNumber),           ATM_Zeta_GUIO_Generals.switch_typeB,       {'groupOrder': 0, 'xPos': 2950, 'yPos': 7200-350*i, 'width': 500, 'height': 250, 'style': 'styleA', 'name': 'PSAR_DisplaySwitch_{:d}'.format(lineNumber), 'releaseFunction': self._onSettingsContentUpdate})
                psarList[str(lineNumber)] = {'text': "PSAR {:d}".format(lineNumber)}
            yPosPoint0 = 7200-350*(_NMAXLINES['PSAR']-1)
            self.settingsSubPages['PSAR'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'PSAR_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = psarList, displayTargets = 'all')

        #<IVP Settings>
        if (True):
            self.settingsSubPages['IVP'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MI_IVP'), 'fontSize': 100})
            self.settingsSubPages['IVP'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width':                   550, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  650, 'yPos': 9300, 'width':                  1500, 'height': 250, 'style': 'styleA', 'name': 'IVP_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2250, 'yPos': 9300, 'width':                   500, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2850, 'yPos': 9300, 'width':                   600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'IVP_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'IVP_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['IVP'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
            ivpLineTargets = {'RAW':            {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPRAW')},
                              'CCURRENTANCHOR': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCCURRENTANCHOR')},
                              'CPREVANCHOR':    {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCPREVANCHOR')}}
            self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = ivpLineTargets, displayTargets = 'all')

            self.settingsSubPages['IVP'].addGUIO("INDICATOR_BLOCKTITLE_IVPDISPLAY",               ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPDISPLAY'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_DISPLAYTEXT",                  ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 7200, 'width':                  1500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPRAWDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_DISPLAYSWITCH",                ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1600, 'yPos': 7200, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_DisplaySwitch_RAW', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_COLORTEXT",                    ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2200, 'yPos': 7200, 'width':                   600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_COLOR",                        ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2900, 'yPos': 7200, 'width':                   550, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_DISPLAYWIDTHTEXT",             ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6850, 'width':                  1000, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPDISPLAYWIDTH'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_DISPLAYWIDTHSLIDER",           ATM_Zeta_GUIO_Generals.slider_typeA,                 {'groupOrder': 0, 'xPos': 1100, 'yPos': 6900, 'width':                  1650, 'height': 150, 'style': 'styleA', 'name': 'IVP_DisplayWidthSlider_RAW', 'valueUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_DISPLAYWIDTHVALUETEXT",        ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2850, 'yPos': 6850, 'width':                   600, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80})

            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCCURRENTANCHOR_DISPLAYTEXT",       ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6500, 'width':                  1800, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCCURRENTANCHORDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCCURRENTANCHOR_DISPLAYSWITCH",     ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1900, 'yPos': 6500, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_DisplaySwitch_IVPCCURRENTANCHOR', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCCURRENTANCHOR_COLORTEXT",         ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2500, 'yPos': 6500, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCCURRENTANCHOR_COLOR",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 3100, 'yPos': 6500, 'width':                   350, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPREVANCHOR_DISPLAYTEXT",          ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6150, 'width':                  1800, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCPREVANCHORDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPREVANCHOR_DISPLAYSWITCH",        ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1900, 'yPos': 6150, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_DisplaySwitch_IVPCPREVANCHOR', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPREVANCHOR_COLORTEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2500, 'yPos': 6150, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPREVANCHOR_COLOR",                ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 3100, 'yPos': 6150, 'width':                   350, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCEXTENSION_DISPLAYTEXT",           ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 5800, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCSHOWEXTENSION'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCEXTENSION_DISPLAYSWITCH",         ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': 5800, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_DisplaySwitch_SHOWEXTENSION', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPOSITIONAL_DISPLAYTEXT",          ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 5450, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCSHOWPOSITIONAL'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPCPOSITIONAL_DISPLAYSWITCH",        ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': 5450, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_DisplaySwitch_SHOWPOSITIONAL', 'statusUpdateFunction': self._onSettingsContentUpdate})

            self.settingsSubPages['IVP'].addGUIO("INDICATOR_BLOCKTITLE_IVPPARAMS",                ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 5100, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPPARAMS'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_INTERVALTEXT",                 ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 4750, 'width':                   800, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVAL'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_INTERVALINPUT",                ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos':  900, 'yPos': 4750, 'width':                   750, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'IVP_IntervalTextInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_USEBLETEXT",                   ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 1750, 'yPos': 4750, 'width':                  1100, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPUSEBLE'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPRAW_USEBLESWITCH",                 ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': 4750, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_UseBollingerEnhancement', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_MINGAMMAFACTORTEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 4400, 'width':                  1300, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPMINGAMMAFACTOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_MINGAMMAFACTORSLIDER",    ATM_Zeta_GUIO_Generals.slider_typeA,                 {'groupOrder': 0, 'xPos': 1400, 'yPos': 4450, 'width':                  1350, 'height': 150, 'style': 'styleA', 'name': 'IVP_MinGammaFactor', 'valueUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_MINGAMMAFACTORVALUETEXT", ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2850, 'yPos': 4400, 'width':                   600, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_USEAGFTEXT",              ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 4050, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPUSEAGF'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_USEAGFSWITCH",            ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 2950, 'yPos': 4050, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'IVP_UseActiveGammaFactor', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_AGFREFLENTEXT",           ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 3700, 'width':                   950, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPAGFREFLEN'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_AGFREFLENINPUT",          ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos': 1050, 'yPos': 3700, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'IVP_AGFRefLenInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_AGFMATYPETEXT",           ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 1650, 'yPos': 3700, 'width':                   950, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPAGFMATYPE'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_AGFMATYPESELECTION",      ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos': 2700, 'yPos': 3700, 'width':                   750, 'height': 250, 'style': 'styleA', 'name': 'IVP_AGFMATypeSelectionBox', 'nDisplay': 3, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            maTypes = {'SMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_SMA_ABBR')},
                       'WMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_WMA_ABBR')},
                       'EMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_EMA_ABBR')}}
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFMATYPESELECTION"].setSelectionList(selectionList = maTypes, displayTargets = 'all')
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CLUSTERINGRANGETEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,               {'groupOrder': 0, 'xPos':    0, 'yPos': 3350, 'width': 1200, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCLUSTERINGRANGE'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CLUSTERINGRANGESLIDER",    ATM_Zeta_GUIO_Generals.slider_typeA,                {'groupOrder': 0, 'xPos': 1300, 'yPos': 3400, 'width': 1550, 'height': 150, 'style': 'styleA', 'name': 'IVP_ClusteringRange', 'valueUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CLUSTERINGRANGEVALUETEXT", ATM_Zeta_GUIO_Generals.textBox_typeA,               {'groupOrder': 0, 'xPos': 2950, 'yPos': 3350, 'width':  500, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ECMINTEXT",               ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 3000, 'width':  800, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCECMIN'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ECMINTEXTINPUT",          ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos':  900, 'yPos': 3000, 'width':  775, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'IVP_ECMinInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ECMAXTEXT",               ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 1775, 'yPos': 3000, 'width':  800, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCECMAX'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ECMAXTEXTINPUT",          ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos': 2675, 'yPos': 3000, 'width':  775, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'IVP_ECMaxInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CSACCELERATIONFACTORTEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,          {'groupOrder': 0, 'xPos':    0, 'yPos': 2650, 'width':  700, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCCSACCELERATIONFACTOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CSACCELERATIONFACTORSLIDER",    ATM_Zeta_GUIO_Generals.slider_typeA,           {'groupOrder': 0, 'xPos':  800, 'yPos': 2700, 'width': 1950, 'height': 150, 'style': 'styleA', 'name': 'IVP_CSAccelerationFactor', 'valueUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_CSACCELERATIONFACTORVALUETEXT", ATM_Zeta_GUIO_Generals.textBox_typeA,          {'groupOrder': 0, 'xPos': 2850, 'yPos': 2650, 'width':  600, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ANCHORRANGERFACTORTEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,            {'groupOrder': 0, 'xPos':    0, 'yPos': 2300, 'width':  700, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:IVPCANCHORRANGERFACTOR'), 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ANCHORRANGERFACTORSLIDER",    ATM_Zeta_GUIO_Generals.slider_typeA,             {'groupOrder': 0, 'xPos':  800, 'yPos': 2350, 'width': 1950, 'height': 150, 'style': 'styleA', 'name': 'IVP_AnchorRangerFactor', 'valueUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['IVP'].addGUIO("INDICATOR_IVPFILTERED_ANCHORRANGERFACTORVALUETEXT", ATM_Zeta_GUIO_Generals.textBox_typeA,            {'groupOrder': 0, 'xPos': 2850, 'yPos': 2300, 'width':  600, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80})
            self.settingsSubPages['IVP'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': 1950, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'IVP_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})
                
        #<PIP Settings>
        if (True):
            self.settingsSubPages['PIP'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_MI_PIP'), 'fontSize': 100})
            self.settingsSubPages['PIP'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width':  600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  700, 'yPos': 9300, 'width': 1200, 'height': 250, 'style': 'styleA', 'name': 'PIP_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2000, 'yPos': 9300, 'width':  700, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2800, 'yPos': 9300, 'width':  650, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'PIP_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'PIP_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['PIP'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80}) #VIP
            pipLineTargets = {'BUYPOS':  {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPBUYPOS')},
                              'SELLPOS': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPSELLPOS')}}
            self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = pipLineTargets, displayTargets = 'all')

            self.settingsSubPages['PIP'].addGUIO("INDICATOR_BLOCKTITLE_PIPDISPLAY", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPDISPLAY'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['PIP'].addGUIO("INDICATOR_BUYPOS_TEXT",           ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 7200, 'width':                   900, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPBUYPOS'), 'fontSize': 80})
            self.settingsSubPages['PIP'].addGUIO("INDICATOR_BUYPOS_COLOR",          ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 1000, 'yPos': 7200, 'width':                   675, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['PIP'].addGUIO("INDICATOR_SELLPOS_TEXT",          ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 1775, 'yPos': 7200, 'width':                   900, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPSELLPOS'), 'fontSize': 80})
            self.settingsSubPages['PIP'].addGUIO("INDICATOR_SELLPOS_COLOR",         ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2775, 'yPos': 7200, 'width':                   675, 'height': 250, 'style': 'styleA', 'mode': True})

            self.settingsSubPages['PIP'].addGUIO("INDICATOR_BLOCKTITLE_PIPSETTINGS", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 6850, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:PIPSETTINGS'), 'fontSize': 90, 'anchor': 'SW'})

            self.settingsSubPages['PIP'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': 6500, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'PIP_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})

        #<VOL Settings>
        if (True):
            self.settingsSubPages['VOL'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SI_VOL'), 'fontSize': 100})
            self.settingsSubPages['VOL'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width':  600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  700, 'yPos': 9300, 'width': 1200, 'height': 250, 'style': 'styleA', 'name': 'VOL_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2000, 'yPos': 9300, 'width':  700, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2800, 'yPos': 9300, 'width':  650, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'VOL_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'VOL_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
            self.settingsSubPages['VOL'].addGUIO("INDICATORINDEX_BLOCKTITLE_MA",    ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLSETTINGS'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_VOLTYPETEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 7200, 'width': 1500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLTYPE'), 'fontSize': 80})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_VOLTYPESELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos': 1600, 'yPos': 7200, 'width': 1850, 'height': 250, 'style': 'styleA', 'name': 'VOL_VolTypeSelection', 'nDisplay': 4, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            volTypes = {'BASE':    {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLTYPE_BASE')},
                        'QUOTE':   {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLTYPE_QUOTE')},
                        'BASETB':  {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLTYPE_BASETB')},
                        'QUOTETB': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:VOLTYPE_QUOTETB')}}
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_VOLTYPESELECTION"].setSelectionList(selectionList = volTypes, displayTargets = 'all')
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_MATYPETEXT",       ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6850, 'width': 1500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE'), 'fontSize': 80})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_MATYPESELECTION",  ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos': 1600, 'yPos': 6850, 'width': 1850, 'height': 250, 'style': 'styleA', 'name': 'VOL_MATypeSelection', 'nDisplay': 3, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            maTypes = {'SMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_SMA')},
                        'WMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_WMA')},
                        'EMA': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MATYPE_EMA')}}
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_MATYPESELECTION"].setSelectionList(selectionList = maTypes, displayTargets = 'all')
            self.settingsSubPages['VOL'].addGUIO("INDICATORINDEX_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 6500, 'width':  800, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),    'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORINTERVAL_COLUMNTITLE",  ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':  900, 'yPos': 6500, 'width':  550, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVAL'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORWIDTH_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1550, 'yPos': 6500, 'width':  550, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:WIDTH'),    'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORCOLOR_COLUMNTITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2200, 'yPos': 6500, 'width':  650, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'),    'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['VOL'].addGUIO("INDICATORDISPLAY_COLUMNTITLE",   ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2950, 'yPos': 6500, 'width':  500, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:DISPLAY'),  'fontSize': 90, 'anchor': 'SW'})
            volMAList = dict()
            for i in range (_NMAXLINES['VOL']):
                lineNumber = i+1
                self.settingsSubPages['VOL'].addGUIO("INDICATOR_VOL{:d}".format(lineNumber),               ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos':    0, 'yPos': 6150-350*i, 'width': 800, 'height': 250, 'style': 'styleB', 'name': 'VOL_LineActivationSwitch_{:d}'.format(lineNumber), 'text': 'VOLMA{:d}'.format(lineNumber), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['VOL'].addGUIO("INDICATOR_VOL{:d}_INTERVALINPUT".format(lineNumber), ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos':  900, 'yPos': 6150-350*i, 'width': 550, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'VOL_IntervalTextInputBox_{:d}'.format(lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['VOL'].addGUIO("INDICATOR_VOL{:d}_WIDTHINPUT".format(lineNumber),    ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': 1550, 'yPos': 6150-350*i, 'width': 550, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'VOL_WidthTextInputBox_{:d}'.format(lineNumber), 'textUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['VOL'].addGUIO("INDICATOR_VOL{:d}_LINECOLOR".format(lineNumber),     ATM_Zeta_GUIO_Generals.LED_typeA,          {'groupOrder': 0, 'xPos': 2200, 'yPos': 6150-350*i, 'width': 650, 'height': 250, 'style': 'styleA', 'mode': True})
                self.settingsSubPages['VOL'].addGUIO("INDICATOR_VOL{:d}_DISPLAY".format(lineNumber),       ATM_Zeta_GUIO_Generals.switch_typeB,       {'groupOrder': 0, 'xPos': 2950, 'yPos': 6150-350*i, 'width': 500, 'height': 250, 'style': 'styleA', 'name': 'VOL_DisplaySwitch_{:d}'.format(lineNumber), 'releaseFunction': self._onSettingsContentUpdate})
                volMAList[str(lineNumber)] = {'text': "VOLMA {:d}".format(lineNumber)}
            yPosPoint0 = 6150-350*(_NMAXLINES['VOL']-1)
            self.settingsSubPages['VOL'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'VOL_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = volMAList, displayTargets = 'all')

        #<MMACD Settings>
        if (True):
            self.settingsSubPages['MMACD'].addGUIO("SUBPAGETITLE", ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SI_MMACD'), 'fontSize': 100})
            self.settingsSubPages['MMACD'].addGUIO("NAGBUTTON",    ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_TITLE",           ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 9650, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINECOLOR'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_TEXT",            ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 9300, 'width':                   550, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:LINETARGET'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_TARGETSELECTION", ATM_Zeta_GUIO_Generals.selectionBox_typeB,           {'groupOrder': 2, 'xPos':  650, 'yPos': 9300, 'width':                  1500, 'height': 250, 'style': 'styleA', 'name': 'MMACD_LineSelectionBox', 'nDisplay': 5, 'fontSize': 80, 'selectionUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_LED",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2250, 'yPos': 9300, 'width':                   500, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_APPLYCOLOR",      ATM_Zeta_GUIO_Generals.button_typeA,                 {'groupOrder': 0, 'xPos': 2850, 'yPos': 9300, 'width':                   600, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYCOLOR'), 'fontSize': 80, 'name': 'MMACD_ApplyColor', 'releaseFunction': self._onSettingsContentUpdate})
            for index, componentType in enumerate(('R', 'G', 'B', 'A')):
                self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_{:s}_TEXT".format(componentType),   ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos':    0, 'yPos': 8950-350*index, 'width':  500, 'height': 250, 'style': 'styleA', 'text': componentType, 'fontSize': 80})
                self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_{:s}_SLIDER".format(componentType), ATM_Zeta_GUIO_Generals.slider_typeA,  {'groupOrder': 0, 'xPos':  600, 'yPos': 8950-350*index, 'width': 2050, 'height': 150, 'style': 'styleA', 'name': 'MMACD_Color_{:s}'.format(componentType), 'valueUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MMACD'].addGUIO("INDICATORCOLOR_{:s}_VALUE".format(componentType),  ATM_Zeta_GUIO_Generals.textBox_typeA, {'groupOrder': 0, 'xPos': 2750, 'yPos': 8950-350*index, 'width':  700, 'height': 250, 'style': 'styleA', 'text': "-", 'fontSize': 80})
            mmacdLineTargets = {'MMACD':      {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDMMACD')},
                                'SIGNAL':     {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDSIGNAL')},
                                'HISTOGRAM+': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDHISTOGRAM+')},
                                'HISTOGRAM-': {'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDHISTOGRAM-')}}
            self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelectionList(selectionList = mmacdLineTargets, displayTargets = 'all')
            
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_BLOCKTITLE_DISPLAY",       ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 7550, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDDISPLAY'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACD_DISPLAYTEXT",        ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 7200, 'width':                  1300, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDMMACDDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACD_DISPLAYSWITCH",      ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1400, 'yPos': 7200, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'MMACD_DisplaySwitch_MMACD', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACD_COLORTEXT",          ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2000, 'yPos': 7200, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACD_COLOR",              ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2600, 'yPos': 7200, 'width':                   850, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNAL_DISPLAYTEXT",       ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6850, 'width':                  1300, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDSIGNALDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNAL_DISPLAYSWITCH",     ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1400, 'yPos': 6850, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'MMACD_DisplaySwitch_SIGNAL', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNAL_COLORTEXT",         ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2000, 'yPos': 6850, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNAL_COLOR",             ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2600, 'yPos': 6850, 'width':                   850, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_HISTOGRAM_DISPLAYTEXT",    ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 6500, 'width':                  1300, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDHISTOGRAMDISPLAY'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_HISTOGRAM_DISPLAYSWITCH",  ATM_Zeta_GUIO_Generals.switch_typeB,                 {'groupOrder': 0, 'xPos': 1400, 'yPos': 6500, 'width':                   500, 'height': 250, 'style': 'styleA', 'name': 'MMACD_DisplaySwitch_HISTOGRAM', 'statusUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_HISTOGRAM_COLORTEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos': 2000, 'yPos': 6500, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:COLOR'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_HISTOGRAM+_COLOR",         ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 2600, 'yPos': 6500, 'width':                   400, 'height': 250, 'style': 'styleA', 'mode': True})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_HISTOGRAM-_COLOR",         ATM_Zeta_GUIO_Generals.LED_typeA,                    {'groupOrder': 0, 'xPos': 3050, 'yPos': 6500, 'width':                   400, 'height': 250, 'style': 'styleA', 'mode': True})
            
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_BLOCKTITLE_MMACDSETTINGS",   ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 6150, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDSETTINGS'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNALINTERVALTEXT",         ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 5800, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MMACDSIGNALINTERVAL'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_SIGNALINTERVALTEXTINPUT",    ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos': 2950, 'yPos': 5800, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'MMACD_SignalIntervalTextInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MSDELTAMAINTERVALTEXT",      ATM_Zeta_GUIO_Generals.textBox_typeA,                {'groupOrder': 0, 'xPos':    0, 'yPos': 5450, 'width':                  2850, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:MSDELTAMAINTERVAL'), 'fontSize': 80})
            self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MSDELTAMAINTERVALTEXTINPUT", ATM_Zeta_GUIO_Generals.textInputBox_typeA,           {'groupOrder': 0, 'xPos': 2950, 'yPos': 5450, 'width':                   500, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'MMACD_MSDeltaMAIntervalTextInputBox', 'textUpdateFunction': self._onSettingsContentUpdate})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORINDEX_COLUMNTITLE1",          ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 5100, 'width':                   800, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),    'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORINTERVAL_COLUMNTITLE1",       ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':  900, 'yPos': 5100, 'width':                   775, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVAL'), 'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORINDEX_COLUMNTITLE2",          ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 1775, 'yPos': 5100, 'width':                   800, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INDEX'),    'fontSize': 90, 'anchor': 'SW'})
            self.settingsSubPages['MMACD'].addGUIO("INDICATORINTERVAL_COLUMNTITLE2",       ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos': 2675, 'yPos': 5100, 'width':                   775, 'height': 250, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:INTERVAL'), 'fontSize': 90, 'anchor': 'SW'})
            for lineIndex in range (_NMAXLINES['MMACD']):
                lineNumber = lineIndex+1; rowNumber = math.ceil(lineNumber/2)
                if (lineIndex%2 == 0): coordX = 0
                else:                  coordX = 1775
                self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACDMA{:d}".format(lineNumber),               ATM_Zeta_GUIO_Generals.switch_typeC,       {'groupOrder': 0, 'xPos': coordX,     'yPos': 5100-rowNumber*350, 'width': 800, 'height': 250, 'style': 'styleB', 'name': 'MMACD_LineActivationSwitch_{:d}'.format(lineNumber), 'text': 'MA {:d}'.format(lineNumber), 'fontSize': 80, 'statusUpdateFunction': self._onSettingsContentUpdate})
                self.settingsSubPages['MMACD'].addGUIO("INDICATOR_MMACDMA{:d}_INTERVALINPUT".format(lineNumber), ATM_Zeta_GUIO_Generals.textInputBox_typeA, {'groupOrder': 0, 'xPos': coordX+900, 'yPos': 5100-rowNumber*350, 'width': 775, 'height': 250, 'style': 'styleA', 'text': "", 'fontSize': 80, 'name': 'MMACD_IntervalTextInputBox_{:d}'.format(lineNumber),                             'textUpdateFunction': self._onSettingsContentUpdate})
            yPosPoint0 = 5100-math.ceil(_NMAXLINES['MMACD']/2)*350
            self.settingsSubPages['MMACD'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'MMACD_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})

        #<DMIxADX Settings>
        if (True):
            self.settingsSubPages['DMIxADX'].addGUIO("SUBPAGETITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SI_DMIxADX'), 'fontSize': 100})
            self.settingsSubPages['DMIxADX'].addGUIO("NAGBUTTON",        ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['DMIxADX'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'DMIxADX_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})

        #<MFI Settings>
        if (True):
            self.settingsSubPages['MFI'].addGUIO("SUBPAGETITLE",     ATM_Zeta_GUIO_Generals.passiveGraphics_wrapperTypeC, {'groupOrder': 0, 'xPos':    0, 'yPos': 10000, 'width': subPageViewSpaceWidth, 'height': 300, 'style': 'styleB', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:TITLE_SI_MFI'), 'fontSize': 100})
            self.settingsSubPages['MFI'].addGUIO("NAGBUTTON",        ATM_Zeta_GUIO_Generals.button_typeB,                 {'groupOrder': 0, 'xPos': 3050, 'yPos': 10050, 'width': 400,                   'height': 200, 'style': 'styleB', 'image': 'returnIcon_512x512.png', 'imageSize': (170, 170), 'imageRGBA': self.visualManager.getFromColorTable('ICON_COLORING'), 'name': 'navButton_toHome', 'releaseFunction': self.__onSettingsNavButtonClick})
            self.settingsSubPages['MFI'].addGUIO("APPLYNEWSETTINGS", ATM_Zeta_GUIO_Generals.button_typeA, {'groupOrder': 0, 'xPos': 0, 'yPos': yPosPoint0-350, 'width': subPageViewSpaceWidth, 'height': 250, 'style': 'styleA', 'text': self.visualManager.getTextPack('GUIO_CHARTDRAWER:APPLYSETTINGS'), 'fontSize': 80, 'name': 'MFI_ApplySettings', 'releaseFunction': self._onSettingsContentUpdate})

    def __readObjectConfig(self):
        if (self.objectConfig_preset != None):
            for configKeyCode in self.objectConfig_preset:
                if configKeyCode in self.objectConfig:
                    try:
                        configContent    = self.objectConfig_preset[configKeyCode] #Preset Object Configuration for the corresponding configKey
                        expectedDataType = type(self.objectConfig[configKeyCode])  #Expected data type (According to the intial configData)

                        #Convert read preset objection configuration into expected data type
                        #[1]: INTEGER Type
                        if (expectedDataType == int):   typeConverted = int(configContent)
                        #[2]: FLOAT Type
                        elif (expectedDataType == float): typeConverted = float(configContent)
                        #[3]: STRING Type
                        elif (expectedDataType == str):   
                            if ((configContent == 'None') or (configContent == 'NONE')): typeConverted = None
                            else:                                                        typeConverted = configContent
                        #[4]: BOOL Type
                        elif (expectedDataType == bool):
                            #First see if the preset config data can be interpreted as an integer, and if can, interpret it as 'True', if it is greater than or equal to 1
                            try:
                                configContent_asInt = int(configContent)
                                if (0 < configContent_asInt): typeConverted = True
                                else:                         typeConverted = False
                            #If it cannot be read as an integer, interpret it as 'True' if its string form is either "True" or "TRUE", and 'False' otherwise
                            except:
                                if ((configContent == 'True') or (configContent == 'TRUE')): typeConverted = True
                                else:                                                        typeConverted = False
                        #[5]: NONE Type
                        elif (self.objectConfig[configKeyCode] == None): 
                            if ((configContent == 'None') or (configContent == 'NONE')): typeConverted = None
                            else:                                                        typeConverted = configContent

                        #Local Tracker Update
                        if (configKeyCode[-14:] == 'DisplayContent'):
                            if (typeConverted in _SITYPES): self.objectConfig[configKeyCode] = typeConverted
                            else:                               self.objectConfig[configKeyCode] = None
                        else: self.objectConfig[configKeyCode] = typeConverted
                    except: print(termcolor.colored("An error ocrrued while attempting to match configuration data type for object name {:s}: configKeyCode: {:s}, originalType: {:s}, configData: {:s}".format(self.name, configKeyCode, str(type(self.objectConfig[configKeyCode])), self.objectConfig_preset[configKeyCode]), 'light_red'))
                else: print(termcolor.colored("An unrecognizable configuration detected while reading GUIOConfig for {:s}: '{:s}'".format(self.name, configKeyCode), 'light_red'))

    def __matchGUIOsToConfig(self):
        #<MAIN>
        if (True):
            #---MI Compute
            for miType in _MITYPES: self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_{:s}".format(miType)].setStatus(self.objectConfig['{:s}Compute'.format(miType)], callStatusUpdateFunction = False)
            #---SI Compute
            for siType in _SITYPES: self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_{:s}".format(siType)].setStatus(self.objectConfig['{:s}Compute'.format(siType)], callStatusUpdateFunction = False)
            #---SI Viewer
            unassignedSIViewerNumbers = list(range(1, len(_SITYPES)+1))
            unassignedSIType          = list(_SITYPES)
            for siViewerNumber in range (1, len(_SITYPES)+1):
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber)].setStatus(self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)], callStatusUpdateFunction = False)
                siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber)]
                if (siAlloc in _SITYPES):
                    self.siTypes_siViewerAlloc[siAlloc] = siViewerNumber
                    self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSELECTION{:d}".format(siViewerNumber)].setSelected(siAlloc, callSelectionUpdateFunction = False)
                    unassignedSIViewerNumbers.remove(siViewerNumber); unassignedSIType.remove(siAlloc)
            for i in range (len(unassignedSIViewerNumbers)):
                unassignedSIViewerNumber = unassignedSIViewerNumbers[i]
                unassignedSIType         = unassignedSIType[i]
                self.objectConfig['SIVIEWER{:d}SIAlloc'.format(unassignedSIViewerNumber)] = unassignedSIType
                self.siTypes_siViewerAlloc[unassignedSIType] = unassignedSIViewerNumber
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSELECTION{:d}".format(unassignedSIViewerNumber)].setSelected(unassignedSIType, callSelectionUpdateFunction = False)

            #---Auxillaries
            self.settingsSubPages['MAIN'].GUIOs["AUX_SHOWAUXBAR_SWITCH"].setStatus(self.objectConfig['UseAuxBar'], callStatusUpdateFunction = False)
            self.settingsSubPages['MAIN'].GUIOs["AUX_DISPLAYEVENTS_SWITCH"].setStatus(self.objectConfig['DisplayEvents'], callStatusUpdateFunction = False)
            self.settingsSubPages['MAIN'].GUIOs["AUX_KLINECOLORTYPE_SELECTIONBOX"].setSelected(self.objectConfig['KlineColorType'], callSelectionUpdateFunction = False)
            self.settingsSubPages['MAIN'].GUIOs["AUX_TIMEZONE_SELECTIONBOX"].setSelected(self.objectConfig['TimeZone'], callSelectionUpdateFunction = False)
        #<MAs>
        if (True):
            for miType in ('SMA','WMA','EMA'):
                for lineIndex in range (_NMAXLINES[miType]):
                    lineNumber = lineIndex+1
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}".format(miType,lineNumber)].setStatus(self.objectConfig['{:s}{:d}Display'.format(miType,lineNumber)])
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_INTERVALINPUT".format(miType,lineNumber)].updateText(str(self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)]))
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_WIDTHINPUT".format(miType,lineNumber)].updateText(str(self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)]))
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_LINECOLOR".format(miType,lineNumber)].updateColor(self.objectConfig['{:s}{:d}colorR%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                                self.objectConfig['{:s}{:d}colorG%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                                self.objectConfig['{:s}{:d}colorB%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                                self.objectConfig['{:s}{:d}colorA%{:s}'.format(miType,lineNumber,self.currentGUITheme)])
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_DISPLAY".format(miType,lineNumber)].setStatus(self.objectConfig['{:s}{:d}Display'.format(miType,lineNumber)])
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('1')
                self.settingsSubPages[miType].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<PSAR>
        if (True):
            for lineIndex in range (_NMAXLINES['PSAR']):
                lineNumber = lineIndex+1
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}".format(lineNumber)].setStatus(self.objectConfig['PSAR{:d}Compute'.format(lineNumber)])
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_STARTINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}start'.format(lineNumber)]))
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_ACCELERATIONINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)]))
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_MAXIMUMINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]))
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_SIZEINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}Size'.format(lineNumber)]))
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['PSAR{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['PSAR{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['PSAR{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['PSAR{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_DISPLAY".format(lineNumber)].setStatus(self.objectConfig['PSAR{:d}Display'.format(lineNumber)])
            self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('1')
            self.settingsSubPages['PSAR'].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<BOL>
        if (True):
            self.settingsSubPages['BOL'].GUIOs["INDICATOR_MATYPESELECTION"].setSelected(self.objectConfig['BOLMAType'])
            for lineIndex in range (_NMAXLINES['BOL']):
                lineNumber = lineIndex+1
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}".format(lineNumber)].setStatus(self.objectConfig['BOL{:d}Compute'.format(lineNumber)])
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_INTERVALINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}nSamples'.format(lineNumber)]))
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_BANDWIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)]))
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_WIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}Width'.format(lineNumber)]))
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['BOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_DISPLAY".format(lineNumber)].setStatus(self.objectConfig['BOL{:d}Display'.format(lineNumber)])
            self.settingsSubPages['BOL'].GUIOs["INDICATOR_DISPLAYCONTENTS_BOLCENTERSWITCH"].setStatus(self.objectConfig['BOLdisplayCenterLine'])
            self.settingsSubPages['BOL'].GUIOs["INDICATOR_DISPLAYCONTENTS_BOLBANDSWITCH"].setStatus(self.objectConfig['BOLdisplayBand'])
            self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('1')
            self.settingsSubPages['BOL'].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<IVP>
        if (True):
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_DISPLAYSWITCH"].setStatus(self.objectConfig['IVPRAWDisplay'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_COLOR"].updateColor(self.objectConfig['IVPRAWcolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                        self.objectConfig['IVPRAWcolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                        self.objectConfig['IVPRAWcolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                        self.objectConfig['IVPRAWcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_DISPLAYWIDTHSLIDER"].setSliderValue((self.objectConfig['IVPRAWDisplayWidth']-0.1)/0.9*100)
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_DISPLAYWIDTHVALUETEXT"].updateText(str(self.objectConfig['IVPRAWDisplayWidth']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCCURRENTANCHOR_DISPLAYSWITCH"].setStatus(self.objectConfig['IVPCCURRENTANCHORDisplay'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCCURRENTANCHOR_COLOR"].updateColor(self.objectConfig['IVPCCURRENTANCHORcolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPREVANCHOR_DISPLAYSWITCH"].setStatus(self.objectConfig['IVPCPREVANCHORDisplay'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPREVANCHOR_COLOR"].updateColor(self.objectConfig['IVPCPREVANCHORcolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                             self.objectConfig['IVPCPREVANCHORcolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                             self.objectConfig['IVPCPREVANCHORcolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                             self.objectConfig['IVPCPREVANCHORcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_USEBLESWITCH"].setStatus(self.objectConfig['IVPUseBLE'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_INTERVALINPUT"].updateText(str(self.objectConfig['IVPnSamples']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_MINGAMMAFACTORSLIDER"].setSliderValue((self.objectConfig['IVPMinGammaFactorPerc']-0.05)*(100/1.95))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_MINGAMMAFACTORVALUETEXT"].updateText("{:.2f} %".format(self.objectConfig['IVPMinGammaFactorPerc']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_USEAGFSWITCH"].setStatus(self.objectConfig['IVPUseAGF'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFREFLENINPUT"].updateText(str(self.objectConfig['IVPAGFRefLen']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFMATYPESELECTION"].setSelected(self.objectConfig['IVPAGFMAType'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCEXTENSION_DISPLAYSWITCH"].setStatus(self.objectConfig['IVPCExtension'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPOSITIONAL_DISPLAYSWITCH"].setStatus(self.objectConfig['IVPCPositional'])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CLUSTERINGRANGESLIDER"].setSliderValue((self.objectConfig['IVPClusteringRange']-2)*(100/98))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CLUSTERINGRANGEVALUETEXT"].updateText("{:.1f} %".format(self.objectConfig['IVPClusteringRange']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMINTEXTINPUT"].updateText(str(self.objectConfig['IVPCExistenceCounterMin']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMAXTEXTINPUT"].updateText(str(self.objectConfig['IVPCExistenceCounterMax']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CSACCELERATIONFACTORSLIDER"].setSliderValue((self.objectConfig['IVPCCSAccelerationFactor']-0.05)*(100/0.95))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CSACCELERATIONFACTORVALUETEXT"].updateText("{:.2f}".format(self.objectConfig['IVPCCSAccelerationFactor']))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ANCHORRANGERFACTORSLIDER"].setSliderValue((self.objectConfig['IVPCAnchorRangerFactor']-0.1)*(100/0.9))
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ANCHORRANGERFACTORVALUETEXT"].updateText("{:.2f}".format(self.objectConfig['IVPCAnchorRangerFactor']))
            self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('RAW')
            self.settingsSubPages['IVP'].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<PIP>
        if (True):
            self.settingsSubPages['PIP'].GUIOs["INDICATOR_BUYPOS_COLOR"].updateColor(self.objectConfig['PIPBUYPOScolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                     self.objectConfig['PIPBUYPOScolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                     self.objectConfig['PIPBUYPOScolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                     self.objectConfig['PIPBUYPOScolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['PIP'].GUIOs["INDICATOR_SELLPOS_COLOR"].updateColor(self.objectConfig['PIPSELLPOScolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['PIPSELLPOScolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['PIPSELLPOScolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['PIPSELLPOScolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('BUYPOS')
            self.settingsSubPages['PIP'].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<VOL>
        if (True):
            for lineIndex in range (_NMAXLINES['VOL']):
                lineNumber = lineIndex+1
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}".format(lineNumber)].setStatus(self.objectConfig['VOL{:d}Compute'.format(lineNumber)])
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_INTERVALINPUT".format(lineNumber)].updateText(str(self.objectConfig['VOL{:d}nSamples'.format(lineNumber)]))
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_WIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['VOL{:d}Width'.format(lineNumber)]))
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_DISPLAY".format(lineNumber)].setStatus(self.objectConfig['VOL{:d}Display'.format(lineNumber)])
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_VOLTYPESELECTION"].setSelected(self.objectConfig['VOLType'], callSelectionUpdateFunction = False)
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_MATYPESELECTION"].setSelected(self.objectConfig['VOLMAType'], callSelectionUpdateFunction = False)
            self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('1')
            self.settingsSubPages['VOL'].GUIOs["APPLYNEWSETTINGS"].deactivate()
        #<MMACD>
        if (True):
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACD_DISPLAYSWITCH"].setStatus(self.objectConfig['MMACDMMACDDisplay'])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_SIGNAL_DISPLAYSWITCH"].setStatus(self.objectConfig['MMACDSIGNALDisplay'])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_HISTOGRAM_DISPLAYSWITCH"].setStatus(self.objectConfig['MMACDHISTOGRAMDisplay'])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACD_COLOR"].updateColor(self.objectConfig['MMACDMMACDcolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['MMACDMMACDcolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['MMACDMMACDcolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                      self.objectConfig['MMACDMMACDcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_SIGNAL_COLOR"].updateColor(self.objectConfig['MMACDSIGNALcolorR%{:s}'.format(self.currentGUITheme)], 
                                                                                       self.objectConfig['MMACDSIGNALcolorG%{:s}'.format(self.currentGUITheme)], 
                                                                                       self.objectConfig['MMACDSIGNALcolorB%{:s}'.format(self.currentGUITheme)], 
                                                                                       self.objectConfig['MMACDSIGNALcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_HISTOGRAM+_COLOR"].updateColor(self.objectConfig['MMACDHISTOGRAM+colorR%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM+colorG%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM+colorB%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM+colorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_HISTOGRAM-_COLOR"].updateColor(self.objectConfig['MMACDHISTOGRAM-colorR%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM-colorG%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM-colorB%{:s}'.format(self.currentGUITheme)], 
                                                                                           self.objectConfig['MMACDHISTOGRAM-colorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_SIGNALINTERVALTEXTINPUT"].updateText(str(self.objectConfig['MMACDSignalInterval']))
            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MSDELTAMAINTERVALTEXTINPUT"].updateText(str(self.objectConfig['MMACDSignalDeltaMAInterval']))
            for lineIndex in range (_NMAXLINES['MMACD']):
                lineNumber = lineIndex+1
                self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACDMA{:d}".format(lineNumber)].setStatus(self.objectConfig['MMACD{:d}Compute'.format(lineNumber)])
                self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACDMA{:d}_INTERVALINPUT".format(lineNumber)].updateText(str(self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)]))
            self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected('MMACD')
            self.settingsSubPages['MMACD'].GUIOs["APPLYNEWSETTINGS"].deactivate()

        #Set SubIndicator Switch Activation
        if (True):
            for siViewerNumber in range (1, len(_SITYPES)+1):
                if (siViewerNumber <= self.usableSIViewers): self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber)].activate()
                else:
                    self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber)].setStatus(False)
                    self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber)].deactivate()

        #Final 'AUX_SAVECONFIGURATION' Deactivation
        self.settingsSubPages['MAIN'].GUIOs["AUX_SAVECONFIGURATION"].deactivate()
    #Object Configuration & GUIO Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #DisplayBox Control ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __configureDisplayBoxes(self, onInit = False):
        #[1]: Determine Vertical DisplayBox Order
        if (True):
            #--- Temporal Grid
            self.displayBox_VerticalSection_Order = ['TEMPORALGRID']; self.displayBox_VisibleBoxes = ['MAINGRID_TEMPORAL', 'SETTINGSBUTTONFRAME']
            #--- SI Viewers (Reverse Order)
            for siViewerNumber in range (self.usableSIViewers, 0, -1):
                if (self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)] == True):
                    self.displayBox_VerticalSection_Order.append('SIVIEWER{:d}'.format(siViewerNumber))
                    self.displayBox_VisibleBoxes += ['SIVIEWER{:d}'.format(siViewerNumber)]
            #--- Klines Price
            self.displayBox_VerticalSection_Order.append('KLINESPRICE')
            self.displayBox_VisibleBoxes += ['KLINESPRICE']
            #--- AUX Bar
            if (self.settingsSubPages['MAIN'].GUIOs['AUX_SHOWAUXBAR_SWITCH'].getStatus() == True): 
                self.displayBox_VerticalSection_Order.append('AUXILLARYBAR')
                self.displayBox_VisibleBoxes.append('AUXILLARYBAR')
            
        #[2]: Determine DisplayBox Dimensions
        if (True):
            #---Determin General Section Width
            displayBoxWidth_leftSection  = self.width - _GD_DISPLAYBOX_RIGHTSECTION_WIDTH - _GD_DISPLAYBOX_GOFFSET
            displayBoxWidth_rightSection = _GD_DISPLAYBOX_RIGHTSECTION_WIDTH

            #---Determine Vertical Section Height
            nVisibleVerticalSections = len(self.displayBox_VerticalSection_Order)
            nVisibleSIViewers        = len([verticalSectionName for verticalSectionName in self.displayBox_VerticalSection_Order if verticalSectionName[:8] == 'SIVIEWER'])
            nAvailableHeight = self.height - _GD_DISPLAYBOX_GOFFSET*(nVisibleVerticalSections-1) - _GD_DISPLAYBOX_MAINGRIDTEMPORAL_HEIGHT
            if ('AUXILLARYBAR' in self.displayBox_VerticalSection_Order): nAvailableHeight -= _GD_DISPLAYBOX_AUXILLARYBAR_HEIGHT
            nAvailableHeight -= _GD_DISPLAYBOX_SIVIEWER_HEIGHT*nVisibleSIViewers
            displayBoxHeight_KLINESPRICE = nAvailableHeight
        
            #---Set DisplayBox Coordinates and Dimensions
            verticalSectionYPos = self.yPos
            for verticalSectionName in self.displayBox_VerticalSection_Order:
                if (verticalSectionName == 'TEMPORALGRID'):
                    #Define DisplayBox and DrawBox Dimensions for 'MAINGRID_TEMPORAL'
                    displayBox_MAINGRID_TEMPORAL = (self.xPos, verticalSectionYPos, displayBoxWidth_leftSection , _GD_DISPLAYBOX_MAINGRIDTEMPORAL_HEIGHT)
                    drawBox_MAINGRID_TEMPORAL    = (displayBox_MAINGRID_TEMPORAL[0]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_TEMPORAL[1]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_TEMPORAL[2]-_GD_DISPLAYBOX_GOFFSET*2, displayBox_MAINGRID_TEMPORAL[3]-_GD_DISPLAYBOX_GOFFSET*2)
                    self.displayBox['MAINGRID_TEMPORAL']                     = displayBox_MAINGRID_TEMPORAL
                    self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'] = drawBox_MAINGRID_TEMPORAL
                
                    #Define DisplayBox Dimensions for 'SETTINGSBUTTONFRAME'
                    displayBox_SETTINGSBUTTONFRAME = (self.xPos+displayBoxWidth_leftSection+_GD_DISPLAYBOX_GOFFSET, verticalSectionYPos, displayBoxWidth_rightSection, _GD_DISPLAYBOX_MAINGRIDTEMPORAL_HEIGHT)
                    self.displayBox['SETTINGSBUTTONFRAME'] = displayBox_SETTINGSBUTTONFRAME

                    verticalSectionYPos += _GD_DISPLAYBOX_MAINGRIDTEMPORAL_HEIGHT+_GD_DISPLAYBOX_GOFFSET

                elif (verticalSectionName[:8] == 'SIVIEWER'):
                    #Define DisplayBox and DrawBox Dimensions for 'SIVIEWER[X]'
                    displayBox_SIVIEWER = (self.xPos, verticalSectionYPos, displayBoxWidth_leftSection , _GD_DISPLAYBOX_SIVIEWER_HEIGHT)
                    drawBox_SIVIEWER    = (displayBox_SIVIEWER[0]+_GD_DISPLAYBOX_GOFFSET, displayBox_SIVIEWER[1]+_GD_DISPLAYBOX_GOFFSET, displayBox_SIVIEWER[2]-_GD_DISPLAYBOX_GOFFSET*2, displayBox_SIVIEWER[3]-_GD_DISPLAYBOX_GOFFSET*2)
                    self.displayBox[verticalSectionName]                     = displayBox_SIVIEWER
                    self.displayBox_graphics[verticalSectionName]['DRAWBOX'] = drawBox_SIVIEWER
                
                    #Define DisplayBox and DrawBox Dimensions for 'MAINGRID_SIVIEWER[X]'
                    displayBox_MAINGRID_SIVIEWER = (self.xPos+displayBoxWidth_leftSection+_GD_DISPLAYBOX_GOFFSET, verticalSectionYPos, displayBoxWidth_rightSection, _GD_DISPLAYBOX_SIVIEWER_HEIGHT)
                    drawBox_MAINGRID_SIVIEWER    = (displayBox_MAINGRID_SIVIEWER[0]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_SIVIEWER[1]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_SIVIEWER[2]-_GD_DISPLAYBOX_GOFFSET*2, displayBox_MAINGRID_SIVIEWER[3]-_GD_DISPLAYBOX_GOFFSET*2)
                    self.displayBox['MAINGRID_'+verticalSectionName]                     = displayBox_MAINGRID_SIVIEWER
                    self.displayBox_graphics['MAINGRID_'+verticalSectionName]['DRAWBOX'] = drawBox_MAINGRID_SIVIEWER

                    verticalSectionYPos += _GD_DISPLAYBOX_SIVIEWER_HEIGHT+_GD_DISPLAYBOX_GOFFSET

                elif (verticalSectionName == 'KLINESPRICE'):
                    #Define DisplayBox and DrawBox Dimensions for 'KLINESPRICE'
                    displayBox_KLINESPRICE = (self.xPos, verticalSectionYPos, displayBoxWidth_leftSection , displayBoxHeight_KLINESPRICE)
                    drawBox_KLINESPRICE    = (displayBox_KLINESPRICE[0]+_GD_DISPLAYBOX_GOFFSET, displayBox_KLINESPRICE[1]+_GD_DISPLAYBOX_GOFFSET, displayBox_KLINESPRICE[2]-_GD_DISPLAYBOX_GOFFSET*2, displayBox_KLINESPRICE[3]-_GD_DISPLAYBOX_GOFFSET*2)
                    self.displayBox['KLINESPRICE']                     = displayBox_KLINESPRICE
                    self.displayBox_graphics['KLINESPRICE']['DRAWBOX'] = drawBox_KLINESPRICE

                    #Define DisplayBox and DrawBox Dimensions for 'MAINGRID_KLINESPRICE'
                    displayBox_MAINGRID_KLINESPRICE = (self.xPos+displayBoxWidth_leftSection+_GD_DISPLAYBOX_GOFFSET, verticalSectionYPos, displayBoxWidth_rightSection, displayBoxHeight_KLINESPRICE)
                    drawBox_MAINGRID_KLINESPRICE    = (displayBox_MAINGRID_KLINESPRICE[0]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_KLINESPRICE[1]+_GD_DISPLAYBOX_GOFFSET, displayBox_MAINGRID_KLINESPRICE[2]-_GD_DISPLAYBOX_GOFFSET*2, displayBox_MAINGRID_KLINESPRICE[3]-_GD_DISPLAYBOX_GOFFSET*2)
                    self.displayBox['MAINGRID_KLINESPRICE']                     = displayBox_MAINGRID_KLINESPRICE
                    self.displayBox_graphics['MAINGRID_KLINESPRICE']['DRAWBOX'] = drawBox_MAINGRID_KLINESPRICE

                    verticalSectionYPos += displayBoxHeight_KLINESPRICE+_GD_DISPLAYBOX_GOFFSET

                elif (verticalSectionName == 'AUXILLARYBAR'):
                    #Define DisplayBox Dimensions for 'AUXILLARYBAR'
                    displayBox_AUXILLARYBAR = (self.xPos, verticalSectionYPos, self.width, _GD_DISPLAYBOX_AUXILLARYBAR_HEIGHT)
                    self.displayBox['AUXILLARYBAR'] = displayBox_AUXILLARYBAR
                
        #[3]: Set DisplayBox Objects (HitBox, Images, FrameSprites, CamGroups, RCLCGs, etc.)
        if (True):
            self.nMaxVerticalGridLines = int((self.displayBox['MAINGRID_TEMPORAL'][2]-_GD_DISPLAYBOX_GOFFSET*2)*self.scaler/_GD_DISPLAYBOX_GRID_VERTICALLINEPIXELINTERVAL)
            self.nMaxHorizontalGridLines['KLINESPRICE'] = int((self.displayBox['KLINESPRICE'][3]-_GD_DISPLAYBOX_GOFFSET*2)*self.scaler/_GD_DISPLAYBOX_GRID_HORIZONTALLINEPIXELINTERVAL)

            if (onInit == True):
                for displayBoxName in self.displayBox:
                    self.mouse_DragDX[displayBoxName] = 0; self.mouse_DragDY[displayBoxName] = 0; self.mouse_ScrollDX[displayBoxName] = 0; self.mouse_ScrollDY[displayBoxName] = 0
                    #---MAINGRID_TEMPORAL
                    if (displayBoxName == 'MAINGRID_TEMPORAL'):
                        displayBox = self.displayBox['MAINGRID_TEMPORAL']
                        drawBox    = self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX']
                        
                        #Generate Graphic Sprites and Hitboxes
                        self.hitBox['MAINGRID_TEMPORAL'] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(drawBox[0], drawBox[1], drawBox[2], drawBox[3])
                        self.images['MAINGRID_TEMPORAL'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                        self.frameSprites['MAINGRID_TEMPORAL'] = pyglet.sprite.Sprite(x = displayBox[0]*self.scaler, y = displayBox[1]*self.scaler, img = self.images['MAINGRID_TEMPORAL'][0], batch = self.batch, group = self.group_0)

                        #Setup CamGroup
                        self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP'] = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window = self.window, order = self.groupOrder+1, viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_y0 = 0, projection_y1 = drawBox[3]*self.scaler)

                        #Setup Grids
                        self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'] = list()
                        self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'] = list()
                        for i in range (self.nMaxVerticalGridLines):
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, (_GD_DISPLAYBOX_GRID_VERTICALTEXTHEIGHT+_GD_DISPLAYBOX_GOFFSET)*self.scaler, 0, drawBox[3]*self.scaler, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP']))
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                              xPos = 0, yPos = 0, width = _GD_DISPLAYBOX_GRID_VERTICALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_VERTICALTEXTHEIGHT, showElementBox = False, anchor = 'CENTER'))
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][-1].visible = False
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][-1].hide()

                    #---SETTINGSBUTTONFRAME
                    elif (displayBoxName == 'SETTINGSBUTTONFRAME'):
                        self.hitBox['SETTINGSBUTTONFRAME'] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(self.displayBox['SETTINGSBUTTONFRAME'][0], self.displayBox['SETTINGSBUTTONFRAME'][1], self.displayBox['SETTINGSBUTTONFRAME'][2], self.displayBox['SETTINGSBUTTONFRAME'][3])
                        self.images['SETTINGSBUTTONFRAME_DEFAULT'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrameInteractable_DEFAULT", self.displayBox['SETTINGSBUTTONFRAME'][2]*self.scaler, self.displayBox['SETTINGSBUTTONFRAME'][3]*self.scaler)
                        self.images['SETTINGSBUTTONFRAME_HOVERED'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrameInteractable_HOVERED", self.displayBox['SETTINGSBUTTONFRAME'][2]*self.scaler, self.displayBox['SETTINGSBUTTONFRAME'][3]*self.scaler)
                        self.images['SETTINGSBUTTONFRAME_PRESSED'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrameInteractable_PRESSED", self.displayBox['SETTINGSBUTTONFRAME'][2]*self.scaler, self.displayBox['SETTINGSBUTTONFRAME'][3]*self.scaler)
                        self.images['SETTINGSBUTTONFRAME_ICON'] = self.imageManager.getImage('settingsIcon_512x512.png', (round(self.displayBox['SETTINGSBUTTONFRAME'][3]*0.65*self.scaler), round(self.displayBox['SETTINGSBUTTONFRAME'][3]*0.65*self.scaler)))

                        self.frameSprites['SETTINGSBUTTONFRAME'] = pyglet.sprite.Sprite(x = self.displayBox['SETTINGSBUTTONFRAME'][0]*self.scaler, y = self.displayBox['SETTINGSBUTTONFRAME'][1]*self.scaler, img = self.images['SETTINGSBUTTONFRAME_DEFAULT'][0], batch = self.batch, group = self.group_0)
                        self.frameSprites['SETTINGSBUTTONFRAME_ICON'] = pyglet.sprite.Sprite(x = (self.displayBox['SETTINGSBUTTONFRAME'][0]+self.displayBox['SETTINGSBUTTONFRAME'][2]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].width/2, 
                                                                                                y = (self.displayBox['SETTINGSBUTTONFRAME'][1]+self.displayBox['SETTINGSBUTTONFRAME'][3]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].height/2, 
                                                                                                img = self.images['SETTINGSBUTTONFRAME'+'_ICON'], batch = self.batch, group = self.group_1)
                        iconColoring = self.visualManager.getFromColorTable('ICON_COLORING')
                        self.frameSprites['SETTINGSBUTTONFRAME_ICON'].color = (iconColoring[0], iconColoring[1], iconColoring[2]); self.frameSprites['SETTINGSBUTTONFRAME'+'_ICON'].opacity = iconColoring[3]

                    #---KLINESPRICE
                    elif (displayBoxName == 'KLINESPRICE'):
                        displayBox          = self.displayBox['KLINESPRICE']
                        displayBox_MAINGRID = self.displayBox['MAINGRID_KLINESPRICE']
                        drawBox             = self.displayBox_graphics['KLINESPRICE']['DRAWBOX']
                        drawBox_MAINGRID    = self.displayBox_graphics['MAINGRID_KLINESPRICE']['DRAWBOX']

                        #Generate Graphic Sprites and Hitboxes
                        self.hitBox['KLINESPRICE'] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(drawBox[0], drawBox[1], drawBox[2], drawBox[3])
                        self.images['KLINESPRICE'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                        self.frameSprites['KLINESPRICE'] = pyglet.sprite.Sprite(x = displayBox[0]*self.scaler, y = displayBox[1]*self.scaler, img = self.images['KLINESPRICE'][0], batch = self.batch, group = self.group_0)
                        self.hitBox['MAINGRID_KLINESPRICE'] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(drawBox_MAINGRID[0], drawBox_MAINGRID[1], drawBox_MAINGRID[2], drawBox_MAINGRID[3])
                        self.images['MAINGRID_KLINESPRICE'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox_MAINGRID[2]*self.scaler, displayBox_MAINGRID[3]*self.scaler)
                        self.frameSprites['MAINGRID_KLINESPRICE'] = pyglet.sprite.Sprite(x = displayBox_MAINGRID[0]*self.scaler, y = displayBox_MAINGRID[1]*self.scaler, img = self.images['MAINGRID_KLINESPRICE'][0], batch = self.batch, group = self.group_0)

                        #Setup CamGroup and DisplaySpaceManager
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP'] = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window=self.window, order = self.groupOrder+1, viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = drawBox[2]*self.scaler)
                        self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP']   = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window=self.window, order = self.groupOrder+1, viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_y0 = 0, projection_y1 = drawBox[3]*self.scaler)
                        self.displayBox_graphics['KLINESPRICE']['RCLCG']                   = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, fsdResolution_y = 2)
                        self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED']            = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = 100, fsdResolution_y = 5)
                        self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED']            = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, projection_y0 = 0, projection_y1 = 100)
                        self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP'] = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window = self.window, order = self.groupOrder+1, viewport_x=drawBox_MAINGRID[0]*self.scaler, viewport_y=drawBox_MAINGRID[1]*self.scaler, viewport_width=drawBox_MAINGRID[2]*self.scaler, viewport_height=drawBox_MAINGRID[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = drawBox_MAINGRID[2]*self.scaler)
                            
                        #Description Texts
                        self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.group_hd0, text = "", 
                                                                                                                             defaultTextStyle    = self.effectiveTextStyle['CONTENT_DEFAULT'],
                                                                                                                             auxillaryTextStyles = {'POSITIVE_1': self.effectiveTextStyle['CONTENT_POSITIVE_1'], 'NEGATIVE_1': self.effectiveTextStyle['CONTENT_NEGATIVE_1'], 'NEUTRAL_1':  self.effectiveTextStyle['CONTENT_NEUTRAL_1'],
                                                                                                                                                    'POSITIVE_2': self.effectiveTextStyle['CONTENT_POSITIVE_2'], 'NEGATIVE_2': self.effectiveTextStyle['CONTENT_NEGATIVE_2'], 'NEUTRAL_2':  self.effectiveTextStyle['CONTENT_NEUTRAL_2'],
                                                                                                                                                    'DEFAULT':    self.effectiveTextStyle['CONTENT_DEFAULT']},
                                                                                                                             xPos = drawBox[0], yPos = drawBox[1]+drawBox[3]-200, width = drawBox[2], height = 200, showElementBox = False, anchor = 'W')
                        self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.group_hd0, text = "", 
                                                                                                                             defaultTextStyle    = self.effectiveTextStyle['CONTENT_DEFAULT'],
                                                                                                                             auxillaryTextStyles = {'POSITIVE_1': self.effectiveTextStyle['CONTENT_POSITIVE_1'], 'NEGATIVE_1': self.effectiveTextStyle['CONTENT_NEGATIVE_1'], 'NEUTRAL_1':  self.effectiveTextStyle['CONTENT_NEUTRAL_1'],
                                                                                                                                                    'POSITIVE_2': self.effectiveTextStyle['CONTENT_POSITIVE_2'], 'NEGATIVE_2': self.effectiveTextStyle['CONTENT_NEGATIVE_2'], 'NEUTRAL_2':  self.effectiveTextStyle['CONTENT_NEUTRAL_2'],
                                                                                                                                                    'DEFAULT':    self.effectiveTextStyle['CONTENT_DEFAULT']},
                                                                                                                             xPos = drawBox[0], yPos = drawBox[1]+drawBox[3]-400, width = drawBox[2], height = 200, showElementBox = False, anchor = 'W')
                        self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.group_hd0, text = "", 
                                                                                                                       defaultTextStyle    = self.effectiveTextStyle['CONTENT_DEFAULT'],
                                                                                                                       auxillaryTextStyles = {'POSITIVE_1': self.effectiveTextStyle['CONTENT_POSITIVE_1'], 'NEGATIVE_1': self.effectiveTextStyle['CONTENT_NEGATIVE_1'], 'NEUTRAL_1':  self.effectiveTextStyle['CONTENT_NEUTRAL_1'],
                                                                                                                                              'POSITIVE_2': self.effectiveTextStyle['CONTENT_POSITIVE_2'], 'NEGATIVE_2': self.effectiveTextStyle['CONTENT_NEGATIVE_2'], 'NEUTRAL_2':  self.effectiveTextStyle['CONTENT_NEUTRAL_2'],
                                                                                                                                              'DEFAULT':    self.effectiveTextStyle['CONTENT_DEFAULT']},
                                                                                                                       xPos = drawBox[0], yPos = drawBox[1], width = drawBox[2], height = 200, showElementBox = False, anchor = 'W')

                        #Setup Positional Highlight
                        self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED']  = pyglet.shapes.Rectangle(x = 0, y = 0, width = 0, height = drawBox[3]*self.scaler, color = self.posHighlightColor_hovered,  batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP'])
                        self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'] = pyglet.shapes.Rectangle(x = 0, y = 0, width = 0, height = drawBox[3]*self.scaler, color = self.posHighlightColor_selected, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP'])
                        self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible  = False
                        self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].visible = False
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDELINE'] = pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 3, color = self.guideColor, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP'])
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP'], text = "", defaultTextStyle = self.effectiveTextStyle['GUIDECONTENT'],
                                                                                                                                xPos = 0, yPos = 0, width = drawBox[2], height = _GD_DISPLAYBOX_GUIDE_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'E')
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDELINE'].visible = False
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'].hide()

                        #Setup Grids
                        self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'] = list()
                        self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'] = list()
                        self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'] = list()
                        self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'] = list()
                        for i in range (self.nMaxHorizontalGridLines['KLINESPRICE']):
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP']))
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'][-1].visible = False
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, _GD_DISPLAYBOX_GOFFSET*self.scaler, 0, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP']))
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                                   xPos = _GD_DISPLAYBOX_GOFFSET*2, yPos = 0, width = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'W'))
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'][-1].visible = False
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'][-1].hide()
                        for i in range (self.nMaxVerticalGridLines):
                            self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, 0, 0, drawBox[3]*self.scaler, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP']))
                            self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][-1].visible = False

                    #---SIVIEWER
                    elif (displayBoxName[:8] == 'SIVIEWER'):
                        siIndex = int(displayBoxName[8:])
                        dBoxName          = 'SIVIEWER{:d}'.format(siIndex)
                        dBoxName_MAINGRID = 'MAINGRID_SIVIEWER{:d}'.format(siIndex)
                        if (self.displayBox[displayBoxName] == None):
                            displayBox          = (0, 0, 10, 10)
                            displayBox_MAINGRID = (0, 0, 10, 10)
                            drawBox             = (0, 0, 10, 10)
                            drawBox_MAINGRID    = (0, 0, 10, 10)
                            displayed = False
                        else:
                            displayBox          = self.displayBox[dBoxName]
                            displayBox_MAINGRID = self.displayBox[dBoxName_MAINGRID]
                            drawBox             = self.displayBox_graphics[dBoxName]['DRAWBOX']
                            drawBox_MAINGRID    = self.displayBox_graphics[dBoxName_MAINGRID]['DRAWBOX']
                            displayed = True

                        #Generate Graphic Sprites and Hitboxes
                        self.hitBox[dBoxName] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(drawBox[0], drawBox[1], drawBox[2], drawBox[3])
                        self.images[dBoxName] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                        self.frameSprites[dBoxName] = pyglet.sprite.Sprite(x = displayBox[0]*self.scaler, y = displayBox[1]*self.scaler, img = self.images[dBoxName][0], batch = self.batch, group = self.group_0)
                        self.hitBox[dBoxName_MAINGRID] = ATM_Zeta_GUI_HitBoxes.hitBox_Rectangular(drawBox_MAINGRID[0], drawBox_MAINGRID[1], drawBox_MAINGRID[2], drawBox_MAINGRID[3])
                        self.images[dBoxName_MAINGRID] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox_MAINGRID[2]*self.scaler, displayBox_MAINGRID[3]*self.scaler)
                        self.frameSprites[dBoxName_MAINGRID] = pyglet.sprite.Sprite(x = displayBox_MAINGRID[0]*self.scaler, y = displayBox_MAINGRID[1]*self.scaler, img = self.images[dBoxName_MAINGRID][0], batch = self.batch, group = self.group_0)

                        #Setup CamGroup and DisplaySpaceManager
                        self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'] = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window = self.window, order = self.groupOrder+1, viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = drawBox[2]*self.scaler)
                        self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP']   = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window = self.window, order = self.groupOrder+1, viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_y0 = 0, projection_y1 = drawBox[3]*self.scaler)
                        self.displayBox_graphics[dBoxName]['RCLCG']                   = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, fsdResolution_y = 2)
                        self.displayBox_graphics[dBoxName]['RCLCG_XFIXED']            = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = 100, fsdResolution_y = 5)
                        self.displayBox_graphics[dBoxName]['RCLCG_YFIXED']            = ATM_Zeta_GUI_AdvancedPygletGroups.resolutionControlledLayeredCameraGroup(window = self.window, batch = self.batch, viewport_x = drawBox[0]*self.scaler, viewport_y = drawBox[1]*self.scaler, viewport_width = drawBox[2]*self.scaler, viewport_height = drawBox[3]*self.scaler, order = self.groupOrder+2, parentCameraGroup = self.parentCameraGroup, projection_y0 = 0, projection_y1 = 100)
                        self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'] = ATM_Zeta_GUI_AdvancedPygletGroups.cameraGroup(window = self.window, order = self.groupOrder+1, viewport_x=drawBox_MAINGRID[0]*self.scaler, viewport_y=drawBox_MAINGRID[1]*self.scaler, viewport_width=drawBox_MAINGRID[2]*self.scaler, viewport_height=drawBox_MAINGRID[3]*self.scaler, parentCameraGroup = self.parentCameraGroup, projection_x0 = 0, projection_x1 = drawBox_MAINGRID[2]*self.scaler)
                            
                        #Description Texts
                        self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.group_hd0, text = "", 
                                                                                                                        defaultTextStyle    = self.effectiveTextStyle['CONTENT_DEFAULT'],
                                                                                                                        auxillaryTextStyles = {'POSITIVE_1': self.effectiveTextStyle['CONTENT_POSITIVE_1'], 'NEGATIVE_1': self.effectiveTextStyle['CONTENT_NEGATIVE_1'], 'NEUTRAL_1':  self.effectiveTextStyle['CONTENT_NEUTRAL_1'],
                                                                                                                                               'POSITIVE_2': self.effectiveTextStyle['CONTENT_POSITIVE_2'], 'NEGATIVE_2': self.effectiveTextStyle['CONTENT_NEGATIVE_2'], 'NEUTRAL_2':  self.effectiveTextStyle['CONTENT_NEUTRAL_2'],
                                                                                                                                               'DEFAULT':    self.effectiveTextStyle['CONTENT_DEFAULT']},
                                                                                                                        xPos = drawBox[0], yPos = drawBox[1]+drawBox[3]-200, width = drawBox[2], height = 200, showElementBox = False, anchor = 'W')

                        #Setup Positional Highlight
                        self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_HOVERED']  = pyglet.shapes.Rectangle(x = 0, y = 0, width = 0, height = drawBox[3]*self.scaler, color = self.posHighlightColor_hovered,  batch = self.batch, group = self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'])
                        self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_SELECTED'] = pyglet.shapes.Rectangle(x = 0, y = 0, width = 0, height = drawBox[3]*self.scaler, color = self.posHighlightColor_selected, batch = self.batch, group = self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'])
                        self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_HOVERED'].visible  = False
                        self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_SELECTED'].visible = False
                        self.displayBox_graphics[dBoxName]['HORIZONTALGUIDELINE'] = pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 3, color = self.guideColor, batch = self.batch, group = self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'])
                        self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'] = ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'], text = "", defaultTextStyle = self.effectiveTextStyle['GUIDECONTENT'],
                                                                                                                           xPos = 0, yPos = 0, width = drawBox[2], height = _GD_DISPLAYBOX_GUIDE_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'E')
                        self.displayBox_graphics[dBoxName]['HORIZONTALGUIDELINE'].visible = False
                        self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'].hide()

                        #Setup Grids
                        self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'] = list()
                        self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES'] = list()
                        self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'] = list()
                        self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'] = list()
                        for i in range (self.nMaxHorizontalGridLines[dBoxName]):
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP']))
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'][-1].visible = False
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, _GD_DISPLAYBOX_GOFFSET*self.scaler, 0, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP']))
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                              xPos = _GD_DISPLAYBOX_GOFFSET*2, yPos = 0, width = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'W'))
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'][-1].visible = False
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'][-1].hide()
                        for i in range (self.nMaxVerticalGridLines):
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, 0, 0, drawBox[3]*self.scaler, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP']))
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES'][-1].visible = False

                        #If this SIViewer is activated, add it to the visibleSIViewers set. If not, hide it
                        if (displayed == True): self.displayBox_graphics_visibleSIViewers.add(dBoxName)
                        else:                   self.__hideDisplayBox(dBoxName)

                    #---AUXILLARYBAR
                    elif (displayBoxName == 'AUXILLARYBAR'):
                        if (self.displayBox['AUXILLARYBAR'] == None):
                            displayBox = (0, 0, 10, 10)
                            displayed = False
                        else:
                            displayBox = self.displayBox['AUXILLARYBAR']
                            displayed = True

                        #Generate Graphic Sprites and Hitboxes
                        self.images['AUXILLARYBAR'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                        self.frameSprites['AUXILLARYBAR'] = pyglet.sprite.Sprite(x = displayBox[0]*self.scaler, y = displayBox[1]*self.scaler, img = self.images['AUXILLARYBAR'][0], batch = self.batch, group = self.group_0)

                        #If this displayBox is not activated, hide it
                        if (displayed == False): self.__hideDisplayBox('AUXILLARYBAR')
            else:
                for displayBoxName in self.displayBox:
                    if (displayBoxName in self.displayBox_VisibleBoxes):
                        self.mouse_DragDX[displayBoxName] = 0; self.mouse_DragDY[displayBoxName] = 0; self.mouse_ScrollDX[displayBoxName] = 0; self.mouse_ScrollDY[displayBoxName] = 0
                        #SETTINGSBUTTONFRAME
                        if (displayBoxName == 'SETTINGSBUTTONFRAME'):
                            displayBox = self.displayBox['SETTINGSBUTTONFRAME']
                            self.hitBox['SETTINGSBUTTONFRAME'].reposition(xPos = displayBox[0], yPos = displayBox[1])
                            self.frameSprites['SETTINGSBUTTONFRAME'].position = (displayBox[0]*self.scaler, displayBox[1]*self.scaler, self.frameSprites['SETTINGSBUTTONFRAME'].z)
                            self.frameSprites['SETTINGSBUTTONFRAME_ICON'].position = ((displayBox[0]+displayBox[2]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].width/2,
                                                                                      (displayBox[1]+displayBox[3]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].height/2,
                                                                                      self.frameSprites['SETTINGSBUTTONFRAME'].z)
                        #KLINESPRICE
                        elif (displayBoxName == 'KLINESPRICE'):
                            displayBox          = self.displayBox['KLINESPRICE']
                            displayBox_MAINGRID = self.displayBox['MAINGRID_KLINESPRICE']
                            drawBox             = self.displayBox_graphics['KLINESPRICE']['DRAWBOX']
                            drawBox_MAINGRID    = self.displayBox_graphics['MAINGRID_KLINESPRICE']['DRAWBOX']

                            #Reposition & Resize Graphics and Hitboxes
                            self.hitBox['KLINESPRICE'].reposition(xPos = drawBox[0], yPos = drawBox[1])
                            self.hitBox['KLINESPRICE'].resize(width = drawBox[2], height = drawBox[3])
                            self.images['KLINESPRICE'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                            self.frameSprites['KLINESPRICE'].position = (displayBox[0]*self.scaler, displayBox[1]*self.scaler, self.frameSprites['KLINESPRICE'].z)
                            self.frameSprites['KLINESPRICE'].image = self.images['KLINESPRICE'][0]
                            self.hitBox['MAINGRID_KLINESPRICE'].reposition(xPos = drawBox_MAINGRID[0], yPos = drawBox_MAINGRID[1])
                            self.hitBox['MAINGRID_KLINESPRICE'].resize(width = drawBox_MAINGRID[2], height = drawBox_MAINGRID[3])
                            self.images['MAINGRID_KLINESPRICE'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox_MAINGRID[2]*self.scaler, displayBox_MAINGRID[3]*self.scaler)
                            self.frameSprites['MAINGRID_KLINESPRICE'].position = (displayBox_MAINGRID[0]*self.scaler, displayBox_MAINGRID[1]*self.scaler, self.frameSprites['MAINGRID_KLINESPRICE'].z)
                            self.frameSprites['MAINGRID_KLINESPRICE'].image = self.images['MAINGRID_KLINESPRICE'][0]

                            #Reposition & Resize CamGroups and RCLCGs
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_x0 = 0, projection_x1 = drawBox[2]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP'].updateProjection(projection_y0 = 0, projection_y1 = drawBox[3]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['RCLCG'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox_MAINGRID[0]*self.scaler, viewport_y=drawBox_MAINGRID[1]*self.scaler, viewport_width=drawBox_MAINGRID[2]*self.scaler, viewport_height=drawBox_MAINGRID[3]*self.scaler)
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_x0 = 0, projection_x1 = drawBox_MAINGRID[2]*self.scaler)

                            #Reposition & Resize Auxillary Objects
                            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].moveTo(x = drawBox[0], y = drawBox[1]+drawBox[3]-200)
                            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].changeSize(width = drawBox[2])
                            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].moveTo(x = drawBox[0], y = drawBox[1]+drawBox[3]-400)
                            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].changeSize(width = drawBox[2])
                            self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].moveTo(x = drawBox[0], y = drawBox[1])
                            self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].changeSize(width = drawBox[2])
                            self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].height  = drawBox[3]*self.scaler
                            self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].height = drawBox[3]*self.scaler
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDELINE'].x2 = drawBox[2]*self.scaler
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'].changeSize(width = drawBox[2])

                            #Setup Grids
                            for horizontalGridText in self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS']: horizontalGridText.delete()
                            self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'] = list()
                            self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'] = list()
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'] = list()
                            self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'] = list()
                            for i in range (self.nMaxHorizontalGridLines['KLINESPRICE']):
                                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_CAMGROUP']))
                                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES'][-1].visible = False
                                self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, _GD_DISPLAYBOX_GOFFSET*self.scaler, 0, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP']))
                                self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                                       xPos = _GD_DISPLAYBOX_GOFFSET*2, yPos = 0, width = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'W'))
                                self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES'][-1].visible = False
                                self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS'][-1].hide()
                                
                            for i in range (self.nMaxVerticalGridLines):
                                self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, 0, 0, drawBox[3]*self.scaler, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP']))
                                self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][-1].visible = False

                        #MAINGRID_TEMPORAL
                        elif (displayBoxName == 'MAINGRID_TEMPORAL'):
                            displayBox = self.displayBox['MAINGRID_TEMPORAL']
                            drawBox    = self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX']

                            #Reposition & Resize Graphics and Hitboxes
                            self.hitBox['MAINGRID_TEMPORAL'].reposition(xPos = drawBox[0], yPos = drawBox[1])
                            self.hitBox['MAINGRID_TEMPORAL'].resize(width = drawBox[2], height = drawBox[3])
                            self.images['MAINGRID_TEMPORAL'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                            self.frameSprites['MAINGRID_TEMPORAL'].position = (displayBox[0]*self.scaler, displayBox[1]*self.scaler, self.frameSprites['MAINGRID_TEMPORAL'].z)
                            self.frameSprites['MAINGRID_TEMPORAL'].image = self.images['MAINGRID_TEMPORAL'][0]

                            #Reposition & Resize CamGroups and RCLCGs
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)

                            #Setup Grids
                            for verticalGridText in self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS']: verticalGridText.delete()
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'] = list()
                            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'] = list()
                            for i in range (self.nMaxVerticalGridLines):
                                self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, (_GD_DISPLAYBOX_GRID_VERTICALTEXTHEIGHT+_GD_DISPLAYBOX_GOFFSET)*self.scaler, 0, drawBox[3]*self.scaler, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP']))
                                self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                                  xPos = 0, yPos = 0, width = _GD_DISPLAYBOX_GRID_VERTICALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_VERTICALTEXTHEIGHT, showElementBox = False, anchor = 'CENTER'))
                                self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][-1].visible = False
                                self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][-1].hide()
                                
                        #SIVIEWER
                        elif (displayBoxName[:8] == 'SIVIEWER'):
                            siIndex = int(displayBoxName[8:])
                            dBoxName          = 'SIVIEWER{:d}'.format(siIndex)
                            dBoxName_MAINGRID = 'MAINGRID_SIVIEWER{:d}'.format(siIndex)
                            displayBox          = self.displayBox[dBoxName]
                            displayBox_MAINGRID = self.displayBox[dBoxName_MAINGRID]
                            drawBox          = self.displayBox_graphics[dBoxName]['DRAWBOX']
                            drawBox_MAINGRID = self.displayBox_graphics[dBoxName_MAINGRID]['DRAWBOX']
                                
                            #Reposition & Resize Graphics and Hitboxes
                            self.hitBox[dBoxName].reposition(xPos = drawBox[0], yPos = drawBox[1])
                            self.hitBox[dBoxName].resize(width = drawBox[2], height = drawBox[3])
                            self.hitBox[dBoxName].activate()
                            self.images[dBoxName] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox[2]*self.scaler, displayBox[3]*self.scaler)
                            self.frameSprites[dBoxName].position = (displayBox[0]*self.scaler, displayBox[1]*self.scaler, self.frameSprites[dBoxName].z)
                            self.frameSprites[dBoxName].image = self.images[dBoxName][0]
                            self.frameSprites[dBoxName].visible = True
                            self.hitBox[dBoxName_MAINGRID].reposition(xPos = drawBox_MAINGRID[0], yPos = drawBox_MAINGRID[1])
                            self.hitBox[dBoxName_MAINGRID].resize(width = drawBox_MAINGRID[2], height = drawBox_MAINGRID[3])
                            self.hitBox[dBoxName_MAINGRID].activate()
                            self.images[dBoxName_MAINGRID] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", displayBox_MAINGRID[2]*self.scaler, displayBox_MAINGRID[3]*self.scaler)
                            self.frameSprites[dBoxName_MAINGRID].position = (displayBox_MAINGRID[0]*self.scaler, displayBox_MAINGRID[1]*self.scaler, self.frameSprites[dBoxName_MAINGRID].z)
                            self.frameSprites[dBoxName_MAINGRID].image = self.images[dBoxName_MAINGRID][0]
                            self.frameSprites[dBoxName_MAINGRID].visible = True
                                
                            #Reposition & Resize CamGroups and RCLCGs
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_x0 = 0, projection_x1 = drawBox[2]*self.scaler)
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'].updateProjection(projection_y0 = 0, projection_y1 = drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'].show()
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'].show()
                            self.displayBox_graphics[dBoxName]['RCLCG'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['RCLCG_XFIXED'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['RCLCG_YFIXED'].updateViewport(viewport_x=drawBox[0]*self.scaler, viewport_y=drawBox[1]*self.scaler, viewport_width=drawBox[2]*self.scaler, viewport_height=drawBox[3]*self.scaler)
                            self.displayBox_graphics[dBoxName]['RCLCG'].show()
                            self.displayBox_graphics[dBoxName]['RCLCG_XFIXED'].show()
                            self.displayBox_graphics[dBoxName]['RCLCG_YFIXED'].show()
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'].updateViewport(viewport_x=drawBox_MAINGRID[0]*self.scaler, viewport_y=drawBox_MAINGRID[1]*self.scaler, viewport_width=drawBox_MAINGRID[2]*self.scaler, viewport_height=drawBox_MAINGRID[3]*self.scaler)
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_x0 = 0, projection_x1 = drawBox_MAINGRID[2]*self.scaler)
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'].show()
                                
                            #Reposition & Resize Auxillary Objects
                            self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].moveTo(x = drawBox[0], y = drawBox[1]+drawBox[3]-200)
                            self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].changeSize(width = drawBox[2], height = 200)
                            self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_HOVERED'].height  = drawBox[3]*self.scaler
                            self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_SELECTED'].height = drawBox[3]*self.scaler
                            self.displayBox_graphics[dBoxName]['HORIZONTALGUIDELINE'].x2 = drawBox[2]*self.scaler
                            self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'].changeSize(width = drawBox[2])

                            #Setup Grids
                            for horizontalGridText in self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS']: horizontalGridText.delete()
                            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'] = list()
                            self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES']   = list()
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'] = list()
                            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'] = list()
                            for i in range (self.nMaxHorizontalGridLines[dBoxName]):
                                self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, drawBox[2]*self.scaler, 0, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP']))
                                self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES'][-1].visible = False
                                self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'].append(pyglet.shapes.Line(0, 0, _GD_DISPLAYBOX_GOFFSET*self.scaler, 0, width = 3, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP']))
                                self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'].append(ATM_Zeta_GUI_TextControl.textObject_SL(scaler = self.scaler, batch = self.batch, group = self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'], text = "-", defaultTextStyle = self.effectiveTextStyle['GRID'],
                                                                                                                                                  xPos = _GD_DISPLAYBOX_GOFFSET*2, yPos = 0, width = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTWIDTH, height = _GD_DISPLAYBOX_GRID_HORIZONTALTEXTHEIGHT, showElementBox = False, anchor = 'W'))
                                self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES'][-1].visible = False
                                self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS'][-1].hide()
                            for i in range (self.nMaxVerticalGridLines):
                                self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES'].append(pyglet.shapes.Line(0, 0, 0, drawBox[3]*self.scaler, width = 1, color = self.gridColor, batch = self.batch, group = self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP']))
                                self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES'][-1].visible = False

                            #Add to the visibleSIViewers set (If already exists, simply won't do anything)
                            self.displayBox_graphics_visibleSIViewers.add(displayBoxName)

                        #AUXILLARYBAR
                        elif (displayBoxName == 'AUXILLARYBAR'):
                            displayBox = self.displayBox['AUXILLARYBAR']

                            #Reposition & Resize Graphics
                            self.images['AUXILLARYBAR'] = self.imageManager.getImageByCode("chartDrawer_typeA_"+self.style+"_displayBoxFrame", self.displayBox['AUXILLARYBAR'][2]*self.scaler, self.displayBox['AUXILLARYBAR'][3]*self.scaler)
                            self.frameSprites['AUXILLARYBAR'].position = (self.displayBox['AUXILLARYBAR'][0]*self.scaler, self.displayBox['AUXILLARYBAR'][1]*self.scaler, self.frameSprites['AUXILLARYBAR'].z)
                            self.frameSprites['AUXILLARYBAR'].image = self.images['AUXILLARYBAR'][0]
                            self.frameSprites['AUXILLARYBAR'].visible = True

                    else: self.__hideDisplayBox(displayBoxName)

        #[4]: Size and Position Klines Loading Gauge Bar and Text
        if (True):
            self.klinesLoadingGaugeBar.resize(width      = round(self.width*0.9), height = _GD_KLINESLOADINGGAUGEBAR_HEIGHT)
            self.klinesLoadingTextBox_perc.resize(width  = round(self.width*0.9), height = _GD_KLINESLOADINGGAUGEBAR_HEIGHT)
            self.klinesLoadingTextBox.resize(width       = round(self.width*0.9), height = 200)
            self.klinesLoadingGaugeBar.moveTo(x     = round(self.xPos+self.width*0.05), y = round(self.yPos+self.height/2-_GD_KLINESLOADINGGAUGEBAR_HEIGHT))
            self.klinesLoadingTextBox_perc.moveTo(x = round(self.xPos+self.width*0.05), y = round(self.yPos+self.height/2-_GD_KLINESLOADINGGAUGEBAR_HEIGHT))
            self.klinesLoadingTextBox.moveTo(x      = round(self.xPos+self.width*0.05), y = round(self.yPos+self.height/2))

    def __hideDisplayBox(self, displayBoxName):
        #Deactivate and hide AUXILLARYBAR
        if (displayBoxName == 'AUXILLARYBAR'): 
            #Hitbox & Frame Graphics
            self.frameSprites['AUXILLARYBAR'].visible = False

        #Deactivate and hide SIVIEWER[X]
        elif ((displayBoxName[:8] == 'SIVIEWER') and (displayBoxName in self.displayBox_graphics_visibleSIViewers)):
            siIndex = int(displayBoxName[8:])
            dBoxName          = 'SIVIEWER{:d}'.format(siIndex)
            dBoxName_MAINGRID = 'MAINGRID_SIVIEWER{:d}'.format(siIndex)
            #Hitbox & Frame Graphics
            self.hitBox[displayBoxName].deactivate()
            self.frameSprites[displayBoxName].visible = False
            #CamGroups and RCLCGs
            self.displayBox_graphics[dBoxName]['HORIZONTALGRID_CAMGROUP'].hide()
            self.displayBox_graphics[dBoxName]['VERTICALGRID_CAMGROUP'].hide()
            self.displayBox_graphics[dBoxName]['RCLCG'].hide()
            self.displayBox_graphics[dBoxName]['RCLCG_XFIXED'].hide()
            self.displayBox_graphics[dBoxName]['RCLCG_YFIXED'].hide()
            self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_CAMGROUP'].hide()
            #Descriptors & Guides
            self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].hide()
            self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_HOVERED'].visible = False
            self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_SELECTED'].visible = False
            self.displayBox_graphics[dBoxName]['HORIZONTALGUIDELINE'].visible = False
            self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'].hide()
            #Grids
            for horizontalGridText in self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS']: horizontalGridText.hide()
            self.displayBox_graphics_visibleSIViewers.remove(displayBoxName)
            
    def __initializeSIViewer(self, siViewerNumber):
        #SIViewerCode
        siViewerCode = 'SIVIEWER{:d}'.format(siViewerNumber)
        #Graphcis Clearing
        self.displayBox_graphics[siViewerCode]['RCLCG'].clearAll()
        self.displayBox_graphics[siViewerCode]['RCLCG_XFIXED'].clearAll()
        self.displayBox_graphics[siViewerCode]['RCLCG_YFIXED'].clearAll()
        #Vertical Value Initialization
        self.verticalValue_min[siViewerCode] = 0
        self.verticalValue_max[siViewerCode] = 1
        self.verticalValue_loaded[siViewerCode] = False
    #DisplayBox Control END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #General Object Processing & User Interaction Control -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def process(self, t_elapsed_ns):
        #Mouse Event Interpretation
        mei_beg = time.perf_counter_ns()
        if (_TIMEINTERVAL_MOUSEINTERPRETATION_NS <= time.perf_counter_ns() - self.mouse_Event_lastInterpreted_ns):
            #[1]: Mouse Drag Handling
            if (self.mouse_Dragged == True):
                for section in self.mouse_DragDX: #Iterating over 'self.mouseDragDX' or 'self.mouseDragDY' does not matter
                    #Drag Delta
                    drag_dx = self.mouse_DragDX[section]; drag_dy = self.mouse_DragDY[section]
                    #Drag Responses
                    if ((drag_dx != 0) or (drag_dy != 0)):
                        if   (section == 'KLINESPRICE'):            self.__editVPosition(displayBoxName = 'KLINESPRICE', delta_drag = drag_dy); self.__editHPosition(delta_drag = drag_dx)
                        elif (section == 'MAINGRID_KLINESPRICE'):   self.__editVMagFactor(displayBoxName = 'KLINESPRICE', delta_drag = drag_dy)
                        elif (section == 'MAINGRID_TEMPORAL'):      self.__editHMagFactor(delta_drag = drag_dx)
                        elif (section[:8] == 'SIVIEWER'):           self.__editHPosition(delta_drag = drag_dx)
                        elif (section[:17] == 'MAINGRID_SIVIEWER'):
                            siViewerNumber = int(section[17:])
                            siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber)]
                            if (siAlloc == 'VOL'): self.__editVMagFactor(displayBoxName = section.split("_")[1], delta_drag = drag_dy, anchor = 'BOTTOM')
                            else:                  self.__editVMagFactor(displayBoxName = section.split("_")[1], delta_drag = drag_dy)
                        #Delta Reset
                        self.mouse_DragDX[section] = 0; self.mouse_DragDY[section] = 0
                #Post-Interpretation
                self.mouseDragged = False

            #[2]: Mouse Scroll Handling
            if (self.mouse_Scrolled == True):
                for section in self.mouse_ScrollDX: #Iterating over 'self.mouseScrollDX' or 'self.mouseScrollDY' does not matter
                    #Scroll Delta
                    scroll_dx = self.mouse_ScrollDX[section]; scroll_dy = self.mouse_ScrollDY[section]
                    #Scroll Responses
                    if ((scroll_dx != 0) or (scroll_dy != 0)):
                        if (section == 'SETTINGSFRAME'):
                            self.internalGUIOs_SETTINGS_viewRange[0] += scroll_dy*5
                            self.internalGUIOs_SETTINGS_viewRange[1] += scroll_dy*5
                            self.__onSettingsViewRangeUpdate(byScrollBar=False)
                        elif (section == 'KLINESPRICE'):            self.__editHMagFactor(delta_scroll = scroll_dy); self.__updatePosHighlight(self.mouse_Event_lastRead['x'], self.mouse_Event_lastRead['y'], self.mouse_lastHoveredSection, updateType = 0)
                        elif (section == 'MAINGRID_KLINESPRICE'):   pass
                        elif (section == 'MAINGRID_TEMPORAL'):      pass
                        elif (section[:8] == 'SIVIEWER'):           self.__editHMagFactor(delta_scroll = scroll_dy); self.__updatePosHighlight(self.mouse_Event_lastRead['x'], self.mouse_Event_lastRead['y'], self.mouse_lastHoveredSection, updateType = 0)
                        elif (section[:17] == 'MAINGRID_SIVIEWER'): pass
                        #Delta Reset
                        self.mouse_ScrollDX[section] = 0; self.mouse_ScrollDY[section] = 0
                self.mouse_Scrolled = False

            #[3]: Period Counter Reset
            self.mouse_Event_lastInterpreted_ns = time.perf_counter_ns()

        if (self.posHighlight_updatedPositions != None) and (_TIMEINTERVAL_POSHIGHLIGHTUPDATE <= mei_beg - self.posHighlight_lastUpdated_ns): self.__onPosHighlightUpdate()

        #Klines Update
        if ((self.klines_fetchComplete == True) and (self.mouse_Event_currentlyPressed == False) and (_TIMEINTERVAL_POSTSCROLLWAITTIME <= mei_beg - self.mouse_lastScrolled_ns)):
            elapsedSoFar = time.perf_counter_ns() - mei_beg
            #If there exist klines to process
            if (0 < len(self.klines_toProcess)):
                if (elapsedSoFar < _TIMELIMIT_KLINESPROCESS_NS):
                    klines_toProcess_list = list(self.klines_toProcess.keys()); klines_toProcess_list.sort()
                    while (0 < len(klines_toProcess_list)):
                        self.__processKline(klines_toProcess_list.pop(0))
                        if ((_TIMELIMIT_KLINESPROCESS_NS < time.perf_counter_ns()-mei_beg) or (self.mouse_Event_currentlyPressed == True) or (self.mouse_Scrolled == True) or (self.posHighlight_updatedPositions != None)): break
            #If there exist no klines to process, draw any drawable klines
            elif (0 < len(self.klines_drawQueue)):
                if (elapsedSoFar < _TIMELIMIT_KLINESDRAW_NS):
                    #Determine timestamps to draw
                    if (len(self.klines_drawQueue) < len(self.horizontalViewRange_timestampsInViewRange)): drawQueueTimestamps = [ts for ts in self.klines_drawQueue if ts in self.horizontalViewRange_timestampsInViewRange]
                    else:                                                                                  drawQueueTimestamps = [ts for ts in self.horizontalViewRange_timestampsInViewRange if ts in self.klines_drawQueue]
                    if (len(drawQueueTimestamps) == 0):
                        if (len(self.klines_drawQueue) < len(self.horizontalViewRange_timestampsInBufferZone)): drawQueueTimestamps = [ts for ts in self.klines_drawQueue if ts in self.horizontalViewRange_timestampsInBufferZone]
                        else:                                                                                   drawQueueTimestamps = [ts for ts in self.horizontalViewRange_timestampsInBufferZone if ts in self.klines_drawQueue]
                    #Draw
                    while (0 < len(drawQueueTimestamps)):
                        self.__processKlineDrawQueue(drawQueueTimestamps.pop(0))
                        if ((_TIMELIMIT_KLINESDRAW_NS < time.perf_counter_ns()-mei_beg) or (self.mouse_Event_currentlyPressed == True) or (self.mouse_Scrolled == True) or (self.posHighlight_updatedPositions != None)): break
            #If there exist no kliens to draw, remove any out-of-sight klines
            elif (0 < len(self.klines_drawRemovalQueue)):
                if (elapsedSoFar < _TIMELIMIT_KLINESDRAWREMOVAL_NS):
                    while (0 < len(self.klines_drawRemovalQueue)):
                        self.__processKlineDrawRemovalQueue(self.klines_drawRemovalQueue.pop())
                        if ((_TIMELIMIT_KLINESDRAWREMOVAL_NS < time.perf_counter_ns()-mei_beg) or (self.mouse_Event_currentlyPressed == True) or (self.mouse_Scrolled == True) or (self.posHighlight_updatedPositions != None)): break

        #Subpage Processing
        self.settingsSubPages[self.settingsSubPage_Current].process(t_elapsed_ns)
        
    def handleMouseEvent(self, event):
        if (self.klines_fetching == False):
            if (event['eType'] == "MOVED"):
                #Find hovering section
                hoveredSection = None
                if (self.settingsSubPage_Opened == True) and (self.settingsSubPages[self.settingsSubPage_Current].isTouched(event['x'], event['y']) == True): hoveredSection = 'SETTINGSSUBPAGE'
                else:
                    for displayBoxName in self.hitBox:
                        if (self.hitBox[displayBoxName].isTouched(event['x'], event['y']) == True): hoveredSection = displayBoxName; break
                #Hovering Section Has Not Changed
                if (hoveredSection == self.mouse_lastHoveredSection):
                    if (hoveredSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                #Hovering Section Changed
                else:
                    #[1]: New Hovered Section is 'SETTINGSBUTTONFRAME'
                    if (hoveredSection == 'SETTINGSBUTTONFRAME'):
                        self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_HOVERED'][0]
                        self.settingsButtonStatus = 'HOVERED'
                    #  or New Hovered Section is 'SETTINGSSUBPAGE'
                    elif (hoveredSection == 'SETTINGSSUBPAGE'):
                        self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent({'eType': "HOVERENTERED", 'x': event['x'], 'y': event['y']})
                    #  or New Hovered Section is None
                    elif (hoveredSection == None):
                        self.__updatePosHighlight(event['x'], event['y'], hoveredSection, updateType = 1)
                    #[2]: Last Hovered Section was 'SETTINGSBUTTONFRAME'
                    if (self.mouse_lastHoveredSection == 'SETTINGSBUTTONFRAME'):
                        self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_DEFAULT'][0]
                        self.settingsButtonStatus = 'DEFAULT'
                    #  or Last Hovered Section was 'SETTINGSSUBPAGE'
                    elif (self.mouse_lastHoveredSection == 'SETTINGSSUBPAGE'):
                        self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent({'eType': "HOVERESCAPED", 'x': event['x'], 'y': event['y']})
                #POSHIGHLIGHT Control
                if ((hoveredSection != None) and ((hoveredSection == 'KLINESPRICE') or (hoveredSection[:8] == 'SIVIEWER'))): self.__updatePosHighlight(event['x'], event['y'], hoveredSection, updateType = 0)
                #Recording
                self.mouse_lastHoveredSection = hoveredSection
        
            elif (event['eType'] == "PRESSED"):
                if (self.mouse_lastHoveredSection != self.mouse_lastSelectedSection):
                    if (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent({'eType': "SELECTIONESCAPED", 'x': event['x'], 'y': event['y'], 'button': event['button'], 'modifiers': event['modifiers']})
                if (self.mouse_lastHoveredSection == 'SETTINGSBUTTONFRAME'):
                    self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_PRESSED'][0]
                    self.settingsButtonStatus = 'PRESSED'
                elif (self.mouse_lastHoveredSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                #POSHIGHLIGHT Control
                if ((self.mouse_lastHoveredSection != None) and ((self.mouse_lastHoveredSection == 'KLINESPRICE') or (self.mouse_lastHoveredSection[:8] == 'SIVIEWER'))): self.__updatePosHighlight(event['x'], event['y'], self.mouse_lastHoveredSection, updateType = 1)
                #Recording
                self.mouse_lastSelectedSection = self.mouse_lastHoveredSection
                self.mouse_Event_lastPressed = event
                self.mouse_Event_currentlyPressed = True
        
            elif (event['eType'] == "RELEASED"):
                if (self.mouse_lastSelectedSection == self.mouse_lastHoveredSection):
                    if (self.mouse_lastHoveredSection == 'SETTINGSBUTTONFRAME'):
                        self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_HOVERED'][0]
                        self.settingsButtonStatus = 'HOVERED'
                        self.__onSettingsButtonClick()
                    elif (self.mouse_lastHoveredSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                else:
                    if (self.mouse_lastSelectedSection == 'SETTINGSBUTTONFRAME'):
                        self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_DEFAULT'][0]
                        self.settingsButtonStatus = 'DEFAULT'
                    elif (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent({'eType': "HOVERESCAPED", 'x': event['x'], 'y': event['y']})
                    if (self.mouse_lastHoveredSection == 'SETTINGSBUTTONFRAME'):
                        self.frameSprites['SETTINGSBUTTONFRAME'].image = self.images['SETTINGSBUTTONFRAME_HOVERED'][0]
                        self.settingsButtonStatus = 'HOVERED'
                    elif (self.mouse_lastHoveredSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent({'eType': "HOVEREENTERED", 'x': event['x'], 'y': event['y']})
                #POSHIGHLIGHT Control
                if ((self.mouse_lastHoveredSection != None) and ((self.mouse_lastHoveredSection == 'KLINESPRICE') or (self.mouse_lastHoveredSection[:8] == 'SIVIEWER'))): 
                    self.__updatePosHighlight(event['x'], event['y'], self.mouse_lastHoveredSection, updateType = 0)
                    if ((self.mouse_Event_lastPressed != None) and (self.mouse_Event_lastPressed['x'] == event['x']) and (self.mouse_Event_lastPressed['y'] == event['y'])):
                        #LEFT MOUSE BUTTON -> POSSELECTION Update
                        if (event['button'] == 1): self.__updatePosSelection(updateType = 0)   
                        #RIGHT MOUSE BUTTON -> moveToExtremaCenter
                        elif (event['button'] == 4):
                            if (self.mouse_lastHoveredSection == 'KLINESPRICE'): self.__editVVR_toExtremaCenter(displayBoxName = self.mouse_lastHoveredSection)
                            else:
                                siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(int(self.mouse_lastHoveredSection[8:]))]
                                if   (siAlloc == 'VOL'):   self.__editVVR_toExtremaCenter(displayBoxName = self.mouse_lastHoveredSection, extension_b = 0.0, extension_t = 0.2)
                                elif (siAlloc == 'MMACD'): self.__editVVR_toExtremaCenter(displayBoxName = self.mouse_lastHoveredSection, extension_b = 0.1, extension_t = 0.1)
                self.mouse_Event_currentlyPressed = False

            elif (event['eType'] == "DRAGGED"):
                #Find hovering section
                hoveredSection = None
                if (self.settingsSubPage_Opened == True) and (self.settingsSubPages[self.settingsSubPage_Current].isTouched(event['x'], event['y']) == True): hoveredSection = 'SETTINGSSUBPAGE'
                else:
                    for displayBoxName in self.hitBox:
                        if (self.hitBox[displayBoxName].isTouched(event['x'], event['y']) == True): hoveredSection = displayBoxName; break
                #Drag Source
                if (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                elif (self.mouse_lastSelectedSection != None) and (self.mouse_lastSelectedSection != 'SETTINGSBUTTONFRAME'): 
                    self.mouse_DragDX[self.mouse_lastSelectedSection] += event['dx']
                    self.mouse_DragDY[self.mouse_lastSelectedSection] += event['dy']
                    self.mouse_Dragged = True
                self.mouse_lastHoveredSection = hoveredSection
        
            elif (event['eType'] == "SCROLLED"):
                if (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                elif (self.mouse_lastSelectedSection != None):
                    self.mouse_ScrollDX[self.mouse_lastSelectedSection] += event['scroll_x']
                    self.mouse_ScrollDY[self.mouse_lastSelectedSection] += event['scroll_y']
                    self.mouse_Scrolled = True
                    self.mouse_lastScrolled_ns = time.perf_counter_ns()
        
            elif (event['eType'] == "SELECTIONESCAPED"):
                if (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleMouseEvent(event)
                self.mouse_lastSelectedSection = None
        
            elif (event['eType'] == "HOVERESCAPED"):
                self.__updatePosHighlight(event['x'], event['y'], None, updateType = 1)
                self.mouse_lastSelectedSection = None

        self.mouse_Event_lastRead = event

    def __updatePosHighlight(self, mouseX, mouseY, hoveredSection, updateType):
        if (updateType == 0):
            try:
                #Get Position Within the DrawBox
                xWithinDrawBox = mouseX-self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][0]
                yWithinDrawBox = mouseY-self.displayBox_graphics[hoveredSection]['DRAWBOX'][1]
                #Compute Abstract Space Position
                xValHovered = xWithinDrawBox/self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][2]*(self.horizontalViewRange[1]-self.horizontalViewRange[0])+self.horizontalViewRange[0]
                yValHovered = yWithinDrawBox/self.displayBox_graphics[hoveredSection]['DRAWBOX'][3]*(self.verticalViewRange[hoveredSection][1]-self.verticalViewRange[hoveredSection][0])+self.verticalViewRange[hoveredSection][0]
                #Get Timestamp Interval Position
                tsIntervalHovered_0 = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = xValHovered, mrktReg = self.mrktRegTS, nTicks = 0)

                #If there exist no previous hoveredPosition
                if (self.posHighlight_hoveredPos[2] == None): 
                    self.posHighlight_updatedPositions = [True, True]
                    self.posHighlight_hoveredPos = (tsIntervalHovered_0, yValHovered, hoveredSection, None)
                #If there exist a previous hoveredPoisiton
                else:
                    self.posHighlight_updatedPositions = [False, False]
                    if (self.posHighlight_hoveredPos[0] != tsIntervalHovered_0): self.posHighlight_updatedPositions[0] = True
                    if (self.posHighlight_hoveredPos[1] != yValHovered):         self.posHighlight_updatedPositions[1] = True
                    if (self.posHighlight_hoveredPos[2] != hoveredSection): self.posHighlight_hoveredPos = (tsIntervalHovered_0, yValHovered, hoveredSection, self.posHighlight_hoveredPos[2])
                    else:                                                   self.posHighlight_hoveredPos = (tsIntervalHovered_0, yValHovered, hoveredSection, hoveredSection)
            except:
                self.posHighlight_hoveredPos = (None, None, None, self.posHighlight_hoveredPos[2])
                self.posHighlight_updatedPositions = [True, True]

        elif (updateType == 1):
            if (self.posHighlight_hoveredPos[2] != None):
                self.posHighlight_hoveredPos = (None, None, None, self.posHighlight_hoveredPos[2])
                self.posHighlight_updatedPositions = [True, True]

    def __onPosHighlightUpdate(self):
        #Horizontal Elements Update
        #print(self.posHighlight_updatedPositions, self.posHighlight_hoveredPos)
        if (self.posHighlight_updatedPositions[0] == True):
            if (self.posHighlight_hoveredPos[2] == None): 
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible = False
                for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].visible = False
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].hide()
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].hide()
                self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].hide()
                for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].hide()
            else:
                #Visibility Control
                if (self.posHighlight_hoveredPos[3] == None):
                    self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible = True
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].visible = True
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].show()
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].show()
                    self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].show()
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].show()

                #Update Highligter Graphics
                ts_rightEnd = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = self.posHighlight_hoveredPos[0], mrktReg = self.mrktRegTS, nTicks = 1)
                pixelPerTS = self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][2]*self.scaler / (self.horizontalViewRange[1]-self.horizontalViewRange[0])
                highlightShape_x     = round((self.posHighlight_hoveredPos[0]-self.verticalGrid_intervals[0])*pixelPerTS, 1)
                highlightShape_width = round((ts_rightEnd-self.posHighlight_hoveredPos[0])*pixelPerTS,                    1)
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].x     = highlightShape_x
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].width = highlightShape_width
                if (self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible == False): self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible = True
                for displayBoxName in self.displayBox_graphics_visibleSIViewers:
                    self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].x     = highlightShape_x
                    self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].width = highlightShape_width
                    if (self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].visible == False): self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_HOVERED'].visible = True

                #Update Kline Descriptor
                if (self.posHighlight_hoveredPos[0] in self.klines['raw']):
                    p_open  = self.klines['raw'][self.posHighlight_hoveredPos[0]][2]
                    p_high  = self.klines['raw'][self.posHighlight_hoveredPos[0]][3]
                    p_low   = self.klines['raw'][self.posHighlight_hoveredPos[0]][4]
                    p_close = self.klines['raw'][self.posHighlight_hoveredPos[0]][5]
                    if   (p_open < p_close):  klineColor = 'POSITIVE_{:d}'.format(self.objectConfig['KlineColorType'])
                    elif (p_close < p_open):  klineColor = 'NEGATIVE_{:d}'.format(self.objectConfig['KlineColorType'])
                    elif (p_open == p_close): klineColor = 'NEUTRAL_{:d}'.format(self.objectConfig['KlineColorType'])
                    #DisplayBox 'KLINESPRICE'
                    #Klines
                    pPrecision = self.verticalViewRange_precision['KLINESPRICE']
                    displayText_time  = datetime.fromtimestamp(self.posHighlight_hoveredPos[0]+self.timezoneDelta, tz = timezone.utc).strftime(" %Y/%m/%d %H:%M"); tp1 = len(displayText_time)
                    displayText_open  = " OPEN: {:s}".format(str(round(p_open,   pPrecision))); tp2 = tp1 + len(displayText_open) 
                    displayText_high  = " HIGH: {:s}".format(str(round(p_high,   pPrecision))); tp3 = tp2 + len(displayText_high)
                    displayText_low   = " LOW: {:s}".format(str(round(p_low,     pPrecision))); tp4 = tp3 + len(displayText_low)
                    displayText_close = " CLOSE: {:s}".format(str(round(p_close, pPrecision))); tp5 = tp4 + len(displayText_close)
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].setText(displayText_time+displayText_open+displayText_high+displayText_low+displayText_close, [((0,     tp1+5), 'DEFAULT'),
                                                                                                                                                                                ((tp1+6, tp2),   klineColor),
                                                                                                                                                                                ((tp2+1, tp2+5), 'DEFAULT'),
                                                                                                                                                                                ((tp2+6, tp3),   klineColor),
                                                                                                                                                                                ((tp3+1, tp3+4), 'DEFAULT'),
                                                                                                                                                                                ((tp3+5, tp4),   klineColor),
                                                                                                                                                                                ((tp4+1, tp4+6), 'DEFAULT'),
                                                                                                                                                                                ((tp4+7, tp5-1), klineColor)])
                    #Main-Indicators
                    if (('IVP' in self.klines) and (self.posHighlight_hoveredPos[0] in self.klines['IVP'])):
                        ivpResult = self.klines['IVP'][self.posHighlight_hoveredPos[0]]
                        infoText2 = " [IVP] nDivisions: {:d}, Gamma Factor: {:.2f} % [{:s}]".format(len(ivpResult['ivp_raw']), ivpResult['gammaFactor_effective']*100, str(ivpResult['betaFactor_effective']))
                        print(self.klines['IVP'][self.posHighlight_hoveredPos[0]]['ivp_filteredClusterEvents'], self.klines['IVP'][self.posHighlight_hoveredPos[0]]['anchorClusterIndex'])
                    else: infoText2 = ""
                    #---Check for this for info line 2, since cases where the previous text and the new text are the same are expected to occur frequently
                    previousText = self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].getText()
                    if (previousText != infoText2): self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].setText(infoText2)
                    #EVENTS
                    if (self.objectConfig['DisplayEvents'] == True):
                        if (('EVENTS' in self.klines) and (self.posHighlight_hoveredPos[0] in self.klines['EVENTS'])):
                            analysisEvents = self.klines['EVENTS'][self.posHighlight_hoveredPos[0]]
                            nAnalysisEvents = len(analysisEvents)
                            eventsText = " "
                            for index, analysisEvent in enumerate(analysisEvents): 
                                if (index == nAnalysisEvents-1): eventsText += analysisEvent
                                else:                            eventsText += "{:s}, ".format(analysisEvent)
                            self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].setText(eventsText)
                        else: self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].setText("")
                    #SIViewers
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers:
                        siViewerNumber = int(displayBoxName[8:])
                        siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber)]
                        displayText = ""
                        textFormats = list()
                        if (siAlloc == 'VOL'):
                            if ('VOL' in self.klines and self.posHighlight_hoveredPos[0] in self.klines['VOL']):
                                textBlock = " [SI{:d} - VOL]".format(siViewerNumber)
                                displayText += textBlock; textFormats.append(((0, len(textBlock)-1), 'DEFAULT'))
                                volValue = self.klines['VOL'][self.posHighlight_hoveredPos[0]]['value']
                                if (self.objectConfig['VOLType'] == 'BASE'):    textBlock = " VOL_BASE: {:s} {:s}".format(str(volValue),    self.currencyInfo['baseAsset']);  textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+10), 'DEFAULT')); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1), klineColor))
                                if (self.objectConfig['VOLType'] == 'QUOTE'):   textBlock = " VOL_QUOTE: {:s} {:s}".format(str(volValue),   self.currencyInfo['quoteAsset']); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+11), 'DEFAULT')); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1), klineColor))
                                if (self.objectConfig['VOLType'] == 'BASETB'):  textBlock = " VOL_BASETB: {:s} {:s}".format(str(volValue),  self.currencyInfo['baseAsset']);  textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+12), 'DEFAULT')); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1), klineColor))
                                if (self.objectConfig['VOLType'] == 'QUOTETB'): textBlock = " VOL_QUOTETB: {:s} {:s}".format(str(volValue), self.currencyInfo['quoteAsset']); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+13), 'DEFAULT')); textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1), klineColor))
                                displayText += textBlock
                                for analysisCode in self.siTypes_analysisCodes[siAlloc]:
                                    if (analysisCode in self.klines and self.posHighlight_hoveredPos[0] in self.klines[analysisCode]):
                                        if (analysisCode != 'VOL'):
                                            #TextStyle Check
                                            lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
                                            currentLineStyle = self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['DESCRIPTIONTEXT1'].getTextStyle(lineNumber)
                                            currentLineColor = (self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)])
                                            if (currentLineStyle == None) or (currentLineStyle['color'] != currentLineColor):
                                                newTextStyle = self.effectiveTextStyle['CONTENT_DEFAULT'].copy()
                                                newTextStyle['color'] = currentLineColor
                                                self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['DESCRIPTIONTEXT1'].addTextStyle(str(lineNumber), newTextStyle)

                                            #Text & Format Array Construction
                                            textBlock = " {:s}: {:s}".format(analysisCode, str(self.klines[analysisCode][self.posHighlight_hoveredPos[0]]['value']))
                                            displayText += textBlock;
                                            textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+len(analysisCode)+3), 'DEFAULT'))
                                            textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1),    str(lineNumber)))
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].setText(displayText, textFormats)
                            else:
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].setText(" [SI{:d} - VOL]".format(siViewerNumber))
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].editTextStyle('all', 'DEFAULT')
                        elif (siAlloc == 'MMACD'):
                            if ('MMACD' in self.klines and self.posHighlight_hoveredPos[0] in self.klines['MMACD']):
                                textBlock = " [SI{:d} - MMACD]".format(siViewerNumber)
                                displayText += textBlock; textFormats.append(((0, len(textBlock)-1), 'DEFAULT'))
                                displayValues = {'MMACD':     self.klines['MMACD'][self.posHighlight_hoveredPos[0]]['mmacd'],
                                                 'SIGNAL':    self.klines['MMACD'][self.posHighlight_hoveredPos[0]]['signal'],
                                                 'HISTOGRAM': self.klines['MMACD'][self.posHighlight_hoveredPos[0]]['msDeltaMAMomentum']}
                                for valueType in ('MMACD', 'SIGNAL', 'HISTOGRAM'):
                                    #TextStyle Check
                                    if (valueType == 'HISTOGRAM'):
                                        if (0 <= displayValues['HISTOGRAM']): textStyleName = 'HISTOGRAM+'
                                        else:                                 textStyleName = 'HISTOGRAM-'
                                    else: textStyleName = valueType
                                    currentLineStyle = self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['DESCRIPTIONTEXT1'].getTextStyle(textStyleName)
                                    currentLineColor = (self.objectConfig['MMACD{:s}colorR%{:s}'.format(textStyleName, self.currentGUITheme)],
                                                        self.objectConfig['MMACD{:s}colorG%{:s}'.format(textStyleName, self.currentGUITheme)],
                                                        self.objectConfig['MMACD{:s}colorB%{:s}'.format(textStyleName, self.currentGUITheme)],
                                                        self.objectConfig['MMACD{:s}colorA%{:s}'.format(textStyleName, self.currentGUITheme)])
                                    if (currentLineStyle == None) or (currentLineStyle['color'] != currentLineColor):
                                        newTextStyle = self.effectiveTextStyle['CONTENT_DEFAULT'].copy()
                                        newTextStyle['color'] = currentLineColor
                                        self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['DESCRIPTIONTEXT1'].addTextStyle(textStyleName, newTextStyle)
                                        
                                    #Text & Format Array Construction
                                    textBlock = " {:s}: {:s}".format(valueType, str(displayValues[valueType]))
                                    displayText += textBlock;
                                    textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][1]+len(valueType)+3), 'DEFAULT'))
                                    textFormats.append(((textFormats[-1][0][1]+1, textFormats[-1][0][0]+len(textBlock)-1),  textStyleName))
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].setText(displayText, textFormats)
                            else:
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].setText(" [SI{:d} - MMACD]".format(siViewerNumber))
                                self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].editTextStyle('all', 'DEFAULT')
                else:
                    displayText_time  = datetime.fromtimestamp(self.posHighlight_hoveredPos[0]+self.timezoneDelta, tz = timezone.utc).strftime(" %Y/%m/%d %H:%M")
                    displayText_open  = " OPEN: -"
                    displayText_high  = " HIGH: -"
                    displayText_low   = " LOW: -"
                    displayText_close = " CLOSE: -"
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].setText(displayText_time+displayText_open+displayText_high+displayText_low+displayText_close)
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].editTextStyle('all', 'DEFAULT')
                    self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].setText("")
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers:
                        siViewerNumber = int(displayBoxName[8:])
                        siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber)]
                        self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].setText(" [SI{:d} - {:s}]".format(siViewerNumber, str(siAlloc)))
                        self.displayBox_graphics[displayBoxName]['DESCRIPTIONTEXT1'].editTextStyle('all', 'DEFAULT')
                    self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].setText("")


        #Vertcial Elements Update
        if (self.posHighlight_updatedPositions[1] == True):
            if (self.posHighlight_hoveredPos[2] == None):
                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDELINE'].visible = False
                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'].hide()
                for displayBoxName in self.displayBox_graphics_visibleSIViewers: 
                    self.displayBox_graphics[displayBoxName]['HORIZONTALGUIDELINE'].visible = False
                    self.displayBox_graphics[displayBoxName]['HORIZONTALGUIDETEXT'].hide()
            else:
                dBox_current  = self.posHighlight_hoveredPos[2]
                dBox_previous = self.posHighlight_hoveredPos[3]
                #Visibility Control
                if (dBox_previous == None):
                    self.displayBox_graphics[dBox_current]['HORIZONTALGUIDELINE'].visible = True
                    self.displayBox_graphics[dBox_current]['HORIZONTALGUIDETEXT'].show()
                elif (dBox_previous != dBox_current):
                    self.displayBox_graphics[dBox_current]['HORIZONTALGUIDELINE'].visible = True
                    self.displayBox_graphics[dBox_current]['HORIZONTALGUIDETEXT'].show()
                    self.displayBox_graphics[dBox_previous]['HORIZONTALGUIDELINE'].visible = False
                    self.displayBox_graphics[dBox_previous]['HORIZONTALGUIDETEXT'].hide()
                    
                #Update Highligter Graphics
                pixelPerVal = self.displayBox_graphics[dBox_current]['DRAWBOX'][3]*self.scaler / (self.verticalViewRange[dBox_current][1]-self.verticalViewRange[dBox_current][0])
                try:    verticalHoverLine_y = round((self.posHighlight_hoveredPos[1]-self.horizontalGridIntervals[dBox_current][0])*pixelPerVal, 1)
                except: verticalHoverLine_y = round(self.posHighlight_hoveredPos[1]*pixelPerVal,                                                 1)
                self.displayBox_graphics[dBox_current]['HORIZONTALGUIDELINE'].y  = verticalHoverLine_y
                self.displayBox_graphics[dBox_current]['HORIZONTALGUIDELINE'].y2 = verticalHoverLine_y

                #Update Vertical Value Text
                dFromCeiling = self.displayBox_graphics[dBox_current]['HORIZONTALGRID_CAMGROUP'].projection_y1-verticalHoverLine_y
                if (dFromCeiling < _GD_DISPLAYBOX_GUIDE_HORIZONTALTEXTHEIGHT*self.scaler): self.displayBox_graphics[dBox_current]['HORIZONTALGUIDETEXT'].moveTo(y = verticalHoverLine_y/self.scaler-_GD_DISPLAYBOX_GUIDE_HORIZONTALTEXTHEIGHT)
                else:                                                            self.displayBox_graphics[dBox_current]['HORIZONTALGUIDETEXT'].moveTo(y = verticalHoverLine_y/self.scaler)
                self.displayBox_graphics[dBox_current]['HORIZONTALGUIDETEXT'].setText(str(round(self.posHighlight_hoveredPos[1], self.verticalViewRange_precision[dBox_current])))

        self.posHighlight_updatedPositions = None

    def __updatePosSelection(self, updateType):
        #By button press->release
        if (updateType == 0):
            if (self.posHighlight_hoveredPos[2] != None):
                if (self.posHighlight_hoveredPos[0] == self.posHighlight_selectedPos):
                    self.posHighlight_selectedPos = None
                    self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].visible = False
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].visible = False
                else:
                    self.posHighlight_selectedPos = self.posHighlight_hoveredPos[0]
                    shape_xPos  = self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].x
                    shape_width = self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].width
                    self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].x     = shape_xPos
                    self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].width = shape_width
                    self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].visible = True
                    for displayBoxName in self.displayBox_graphics_visibleSIViewers: 
                        self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].x     = shape_xPos
                        self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].width = shape_width
                        self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].visible = True
                self.__onPosSelectionUpdate()
        #By HorizontalViewRange Update
        elif (updateType == 1):
            if (self.posHighlight_selectedPos != None):
                tsPosEnd = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = self.posHighlight_selectedPos, mrktReg = self.mrktRegTS, nTicks = 1)
                pixelPerTS = self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][2]*self.scaler / (self.horizontalViewRange[1]-self.horizontalViewRange[0])
                shape_xPos  = round((self.posHighlight_selectedPos-self.verticalGrid_intervals[0])*pixelPerTS, 1)
                shape_width = round((tsPosEnd-self.posHighlight_selectedPos)*pixelPerTS,                       1)
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].x     = shape_xPos
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].width = shape_width
                for displayBoxName in self.displayBox_graphics_visibleSIViewers: 
                    self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].x     = shape_xPos
                    self.displayBox_graphics[displayBoxName]['POSHIGHLIGHT_SELECTED'].width = shape_width

    def __onPosSelectionUpdate(self):
        #IVP Update
        if ('IVP' in self.klines_analysisParams):
            if (self.posHighlight_selectedPos == None): self.__removeAnalysisData(analysisCode = 'IVP', removalType = 2, removalType_Graphics = 0b00011)
            else:
                if ('IVP' in self.klines) and (self.posHighlight_selectedPos in self.klines['IVP']):
                    if (self.posHighlight_selectedPos in self.klines_drawQueue): self.klines_drawQueue[self.posHighlight_selectedPos]['IVP'] = None
                    else:                                                        self.klines_drawQueue[self.posHighlight_selectedPos] = {'IVP': None}

    def handleKeyEvent(self, event):
        if (self.hidden == False):
            if (self.mouse_lastSelectedSection == 'SETTINGSSUBPAGE'): self.settingsSubPages[self.settingsSubPage_Current].handleKeyEvent(event)
    #General Object Processing & User Interaction Control END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Basic Object Control -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def show(self):
        self.hidden = False
        for displayBoxName in self.frameSprites: self.frameSprites[displayBoxName].visible = True
        if (self.settingsSubPage_Opened == True): self.settingsSubPages[self.settingsSubPage_Current].show()

    def hide(self):
        self.hidden = True
        for displayBoxName in self.frameSprites: self.frameSprites[displayBoxName].visible = False
        self.settingsSubPages[self.settingsSubPage_Current].hide()

    def isHidden(self): 
        return self.hidden
        
    def moveTo(self, x, y):
        dx = x - self.xPos; dy = y - self.yPos
        self.xPos = x; self.yPos = y
        for displayBoxName in self.displayBox:
            if (self.displayBox[displayBoxName] != None):
                self.displayBox[displayBoxName] = (self.displayBox[displayBoxName][0]+dx, self.displayBox[displayBoxName][1]+dy, self.displayBox[displayBoxName][2], self.displayBox[displayBoxName][3])
                if (displayBoxName == 'SETTINGSBUTTONFRAME'):
                    self.hitBox['SETTINGSBUTTONFRAME'].reposition(xPos = self.displayBox['SETTINGSBUTTONFRAME'][0], yPos = self.displayBox['SETTINGSBUTTONFRAME'][1])
                    self.frameSprites['SETTINGSBUTTONFRAME'].position = (self.displayBox['SETTINGSBUTTONFRAME'][0]*self.scaler, self.displayBox['SETTINGSBUTTONFRAME'][1]*self.scaler, self.frameSprites['SETTINGSBUTTONFRAME'].z)
                    self.frameSprites['SETTINGSBUTTONFRAME_ICON'].position = ((self.displayBox['SETTINGSBUTTONFRAME'][0]+self.displayBox['SETTINGSBUTTONFRAME'][2]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].width/2,
                                                                              (self.displayBox['SETTINGSBUTTONFRAME'][1]+self.displayBox['SETTINGSBUTTONFRAME'][3]/2)*self.scaler-self.images['SETTINGSBUTTONFRAME_ICON'].height/2,
                                                                              self.frameSprites['SETTINGSBUTTONFRAME_ICON'].z)
                else:
                    self.hitBox[displayBoxName].reposition(xPos = self.displayBox[displayBoxName][0]+_GD_DISPLAYBOX_GOFFSET, yPos = self.displayBox[displayBoxName][1]+_GD_DISPLAYBOX_GOFFSET)
                    self.frameSprites[displayBoxName].position = (self.displayBox[displayBoxName][0]*self.scaler, self.displayBox[displayBoxName][1]*self.scaler, self.frameSprites[displayBoxName].z)
        for settingsSubPageName in self.settingsSubPages: self.settingsSubPages[settingsSubPageName].moveTo(x = self.xPos+50, y = self.yPos+50)
        self.hitBox_Object.reposition(xPos = self.xPos, yPos = self.yPos)

    def resize(self, width, height):
        self.width = width; self.height = height
        #Set SubIndicator Switch Activation
        self.usableSIViewers = min([int((self.height-_GD_OBJECT_MINHEIGHT-(_GD_DISPLAYBOX_AUXILLARYBAR_HEIGHT+_GD_DISPLAYBOX_GOFFSET))/(_GD_DISPLAYBOX_SIVIEWER_HEIGHT+_GD_DISPLAYBOX_GOFFSET)), len(_SITYPES)])
        for siViewerIndex in range (len(_SITYPES)):
            if (siViewerIndex < self.usableSIViewers):
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SHOW{:d}".format(siViewerIndex+1)].activate()
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SELECTION{:d}".format(siViewerIndex+1)].activate()
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SHOW{:d}".format(siViewerIndex+1)].setStatus(self.objectConfig['SI{:d}Display'.format(siViewerIndex+1)] == True)
            else:
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SHOW{:d}".format(siViewerIndex+1)].deactivate()
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SELECTION{:d}".format(siViewerIndex+1)].deactivate()
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_SHOW{:d}".format(siViewerIndex+1)].setStatus(False)
        self.__setDisplayBoxDimensions()
        for settingsSubPageName in self.settingsSubPages: self.settingsSubPages[settingsSubPageName].resize(width = 3700, height = self.height-100)
        self.hitBox_Object.resize(width = self.width, height = self.height)

    def isTouched(self, mouseX, mouseY):
        if (self.hidden == False): return self.hitBox_Object.isTouched(mouseX, mouseY)
        else: return False

    def setName(self, name): 
        self.name = name

    def getName(self): 
        return self.name

    def on_GUIThemeUpdate(self, **kwargs):
        #Bring in updated textStyle and colors
        self.currentGUITheme = self.visualManager.getGUITheme()

        newEffectiveTextStyle = self.visualManager.getTextStyle('chartDrawer_'+self.textStyle)
        for styleTarget in newEffectiveTextStyle: newEffectiveTextStyle[styleTarget]['font_size'] = self.effectiveTextStyle[styleTarget]['font_size']
        self.effectiveTextStyle = newEffectiveTextStyle
        
        self.gridColor       = self.visualManager.getFromColorTable('CHARTDRAWER_GRID')
        self.gridColor_Heavy = self.visualManager.getFromColorTable('CHARTDRAWER_GRIDHEAVY')
        self.guideColor      = self.visualManager.getFromColorTable('CHARTDRAWER_GUIDECONTENT')
        self.posHighlightColor_hovered  = self.visualManager.getFromColorTable('CHARTDRAWER_POSHOVERED')
        self.posHighlightColor_selected = self.visualManager.getFromColorTable('CHARTDRAWER_POSSELECTED')

        #Object Image Update
        for displayBoxName in self.displayBox:
            if (self.displayBox[displayBoxName] != None):
                if (displayBoxName == 'SETTINGSBUTTONFRAME'):
                    self.images['SETTINGSBUTTONFRAME_DEFAULT'] = self.imageManager.getImageByLoadIndex(self.images['SETTINGSBUTTONFRAME_DEFAULT'][1])
                    self.images['SETTINGSBUTTONFRAME_HOVERED'] = self.imageManager.getImageByLoadIndex(self.images['SETTINGSBUTTONFRAME_HOVERED'][1])
                    self.images['SETTINGSBUTTONFRAME_PRESSED'] = self.imageManager.getImageByLoadIndex(self.images['SETTINGSBUTTONFRAME_PRESSED'][1])
                    iconColoring = self.visualManager.getFromColorTable('ICON_COLORING')
                    self.frameSprites[displayBoxName].image = self.images['SETTINGSBUTTONFRAME_'+self.settingsButtonStatus][0]
                    self.frameSprites['SETTINGSBUTTONFRAME_ICON'].color = (iconColoring[0], iconColoring[1], iconColoring[2]); self.frameSprites['SETTINGSBUTTONFRAME'+'_ICON'].opacity = iconColoring[3]
                else:
                    self.images[displayBoxName] = self.imageManager.getImageByLoadIndex(self.images[displayBoxName][1])
                    self.frameSprites[displayBoxName].image = self.images[displayBoxName][0]
                    
        #Grid and Guide Lines & Text Update
        for displayBoxName in self.displayBox:
            if (displayBoxName == 'KLINESPRICE'):
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['CONTENT_DEFAULT'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('POSITIVE_1', self.effectiveTextStyle['CONTENT_POSITIVE_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('NEGATIVE_1', self.effectiveTextStyle['CONTENT_NEGATIVE_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('NEUTRAL_1',  self.effectiveTextStyle['CONTENT_NEUTRAL_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('POSITIVE_2', self.effectiveTextStyle['CONTENT_POSITIVE_2'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('NEGATIVE_2', self.effectiveTextStyle['CONTENT_NEGATIVE_2'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].addTextStyle('NEUTRAL_2',  self.effectiveTextStyle['CONTENT_NEUTRAL_2'])

                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['CONTENT_DEFAULT'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('POSITIVE_1', self.effectiveTextStyle['CONTENT_POSITIVE_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('NEGATIVE_1', self.effectiveTextStyle['CONTENT_NEGATIVE_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('NEUTRAL_1',  self.effectiveTextStyle['CONTENT_NEUTRAL_1'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('POSITIVE_2', self.effectiveTextStyle['CONTENT_POSITIVE_2'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('NEGATIVE_2', self.effectiveTextStyle['CONTENT_NEGATIVE_2'])
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].addTextStyle('NEUTRAL_2',  self.effectiveTextStyle['CONTENT_NEUTRAL_2'])

                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].color  = self.posHighlightColor_hovered
                self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].color = self.posHighlightColor_selected
                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDELINE'].color = self.guideColor
                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'].on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['GUIDECONTENT'])

                for gridLineShape in self.displayBox_graphics['KLINESPRICE']['HORIZONTALGRID_LINES']:        gridLineShape.color = self.gridColor
                for gridLineShape in self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES']:          gridLineShape.color = self.gridColor
                for gridLineShape in self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_LINES']: gridLineShape.color = self.gridColor
                for gridLineText  in self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS']: gridLineText.on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['GRID'])

            elif ((displayBoxName[:8] == 'SIVIEWER') and (displayBoxName in self.displayBox_graphics_visibleSIViewers)):
                siIndex = int(displayBoxName[8:])
                dBoxName          = 'SIVIEWER{:d}'.format(siIndex)
                dBoxName_MAINGRID = 'MAINGRID_SIVIEWER{:d}'.format(siIndex)

                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['CONTENT_DEFAULT'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('POSITIVE_1', self.effectiveTextStyle['CONTENT_POSITIVE_1'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('NEGATIVE_1', self.effectiveTextStyle['CONTENT_NEGATIVE_1'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('NEUTRAL_1',  self.effectiveTextStyle['CONTENT_NEUTRAL_1'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('POSITIVE_2', self.effectiveTextStyle['CONTENT_POSITIVE_2'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('NEGATIVE_2', self.effectiveTextStyle['CONTENT_NEGATIVE_2'])
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].addTextStyle('NEUTRAL_2',  self.effectiveTextStyle['CONTENT_NEUTRAL_2'])

                self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_HOVERED'].color  = self.posHighlightColor_hovered
                self.displayBox_graphics[dBoxName]['POSHIGHLIGHT_SELECTED'].color = self.posHighlightColor_selected
                self.displayBox_graphics[dBoxName]['HORIZONTALGUIDELINE'].color = self.guideColor
                self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'].on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['GUIDECONTENT'])

                for gridLineShape in self.displayBox_graphics[dBoxName]['HORIZONTALGRID_LINES']:          gridLineShape.color = self.gridColor
                for gridLineShape in self.displayBox_graphics[dBoxName]['VERTICALGRID_LINES']:            gridLineShape.color = self.gridColor
                for gridLineShape in self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_LINES']: gridLineShape.color = self.gridColor
                for gridLineText  in self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS']: gridLineText.on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['GRID'])

            elif (displayBoxName == 'MAINGRID_TEMPORAL'):
                for gridLineShape in self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES']: gridLineShape.color = self.gridColor
                for gridLineText  in self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS']: gridLineText.on_GUIThemeUpdate(newDefaultTextStyle = self.effectiveTextStyle['GRID'])
        
        #Klines Loading GaugeBar Related
        self.images['KLINELOADINGCOVER'] = self.imageManager.getImageByLoadIndex(self.images['KLINELOADINGCOVER'][1])
        self.frameSprites['KLINELOADINGCOVER'].image = self.images['KLINELOADINGCOVER'][0]
        self.klinesLoadingGaugeBar.on_GUIThemeUpdate(**kwargs)
        self.klinesLoadingTextBox_perc.on_GUIThemeUpdate(**kwargs)
        self.klinesLoadingTextBox.on_GUIThemeUpdate(**kwargs)

        #Update Settings Subpages
        for subPageInstance in self.settingsSubPages.values(): subPageInstance.on_GUIThemeUpdate(**kwargs)
        
        #Update Configuration Objects Color
        if (True): #<--- Placed simply for a better readability
            #<MAs>
            for miType in ('SMA','WMA','EMA'):
                for lineIndex in range (_NMAXLINES[miType]):
                    lineNumber = lineIndex+1
                    self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_LINECOLOR".format(miType,lineNumber)].updateColor(self.objectConfig['{:s}{:d}colorR%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                              self.objectConfig['{:s}{:d}colorG%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                              self.objectConfig['{:s}{:d}colorB%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                                                                                                              self.objectConfig['{:s}{:d}colorA%{:s}'.format(miType,lineNumber,self.currentGUITheme)])
                self._onSettingsContentUpdate(self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
                #self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].setSelected(self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected())
            #<PSAR>
            for lineIndex in range (_NMAXLINES['PSAR']):
                lineNumber = lineIndex+1
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['PSAR{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                   self.objectConfig['PSAR{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                   self.objectConfig['PSAR{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                   self.objectConfig['PSAR{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
            self._onSettingsContentUpdate(self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
            #<BOL>
            for lineIndex in range (_NMAXLINES['BOL']):
                lineNumber = lineIndex+1
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                 self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                 self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                 self.objectConfig['BOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
            self._onSettingsContentUpdate(self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
            #<IVP>
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_COLOR"].updateColor(self.objectConfig['IVPRAWcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                     self.objectConfig['IVPRAWcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                     self.objectConfig['IVPRAWcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                     self.objectConfig['IVPRAWcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCCURRENTANCHOR_COLOR"].updateColor(self.objectConfig['IVPCCURRENTANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                                self.objectConfig['IVPCCURRENTANCHORcolorA%{:s}'.format(self.currentGUITheme)])
            self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPREVANCHOR_COLOR"].updateColor(self.objectConfig['IVPCPREVANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                             self.objectConfig['IVPCPREVANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                             self.objectConfig['IVPCPREVANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                             self.objectConfig['IVPCPREVANCHORcolorA%{:s}'.format(self.currentGUITheme)])
            self._onSettingsContentUpdate(self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
            #<PIP>
            self._onSettingsContentUpdate(self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
            #<VOL>
            for lineIndex in range (_NMAXLINES['VOL']):
                lineNumber = lineIndex+1
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_LINECOLOR".format(lineNumber)].updateColor(self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                                                                                                    self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
            self._onSettingsContentUpdate(self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])
            #<MMACD>
            for targetLine in ('MMACD', 'SIGNAL', 'HISTOGRAM+', 'HISTOGRAM-'):
                self.settingsSubPages['MMACD'].GUIOs["INDICATOR_{:s}_COLOR".format(targetLine)].updateColor(self.objectConfig['MMACD{:s}colorR%{:s}'.format(targetLine,self.currentGUITheme)], 
                                                                                                            self.objectConfig['MMACD{:s}colorG%{:s}'.format(targetLine,self.currentGUITheme)], 
                                                                                                            self.objectConfig['MMACD{:s}colorB%{:s}'.format(targetLine,self.currentGUITheme)], 
                                                                                                            self.objectConfig['MMACD{:s}colorA%{:s}'.format(targetLine,self.currentGUITheme)])
            self._onSettingsContentUpdate(self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_TARGETSELECTION"])

        #Register redraw queues
        for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
            if (timestamp in self.klines['raw']):
                if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp]['KLINE'] = 0
                else:                                    self.klines_drawQueue[timestamp] = {'KLINE': 0}
        for analysisCode in self.klines_analysisParams.keys():
            for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
                if (timestamp in self.klines_processed) and (analysisCode in self.klines_processed[timestamp]):
                    if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp][analysisCode] = 0
                    else:                                    self.klines_drawQueue[timestamp] = {analysisCode: 0}

    def on_LanguageUpdate(self, **kwargs):
        #Bring in updated textStyle
        newEffectiveTextStyle = self.visualManager.getTextStyle('chartDrawer_'+self.textStyle)
        for styleTarget in newEffectiveTextStyle: newEffectiveTextStyle[styleTarget]['font_size'] = self.effectiveTextStyle[styleTarget]['font_size']
        self.effectiveTextStyle = newEffectiveTextStyle
        
        #Grid and Guide Lines & Text Update
        for displayBoxName in self.displayBox:
            if (displayBoxName == 'KLINESPRICE'):
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].on_LanguageUpdate(**kwargs)
                self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].on_LanguageUpdate(**kwargs)
                self.displayBox_graphics['KLINESPRICE']['HORIZONTALGUIDETEXT'].on_LanguageUpdate(**kwargs)
                for gridLineText  in self.displayBox_graphics['MAINGRID_KLINESPRICE']['HORIZONTALGRID_TEXTS']: gridLineText.on_LanguageUpdate(**kwargs)

            elif ((displayBoxName[:8] == 'SIVIEWER') and (displayBoxName in self.displayBox_graphics_visibleSIViewers)):
                siIndex = int(displayBoxName[8:])
                dBoxName          = 'SIVIEWER{:d}'.format(siIndex)
                dBoxName_MAINGRID = 'MAINGRID_SIVIEWER{:d}'.format(siIndex)
                self.displayBox_graphics[dBoxName]['DESCRIPTIONTEXT1'].on_LanguageUpdate(**kwargs)
                self.displayBox_graphics[dBoxName]['HORIZONTALGUIDETEXT'].on_LanguageUpdate(**kwargs)
                for gridLineText in self.displayBox_graphics[dBoxName_MAINGRID]['HORIZONTALGRID_TEXTS']: gridLineText.on_LanguageUpdate(**kwargs)

            elif (displayBoxName == 'MAINGRID_TEMPORAL'):
                for gridLineText  in self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS']: gridLineText.on_LanguageUpdate(**kwargs)

        #Klines Loading GaugeBar Related
        self.klinesLoadingTextBox_perc.on_LanguageUpdate(**kwargs)
        self.klinesLoadingTextBox.on_LanguageUpdate(**kwargs)

        #Update Settings Subpages
        for subPageInstance in self.settingsSubPages.values(): subPageInstance.on_LanguageUpdate(**kwargs)
    #Basic Object Control END ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Configuration Update Control -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __onSettingsButtonClick(self):
        #Close the settings subpage
        if (self.settingsSubPage_Opened == True): 
            self.settingsSubPages[self.settingsSubPage_Current].hide()
            self.settingsSubPage_Opened = False
        #Open the settings subpage
        else: 
            self.settingsSubPages[self.settingsSubPage_Current].show()
            self.settingsSubPage_Opened = True

    def __onSettingsNavButtonClick(self, objectInstance):
        buttonName = objectInstance.getName()
        previousSubPage = self.settingsSubPage_Current
        if   (buttonName == 'navButton_MI_SMA'):     self.settingsSubPage_Current = 'SMA'
        elif (buttonName == 'navButton_MI_WMA'):     self.settingsSubPage_Current = 'WMA'
        elif (buttonName == 'navButton_MI_EMA'):     self.settingsSubPage_Current = 'EMA'
        elif (buttonName == 'navButton_MI_BOL'):     self.settingsSubPage_Current = 'BOL'
        elif (buttonName == 'navButton_MI_PSAR'):    self.settingsSubPage_Current = 'PSAR'
        elif (buttonName == 'navButton_MI_IVP'):     self.settingsSubPage_Current = 'IVP'
        elif (buttonName == 'navButton_MI_PIP'):     self.settingsSubPage_Current = 'PIP'
        elif (buttonName == 'navButton_SI_VOL'):     self.settingsSubPage_Current = 'VOL'
        elif (buttonName == 'navButton_SI_MMACD'):   self.settingsSubPage_Current = 'MMACD'
        elif (buttonName == 'navButton_SI_DMIxADX'): self.settingsSubPage_Current = 'DMIxADX'
        elif (buttonName == 'navButton_SI_MFI'):     self.settingsSubPage_Current = 'MFI'
        elif (buttonName == 'navButton_toHome'):     self.settingsSubPage_Current = 'MAIN'
        self.settingsSubPages[previousSubPage].hide()
        self.settingsSubPages[self.settingsSubPage_Current].show()

    def __onSettingsContentUpdate(self, objectInstnace):
        guioName = objectInstnace.getName()
        guioName_split = guioName.split("_")
        print(guioName_split)
        indicatorType = guioName_split[0]

        activateSaveConfigButton = False

        #Subpage 'MAIN'
        if (indicatorType == 'MAIN'):
            setterType = guioName_split[1] #"AUX_KLINECOLORTYPE_SELECTIONBOX", "AUX_TIMEZONE_SELECTIONBOX"
            if (setterType == 'SHOWAUXBAR'):
                self.__configureDisplayBoxes()
                self.__onHViewRangeUpdate(1)
                for verticalSectionName in self.displayBox_VerticalSection_Order:
                    if (verticalSectionName == 'KLINESPRICE') or (verticalSectionName[:8] == 'SIVIEWER'): self.__onVViewRangeUpdate(verticalSectionName, 1)
                self.objectConfig['UseAuxBar'] = self.settingsSubPages['MAIN'].GUIOs["AUX_SHOWAUXBAR_SWITCH"].getStatus()
                activateSaveConfigButton = True
            elif (setterType == 'DISPLAYEVENTS'):
                self.objectConfig['DisplayEvents'] = self.settingsSubPages['MAIN'].GUIOs["AUX_SHOWAUXBAR_SWITCH"].getStatus()
                if (self.objectConfig['DisplayEvents'] == True): self.klines_drawQueue.update(dict.fromkeys(self.klines_drawn, {'EVENTS': 0}))
                else:
                    for ts in self.klines_drawQueue:
                        if ('EVENTS' in self.klines_drawQueue[ts]): del self.klines_drawQueue[ts]['EVENTS']
                    for ts in self.klines_drawn:
                        if ('EVENTS' in self.klines_drawn[ts]): self.klines_drawn[ts].remove('EVENTS')
                    self.displayBox_graphics['KLINESPRICE']['EVENTSTEXT'].hide()
                activateSaveConfigButton = True
            elif (setterType == 'KLINECOLORTYPE'): 
                selectedColorType = self.settingsSubPages['MAIN'].GUIOs['AUX_KLINECOLORTYPE_SELECTIONBOX'].getSelected()
                self.objectConfig['KlineColor'] = selectedColorType
                self.updateKlineColors(newType = selectedColorType)
                activateSaveConfigButton = True
            elif (setterType == 'TIMEZONE'):       
                selectedTimeZone = self.settingsSubPages['MAIN'].GUIOs['AUX_TIMEZONE_SELECTIONBOX'].getSelected()
                self.objectConfig['TimeZone'] = selectedTimeZone
                print(selectedTimeZone)
                self.updateTimeZone(newTimeZone = selectedTimeZone)
                activateSaveConfigButton = True
            elif (setterType == 'SAVECONFIG'): 
                configToWrite = dict()
                for configKeyCode in self.objectConfig: configToWrite[configKeyCode] = self.objectConfig[configKeyCode]
                self.sysFunc_editGUIOConfig(targetName = self.name, targetContent = configToWrite); self.settingsSubPages['MAIN'].GUIOs["AUX_SAVECONFIGURATION"].deactivate()
            elif (setterType == 'INDICATORSWITCH'):
                analysisType = guioName_split[2]
                self._onSettingsContentUpdate(self.settingsSubPages[analysisType].GUIOs["APPLYNEWSETTINGS"])
                activateSaveConfigButton = True
            elif (setterType == 'SIVIEWERDISPLAYSWITCH'):
                #SIViewerNumber
                siViewerNumber = int(guioName_split[2])
                siViewerCode   = "SIVIEWER{:d}".format(siViewerNumber)
                self.__initializeSIViewer(siViewerNumber)
                #Update Object Config
                newDisplayStatus = self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSWITCH{:d}".format(siViewerNumber)].getStatus()
                self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)] = newDisplayStatus
                #Reconfigure Display Boxes
                self.__configureDisplayBoxes()
                #Update ViewRanges
                self.__editHPosition(delta_drag = 0, updateType = 1)
                self.__onVViewRangeUpdate(displayBoxName = 'KLINESPRICE', updateType = 1)
                for visibleSIViewerCode in self.displayBox_graphics_visibleSIViewers: self.__onVViewRangeUpdate(displayBoxName = visibleSIViewerCode, updateType = 1)
                #Update Draw Queues
                siAlloc = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber)]
                if ((newDisplayStatus == True) and (self.siTypes_analysisCodes[siAlloc] != None)):
                    self.checkVerticalExtremas_SIs[siAlloc]()
                    for analysisCode in self.siTypes_analysisCodes[siAlloc]: self.__addDrawQueuesToBufferZone(analysisCode, drawSignal = _FULLDRAWSIGNALS[siAlloc])
                #Activate Configuration Save Button
                activateSaveConfigButton = True
            elif (setterType == 'SIVIEWERDISPLAYSELECTION'):
                #SIViewerNumbers & SIAlloc
                siViewerNumber1 = int(guioName_split[2]);                   siAlloc1_new = self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSELECTION{:d}".format(siViewerNumber1)].getSelected()
                siViewerNumber2 = self.siTypes_siViewerAlloc[siAlloc1_new]; siAlloc2_new = self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber1)]
                #Update Object Config, GUIO, and SIViewer Control Variable
                self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber1)] = siAlloc1_new; self.siTypes_siViewerAlloc[siAlloc1_new] = siViewerNumber1
                self.objectConfig['SIVIEWER{:d}SIAlloc'.format(siViewerNumber2)] = siAlloc2_new; self.siTypes_siViewerAlloc[siAlloc2_new] = siViewerNumber2
                self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_DISPLAYSELECTION{:d}".format(siViewerNumber2)].setSelected(siAlloc2_new, callSelectionUpdateFunction = False)
                #SIViewer Initialization
                self.__initializeSIViewer(siViewerNumber1)
                self.__initializeSIViewer(siViewerNumber2)
                #Check vertical extremas and update viewRange
                self.checkVerticalExtremas_SIs[siAlloc1_new](); self.__onVViewRangeUpdate(displayBoxName = "SIVIEWER{:d}".format(siViewerNumber1), updateType = 1)
                self.checkVerticalExtremas_SIs[siAlloc2_new](); self.__onVViewRangeUpdate(displayBoxName = "SIVIEWER{:d}".format(siViewerNumber2), updateType = 1)
                #Update Draw Queues
                if (self.siTypes_analysisCodes[siAlloc1_new] != None):
                    for analysisCode in self.siTypes_analysisCodes[siAlloc1_new]: self.__addDrawQueuesToBufferZone(analysisCode, drawSignal = _FULLDRAWSIGNALS[siAlloc1_new])
                if (self.siTypes_analysisCodes[siAlloc2_new] != None):
                    for analysisCode in self.siTypes_analysisCodes[siAlloc2_new]: self.__addDrawQueuesToBufferZone(analysisCode, drawSignal = _FULLDRAWSIGNALS[siAlloc2_new])
                #Activate Configuration Save Button
                activateSaveConfigButton = True

        #Subpage 'SMA' 'WMA' 'EMA'
        elif ((indicatorType == 'SMA') or (indicatorType == 'WMA') or (indicatorType == 'EMA')):
            miType = indicatorType
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):
                lineSelected = self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:s}_LINECOLOR".format(miType, lineSelected)].getColor()
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):
                contentType = guioName_split[2]
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):
                lineSelected = self.settingsSubPages[miType].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:s}_LINECOLOR".format(miType,lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages[miType].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'LineActivationSwitch'): 
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'IntervalTextInputBox'): 
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'WidthTextInputBox'):    
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'):        
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = dict()

                #Check for any changes in the configuration
                if (True):
                    for lineIndex in range (_NMAXLINES[miType]):
                        lineNumber = lineIndex+1
                        updateTracker[lineNumber] = [False, False]
                        #Compute
                        compute_previous = self.objectConfig['{:s}{:d}Compute'.format(miType,lineNumber)]
                        self.objectConfig['{:s}{:d}Compute'.format(miType,lineNumber)] = self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}".format(miType,lineNumber)].getStatus()
                        if ((compute_previous == False) and (self.objectConfig['{:s}{:d}Compute'.format(miType,lineNumber)] == True)): updateTracker[lineNumber][0] = True
                        #Interval
                        interval_previous = self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)]
                        reset = False
                        try:
                            interval = int(self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_INTERVALINPUT".format(miType,lineNumber)].getText())
                            if (0 < interval): self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)] = interval
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)] = 1
                            self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_INTERVALINPUT".format(miType,lineNumber)].updateText(str(self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)]))
                        if (interval_previous != self.objectConfig['{:s}{:d}nSamples'.format(miType,lineNumber)]): updateTracker[lineNumber][0] = True
                        #Width
                        width_previous = self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)]
                        reset = False
                        try:
                            width = int(self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_WIDTHINPUT".format(miType,lineNumber)].getText())
                            if (0 < width): self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)] = width
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)] = 1
                            self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_WIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)]))
                        if (width_previous != self.objectConfig['{:s}{:d}Width'.format(miType,lineNumber)]): updateTracker[lineNumber][1] = True
                        #Color
                        color_previous = (self.objectConfig['{:s}{:d}colorR%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['{:s}{:d}colorG%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['{:s}{:d}colorB%{:s}'.format(miType,lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['{:s}{:d}colorA%{:s}'.format(miType,lineNumber,self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_LINECOLOR".format(miType,lineNumber)].getColor()
                        self.objectConfig['{:s}{:d}colorR%{:s}'.format(miType,lineNumber,self.currentGUITheme)] = color_r
                        self.objectConfig['{:s}{:d}colorG%{:s}'.format(miType,lineNumber,self.currentGUITheme)] = color_g
                        self.objectConfig['{:s}{:d}colorB%{:s}'.format(miType,lineNumber,self.currentGUITheme)] = color_b
                        self.objectConfig['{:s}{:d}colorA%{:s}'.format(miType,lineNumber,self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): updateTracker[lineNumber][1] = True
                        #Line Display
                        display_previous = self.objectConfig['{:s}{:d}Display'.format(miType,lineNumber)]
                        self.objectConfig['{:s}{:d}Display'.format(miType,lineNumber)] = self.settingsSubPages[miType].GUIOs["INDICATOR_{:s}{:d}_DISPLAY".format(miType,lineNumber)].getStatus()
                        if (display_previous != self.objectConfig['{:s}{:d}Display'.format(miType,lineNumber)]): updateTracker[lineNumber][1] = True
                    #MA Compute
                    computeMA_previous = self.objectConfig['{:s}Compute'.format(miType)]
                    self.objectConfig['{:s}Compute'.format(miType)] = self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_{:s}".format(miType)].getStatus()
                    if ((computeMA_previous == False) and (self.objectConfig['{:s}Compute'.format(miType)] == True)):
                        for lineNumber in updateTracker: updateTracker[lineNumber][0] = True
                    
                #Configuration and Queue Update
                configuredMAs = self.__configureAnalysisParams(miType)
                for configuredMA in configuredMAs:
                    lineNumber = self.klines_analysisParams[configuredMA]['lineNumber']
                    if (updateTracker[lineNumber][0] == True):
                        self.__removeAnalysisData(analysisCode = configuredMA, removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = configuredMA, analysisMode = 0)                   #Update process queue
                    elif (updateTracker[lineNumber][1] == True):
                        self.__removeAnalysisData(analysisCode = configuredMA, removalType = 2, removalType_Graphics = None) #Remove previous graphics
                        self.__addDrawQueuesToBufferZone(analysisCode = configuredMA, drawSignal = _FULLDRAWSIGNALS[miType]) #Update draw queue

                #Control Buttons Handling
                self.settingsSubPages[miType].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True
                
        #Subpage 'PSAR'
        elif (indicatorType == 'PSAR'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):
                lineSelected = self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:s}_LINECOLOR".format(lineSelected)].getColor()
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):
                contentType = guioName_split[2]
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                      gValue = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                      bValue = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                      aValue = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):
                lineSelected = self.settingsSubPages['PSAR'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:s}_LINECOLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['PSAR'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'LineActivationSwitch'):     
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'StartTextInputBox'):        
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'AccelerationTextInputBox'): 
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'MaximumTextInputBox'):      
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'SizeTextInputBox'):         
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'):            
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = dict()

                #Check for any changes in the configuration
                if (True):
                    for lineIndex in range (_NMAXLINES['PSAR']):
                        lineNumber = lineIndex+1
                        updateTracker[lineNumber] = [False, False] 
                        #Compute
                        compute_previous = self.objectConfig['PSAR{:d}Compute'.format(lineNumber)]
                        self.objectConfig['PSAR{:d}Compute'.format(lineNumber)] = self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}".format(lineNumber)].getStatus()
                        if ((compute_previous == False) and (self.objectConfig['PSAR{:d}Compute'.format(lineNumber)] == True)): updateTracker[lineNumber][0] = True
                        #Maximum
                        maximum_previous = self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]
                        reset = False
                        try:
                            maximum = round(float(self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_MAXIMUMINPUT".format(lineNumber)].getText()), 3)
                            if (0 < maximum) and (maximum <= 10): self.objectConfig['PSAR{:d}maximum'.format(lineNumber)] = maximum
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['PSAR{:d}maximum'.format(lineNumber)] = 0.200
                            self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_MAXIMUMINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]))
                        if (maximum_previous != self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #Start
                        start_previous = self.objectConfig['PSAR{:d}start'.format(lineNumber)]
                        reset = False
                        try:
                            start = round(float(self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_STARTINPUT".format(lineNumber)].getText()), 3)
                            if ((0 <= start) and (start < self.objectConfig['PSAR{:d}maximum'.format(lineNumber)])): self.objectConfig['PSAR{:d}start'.format(lineNumber)] = start
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['PSAR{:d}start'.format(lineNumber)] = 0.020
                            self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_STARTINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}start'.format(lineNumber)]))
                        if (start_previous != self.objectConfig['PSAR{:d}start'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #Acceleration
                        acceleration_previous = self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)]
                        reset = False
                        try:
                            acceleration = round(float(self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_ACCELERATIONINPUT".format(lineNumber)].getText()), 3)
                            if (0 < acceleration): self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)] = acceleration
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)] = 0.020
                            self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_ACCELERATIONINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)]))
                        if (acceleration_previous != self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #Size
                        size_previous = self.objectConfig['PSAR{:d}Size'.format(lineNumber)]
                        reset = False
                        try:
                            size = int(self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_SIZEINPUT".format(lineNumber)].getText())
                            if (0 < size): self.objectConfig['PSAR{:d}Size'.format(lineNumber)] = size
                            else: reset = False
                        except: reset = False
                        if (reset == True):
                            self.objectConfig['PSAR{:d}Size'.format(lineNumber)] = 1
                            self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_SIZEINPUT".format(lineNumber)].updateText(str(self.objectConfig['PSAR{:d}Size'.format(lineNumber)]))
                        if (size_previous != self.objectConfig['PSAR{:d}Size'.format(lineNumber)]): updateTracker[lineNumber][1] = True
                        #Color
                        color_previous = (self.objectConfig['PSAR{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['PSAR{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['PSAR{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['PSAR{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_LINECOLOR".format(lineNumber)].getColor()
                        self.objectConfig['PSAR{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)] = color_r
                        self.objectConfig['PSAR{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)] = color_g
                        self.objectConfig['PSAR{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)] = color_b
                        self.objectConfig['PSAR{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): updateTracker[lineNumber][1] = True
                        #Line Display
                        display_previous = self.objectConfig['PSAR{:d}Display'.format(lineNumber)]
                        self.objectConfig['PSAR{:d}Display'.format(lineNumber)] = self.settingsSubPages['PSAR'].GUIOs["INDICATOR_PSAR{:d}_DISPLAY".format(lineNumber)].getStatus()
                        if (display_previous != self.objectConfig['PSAR{:d}Display'.format(lineNumber)]): updateTracker[lineNumber][1] = True
                    #PSAR Compute
                    computePSAR_previous = self.objectConfig['PSARCompute']
                    self.objectConfig['PSARCompute'] = self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_PSAR"].getStatus()
                    if ((computePSAR_previous == False) and (self.objectConfig['PSARCompute'] == True)):
                        for lineNumber in updateTracker: updateTracker[lineNumber][0] = True

                #Configuration and Queue Update
                configuredPSARs = self.__configureAnalysisParams('PSAR')
                for configuredPSAR in configuredPSARs:
                    lineNumber = self.klines_analysisParams[configuredPSAR]['lineNumber']
                    if (updateTracker[lineNumber][0] == True):
                        self.__removeAnalysisData(analysisCode = configuredPSAR, removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = configuredPSAR, analysisMode = 0)                   #Update process queue
                    elif (updateTracker[lineNumber][1] == True):
                        self.__removeAnalysisData(analysisCode = configuredPSAR, removalType = 2, removalType_Graphics = None) #Remove previous graphics
                        self.__addDrawQueuesToBufferZone(analysisCode = configuredPSAR, drawSignal = _FULLDRAWSIGNALS['PSAR']) #Update draw queue

                #Control Buttons Handling
                self.settingsSubPages['PSAR'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True

        #Subpage 'BOL'
        elif (indicatorType == 'BOL'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):
                lineSelected = self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:s}_LINECOLOR".format(lineSelected)].getColor()
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):
                contentType = guioName_split[2]
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):
                lineSelected = self.settingsSubPages['BOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:s}_LINECOLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['BOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'LineActivationSwitch'):  
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'BandWidthTextInputBox'): 
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'IntervalTextInputBox'):  
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'WidthTextInputBox'):     
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'):         
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplayContentsSwitch'): 
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'MATypeSelectionBox'):    
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = dict()

                #Check for any changes in the configuration
                if (True):
                    for lineIndex in range (_NMAXLINES['BOL']):
                        lineNumber = lineIndex+1
                        updateTracker[lineNumber] = [False, False, False] #[1]: Analyze, [2]: Draw CenterLine, [3]: Draw Band
                        #Compute
                        compute_previous = self.objectConfig['BOL{:d}Compute'.format(lineNumber)]
                        self.objectConfig['BOL{:d}Compute'.format(lineNumber)] = self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}".format(lineNumber)].getStatus()
                        if ((compute_previous == False) and (self.objectConfig['BOL{:d}Compute'.format(lineNumber)] == True)): updateTracker[lineNumber][0] = True
                        #Interval
                        interval_previous = self.objectConfig['BOL{:d}nSamples'.format(lineNumber)]
                        reset = False
                        try:
                            interval = int(self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_INTERVALINPUT".format(lineNumber)].getText())
                            if (0 < interval): self.objectConfig['BOL{:d}nSamples'.format(lineNumber)] = interval
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['BOL{:d}nSamples'.format(lineNumber)] = 1
                            self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_INTERVALINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}nSamples'.format(lineNumber)]))
                        if (interval_previous != self.objectConfig['BOL{:d}nSamples'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #BandWidth
                        bandWidth_previous = self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)]
                        reset = False
                        try:
                            bandWidth = float(self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_BANDWIDTHINPUT".format(lineNumber)].getText())
                            if (0 < bandWidth): self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)] = bandWidth
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)] = 2.0
                            self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_BANDWIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)]))
                        if (bandWidth_previous != self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #Width
                        width_previous = self.objectConfig['BOL{:d}Width'.format(lineNumber)]
                        reset = False
                        try:
                            width = int(self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_WIDTHINPUT".format(lineNumber)].getText())
                            if (0 < width): self.objectConfig['BOL{:d}Width'.format(lineNumber)] = width
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['BOL{:d}Width'.format(lineNumber)] = 1
                            self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_WIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['BOL{:d}Width'.format(lineNumber)]))
                        if (width_previous != self.objectConfig['BOL{:d}Width'.format(lineNumber)]): updateTracker[lineNumber][1] = True
                        #Color
                        color_previous = (self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)],
                                          self.objectConfig['BOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_LINECOLOR".format(lineNumber)].getColor()
                        self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)] = color_r
                        self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)] = color_g
                        self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)] = color_b
                        self.objectConfig['BOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): updateTracker[lineNumber][1] = True; updateTracker[lineNumber][2] = True
                        #Line Display
                        display_previous = self.objectConfig['BOL{:d}Display'.format(lineNumber)]
                        self.objectConfig['BOL{:d}Display'.format(lineNumber)] = self.settingsSubPages['BOL'].GUIOs["INDICATOR_BOL{:d}_DISPLAY".format(lineNumber)].getStatus()
                        if (display_previous != self.objectConfig['BOL{:d}Display'.format(lineNumber)]): updateTracker[lineNumber][1] = True; updateTracker[lineNumber][2] = True
                    #BOL Compute
                    computeBol_previous = self.objectConfig['BOLCompute']
                    self.objectConfig['BOLCompute'] = self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_BOL"].getStatus()
                    if ((computeBol_previous == False) and (self.objectConfig['BOLCompute'] == True)):
                        for lineNumber in updateTracker: updateTracker[lineNumber][0] = True
                    #MA Type
                    bolMAType_previous = self.objectConfig['BOLMAType']
                    self.objectConfig['BOLMAType'] = self.settingsSubPages['BOL'].GUIOs["INDICATOR_MATYPESELECTION"].getSelected()
                    if (bolMAType_previous != self.objectConfig['BOLMAType']): 
                        for lineNumber in updateTracker: updateTracker[lineNumber][0] = True
                    #CenterLine Display Switch
                    display_bolCenter_previous = self.objectConfig['BOLdisplayCenterLine']
                    self.objectConfig['BOLdisplayCenterLine'] = self.settingsSubPages['BOL'].GUIOs["INDICATOR_DISPLAYCONTENTS_BOLCENTERSWITCH"].getStatus()
                    if (display_bolCenter_previous != self.objectConfig['BOLdisplayCenterLine']): 
                        for lineNumber in updateTracker: updateTracker[lineNumber][1] = True
                    #Band Display Switch
                    display_bolBand_previous = self.objectConfig['BOLdisplayBand']
                    self.objectConfig['BOLdisplayBand'] = self.settingsSubPages['BOL'].GUIOs["INDICATOR_DISPLAYCONTENTS_BOLBANDSWITCH"].getStatus()
                    if (display_bolBand_previous != self.objectConfig['BOLdisplayBand']): 
                        for lineNumber in updateTracker: updateTracker[lineNumber][2] = True

                #Configuration and Queue Update
                configuredBOLs = self.__configureAnalysisParams('BOL')
                for configuredBOL in configuredBOLs:
                    lineNumber = self.klines_analysisParams[configuredBOL]['lineNumber']
                    if (updateTracker[lineNumber][0] == True):
                        self.__removeAnalysisData(analysisCode = configuredBOL, removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = configuredBOL, analysisMode = 0)                   #Update process queue
                    else:
                        drawSignal = 0
                        drawSignal += 0b01*updateTracker[lineNumber][1] #CenterLine
                        drawSignal += 0b10*updateTracker[lineNumber][2] #Band
                        if (0 < drawSignal):
                            self.__removeAnalysisData(analysisCode = configuredBOL, removalType = 2, removalType_Graphics = drawSignal) #Remove previous graphics
                            self.__addDrawQueuesToBufferZone(analysisCode = configuredBOL, drawSignal = drawSignal)                     #Update draw queue

                #Control Buttons Handling
                self.settingsSubPages['BOL'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True

        #Subpage 'IVP'
        elif (indicatorType == 'IVP'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):
                lineSelected = self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVP{:s}_COLOR".format(lineSelected)].getColor()
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):
                contentType = guioName_split[2]
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):
                lineSelected = self.settingsSubPages['IVP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVP{:s}_COLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['IVP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'): 
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplayWidthSlider'):
                lineTarget = guioName_split[2]
                sliderValue = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVP{:s}_DISPLAYWIDTHSLIDER".format(lineTarget)].getSliderValue()
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVP{:s}_DISPLAYWIDTHVALUETEXT".format(lineTarget)].updateText(str(round(sliderValue/100*0.9+0.1, 2)))
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'UseBollingerEnhancement'): 
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'UseActiveDivisionControl'):
                if (self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_USEADCSWITCH"].getStatus() == True): self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_NDIVISIONSINPUT"].deactivate()
                else:                                                                                         self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_NDIVISIONSINPUT"].activate()
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'IntervalTextInputBox'):   
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'MinGammaFactor'):
                sliderValue = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_MINGAMMAFACTORSLIDER"].getSliderValue()
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_MINGAMMAFACTORVALUETEXT"].updateText("{:.2f} %".format(round(sliderValue/100*1.95+0.05, 2)))
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'UseActiveGammaFactor'):  
                if (self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_USEAGFSWITCH"].getStatus() == True): 
                    self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFREFLENINPUT"].activate()
                    self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFMATYPESELECTION"].activate()
                else:                                                                                              
                    self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFREFLENINPUT"].deactivate()
                    self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFMATYPESELECTION"].deactivate()
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'AGFRefLenInputBox'):     
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'AGFMATypeSelectionBox'): 
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ClusteringRange'):
                sliderValue = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CLUSTERINGRANGESLIDER"].getSliderValue()
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CLUSTERINGRANGEVALUETEXT"].updateText("{:.1f} %".format(round(sliderValue/100*98+2, 1)))
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ECMinInputBox'): 
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ECMaxInputBox'): 
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'CSAccelerationFactor'):
                sliderValue = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CSACCELERATIONFACTORSLIDER"].getSliderValue()
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CSACCELERATIONFACTORVALUETEXT"].updateText("{:.2f}".format(round(sliderValue/100*0.95+0.05, 2)))
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'AnchorRangerFactor'):
                sliderValue = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ANCHORRANGERFACTORSLIDER"].getSliderValue()
                self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ANCHORRANGERFACTORVALUETEXT"].updateText("{:.2f}".format(round(sliderValue/100*0.9+0.1, 2)))
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = [False, False, False, False, False, False] #[0]: Analyze, [1]: Draw RAW, [2]: Draw Extension, [3]: Draw Positional, [4]: Draw Current Anchor, [5]: Draw Previous Anchor

                #Check for any changes in the configuration
                if (True):
                    #Computation
                    previous_Compute = self.objectConfig['IVPCompute']
                    self.objectConfig['IVPCompute'] = self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_IVP"].getStatus()
                    if (previous_Compute != self.objectConfig['IVPCompute']): updateTracker[0] = True
                    #Bollinger Enhancement
                    previous_useBLE = self.objectConfig['IVPUseBLE']
                    self.objectConfig['IVPUseBLE'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_USEBLESWITCH"].getStatus()
                    if (previous_useBLE != self.objectConfig['IVPUseBLE']): updateTracker[0] = True
                    #Interval
                    previous_nSamples = self.objectConfig['IVPnSamples']
                    reset = False
                    try:
                        interval = int(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_INTERVALINPUT"].getText())
                        if (0 < interval): self.objectConfig['IVPnSamples'] = interval
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['IVPnSamples'] = 500
                        self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_INTERVALINPUT"].updateText(str(self.objectConfig['IVPnSamples']))
                    if (previous_nSamples != self.objectConfig['IVPnSamples']): updateTracker[0] = True
                    #gammaFactor - minGammaFactor_perc
                    previous_minGammaFactor_perc = self.objectConfig['IVPMinGammaFactorPerc']
                    self.objectConfig['IVPMinGammaFactorPerc'] = round(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_MINGAMMAFACTORSLIDER"].getSliderValue()/100*1.95+0.05, 2)
                    if (previous_minGammaFactor_perc != self.objectConfig['IVPMinGammaFactorPerc']): updateTracker[0] = True
                    #gammaFactor - useAGF
                    previous_useAGF = self.objectConfig['IVPUseAGF']
                    self.objectConfig['IVPUseAGF'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_USEAGFSWITCH"].getStatus()
                    if (previous_useAGF != self.objectConfig['IVPUseAGF']): updateTracker[0] = True
                    #gammaFactor - AGFRefLen
                    previous_AGFRefLen = self.objectConfig['IVPAGFRefLen']
                    reset = False
                    try:
                        afgRefLen = int(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFREFLENINPUT"].getText())
                        if (60 <= afgRefLen): self.objectConfig['IVPAGFRefLen'] = afgRefLen
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['IVPAGFRefLen'] = 120
                        self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFREFLENINPUT"].updateText(str(self.objectConfig['IVPAGFRefLen']))
                    if (previous_AGFRefLen != self.objectConfig['IVPAGFRefLen']): updateTracker[0] = True
                    #gammaFactor - AGFMAType
                    previous_AGFMAType = self.objectConfig['IVPAGFMAType']
                    self.objectConfig['IVPAGFMAType'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_AGFMATYPESELECTION"].getSelected()
                    if (previous_AGFMAType != self.objectConfig['IVPAGFMAType']): updateTracker[0] = True
                    #displaySwitch - RAW
                    displaySwitch_RAW_prev = self.objectConfig['IVPRAWDisplay']
                    self.objectConfig['IVPRAWDisplay'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_DISPLAYSWITCH"].getStatus()
                    if (displaySwitch_RAW_prev != self.objectConfig['IVPRAWDisplay']): updateTracker[1] = True
                    #displaySwitch - IVPCExtension
                    displaySwitch_IVPCExtension_prev = self.objectConfig['IVPCExtension']
                    self.objectConfig['IVPCExtension'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCEXTENSION_DISPLAYSWITCH"].getStatus()
                    if (displaySwitch_IVPCExtension_prev != self.objectConfig['IVPCExtension']): updateTracker[2] = True
                    #displaySwitch - IVPCPositional
                    displaySwitch_IVPCPositional_prev = self.objectConfig['IVPCPositional']
                    self.objectConfig['IVPCPositional'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPOSITIONAL_DISPLAYSWITCH"].getStatus()
                    if (displaySwitch_IVPCPositional_prev != self.objectConfig['IVPCPositional']): updateTracker[3] = True
                    #displaySwitch - IVPCCurrentAnchor
                    displaySwitch_IVPCCurrentAnchor_prev = self.objectConfig['IVPCCURRENTANCHORDisplay']
                    self.objectConfig['IVPCCURRENTANCHORDisplay'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCCURRENTANCHOR_DISPLAYSWITCH"].getStatus()
                    if (displaySwitch_IVPCCurrentAnchor_prev != self.objectConfig['IVPCCURRENTANCHORDisplay']): updateTracker[4] = True
                    #displaySwitch - IVPCPreviousAnchor
                    displaySwitch_IVPCPreviousAnchor_prev = self.objectConfig['IVPCPREVANCHORDisplay']
                    self.objectConfig['IVPCPREVANCHORDisplay'] = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPREVANCHOR_DISPLAYSWITCH"].getStatus()
                    if (displaySwitch_IVPCPreviousAnchor_prev != self.objectConfig['IVPCPREVANCHORDisplay']): updateTracker[5] = True
                    #displayWidth
                    previous_displayWidth_raw = self.objectConfig['IVPRAWDisplayWidth']
                    self.objectConfig['IVPRAWDisplayWidth'] = round(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_DISPLAYWIDTHSLIDER"].getSliderValue()/100*0.9+0.1, 2)
                    if (previous_displayWidth_raw != self.objectConfig['IVPRAWDisplayWidth']): updateTracker[1] = True
                    #IVPRaw Color
                    previous_color_raw = (self.objectConfig['IVPRAWcolorR%{:s}'.format(self.currentGUITheme)],
                                          self.objectConfig['IVPRAWcolorG%{:s}'.format(self.currentGUITheme)],
                                          self.objectConfig['IVPRAWcolorB%{:s}'.format(self.currentGUITheme)],
                                          self.objectConfig['IVPRAWcolorA%{:s}'.format(self.currentGUITheme)])
                    ivpRaw_color = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPRAW_COLOR"].getColor()
                    self.objectConfig['IVPRAWcolorR%{:s}'.format(self.currentGUITheme)] = ivpRaw_color[0]
                    self.objectConfig['IVPRAWcolorG%{:s}'.format(self.currentGUITheme)] = ivpRaw_color[1]
                    self.objectConfig['IVPRAWcolorB%{:s}'.format(self.currentGUITheme)] = ivpRaw_color[2]
                    self.objectConfig['IVPRAWcolorA%{:s}'.format(self.currentGUITheme)] = ivpRaw_color[3]
                    if (previous_color_raw != tuple(ivpRaw_color)): updateTracker[1] = True
                    #IVPC Current Anchor
                    previous_color_cCurrentAnchor = (self.objectConfig['IVPCCURRENTANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                     self.objectConfig['IVPCCURRENTANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                     self.objectConfig['IVPCCURRENTANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                     self.objectConfig['IVPCCURRENTANCHORcolorA%{:s}'.format(self.currentGUITheme)])
                    cCurrentAnchor_color = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCCURRENTANCHOR_COLOR"].getColor()
                    self.objectConfig['IVPCCURRENTANCHORcolorR%{:s}'.format(self.currentGUITheme)] = cCurrentAnchor_color[0]
                    self.objectConfig['IVPCCURRENTANCHORcolorG%{:s}'.format(self.currentGUITheme)] = cCurrentAnchor_color[1]
                    self.objectConfig['IVPCCURRENTANCHORcolorB%{:s}'.format(self.currentGUITheme)] = cCurrentAnchor_color[2]
                    self.objectConfig['IVPCCURRENTANCHORcolorA%{:s}'.format(self.currentGUITheme)] = cCurrentAnchor_color[3]
                    if (previous_color_cCurrentAnchor != tuple(cCurrentAnchor_color)): updateTracker[4] = True
                    #IVPC Previous Anchor
                    previous_color_cPrevAnchor = (self.objectConfig['IVPCPREVANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                  self.objectConfig['IVPCPREVANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                  self.objectConfig['IVPCPREVANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                  self.objectConfig['IVPCPREVANCHORcolorA%{:s}'.format(self.currentGUITheme)])
                    cPrevAnchor_color = self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPCPREVANCHOR_COLOR"].getColor()
                    self.objectConfig['IVPCPREVANCHORcolorR%{:s}'.format(self.currentGUITheme)] = cPrevAnchor_color[0]
                    self.objectConfig['IVPCPREVANCHORcolorG%{:s}'.format(self.currentGUITheme)] = cPrevAnchor_color[1]
                    self.objectConfig['IVPCPREVANCHORcolorB%{:s}'.format(self.currentGUITheme)] = cPrevAnchor_color[2]
                    self.objectConfig['IVPCPREVANCHORcolorA%{:s}'.format(self.currentGUITheme)] = cPrevAnchor_color[3]
                    if (previous_color_cPrevAnchor != tuple(cPrevAnchor_color)): updateTracker[5] = True
                    #ClusteringRange
                    previous_ClusteringRange = self.objectConfig['IVPClusteringRange']
                    self.objectConfig['IVPClusteringRange'] = round(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CLUSTERINGRANGESLIDER"].getSliderValue()/100*98+2, 1)
                    if (previous_ClusteringRange != self.objectConfig['IVPClusteringRange']): updateTracker[0] = True
                    #ECMax
                    previous_ECMax = self.objectConfig['IVPCExistenceCounterMax']
                    reset = False
                    try:
                        ecMax = int(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMAXTEXTINPUT"].getText())
                        if (5 < ecMax): self.objectConfig['IVPCExistenceCounterMax'] = ecMax
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['IVPCExistenceCounterMax'] = 5
                        self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMAXTEXTINPUT"].updateText(str(self.objectConfig['IVPCExistenceCounterMax']))
                    if (previous_ECMax != self.objectConfig['IVPCExistenceCounterMax']): updateTracker[0] = True
                    #ECMin
                    previous_ECMin = self.objectConfig['IVPCExistenceCounterMin']
                    reset = False
                    try:
                        ecMin = int(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMINTEXTINPUT"].getText())
                        if ((1 <= ecMin) and (ecMin < self.objectConfig['IVPCExistenceCounterMax'])): self.objectConfig['IVPCExistenceCounterMin'] = ecMin
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['IVPCExistenceCounterMin'] = 1
                        self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ECMINTEXTINPUT"].updateText(str(self.objectConfig['IVPCExistenceCounterMin']))
                    if (previous_ECMin != self.objectConfig['IVPCExistenceCounterMin']): updateTracker[0] = True
                    #CSAccelerationFactor
                    previous_CSAccelerationFactor = self.objectConfig['IVPCCSAccelerationFactor']
                    self.objectConfig['IVPCCSAccelerationFactor'] = round(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_CSACCELERATIONFACTORSLIDER"].getSliderValue()/100*0.95+0.05, 2)
                    if (previous_CSAccelerationFactor != self.objectConfig['IVPCCSAccelerationFactor']): updateTracker[0] = True
                    #AnchorRangerFactor
                    previous_AnchorRangerFactor = self.objectConfig['IVPCAnchorRangerFactor']
                    self.objectConfig['IVPCAnchorRangerFactor'] = round(self.settingsSubPages['IVP'].GUIOs["INDICATOR_IVPFILTERED_ANCHORRANGERFACTORSLIDER"].getSliderValue()/100*0.9+0.1, 2)
                    if (previous_AnchorRangerFactor != self.objectConfig['IVPCAnchorRangerFactor']): updateTracker[0] = True

                #Content Update Handling
                if (updateTracker[0] == True):
                    configurationResult = self.__configureAnalysisParams('IVP')
                    if (configurationResult == True):
                        self.__removeAnalysisData(analysisCode = 'IVP', removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = 'IVP', analysisMode = 0)                   #Update process queue
                elif ('IVP' in self.klines_analysisParams):
                    drawSignal = 0
                    drawSignal += 0b00001*updateTracker[1] #RAW
                    drawSignal += 0b00010*updateTracker[2] #IVPC Extension
                    drawSignal += 0b00100*updateTracker[3] #IVPC Positional
                    drawSignal += 0b01000*updateTracker[4] #IVPC Anchor
                    drawSignal += 0b10000*updateTracker[5] #IVPC Anchor Previous
                    if (0 < drawSignal):
                        self.__removeAnalysisData(analysisCode = 'IVP', removalType = 2, removalType_Graphics = drawSignal) #Remove previous graphics
                        self.__addDrawQueuesToBufferZone(analysisCode = 'IVP', drawSignal = drawSignal)                     #Update draw queue

                #Settings Control Button
                self.settingsSubPages['IVP'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True
                
        #Subpage 'PIP'
        elif (indicatorType == 'PIP'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):
                lineSelected = self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['PIP'].GUIOs["INDICATOR_{:s}_COLOR".format(lineSelected)].getColor()
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):
                contentType = guioName_split[2]
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):
                lineSelected = self.settingsSubPages['PIP'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['PIP'].GUIOs["INDICATOR_{:s}_COLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['PIP'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['PIP'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = [False, False] #[0]: Re-Analyze, [1]: Re-draw
                
                #Check for any changes in the configuration
                if (True):
                    #Computation
                    previous_Compute = self.objectConfig['PIPCompute']
                    self.objectConfig['PIPCompute'] = self.settingsSubPages['MAIN'].GUIOs["MAININDICATOR_PIP"].getStatus()
                    if (previous_Compute != self.objectConfig['PIPCompute']): updateTracker[0] = True
                    #Colors
                    for targetLine in ('BUYPOS', 'SELLPOS'):
                        color_previous = (self.objectConfig['PIP{:s}colorR%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['PIP{:s}colorG%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['PIP{:s}colorB%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['PIP{:s}colorA%{:s}'.format(targetLine, self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages['PIP'].GUIOs["INDICATOR_{:s}_COLOR".format(targetLine)].getColor()
                        self.objectConfig['PIP{:s}colorR%{:s}'.format(targetLine, self.currentGUITheme)] = color_r
                        self.objectConfig['PIP{:s}colorG%{:s}'.format(targetLine, self.currentGUITheme)] = color_g
                        self.objectConfig['PIP{:s}colorB%{:s}'.format(targetLine, self.currentGUITheme)] = color_b
                        self.objectConfig['PIP{:s}colorA%{:s}'.format(targetLine, self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): updateTracker[1] = True
                    
                #Content Update Handling
                if (updateTracker[0] == True):
                    configurationResult = self.__configureAnalysisParams('PIP')
                    if (configurationResult == True):
                        self.__removeAnalysisData(analysisCode = 'PIP', removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = 'PIP', analysisMode = 0)                   #Update process queue
                elif ((updateTracker[1] == True) and ('PIP' in self.klines_analysisParams)):
                    self.__removeAnalysisData(analysisCode = 'PIP', removalType = 2, removalType_Graphics = None)     #Remove previous graphics
                    self.__addDrawQueuesToBufferZone(analysisCode = 'PIP', drawSignal = _FULLDRAWSIGNALS['PIP'])      #Update draw queue

                #Settings Control Button
                self.settingsSubPages['PIP'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True
        
        #Subpage 'VOL'
        elif (indicatorType == 'VOL'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):       
                lineSelected = self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:s}_LINECOLOR".format(lineSelected)].getColor()
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):                
                contentType = guioName_split[2]
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):           
                lineSelected = self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:s}_LINECOLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['VOL'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'LineActivationSwitch'): 
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'IntervalTextInputBox'): 
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'WidthTextInputBox'):    
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'):        
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'VolTypeSelection'):     
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'MATypeSelection'):      
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):        
                #UpdateTracker Initialization
                updateTracker = {'VOL': [False, False]}

                #Check for any changes in the configuration
                if (True):
                    for lineIndex in range (_NMAXLINES['VOL']):
                        lineNumber = lineIndex+1
                        updateTracker[lineNumber] = [False, False]
                        #Compute
                        compute_previous = self.objectConfig['VOL{:d}Compute'.format(lineNumber)]
                        self.objectConfig['VOL{:d}Compute'.format(lineNumber)] = self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}".format(lineNumber)].getStatus()
                        if ((compute_previous == False) and (self.objectConfig['VOL{:d}Compute'.format(lineNumber)] == True)): updateTracker[lineNumber][0] = True
                        #Interval
                        interval_previous = self.objectConfig['VOL{:d}nSamples'.format(lineNumber)]
                        reset = False
                        try:
                            interval = int(self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_INTERVALINPUT".format(lineNumber)].getText())
                            if (0 < interval): self.objectConfig['VOL{:d}nSamples'.format(lineNumber)] = interval
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['VOL{:d}nSamples'.format(lineNumber)] = 1
                            self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_INTERVALINPUT".format(lineNumber)].updateText(str(self.objectConfig['VOL{:d}nSamples'.format(lineNumber)]))
                        if (interval_previous != self.objectConfig['VOL{:d}nSamples'.format(lineNumber)]): updateTracker[lineNumber][0] = True
                        #Width
                        width_previous = self.objectConfig['VOL{:d}Width'.format(lineNumber)]
                        reset = False
                        try:
                            width = int(self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_WIDTHINPUT".format(lineNumber)].getText())
                            if (0 < width): self.objectConfig['VOL{:d}Width'.format(lineNumber)] = width
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['VOL{:d}Width'.format(lineNumber)] = 1
                            self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_WIDTHINPUT".format(lineNumber)].updateText(str(self.objectConfig['VOL{:d}Width'.format(lineNumber)]))
                        if (width_previous != self.objectConfig['VOL{:d}Width'.format(lineNumber)]): updateTracker[lineNumber][1] = True
                        #Color
                        color_previous = (self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)], 
                                          self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_LINECOLOR".format(lineNumber)].getColor()
                        self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber,self.currentGUITheme)] = color_r
                        self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber,self.currentGUITheme)] = color_g
                        self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber,self.currentGUITheme)] = color_b
                        self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber,self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): updateTracker[lineNumber][1] = True
                        #Line Display
                        display_previous = self.objectConfig['VOL{:d}Display'.format(lineNumber)]
                        self.objectConfig['VOL{:d}Display'.format(lineNumber)] = self.settingsSubPages['VOL'].GUIOs["INDICATOR_VOL{:d}_DISPLAY".format(lineNumber)].getStatus()
                        if (display_previous != self.objectConfig['VOL{:d}Display'.format(lineNumber)]): updateTracker[lineNumber][1] = True
                    #VOL Compute
                    computeVOL_previous = self.objectConfig['VOLCompute']
                    self.objectConfig['VOLCompute'] = self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_VOL"].getStatus()
                    if (computeVOL_previous != self.objectConfig['VOLCompute']):
                        updateTracker['VOL'][0] = True
                        for targetLine in updateTracker: updateTracker[targetLine][0] = True
                    #VOLType
                    volType_previous = self.objectConfig['VOLType']
                    self.objectConfig['VOLType'] = self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_VOLTYPESELECTION"].getSelected()
                    if (volType_previous != self.objectConfig['VOLType']):
                        updateTracker['VOL'][0] = True
                        for targetLine in updateTracker: updateTracker[targetLine][0] = True
                    #VOLMAType
                    volMAType_previous = self.objectConfig['VOLMAType']
                    self.objectConfig['VOLMAType'] = self.settingsSubPages['VOL'].GUIOs["INDICATORCOLOR_MATYPESELECTION"].getSelected()
                    if (volMAType_previous != self.objectConfig['VOLMAType']):
                        for maLineIndex in range (_NMAXLINES['VOL']): updateTracker[maLineIndex+1][0] = True

                #Configuration and Queue Update
                configuredVOLs = self.__configureAnalysisParams('VOL')
                for configuredVOL in configuredVOLs:
                    lineNumber = self.klines_analysisParams[configuredVOL]['lineNumber']
                    if (updateTracker[lineNumber][0] == True):
                        self.__removeAnalysisData(analysisCode = configuredVOL, removalType = 1, removalType_Graphics = None) #Remove previous graphics and analysis
                        self.__addProcessQueuesToBufferZone(analysisCode = configuredVOL, analysisMode = 0)                   #Update process queue
                    elif (updateTracker[lineNumber][1] == True):
                        self.__removeAnalysisData(analysisCode = configuredVOL, removalType = 2, removalType_Graphics = None) #Remove previous graphics
                        self.__addDrawQueuesToBufferZone(analysisCode = configuredVOL, drawSignal = _FULLDRAWSIGNALS['VOL']) #Update draw queue

                #Control Buttons Handling
                self.settingsSubPages['VOL'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True

        #Subpage 'MMACD'
        elif (indicatorType == 'MMACD'):
            setterType = guioName_split[1]
            if (setterType == 'LineSelectionBox'):                
                lineSelected = self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r, color_g, color_b, color_a = self.settingsSubPages['MMACD'].GUIOs["INDICATOR_{:s}_COLOR".format(lineSelected)].getColor()
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_LED'].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_R_VALUE"].updateText(str(color_r))
                self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_G_VALUE"].updateText(str(color_g))
                self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_B_VALUE"].updateText(str(color_b))
                self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_A_VALUE"].updateText(str(color_a))
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_R_SLIDER'].setSliderValue(color_r/255*100)
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_G_SLIDER'].setSliderValue(color_g/255*100)
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_B_SLIDER'].setSliderValue(color_b/255*100)
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_A_SLIDER'].setSliderValue(color_a/255*100)
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
            elif (setterType == 'Color'):                         
                contentType = guioName_split[2]
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_LED'].updateColor(rValue = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100),
                                                                                     gValue = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100),
                                                                                     bValue = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100),
                                                                                     aValue = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100))
                self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_{:s}_VALUE".format(contentType)].updateText(str(int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_{:s}_SLIDER'.format(contentType)].getSliderValue()*255/100)))
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].activate()
            elif (setterType == 'ApplyColor'):                    
                lineSelected = self.settingsSubPages['MMACD'].GUIOs["INDICATORCOLOR_TARGETSELECTION"].getSelected()
                color_r = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_R_SLIDER'].getSliderValue()*255/100)
                color_g = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_G_SLIDER'].getSliderValue()*255/100)
                color_b = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_B_SLIDER'].getSliderValue()*255/100)
                color_a = int(self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_A_SLIDER'].getSliderValue()*255/100)
                self.settingsSubPages['MMACD'].GUIOs["INDICATOR_{:s}_COLOR".format(lineSelected)].updateColor(color_r, color_g, color_b, color_a)
                self.settingsSubPages['MMACD'].GUIOs['INDICATORCOLOR_APPLYCOLOR'].deactivate()
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'DisplaySwitch'):                 
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'SignalIntervalTextInputBox'):    
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'MSDeltaMAIntervalTextInputBox'): 
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'LineActivationSwitch'):          
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'IntervalTextInputBox'):          
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].activate()
            elif (setterType == 'ApplySettings'):
                #UpdateTracker Initialization
                updateTracker = [False, False, False, False] #[0]: Analyze, [1]: Draw MMACD, [2]: Draw SIGNAL, [3]: Draw HISTOGRAM

                #Check for any changes in the configuration
                if (True):
                    #Computation
                    computeMMACD_prev = self.objectConfig['MMACDCompute']
                    self.objectConfig['MMACDCompute'] = self.settingsSubPages['MAIN'].GUIOs["SUBINDICATOR_MMACD"].getStatus()
                    if (computeMMACD_prev != self.objectConfig['MMACDCompute']): updateTracker[0] = True
                    #Signal Interval
                    signalInterval_prev = self.objectConfig['MMACDSignalInterval']
                    reset = False
                    try:
                        signalInterval = int(self.settingsSubPages['MMACD'].GUIOs["INDICATOR_SIGNALINTERVALTEXTINPUT"].getText())
                        if (0 < signalInterval): self.objectConfig['MMACDSignalInterval'] = signalInterval
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['MMACDSignalInterval'] = 10
                        self.settingsSubPages['MMACD'].GUIOs["INDICATOR_SIGNALINTERVALTEXTINPUT"].updateText(str(self.objectConfig['MMACDSignalInterval']))
                    if (signalInterval_prev != self.objectConfig['MMACDSignalInterval']): updateTracker[0] = True
                    #MSDeltaMA Interval
                    msDeltaMAInterval_prev = self.objectConfig['MMACDSignalDeltaMAInterval']
                    reset = False
                    try:
                        msDeltaMAInterval = int(self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MSDELTAMAINTERVALTEXTINPUT"].getText())
                        if (0 < msDeltaMAInterval): self.objectConfig['MMACDSignalDeltaMAInterval'] = msDeltaMAInterval
                        else: reset = True
                    except: reset = True
                    if (reset == True):
                        self.objectConfig['MMACDSignalDeltaMAInterval'] = 5
                        self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MSDELTAMAINTERVALTEXTINPUT"].updateText(str(self.objectConfig['MMACDSignalDeltaMAInterval']))
                    if (msDeltaMAInterval_prev != self.objectConfig['MMACDSignalDeltaMAInterval']): updateTracker[0] = True
                    #MA Activation
                    maActivationUpdated = False
                    for lineNumber in range (1, _NMAXLINES['MMACD']+1):
                        maActivation_prev = self.objectConfig['MMACD{:d}Compute'.format(lineNumber)]
                        self.objectConfig['MMACD{:d}Compute'.format(lineNumber)] = self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACDMA{:d}".format(lineNumber)].getStatus()
                        if (maActivation_prev != self.objectConfig['MMACD{:d}Compute'.format(lineNumber)]): maActivationUpdated = True
                    if (maActivationUpdated == True): updateTracker[0] = True
                    #MA Interval
                    maIntervalUpdated = False
                    for lineNumber in range (1, _NMAXLINES['MMACD']+1):
                        maInterval_prev = self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)]
                        reset = False
                        try:
                            maInterval = int(self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACDMA{:d}_INTERVALINPUT".format(lineNumber)].getText())
                            if (0 < maInterval): self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)] = maInterval
                            else: reset = True
                        except: reset = True
                        if (reset == True):
                            self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)] = 1
                            self.settingsSubPages['MMACD'].GUIOs["INDICATOR_MMACDMA{:d}_INTERVALINPUT".format(lineNumber)].updateText((str(self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)])))
                        if (maInterval_prev != self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)]): maIntervalUpdated = True
                    if (maIntervalUpdated == True): updateTracker[0] = True
                    #Colors
                    for targetLine in ('MMACD', 'SIGNAL', 'HISTOGRAM+', 'HISTOGRAM-'):
                        color_previous = (self.objectConfig['MMACD{:s}colorR%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['MMACD{:s}colorG%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['MMACD{:s}colorB%{:s}'.format(targetLine, self.currentGUITheme)],
                                          self.objectConfig['MMACD{:s}colorA%{:s}'.format(targetLine, self.currentGUITheme)])
                        color_r, color_g, color_b, color_a = self.settingsSubPages['MMACD'].GUIOs["INDICATOR_{:s}_COLOR".format(targetLine)].getColor()
                        self.objectConfig['MMACD{:s}colorR%{:s}'.format(targetLine, self.currentGUITheme)] = color_r
                        self.objectConfig['MMACD{:s}colorG%{:s}'.format(targetLine, self.currentGUITheme)] = color_g
                        self.objectConfig['MMACD{:s}colorB%{:s}'.format(targetLine, self.currentGUITheme)] = color_b
                        self.objectConfig['MMACD{:s}colorA%{:s}'.format(targetLine, self.currentGUITheme)] = color_a
                        if (color_previous != (color_r, color_g, color_b, color_a)): 
                            if   (targetLine == 'MMACD'):      updateTracker[1] = True
                            elif (targetLine == 'SIGNAL'):     updateTracker[2] = True
                            elif (targetLine == 'HISTOGRAM+'): updateTracker[3] = True
                            elif (targetLine == 'HISTOGRAM-'): updateTracker[3] = True
                    #Line Display
                    for targetLine in ('MMACD', 'SIGNAL', 'HISTOGRAM'):
                        displayStatus_prev = self.objectConfig['MMACD{:s}Display'.format(targetLine)]
                        self.objectConfig['MMACD{:s}Display'.format(targetLine)] = self.settingsSubPages['MMACD'].GUIOs["INDICATOR_{:s}_DISPLAYSWITCH".format(targetLine)].getStatus()
                        if (displayStatus_prev != self.objectConfig['MMACD{:s}Display'.format(targetLine)]):
                            if   (targetLine == 'MMACD'):     updateTracker[1] = True
                            elif (targetLine == 'SIGNAL'):    updateTracker[2] = True
                            elif (targetLine == 'HISTOGRAM'): updateTracker[3] = True

                #Content Update Handling
                if (updateTracker[0] == True):
                    configurationResult = self.__configureAnalysisParams('MMACD')
                    #If the configuration result is 'True' (Meaning MMACD is in analysisTarget list), update the process queue
                    if (configurationResult == True):
                        for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone): 
                            if (timestamp in self.klines_toProcess): self.klines_toProcess[timestamp]['MMACD'] = 0
                            else:                                    self.klines_toProcess[timestamp] = {'MMACD': 0}
                else:
                    if ('MMACD' in self.klines_analysisParams):
                        drawSignal = 0
                        drawSignal += 0b001*updateTracker[1] #MMACD
                        drawSignal += 0b010*updateTracker[2] #SIGNAL
                        drawSignal += 0b100*updateTracker[3] #HISTOGRAM
                        if (0 < drawSignal):
                            #Remove Previous Graphics
                            self.__removeAnalysisData(analysisCode = 'MMACD', removalType = 2, removalType_Graphics = drawSignal)
                            #Update Draw Queue
                            for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
                                if (timestamp in self.klines_processed) and ('MMACD' in self.klines_processed[timestamp]):
                                    if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp]['MMACD'] = drawSignal
                                    else:                                    self.klines_drawQueue[timestamp] = {'MMACD': drawSignal}

                #Control Buttons Handling
                self.settingsSubPages['MMACD'].GUIOs['APPLYNEWSETTINGS'].deactivate()
                activateSaveConfigButton = True

        if ((activateSaveConfigButton == True) and (self.settingsSubPages['MAIN'].GUIOs["AUX_SAVECONFIGURATION"].deactivated == True)): self.settingsSubPages['MAIN'].GUIOs["AUX_SAVECONFIGURATION"].activate()

    def __configureAnalysisParams(self, analysisType):
        if (analysisType == 'EVENTS'):
            self.klines_analysisParams['EVENTS'] = {}
            self.klines_analysisTargets['EVENTS'] = 0
            self.klines_analysisTargets_keySet.add('EVENTS')
            configurationResult = True

        elif (analysisType == 'SMA'):
            previousSMAs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:3] == 'SMA'])
            configuredSMAs = set()
            if (self.objectConfig['SMACompute'] == True):
                for lineIndex in range (_NMAXLINES['SMA']):
                    lineNumber = lineIndex+1
                    sma_compute   = self.objectConfig['SMA{:d}Compute'.format(lineNumber)]
                    sma_nSamples  = self.objectConfig['SMA{:d}nSamples'.format(lineNumber)]
                    sma_width     = self.objectConfig['SMA{:d}Width'.format(lineNumber)]
                    if ((sma_compute == True) and (0 < sma_nSamples) and (1 <= sma_width)):
                        analysisCode = "SMA_{:d}".format(sma_nSamples)
                        analysisParams = {'lineNumber': lineNumber,
                                          'nSamples':   sma_nSamples}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        configuredSMAs.add(analysisCode)
            for removedSMA in (previousSMAs-configuredSMAs): self.__removeAnalysisData(analysisCode = removedSMA, removalType = 0)
            configurationResult = configuredSMAs

        elif (analysisType == 'WMA'):
            previousWMAs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:3] == 'WMA'])
            configuredWMAs = set()
            if (self.objectConfig['WMACompute'] == True):
                for lineIndex in range (_NMAXLINES['WMA']):
                    lineNumber = lineIndex+1
                    wma_compute   = self.objectConfig['WMA{:d}Compute'.format(lineNumber)]
                    wma_nSamples  = self.objectConfig['WMA{:d}nSamples'.format(lineNumber)]
                    wma_width     = self.objectConfig['WMA{:d}Width'.format(lineNumber)]
                    if ((wma_compute == True) and (0 < wma_nSamples) and (1 <= wma_width)):
                        analysisCode = "WMA_{:d}".format(wma_nSamples)
                        analysisParams = {'lineNumber': lineNumber,
                                          'nSamples':   wma_nSamples}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        configuredWMAs.add(analysisCode)
            for removedWMA in (previousWMAs-configuredWMAs): self.__removeAnalysisData(analysisCode = removedWMA, removalType = 0)
            configurationResult = configuredWMAs

        elif (analysisType == 'EMA'):
            previousEMAs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:3] == 'EMA'])
            configuredEMAs = set()
            if (self.objectConfig['EMACompute'] == True):
                for lineIndex in range (_NMAXLINES['EMA']):
                    lineNumber = lineIndex+1
                    ema_compute   = self.objectConfig['EMA{:d}Compute'.format(lineNumber)]
                    ema_nSamples  = self.objectConfig['EMA{:d}nSamples'.format(lineNumber)]
                    ema_width     = self.objectConfig['EMA{:d}Width'.format(lineNumber)]
                    if ((ema_compute == True) and (0 < ema_nSamples) and (1 <= ema_width)):
                        analysisCode = "EMA_{:d}".format(ema_nSamples)
                        analysisParams = {'lineNumber': lineNumber,
                                          'nSamples':   ema_nSamples}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        configuredEMAs.add(analysisCode)
            for removedEMA in (previousEMAs-configuredEMAs): self.__removeAnalysisData(analysisCode = removedEMA, removalType = 0)
            configurationResult = configuredEMAs

        elif (analysisType == 'PSAR'):
            previousPSARs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:4] == 'PSAR'])
            configuredPSARs = set()
            if (self.objectConfig['PSARCompute'] == True):
                for lineIndex in range (_NMAXLINES['PSAR']):
                    lineNumber = lineIndex+1
                    psar_compute = self.objectConfig['PSAR{:d}Compute'.format(lineNumber)]
                    psar_start        = self.objectConfig['PSAR{:d}start'.format(lineNumber)]
                    psar_acceleration = self.objectConfig['PSAR{:d}acceleration'.format(lineNumber)]
                    psar_maximum      = self.objectConfig['PSAR{:d}maximum'.format(lineNumber)]
                    psar_size    = self.objectConfig['PSAR{:d}Size'.format(lineNumber)]
                    if ((psar_compute == True) and (0 <= psar_start) and (0 < psar_acceleration) and (0 < psar_maximum) and (1 <= psar_size)):
                        analysisCode = "PSAR_{:.3f}_{:.3f}_{:.3f}".format(psar_start, psar_acceleration, psar_maximum)
                        analysisParams = {'lineNumber': lineNumber,
                                          'start':        psar_start,
                                          'acceleration': psar_acceleration,
                                          'maximum':      psar_maximum}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        configuredPSARs.add(analysisCode)
            for removedPSAR in (previousPSARs-configuredPSARs): self.__removeAnalysisData(analysisCode = removedPSAR, removalType = 0)
            configurationResult = configuredPSARs

        elif (analysisType == 'BOL'):
            previousBOLs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:3] == 'BOL'])
            configuredBOLs = set()
            if (self.objectConfig['BOLCompute'] == True):
                for lineIndex in range (_NMAXLINES['BOL']):
                    lineNumber = lineIndex+1
                    bol_compute   = self.objectConfig['BOL{:d}Compute'.format(lineNumber)]
                    bol_nSamples  = self.objectConfig['BOL{:d}nSamples'.format(lineNumber)]
                    bol_bandWidth = self.objectConfig['BOL{:d}bandWidth'.format(lineNumber)]
                    bol_width     = self.objectConfig['BOL{:d}Width'.format(lineNumber)]
                    if ((bol_compute == True) and (0 < bol_nSamples) and (0 < bol_bandWidth) and (1 <= bol_width)):
                        analysisCode = "BOL_{:d}_{:.1f}".format(bol_nSamples, bol_bandWidth)
                        analysisParams = {'lineNumber': lineNumber,
                                          'maType':     self.objectConfig['BOLMAType'],
                                          'nSamples':   bol_nSamples,
                                          'bandWidth':  bol_bandWidth}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        configuredBOLs.add(analysisCode)
            for removedBOL in (previousBOLs-configuredBOLs): self.__removeAnalysisData(analysisCode = removedBOL, removalType = 0)
            configurationResult = configuredBOLs

        elif (analysisType == 'IVP'):
            if (self.objectConfig['IVPCompute'] == True):
                IVP_nSamples   = self.objectConfig['IVPnSamples']
                if (0 < IVP_nSamples):
                    analysisCode = "IVP"
                    analysisParams = {'nSamples':             IVP_nSamples,
                                      'useBLE':               self.objectConfig['IVPUseBLE'],
                                      'minGammaFactor':       round(self.objectConfig['IVPMinGammaFactorPerc']/100, 4),
                                      'useAGF':               self.objectConfig['IVPUseAGF'],
                                      'AGFRefLen':            self.objectConfig['IVPAGFRefLen'],
                                      'AGFMAType':            self.objectConfig['IVPAGFMAType'],
                                      'clusteringRange':      self.objectConfig['IVPClusteringRange'],
                                      'existenceCounter_min': self.objectConfig['IVPCExistenceCounterMin'],
                                      'existenceCounter_max': self.objectConfig['IVPCExistenceCounterMax'],
                                      'csAccelerationFactor': self.objectConfig['IVPCCSAccelerationFactor'],
                                      'anchorRangerFactor':   self.objectConfig['IVPCAnchorRangerFactor']}
                    self.klines_analysisParams[analysisCode] = analysisParams
                    if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                    self.klines_analysisTargets['IVP'] = 0
                    self.klines_analysisTargets_keySet.add('IVP')
                    configurationResult = True
                else: configurationResult = False
            else: configurationResult = False
            if (configurationResult == False): self.__removeAnalysisData('IVP', 0)

        elif (analysisType == 'PIP'):
            if (self.objectConfig['PIPCompute'] == True):
                analysisCode = "PIP"
                analysisParams = dict()
                self.klines_analysisParams[analysisCode] = analysisParams
                if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                self.klines_analysisTargets['PIP'] = 0
                self.klines_analysisTargets_keySet.add('PIP')
                #Update referer tracker
                referredAnalysisTypes = set(['IVP', 'PSAR', 'MMACD'])
                for existingAnalysisCode in self.klines_analysisTargets:
                    exsitingAnalysisCodeType = existingAnalysisCode.split("_")[0]
                    if (exsitingAnalysisCodeType in referredAnalysisTypes):
                        if (existingAnalysisCode in self.klines_analysisReferers): self.klines_analysisReferers[existingAnalysisCode]['PIP'] = 0
                        else:                                                      self.klines_analysisReferers[existingAnalysisCode] = {'PIP': 0}
                configurationResult = True
            else: configurationResult = False
            if (configurationResult == False): self.__removeAnalysisData('PIP', 0)

        elif (analysisType == 'VOL'):
            previousVOLs   = set([analysisCode for analysisCode in self.klines_analysisParams if analysisCode[:3] == 'VOL'])
            configuredVOLs = set()
            if (self.objectConfig['VOLCompute'] == True):
                analysisCode = "VOL"
                siViewerNumber = self.siTypes_siViewerAlloc['VOL']
                analysisParams = {'valueType': 0, 
                                  'volType': self.objectConfig['VOLType'],
                                  'lineNumber': 'VOL'}
                self.klines_analysisParams[analysisCode] = analysisParams
                if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                self.klines_analysisTargets['VOL'] = 0
                self.klines_analysisTargets_keySet.add('VOL')
                self.siTypes_analysisCodes['VOL'] = set(['VOL'])
                configuredVOLs.add('VOL')
                for lineIndex in range (_NMAXLINES['VOL']):
                    lineNumber = lineIndex+1
                    vol_compute   = self.objectConfig['VOL{:d}Compute'.format(lineNumber)]
                    vol_nSamples  = self.objectConfig['VOL{:d}nSamples'.format(lineNumber)]
                    vol_width     = self.objectConfig['VOL{:d}Width'.format(lineNumber)]
                    if ((vol_compute == True) and (0 < vol_nSamples) and (1 <= vol_width)):
                        analysisCode = "VOL_{:s}_{:d}".format(self.objectConfig['VOLMAType'], vol_nSamples)
                        analysisParams = {'valueType':  self.objectConfig['VOLMAType'],
                                          'volType':    self.objectConfig['VOLType'],
                                          'lineNumber': lineNumber,
                                          'nSamples':   vol_nSamples}
                        self.klines_analysisParams[analysisCode]  = analysisParams
                        if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                        self.klines_analysisTargets[analysisCode] = 0
                        self.klines_analysisTargets_keySet.add(analysisCode)
                        self.siTypes_analysisCodes[analysisType].add(analysisCode)
                        self.verticalValue_loaded["SIVIEWER{:d}".format(siViewerNumber)] = False
                        configuredVOLs.add(analysisCode)
            for removedVOL in (previousVOLs-configuredVOLs): self.__removeAnalysisData(analysisCode = removedVOL, removalType = 0)
            configurationResult = configuredVOLs

        elif (analysisType == 'MMACD'):
            if (self.objectConfig['MMACDCompute'] == True):
                analysisCode = "MMACD"
                siViewerNumber = self.siTypes_siViewerAlloc['MMACD']
                activatedMAs = list()
                for lineIndex in range (_NMAXLINES['MMACD']):
                    lineNumber = lineIndex+1
                    if (self.objectConfig['MMACD{:d}Compute'.format(lineNumber)] == True): activatedMAs.append(self.objectConfig['MMACD{:d}nSamples'.format(lineNumber)])
                if (2 <= len(activatedMAs)):
                    activatedMAs.sort()
                    activatedMACodes = ['EMA_{:d}'.format(maInterval) for maInterval in activatedMAs]
                    analysisParams = {'signal_nSamples':    self.objectConfig['MMACDSignalInterval'],
                                      'msDeltaMA_nSamples': self.objectConfig['MMACDSignalDeltaMAInterval'],
                                      'activatedMAs':       activatedMAs,
                                      'activatedMACodes':   activatedMACodes}
                    self.klines_analysisParams[analysisCode] = analysisParams
                    if (analysisCode not in self.klines): self.klines[analysisCode] = dict()
                    self.klines_analysisTargets[analysisCode] = 0
                    self.klines_analysisTargets_keySet.add(analysisCode)
                    self.siTypes_analysisCodes[analysisType] = set([analysisCode])
                    self.verticalValue_loaded["SIVIEWER{:d}".format(siViewerNumber)] = False
                    configurationResult = True
                else: configurationResult = False
            else: configurationResult = False
            if (configurationResult == False): self.__removeAnalysisData('MMACD', 0)
            
        elif (analysisType == 'DMIxADX'):
            configurationResult = None
            
        elif (analysisType == 'MFI'):
            configurationResult = None
        
        else: configurationResult = None

        #Update referer tracker
        if (True):
            #---Initialize analysisReferers
            self.klines_analysisReferers = dict()
            for targetAnalysisCode in self.klines_analysisTargets: self.klines_analysisReferers[targetAnalysisCode] = dict()
            #---Udpate analysisReferers
            for targetAnalysisCode in self.klines_analysisTargets:
                targetAnalysisType = targetAnalysisCode.split("_")[0]
                if   (targetAnalysisType == 'SMA'):  pass
                elif (targetAnalysisType == 'WMA'):  pass
                elif (targetAnalysisType == 'EMA'):  pass
                elif (targetAnalysisType == 'PSAR'): pass
                elif (targetAnalysisType == 'BOL'):
                    referencedAnalysisCode_MA = "{:s}_{:d}".format(self.objectConfig['BOLMAType'], self.klines_analysisParams[targetAnalysisCode]['nSamples'])
                    if (referencedAnalysisCode_MA in self.klines_analysisReferers): self.klines_analysisReferers[referencedAnalysisCode_MA][targetAnalysisCode] = 0
                elif (targetAnalysisType == 'IVP'):
                    if (self.klines_analysisParams['IVP']['useBLE'] == True):
                        for referencedAnalysisCode in self.klines_analysisReferers:
                            referencedAnalysisType = referencedAnalysisCode.split("_")[0]
                            if (referencedAnalysisType == 'BOL'): self.klines_analysisReferers[referencedAnalysisCode]['IVP'] = 0
                elif (targetAnalysisType == 'PIP'):
                    for referencedAnalysisCode in self.klines_analysisReferers:
                        referencedAnalysisType = referencedAnalysisCode.split("_")[0]
                        if   (referencedAnalysisType == 'PSAR'):  self.klines_analysisReferers[referencedAnalysisCode]['PIP'] = 0
                        elif (referencedAnalysisType == 'IVP'):   self.klines_analysisReferers[referencedAnalysisCode]['PIP'] = 0
                        elif (referencedAnalysisType == 'MMACD'): self.klines_analysisReferers[referencedAnalysisCode]['PIP'] = 0
                elif (targetAnalysisType == 'VOL'): pass
                elif (targetAnalysisType == 'MMACD'):
                    referencedAnalysisCode_MAs = self.klines_analysisParams['MMACD']['activatedMACodes']
                    for referencedAnalysisCode_MA in referencedAnalysisCode_MAs:
                        if (referencedAnalysisCode_MA in self.klines_analysisReferers): self.klines_analysisReferers[referencedAnalysisCode_MA]['MMACD'] = 0
                elif (targetAnalysisType == 'DMIxADX'): pass
                elif (targetAnalysisType == 'MFI'): pass

        #Update BufferZoneFactor
        if (True):
            self.horizontalViewRange_backwardBufferSamples = 0
            for analysisCode in self.klines_analysisParams:
                analysisType = analysisCode.split("_")[0]
                aParam = self.klines_analysisParams[analysisCode]
                if (analysisType == 'SMA'):
                    if (self.horizontalViewRange_backwardBufferSamples < aParam['nSamples']): self.horizontalViewRange_backwardBufferSamples = aParam['nSamples']
                elif (analysisType == 'WMA'):
                    if (self.horizontalViewRange_backwardBufferSamples < aParam['nSamples']): self.horizontalViewRange_backwardBufferSamples = aParam['nSamples']
                elif (analysisType == 'EMA'):
                    if (self.horizontalViewRange_backwardBufferSamples < aParam['nSamples']): self.horizontalViewRange_backwardBufferSamples = aParam['nSamples']
                elif (analysisType == 'BOL'):
                    if (self.horizontalViewRange_backwardBufferSamples < aParam['nSamples']): self.horizontalViewRange_backwardBufferSamples = aParam['nSamples']
                elif (analysisType == 'IVP'):
                    if ((aParam['useAGF'] == True) and (self.horizontalViewRange_backwardBufferSamples < aParam['AGFRefLen'])): self.horizontalViewRange_backwardBufferSamples = aParam['AGFRefLen']
                elif (analysisType == 'VOL'):
                    if (('nSamples' in aParam) and (self.horizontalViewRange_backwardBufferSamples < aParam['nSamples'])): self.horizontalViewRange_backwardBufferSamples = aParam['nSamples']
                elif (analysisType == 'MMACD'):
                    activatedMAs_max = max(aParam['activatedMAs'])
                    if (self.horizontalViewRange_backwardBufferSamples < activatedMAs_max): self.horizontalViewRange_backwardBufferSamples = activatedMAs_max
                elif (analysisType == 'DMIxADX'):
                    pass
                elif (analysisType == 'MFI'):
                    pass

        return configurationResult

    def __removeAnalysisData(self, analysisCode, removalType = 0, removalType_Graphics = None):
        #RemovalTypes
        #0: Remove Analysis, Graphics, and AnalysisParams (On Analysis Registration Removal)
        #1: Remove Analysis and Graphics                  (On Analysis Setup Update)
        #2: Remove Graphics Only                          (On Drawing Setup Update)
        analysisType = analysisCode.split("_")[0]
        if (removalType_Graphics == None): gRemovalSignal = _FULLDRAWSIGNALS[analysisType]
        else:                              gRemovalSignal = removalType_Graphics

        #Graphics Data Removal
        #---Graphic Objects Removal
        if (analysisType == 'SMA'):  
            if (0 < gRemovalSignal&0b1): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode)
        elif (analysisType == 'WMA'):
            if (0 < gRemovalSignal&0b1): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode)
        elif (analysisType == 'EMA'):
            if (0 < gRemovalSignal&0b1): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode)
        elif (analysisType == 'PSAR'):
            if (0 < gRemovalSignal&0b1): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode)
        elif (analysisType == 'BOL'):
            if (0 < gRemovalSignal&0b01): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode+'_LINE')
            if (0 < gRemovalSignal&0b10): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = analysisCode+'_BAND')
        elif (analysisType == 'IVP'):
            if (0 < gRemovalSignal&0b00001): self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(groupName = 'IVPRAW')
            if (0 < gRemovalSignal&0b00010): self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(groupName = 'IVPC_EXTENSION')
            if (0 < gRemovalSignal&0b00100):
                for ts in self.klines_drawn:
                    if ('IVP' in self.klines_drawn[ts]): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = 'IVPC_POSITIONAL_{:d}'.format(ts))
            if (0 < gRemovalSignal&0b01000): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = 'IVPC_POSITIONALCURRENTANCHOR')
            if (0 < gRemovalSignal&0b10000): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = 'IVPC_POSITIONALPREVANCHOR')
        elif (analysisType == 'PIP'):
            pass
        elif (analysisType == 'VOL'):
            siViewerNumber = self.siTypes_siViewerAlloc['VOL']
            if (siViewerNumber != None):
                siViewerCode = "SIVIEWER{:d}".format(siViewerNumber)
                self.displayBox_graphics[siViewerCode]['RCLCG'].clearAll()
        elif (analysisType == 'MMACD'):
            siViewerNumber = self.siTypes_siViewerAlloc['MMACD']
            if (siViewerNumber != None):
                siViewerCode = "SIVIEWER{:d}".format(siViewerNumber)
                if (0 < gRemovalSignal&0b001): self.displayBox_graphics[siViewerCode]['RCLCG'].removeGroup(groupName = 'MMACD_MMACD')
                if (0 < gRemovalSignal&0b010): self.displayBox_graphics[siViewerCode]['RCLCG'].removeGroup(groupName = 'MMACD_SIGNAL')
                if (0 < gRemovalSignal&0b100): self.displayBox_graphics[siViewerCode]['RCLCG'].removeGroup(groupName = 'MMACD_HISTOGRAM')

        #---Draw Trackers Reset
        for ts in self.klines_drawQueue:
            if (analysisCode in self.klines_drawQueue[ts]):
                if (self.klines_drawQueue[ts][analysisCode] == None): self.klines_drawQueue[ts][analysisCode] = _FULLDRAWSIGNALS[analysisType] & ~gRemovalSignal
                else:                                                 self.klines_drawQueue[ts][analysisCode] &= ~gRemovalSignal
                if (self.klines_drawQueue[ts][analysisCode] == 0): del self.klines_drawQueue[ts][analysisCode]

        for ts in self.klines_drawn:
            if (analysisCode in self.klines_drawn[ts]): 
                self.klines_drawn[ts][analysisCode] &= ~gRemovalSignal
                if (self.klines_drawn[ts][analysisCode] == 0): del self.klines_drawn[ts][analysisCode]

        #Analysis Data Removal - Generated Results Clearing
        if (removalType <= 1):
            if (analysisCode in self.klines_analysisParams):
                self.klines[analysisCode].clear()
                for ts in self.klines_toProcess:
                    if (analysisCode in self.klines_toProcess[ts]): del self.klines_toProcess[ts][analysisCode]
                for ts in self.klines_processed:
                    if (analysisCode in self.klines_processed[ts]): self.klines_processed[ts].remove(analysisCode)
                #Referers Update
                for refererAnalysisCode in self.klines_analysisReferers[analysisCode]:
                    #Clear previous analysis data
                    self.__removeAnalysisData(analysisCode = refererAnalysisCode, removalType = 1)
                    #Add new queues
                    for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone): 
                        if (timestamp in self.klines_toProcess): self.klines_toProcess[timestamp][refererAnalysisCode] = 0
                        else:                                    self.klines_toProcess[timestamp] = {refererAnalysisCode: 0}

        #AnalysisParams Removal - Analysis Preparation Removal
        if (removalType == 0):
            if (analysisCode in self.klines_analysisParams):
                del self.klines[analysisCode]
                del self.klines_analysisParams[analysisCode]
                del self.klines_analysisTargets[analysisCode]
                self.klines_analysisTargets_keySet.remove(analysisCode)
                del self.klines_analysisReferers[analysisCode]
                #Reference Tracker Update
                for referencedAnalysisCode in self.klines_analysisReferers:
                    refererAnalysisCodesToRemoved = list()
                    for refererAnalysisCode in self.klines_analysisReferers[referencedAnalysisCode]:
                        refererAnalysisType = refererAnalysisCode.split("_")[0]
                        if (refererAnalysisType == analysisType): refererAnalysisCodesToRemoved.append(refererAnalysisCode)
                    for refererAnalysisCodeToRemove in refererAnalysisCodesToRemoved: del self.klines_analysisReferers[referencedAnalysisCode][refererAnalysisCodeToRemove]

    def __addProcessQueuesToBufferZone(self, analysisCode, analysisMode):
        for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
            if (timestamp in self.klines_toProcess): self.klines_toProcess[timestamp][analysisCode] = analysisMode
            else:                                    self.klines_toProcess[timestamp] = {analysisCode: analysisMode}

    def __addDrawQueuesToBufferZone(self, analysisCode, drawSignal):
        for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
            if (timestamp in self.klines_processed) and (analysisCode in self.klines_processed[timestamp]):
                if (timestamp in self.klines_drawQueue): 
                    if (analysisCode in self.klines_drawQueue[timestamp]):
                        if (self.klines_drawQueue[timestamp][analysisCode] != None): self.klines_drawQueue[timestamp][analysisCode] |= drawSignal
                    else:                                                            self.klines_drawQueue[timestamp][analysisCode] = drawSignal
                else:                                                                self.klines_drawQueue[timestamp] = {analysisCode: drawSignal}

    def updateKlineColors(self, newType):
        if ((newType == 1) or (newType == 2)):
            self.objectConfig['KlineColorType'] = newType
            self.settingsSubPages['MAIN'].GUIOs["AUX_KLINECOLORTYPE_SELECTIONBOX"].setSelected(self.objectConfig['KlineColor'], callSelectionUpdateFunction = False)
            if ('VOL' in self.klines_analysisTargets_keySet): self.klines_drawQueue.update(dict.fromkeys(self.klines_drawn, {'KLINE': 0, 'VOL': 0}))
            else:                                             self.klines_drawQueue.update(dict.fromkeys(self.klines_drawn, {'KLINE': 0}))
            return True
        else: return False

    def updateTimeZone(self, newTimeZone):
        if   (newTimeZone     == 'LOCAL'): self.timezoneDelta = -time.timezone
        elif (newTimeZone[:3] == 'UTC'):   self.timezoneDelta = int(newTimeZone.split("+")[1])*3600
        
        #Update vertical grid texts (Temporal Texts)
        for index in range (len(self.verticalGrid_intervals)):
            timestamp_display = self.verticalGrid_intervals[index] + self.timezoneDelta
            #Grid Text
            if (self.verticalGrid_intervalID <= 10):
                if (timestamp_display % 86400 != 0): dateStrFormat = "%H:%M"
                else:                                dateStrFormat = "%m/%d"
            else:
                if (ATM_Zeta_Auxillaries.isNewMonth(timestamp_display) == True): dateStrFormat = "%Y/%m"
                else:                                                            dateStrFormat = "%m/%d"
            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].setText(datetime.fromtimestamp(timestamp_display, tz = timezone.utc).strftime(dateStrFormat))
            self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].moveTo(x = self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].xPos)
    #Configuration Update Control END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Kline Data Receival Control ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setTarget(self, apiSymbol, intervalID):
        if (self.apiSymbol != None): 
            self.ipcA_ATM.sendFAR(functionID = 'REMOVEKLINESUBSCRIPTION', functionParams = {'requesterID': self.name, 'apiSymbol': self.apiSymbol, 'intervalID': self.intervalID}, FARRHandler = self.__removeKlineSubscription_ResponseHandler, nMaxDispatch = 'INF')
            self.ipcA_ATM.removeFARHandler("KLINERECEIVER_{:s}".format(self.name))

        self.apiSymbol = apiSymbol
        if (self.apiSymbol == None):
            self.intervalID = 0
            self.currencyInfo = None

            #Setup Klines Loading Gauge Objects
            self.frameSprites['KLINELOADINGCOVER'].visible = False
            self.klinesLoadingGaugeBar.hide()
            self.klinesLoadingTextBox.hide()
            self.klinesLoadingTextBox_perc.hide()
            self.klinesLoadingGaugeBar.updateGaugeValue(0)
            self.klinesLoadingTextBox_perc.updateText("-")

            #Reset Klines
            for dataType in self.klines: self.klines[dataType].clear()
            self.klines_fetchComplete = False
            self.klines_fetching      = False
            self.klines_processed.clear()
            self.klines_toProcess.clear()
            self.klines_drawQueue.clear()
            self.klines_drawRemovalQueue.clear()
            
            #Horizontal ViewRange Params Setup
            self.expectedKlineTemporalWidth = _EXPECTEDTEMPORALWIDTHS[self.intervalID]
            nKlinesDisplayable_min = self.displayBox['KLINESPRICE'][2]*self.scaler / _GD_DISPLAYBOX_KLINESPRICE_MAXPIXELWIDTH
            nKlinesDisplayable_max = self.displayBox['KLINESPRICE'][2]*self.scaler / _GD_DISPLAYBOX_KLINESPRICE_MINPIXELWIDTH
            self.horizontalViewRangeWidth_min = nKlinesDisplayable_min * self.expectedKlineTemporalWidth
            self.horizontalViewRangeWidth_max = nKlinesDisplayable_max * self.expectedKlineTemporalWidth
            self.horizontalViewRangeWidth_m = (self.horizontalViewRangeWidth_min-self.horizontalViewRangeWidth_max)/(_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE-_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE)
            self.horizontalViewRangeWidth_b = (self.horizontalViewRangeWidth_min*_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE-self.horizontalViewRangeWidth_max*_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE)/(_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE-_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE)

            #Call this now since no klines will be fetched
            self.__onKlineFetchComplete()
        else:
            self.intervalID = intervalID
            self.currencyInfo = self.ipcA_ATM.getPRD(("MARKETASSETS", self.apiSymbol))

            #Send KDRC Request
            self.ipcA_ATM.sendFAR(functionID = "REQUESTKLINEDEEPRANGECHECK", 
                                  functionParams = {'apiSymbol':                 self.apiSymbol,
                                                    'intervalID':                self.intervalID,
                                                    'recalculateDownloadRanges': True},
                                  FARRHandler = self.__requestKDRC_ResponseHandler, nMaxDispatch = 'INF')

            #Setup Klines Loading Gauge Objects
            self.frameSprites['KLINELOADINGCOVER'].visible = True
            self.klinesLoadingGaugeBar.show()
            self.klinesLoadingTextBox.show()
            self.klinesLoadingTextBox_perc.show()
            self.klinesLoadingGaugeBar.updateGaugeValue(0)
            self.klinesLoadingTextBox_perc.updateText("-")
            self.klinesLoadingTextBox.updateText(self.visualManager.getTextPack('GUIO_CHARTDRAWER:REQUESTINGKDRC'))

            #Update Highlighters and Descriptors
            self.posHighlight_hoveredPos       = (None, None, None, None)
            self.posHighlight_updatedPositions = None
            self.posHighlight_selectedPos      = None
            self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_HOVERED'].visible  = False
            self.displayBox_graphics['KLINESPRICE']['POSHIGHLIGHT_SELECTED'].visible = False
            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT1'].setText("")
            self.displayBox_graphics['KLINESPRICE']['DESCRIPTIONTEXT2'].setText("")
            for siViewerName in self.displayBox_graphics_visibleSIViewers:
                self.displayBox_graphics[siViewerName]['POSHIGHLIGHT_HOVERED'].visible  = False 
                self.displayBox_graphics[siViewerName]['POSHIGHLIGHT_SELECTED'].visible = False
                self.displayBox_graphics[siViewerName]['DESCRIPTIONTEXT1'].setText("")

            #Reset Klines
            for dataType in self.klines: self.klines[dataType].clear()
            self.klines_fetchComplete = False
            self.klines_fetching      = True
            self.klines_processed.clear()
            self.klines_toProcess.clear()
            self.klines_drawQueue.clear()
            self.klines_drawRemovalQueue.clear()
            
            #Horizontal ViewRange Params Setup
            self.expectedKlineTemporalWidth = _EXPECTEDTEMPORALWIDTHS[self.intervalID]
            nKlinesDisplayable_min = self.displayBox['KLINESPRICE'][2]*self.scaler / _GD_DISPLAYBOX_KLINESPRICE_MAXPIXELWIDTH
            nKlinesDisplayable_max = self.displayBox['KLINESPRICE'][2]*self.scaler / _GD_DISPLAYBOX_KLINESPRICE_MINPIXELWIDTH
            self.horizontalViewRangeWidth_min = nKlinesDisplayable_min * self.expectedKlineTemporalWidth
            self.horizontalViewRangeWidth_max = nKlinesDisplayable_max * self.expectedKlineTemporalWidth
            self.horizontalViewRangeWidth_m = (self.horizontalViewRangeWidth_min-self.horizontalViewRangeWidth_max)/(_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE-_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE)
            self.horizontalViewRangeWidth_b = (self.horizontalViewRangeWidth_min*_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE-self.horizontalViewRangeWidth_max*_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE)/(_GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE-_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE)

            #Get Currency Precisions & Update RCLCG Precisions
            self.verticalViewRange_precision['KLINESPRICE'] = self.currencyInfo['pricePrecision']
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = -self.verticalViewRange_precision['KLINESPRICE'])
            self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].setPrecision(precision_y = -self.verticalViewRange_precision['KLINESPRICE'],      precision_x = 0)
            self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = 0)
            for siViewerCode in self.displayBox_graphics_visibleSIViewers:
                self.displayBox_graphics[siViewerCode]['RCLCG'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = 0)
                self.displayBox_graphics[siViewerCode]['RCLCG_XFIXED'].setPrecision(precision_y = 0,                                                         precision_x = 0)
                self.displayBox_graphics[siViewerCode]['RCLCG_YFIXED'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = 0)
            
    def __requestKDRC_ResponseHandler(self, functionResult):
        if (functionResult == True):
            self.ipcA_ATM.sendFAR(functionID = 'ADDKLINESUBSCRIPTION', functionParams = {'requesterID': self.name, 'apiSymbol': self.apiSymbol, 'intervalID': self.intervalID}, FARRHandler = self.__addKlineSubscription_ResponseHandler, nMaxDispatch = 'INF')
            self.ipcA_ATM.addFARHandler("KLINERECEIVER_{:s}".format(self.name), self.__klineReceiver)
        else: 
            self.klinesLoadingTextBox_perc.updateText("Kline Deep Range Check Failed, User Attention Advised")
            print(termcolor.colored("[CHARTDRAWER '{:s}'] Kline Deep Range Change Failed, User Attention Advised".format(self.name), 'light_red'))

    def __addKlineSubscription_ResponseHandler(self, functionResult):
        if (functionResult == True): self.klinesLoadingTextBox.updateText(self.visualManager.getTextPack('GUIO_CHARTDRAWER:LOADINGKLINES'))
        else: print(termcolor.colored("Unexpected Kline Subscription Request Rejection Occurred, User Attention Advised", 'light_red'))
        
    def __removeKlineSubscription_ResponseHandler(self, functionResult):
        if (functionResult == False): print(termcolor.colored("Unexpected Kline Subscription Removal Rejection Occurred, User Attention Advised", 'light_red'))
        
    def __klineReceiver(self, functionParams):
        if ((functionParams['apiSymbol'] == self.apiSymbol) and (functionParams['intervalID'] == self.intervalID)):
            klines = functionParams['klines']
            if (self.klines_fetchComplete == True):
                for kline in klines:
                    #Update Kline raw
                    open_ts = int(kline[0]%1e10); close_ts = kline[1]
                    self.klines['raw'][open_ts] = (open_ts,) + kline[1:]

                    #Update Kline raw_status
                    if (open_ts not in self.klines['raw_status']):
                        raw_status_prev = self.klines['raw_status'][ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = open_ts, mrktReg = self.mrktRegTS, nTicks = -1)]
                        self.klines['raw_status'][open_ts] = {'p_max': raw_status_prev['p_max']}
                    #---p_max
                    if (self.klines['raw_status'][open_ts]['p_max'] < kline[3]): self.klines['raw_status'][open_ts]['p_max'] = kline[3]

                    #Determine if this kline is within the horizontalViewRange, if it is, add the processing queue
                    classification = 0
                    classification += 0b1000*(0 <= open_ts -self.horizontalViewRange[0])
                    classification += 0b0100*(0 <= open_ts -self.horizontalViewRange[1])
                    classification += 0b0010*(0 <  close_ts-self.horizontalViewRange[0])
                    classification += 0b0001*(0 <  close_ts-self.horizontalViewRange[1])
                    if ((classification == 0b0010) or (classification == 0b1010) or (classification == 0b1011) or (classification == 0b0011)):
                        if (open_ts in self.klines_toProcess): self.klines_toProcess[open_ts].update(self.klines_analysisTargets)
                        else:                                  self.klines_toProcess[open_ts] = self.klines_analysisTargets.copy()
                        if (open_ts in self.klines_drawQueue): self.klines_drawQueue[open_ts]['KLINE'] = 0
                        else:                                  self.klines_drawQueue[open_ts] = {'KLINE': 0}
            else:
                for kline in klines:
                    open_ts = int(kline[0]%1e10)
                    self.klines['raw'][open_ts] = (open_ts,) + kline[1:]
                if ('completion' in functionParams):
                    completion = functionParams['completion']
                    if (completion == None): self.klinesLoadingTextBox_perc.updateText("{:d} klines".format(len(self.klines['raw'])))
                    else:
                        self.klinesLoadingGaugeBar.updateGaugeValue(completion)
                        self.klinesLoadingTextBox_perc.updateText("{:.3f} %   /   {:d} klines".format(completion, len(self.klines['raw'])))
                        if (100 <= completion): self.__onKlineFetchComplete()
        else: print(termcolor.colored("Unexpected Klines Received For {:s}_{:d} When {:s}_{:d} Was Expected".format(functionParams['apiSymbol'], functionParams['intervalID'], self.apiSymbol, self.intervalID)))
        
    def __onKlineFetchComplete(self):
        #Post-Fetch Complete Process
        #---Sort Fetched Kline Timestamps
        fetchedTSs = list(self.klines['raw'].keys())
        fetchedTSs.sort()

        #---Find p_max
        p_max = float('-inf')
        for klineTS in fetchedTSs:
            p_high = self.klines['raw'][klineTS][3]
            if (p_max < p_high): p_max = p_high
            self.klines['raw_status'][klineTS] = {'p_max': p_max}

        #Control Variables Update
        self.klines_fetchComplete = True
        self.klines_fetching      = False

        #Loading Indicator Graphics Control
        self.frameSprites['KLINELOADINGCOVER'].visible = False
        self.klinesLoadingGaugeBar.hide()
        self.klinesLoadingTextBox_perc.hide()
        self.klinesLoadingTextBox.hide()

        #Horizontal ViewRange Reset
        self.horizontalViewRange_magnification = 100
        self.horizontalViewRange = [None, round(time.time()+self.expectedKlineTemporalWidth*5)]
        self.horizontalViewRange[0] = round(self.horizontalViewRange[1]-(self.horizontalViewRange_magnification*self.horizontalViewRangeWidth_m+self.horizontalViewRangeWidth_b))
        self.__onHViewRangeUpdate(1)

        #Vertical ViewRange Reset
        self.__editVVR_toExtremaCenter('KLINESPRICE')
        for siViewerCode in self.displayBox_graphics_visibleSIViewers: self.__editVVR_toExtremaCenter(siViewerCode)
    #Kline Data Receival Control END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    #Kline Processing -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __processKline(self, timestamp):
        if (timestamp in self.klines['raw']):
            analysisCodes_toProcess = self.klines_toProcess[timestamp]

            #Sort Analysis Codes to Process
            analysisCodes_toProcess_sorted = list()
            for analysisType in self.__klines_analysisGenerationOrder: analysisCodes_toProcess_sorted += [analysisCode for analysisCode in analysisCodes_toProcess if analysisCode[:len(analysisType)] == analysisType]

            #Process Analysis Targets
            while (0 < len(analysisCodes_toProcess)):
                reprocessTargets = dict()
                analysisCodes_toProcess_sorted = list()
                for analysisType in self.__klines_analysisGenerationOrder: analysisCodes_toProcess_sorted += [analysisCode for analysisCode in analysisCodes_toProcess if analysisCode[:len(analysisType)] == analysisType]
                for analysisCode in analysisCodes_toProcess_sorted:
                    aBeg = time.perf_counter_ns()
                    analysisType = analysisCode.split("_")[0]
                    analysisMode = analysisCodes_toProcess[analysisCode]
                    analysisReport = self.__klines_analysisGenerators[analysisType](analysisMode = analysisMode, klineAccess = self.klines, intervalID = self.intervalID, mrktRegTS = self.mrktRegTS,
                                                                                    precisions = {'price': self.currencyInfo['pricePrecision'], 'quantity': self.currencyInfo['quantityPrecision'], 'quote': self.currencyInfo['quotePrecision']},
                                                                                    timestamp = timestamp, **self.klines_analysisParams[analysisCode])
                    if (analysisReport != None):
                        #If analysis generation was successful, add to the processed and drawQueue
                        if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp][analysisCode] = None
                        else:                                    self.klines_drawQueue[timestamp]= {analysisCode: None}
                        if (timestamp in self.klines_processed): self.klines_processed[timestamp].add(analysisCode)
                        else:                                    self.klines_processed[timestamp] = set([analysisCode])
                        #Post-Analysis Procedures (PAP)
                        if (self.__klines_PAPs[analysisType] != None): self.__klines_PAPs[analysisType](analysisCode, timestamp, analysisReport)
                        #Re-process Targets
                        reprocessTargets.update(self.klines_analysisReferers[analysisCode])
                        if (analysisCode in reprocessTargets): del reprocessTargets[analysisCode]

                    aEnd = time.perf_counter_ns()
                    print("[{:d} {:s} {:s} {:d}] {:.3f} us".format(timestamp, analysisCode, analysisType, analysisMode, (aEnd-aBeg)/1e3), reprocessTargets)
                analysisCodes_toProcess = reprocessTargets
                
            #Add EVENTS draw queue
            analysisReport = self.__klines_analysisGenerators['EVENTS'](analysisMode = 0, klineAccess = self.klines, intervalID = self.intervalID, mrktRegTS = self.mrktRegTS,
                                                                        precisions = {'price': self.currencyInfo['pricePrecision'], 'quantity': self.currencyInfo['quantityPrecision'], 'quote': self.currencyInfo['quotePrecision']},
                                                                        timestamp = timestamp, **self.klines_analysisParams['EVENTS'])
            if (analysisReport != None):
                if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp]['EVENTS'] = None
                else:                                    self.klines_drawQueue[timestamp]= {'EVENTS': None}

        del self.klines_toProcess[timestamp]

    def __analysisGenerator_EVENTS(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
        try:
            analysisEvents = list()
            for analysisCode in klineAccess:
                try: analysisEvents += klineAccess[analysisCode][timestamp]['EVENTS']
                except: pass
            
            #Save analysisEvents
            try:    klineAccess['EVENTS'][timestamp] = analysisEvents
            except: klineAccess['EVENTS'] = {timestamp: analysisEvents}

            #Return True to indicate successful analysis generation
            return True
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to collect EVENTS at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

    def __analysisGenerator_SMA(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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

    def __analysisGenerator_WMA(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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

    def __analysisGenerator_EMA(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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

    def __analysisGenerator_PSAR(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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

    def __analysisGenerator_BOL(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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
                if   (maType == 'SMA'): self.__analysisGenerator_SMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
                elif (maType == 'WMA'): self.__analysisGenerator_WMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
                elif (maType == 'EMA'): self.__analysisGenerator_EMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)
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

    def __analysisGenerator_IVP(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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
    
    def __analysisGenerator_PIP(self, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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

    def __analysisGenerator_VOL(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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
                        self.__analysisGenerator_VOL(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp_previous, **analysisParams_VOLSMA)
                        ema = round((klineAccess['raw'][timestamp][volAccessIndex]*kValue) + (klineAccess[smaCode][timestamp_previous]['value']*(1-kValue)), precisions['price'])

                #Save EMA
                volMAResult = {'valueType': 1, 'value': ema}
                try:    klineAccess[analysisCode][timestamp] = volMAResult
                except: klineAccess[analysisCode] = {timestamp: volMAResult}
                #Return True to indicate succesfful analysis generation
                return True
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate VOL analysis for timestamp {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

    def __analysisGenerator_MMACD(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
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
                    self.__analysisGenerator_EMA(analysisMode = 0, klineAccess = klineAccess, intervalID = intervalID, mrktRegTS = mrktRegTS, precisions = precisions, timestamp = timestamp, **analysisParams_MA)

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
    
    def __analysisGenerator_DMIxADX(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
        try:
            #Return True to indicate successful analysis generation
            return None
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate SMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))
    
    def __analysisGenerator_MFI(self, analysisMode, klineAccess, intervalID, mrktRegTS, precisions, timestamp, **analysisParams):
        try:
            #Return True to indicate successful analysis generation
            return None
        except Exception as e: print(termcolor.colored("An unexpected error occurred while attempting to generate SMA analysis at {:d}\n *".format(timestamp), 'light_red'), termcolor.colored(e, 'light_red'))

    def __PAP_EMA(self, analysisTarget, timestamp, analysisReport):
        #If there exists a EMA result at the next temporal step, add to the toProcess queue as analysisMode=0
        nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
        if ((nextTS in self.klines_processed) and (analysisTarget in self.klines_processed[nextTS])):
            if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS][analysisTarget] = 0
            else:                                 self.klines_toProcess[nextTS] = {analysisTarget: 0}

    def __PAP_PSAR(self, analysisTarget, timestamp, analysisReport):
        #If there exists a PSAR result at the next temporal step, add to the toProcess queue as analysisMode=0
        nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
        if ((nextTS in self.klines_processed) and (analysisTarget in self.klines_processed[nextTS])):
            if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS][analysisTarget] = 0
            else:                                 self.klines_toProcess[nextTS] = {analysisTarget: 0}

    def __PAP_BOL(self, analysisTarget, timestamp, analysisReport):
        if (self.objectConfig['BOLMAType'] == 'EMA'):
            #If there exists a BOL result as EMA base at the next temporal step, add to the toProcess queue as analysisMode=0
            nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
            if ((nextTS in self.klines_processed) and (analysisTarget in self.klines_processed[nextTS])):
                if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS][analysisTarget] = 1
                else:                                 self.klines_toProcess[nextTS] = {analysisTarget: 1}
        
    def __PAP_IVP(self, analysisTarget, timestamp, analysisReport):
        #If there exists a IVP result at the next temporal step, add to the toProcess queue as analysisMode=1
        nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
        if ((nextTS in self.klines_processed) and ('IVP' in self.klines_processed[nextTS])):
            if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS]['IVP'] = 0
            else:                                 self.klines_toProcess[nextTS] = {'IVP': 0}

    def __PAP_PIP(self, analysisTarget, timestamp, analysisReport):
        #If there exists a PIP result at the next temporal step, add to the toProcess queue as analysisMode=1
        nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
        if ((nextTS in self.klines_processed) and ('PIP' in self.klines_processed[nextTS])):
            if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS]['PIP'] = 0
            else:                                 self.klines_toProcess[nextTS] = {'PIP': 0}

    def __PAP_VOL(self, analysisTarget, timestamp, analysisReport):
        analysisType = 'VOL'
        siViewerNumber = self.siTypes_siViewerAlloc[analysisType]
        siViewerCode   = "SIVIEWER{:d}".format(siViewerNumber)
        
        if (self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)]):
            analysisResult = self.klines[analysisTarget][timestamp]
            resultValues = [0, analysisResult['value']]
            verticalExtremaUpdated = self.__PAP_SIVIEWERCONTROL('VOL', timestamp, resultValues, siViewerCode)
            if (verticalExtremaUpdated == True): self.__editVVR_toExtremaCenter(siViewerCode, 0, 0.2)
        
        if (self.objectConfig['VOLMAType'] == 'EMA'):
            #If there exists a VOL result as EMA base at the next temporal step, add to the toProcess queue as analysisMode=0
            nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
            if ((nextTS in self.klines_processed) and (analysisTarget in self.klines_processed[nextTS])):
                if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS][analysisTarget] = 0
                else:                                 self.klines_toProcess[nextTS] = {analysisTarget: 0}

    def __PAP_MMACD(self, analysisTarget, timestamp, analysisReport):
        analysisType = 'MMACD'
        siViewerNumber = self.siTypes_siViewerAlloc[analysisType]
        siViewerCode   = "SIVIEWER{:d}".format(siViewerNumber)

        if (self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)]):
            analysisResult = self.klines[analysisTarget][timestamp]
            resultValues = [0]
            if (self.objectConfig['MMACDMMACDDisplay']     == True): resultValues.append(analysisResult['mmacd'])
            if (self.objectConfig['MMACDSIGNALDisplay']    == True): resultValues.append(analysisResult['signal'])
            if (self.objectConfig['MMACDHISTOGRAMDisplay'] == True): resultValues.append(analysisResult['msDeltaMAMomentum'])
            verticalExtremaUpdated = self.__PAP_SIVIEWERCONTROL('MMACD', timestamp, resultValues, siViewerCode)
            if (verticalExtremaUpdated == True): self.__editVVR_toExtremaCenter(siViewerCode, 0.1, 0.1)
        
        #If there exists a MMACD result at the next temporal step, add to the toProcess queue as analysisMode=0
        nextTS = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp(intervalID = self.intervalID, timestamp = timestamp, mrktReg = self.mrktRegTS, nTicks = 1)
        if ((nextTS in self.klines_processed) and (analysisTarget in self.klines_processed[nextTS])):
            if (nextTS in self.klines_toProcess): self.klines_toProcess[nextTS][analysisTarget] = 1
            else:                                 self.klines_toProcess[nextTS] = {analysisTarget: 1}
            
    def __PAP_DMIxADX(self, analysisTarget, timestamp, analysisReport):
        pass
            
    def __PAP_MFI(self, analysisTarget, timestamp, analysisReport):
        pass

    def __PAP_SIVIEWERCONTROL(self, analysisType, timestamp, resultValues, siViewerCode):
        #Get Timestamp Boundary
        open_ts  = timestamp
        close_ts = self.klines['raw'][timestamp][1]
        #Determine if this kline is within the horizontalViewRange
        classification = 0
        if (0 <= open_ts -self.horizontalViewRange[0]): classification += 0b1000
        if (0 <= open_ts -self.horizontalViewRange[1]): classification += 0b0100
        if (0 <  close_ts-self.horizontalViewRange[0]): classification += 0b0010
        if (0 <  close_ts-self.horizontalViewRange[1]): classification += 0b0001
        if ((classification == 0b0010) or (classification == 0b1010) or (classification == 0b1011) or (classification == 0b0011)):
            #Find the maximum and minimum of the resultValues
            resultValues_min = min(resultValues)
            resultValues_max = max(resultValues)

            #First vertical value has been loaded
            if (self.verticalValue_loaded[siViewerCode] == True):
                verticalExtremaUpdated_Min = (resultValues_min < self.verticalValue_min[siViewerCode])
                verticalExtremaUpdated_Max = (self.verticalValue_max[siViewerCode] < resultValues_max)
                if ((verticalExtremaUpdated_Min == True) or (verticalExtremaUpdated_Max == True)):
                    verticalExtremaWidth_OOM_prev = math.floor(math.log(self.verticalValue_max[siViewerCode]-self.verticalValue_min[siViewerCode], 10))
                    verticalExtremaWidth_OOM_new  = math.floor(math.log(resultValues_max-resultValues_min,                                         10))
                    if (verticalExtremaWidth_OOM_prev != verticalExtremaWidth_OOM_new): self.displayBox_graphics[siViewerCode]['RCLCG'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = verticalExtremaWidth_OOM_new+1-6, transferObjects = True)
                    if (verticalExtremaUpdated_Min == True): self.verticalValue_min[siViewerCode] = resultValues_min
                    if (verticalExtremaUpdated_Max == True): self.verticalValue_max[siViewerCode] = resultValues_max
                    return True

            #First vertical value has not been loaded
            else:
                self.verticalValue_min[siViewerCode] = resultValues_min
                self.verticalValue_max[siViewerCode] = resultValues_max
                verticalExtremaWidth = self.verticalValue_max[siViewerCode]-self.verticalValue_min[siViewerCode]
                if (0 < verticalExtremaWidth):
                    self.verticalValue_loaded[siViewerCode] = True
                    verticalExtremaWidth_OOM = math.floor(math.log(self.verticalValue_max[siViewerCode]-self.verticalValue_min[siViewerCode], 10))
                    self.displayBox_graphics[siViewerCode]['RCLCG'].setPrecision(precision_x = math.floor(math.log(self.expectedKlineTemporalWidth, 10)), precision_y = verticalExtremaWidth_OOM+1-6, transferObjects = True)
                    return True
        return False
    #Kline Processing END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #Kline Drawing --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __processKlineDrawQueue(self, timestamp):
        #Drawn Dictionary Preparation
        if (timestamp not in self.klines_drawn): self.klines_drawn[timestamp] = dict()

        #Process DrawQueues at the corresponding timestamp
        for analysisCode in self.klines_drawQueue[timestamp]:
            try:
                drawn = self.__klines_drawerFunctions[analysisCode.split("_")[0]](self.klines_drawQueue[timestamp][analysisCode], timestamp, analysisCode)
                if (0 < drawn):
                    if (analysisCode in self.klines_drawn[timestamp]): self.klines_drawn[timestamp][analysisCode] |= drawn
                    else:                                              self.klines_drawn[timestamp][analysisCode] = drawn

            except Exception as e:
                print(termcolor.colored("An unexpected error occured while attempting to draw {:s} at {:d}\n *".format(analysisCode, timestamp), 'light_yellow'), termcolor.colored(e, 'light_yellow'))
                if (timestamp in self.klines_toProcess): self.klines_toProcess[timestamp][analysisCode] = 0
                else:                                    self.klines_toProcess[timestamp] = {analysisCode: 0}

        #Descriptor Update
        if (timestamp == self.posHighlight_hoveredPos[0]): self.posHighlight_updatedPositions = [True, True]; self.__onPosHighlightUpdate()

        #Remove the timestamp from the queue
        del self.klines_drawQueue[timestamp]

    def __processKlineDrawRemovalQueue(self, timestamp):
        for analysisCode in self.klines_drawn[timestamp]:
            targetType = analysisCode.split("_")[0]
            if   (targetType == 'KLINE'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'KLINEBODIES')
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'KLINETAILS')
            elif (targetType == 'EVENTS'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'EVENTS')
            elif (targetType == 'SMA'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode)
            elif (targetType == 'WMA'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode)
            elif (targetType == 'EMA'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode)
            elif (targetType == 'PSAR'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode)
            elif (targetType == 'BOL'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode+'_BAND')
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode+'_LINE')
            elif (targetType == 'IVP'):
                self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(shapeName = timestamp, groupName = 'IVPRAW')
                self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(shapeName = timestamp, groupName = 'IVPC_EXTENSION')
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = 'IVPC_POSITIONAL_{:d}'.format(timestamp))
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'IVPC_POSITIONALCURRENTANCHOR')
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'IVPC_POSITIONALPREVANCHOR')
            elif (targetType == 'PIP'):
                pass
            elif (targetType == 'VOL'): self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode)
            elif (targetType == 'MMACD'):
                pass
            elif (targetType == 'DMIxADX'):
                pass
            elif (targetType == 'MFI'):
                pass
        del self.klines_drawn[timestamp]

    def __klineDrawer_KLINE(self, drawSignal, timestamp, analysisCode):
        if (timestamp in self.klines['raw']):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            p_open   = kline_raw[2]
            p_high   = kline_raw[3]
            p_low    = kline_raw[4]
            p_close  = kline_raw[5]

            if (p_open < p_close): #Incremental
                candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_INCREMENTAL'.format(self.objectConfig['KlineColorType']))
                bodyHeight = p_close - p_open
                bodyBottom = p_open
            elif (p_open > p_close): #Decremental
                candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_DECREMENTAL'.format(self.objectConfig['KlineColorType']))
                bodyHeight = p_open - p_close
                bodyBottom = p_close
            else: #Neutral
                candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_NEUTRAL'.format(self.objectConfig['KlineColorType']))
                bodyHeight = pow(10, -self.verticalViewRange_precision['KLINESPRICE'])*10
                bodyBottom = p_close
            tsWidth   = ts_close-ts_open
            tailWidth = tsWidth/5
            tailXPos  = round(ts_open+(tsWidth-tailWidth)/2, 1)
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Rectangle(x = ts_open,  y = bodyBottom, width = ts_close-ts_open-1, height = bodyHeight,   color = candleColor, shapeName = ts_open, shapeGroupName = 'KLINEBODIES', layerNumber = 10)
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Rectangle(x = tailXPos, y = p_low,      width = tailWidth,          height = p_high-p_low, color = candleColor, shapeName = ts_open, shapeGroupName = 'KLINETAILS',  layerNumber = 10)

            return 0b1
        return 0b0

    def __klineDrawer_EVENTS(self, drawSignal, timestamp, analysisCode):
        if (self.objectConfig['DisplayEvents'] == True):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            analysisEvents = self.klines['EVENTS'][timestamp]
            self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED'].removeShape(shapeName = timestamp, groupName = 'EVENTS')
            if (0 < len(analysisEvents)):
                self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED'].addShape_Rectangle(x = ts_open, y = 0, width = ts_close-ts_open-1, height = 1, 
                                                                                            color = (255, 255, 255, 50), 
                                                                                            shapeName = ts_open, shapeGroupName = 'EVENTS', layerNumber = 0)
            return 0b1
        return 0b0

    def __klineDrawer_SMA(self, drawSignal, timestamp, analysisCode):
        lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
        if (self.objectConfig['SMA{:d}Display'.format(lineNumber)] == True):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            sma = self.klines[analysisCode][timestamp]
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = sma, 
                                                                            x2 = ts_close, y2 = sma,
                                                                            color = (self.objectConfig['SMA{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['SMA{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['SMA{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['SMA{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                            width_y = self.objectConfig['SMA{:d}Width'.format(lineNumber)],
                                                                            shapeName = timestamp, shapeGroupName = analysisCode, layerNumber = lineNumber-1)
            return 0b1
        return 0b0

    def __klineDrawer_WMA(self, drawSignal, timestamp, analysisCode):
        lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
        if (self.objectConfig['WMA{:d}Display'.format(lineNumber)] == True):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            wma = self.klines[analysisCode][timestamp]
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = wma, 
                                                                            x2 = ts_close, y2 = wma,
                                                                            color = (self.objectConfig['WMA{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['WMA{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['WMA{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['WMA{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                            width_y = self.objectConfig['WMA{:d}Width'.format(lineNumber)],
                                                                            shapeName = timestamp, shapeGroupName = analysisCode, layerNumber = lineNumber-1)
            return 0b1
        return 0b0

    def __klineDrawer_EMA(self, drawSignal, timestamp, analysisCode):
        lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
        if (self.objectConfig['EMA{:d}Display'.format(lineNumber)] == True):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            ema = self.klines[analysisCode][timestamp]
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = ema, 
                                                                            x2 = ts_close, y2 = ema,
                                                                            color = (self.objectConfig['EMA{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['EMA{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['EMA{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                    self.objectConfig['EMA{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                            width_y = self.objectConfig['EMA{:d}Width'.format(lineNumber)],
                                                                            shapeName = timestamp, shapeGroupName = analysisCode, layerNumber = lineNumber-1)
            return 0b1
        return 0b0

    def __klineDrawer_PSAR(self, drawSignal, timestamp, analysisCode):
        lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
        if (self.objectConfig['PSAR{:d}Display'.format(lineNumber)] == True):
            psar = self.klines[analysisCode][timestamp]
            if (psar['PSAR'] != None):
                kline_raw = self.klines['raw'][timestamp]
                ts_open  = kline_raw[0]
                ts_close = kline_raw[1]
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = psar['PSAR'], 
                                                                                x2 = ts_close, y2 = psar['PSAR'],
                                                                                color = (self.objectConfig['PSAR{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                        self.objectConfig['PSAR{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                        self.objectConfig['PSAR{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                        self.objectConfig['PSAR{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                                width_y = self.objectConfig['PSAR{:d}Size'.format(lineNumber)]*2,
                                                                                shapeName = timestamp, shapeGroupName = analysisCode, layerNumber = lineNumber-1)
            return 0b1
        return 0b0

    def __klineDrawer_BOL(self, drawSignal, timestamp, analysisCode):
        lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']

        if (drawSignal == None): drawSignal = 0b11
        drawn = 0b00
        if (self.objectConfig['BOL{:d}Display'.format(lineNumber)] == True):
            kline_raw = self.klines['raw'][timestamp]
            ts_open  = kline_raw[0]
            ts_close = kline_raw[1]
            bol = self.klines[analysisCode][timestamp]
            
            #[1]: CenterLine
            if (0 < drawSignal&0b01):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode+'_LINE')
                if (self.objectConfig['BOLdisplayCenterLine'] == True):
                    self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = bol[1], 
                                                                                   x2 = ts_close, y2 = bol[1],
                                                                                   color = (self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                            self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                            self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                            255),
                                                                                   width = None, width_x = None, width_y = self.objectConfig['BOL{:d}Width'.format(lineNumber)],
                                                                                   shapeName = timestamp, shapeGroupName = analysisCode+'_LINE', layerNumber = lineNumber-1)
                    drawn += 0b01

            #[2]: Band
            if (0 < drawSignal&0b10):
                self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = analysisCode+'_BAND')
                if (self.objectConfig['BOLdisplayBand'] == True):
                    self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Rectangle(x = ts_open, y = bol[0], width = ts_close-ts_open+1, height = bol[2]-bol[0], 
                                                                                        color = (self.objectConfig['BOL{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                 self.objectConfig['BOL{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                 self.objectConfig['BOL{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                 self.objectConfig['BOL{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                                        shapeName = timestamp, shapeGroupName = analysisCode+'_BAND', layerNumber = lineNumber-1)
                    drawn += 0b10

        return drawn

    def __klineDrawer_IVP(self, drawSignal, timestamp, analysisCode):
        kline_raw = self.klines['raw'][timestamp]
        ts_open  = kline_raw[0]
        ts_close = kline_raw[1]
        ivp_CLUSTERS = self.klines[analysisCode][timestamp]['ivp_filteredClusters']

        if (drawSignal == None): drawSignal = 0b11111
        drawn = 0b00000
        #[1]: RAW
        if (0 < drawSignal&0b00001):
            if (timestamp == self.posHighlight_selectedPos):
                self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(groupName = 'IVPRAW')
                if (self.objectConfig['IVPRAWDisplay'] == True):
                    ivp_IVPRAW         = self.klines[analysisCode][timestamp]['ivp_raw']; ivp_IVPRAW_max = self.klines[analysisCode][timestamp]['ivp_raw_max']
                    ivp_DIVISIONHEIGHT = self.klines[analysisCode][timestamp]['divisionHeight']
                    ivp_CLUSTERINGINDEX_BEG = self.klines[analysisCode][timestamp]['ivp_clusteringIndex_beg']; ivp_CLUSTERINGINDEX_END = self.klines[analysisCode][timestamp]['ivp_clusteringIndex_end']
                    widthMax = 100*self.objectConfig['IVPRAWDisplayWidth']
                    for ivpIndex in range (ivp_CLUSTERINGINDEX_BEG, ivp_CLUSTERINGINDEX_END+1):
                        dWidth = round(widthMax*ivp_IVPRAW[ivpIndex]/ivp_IVPRAW_max, 1)
                        self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].addShape_Rectangle(x      = 100-dWidth, 
                                                                                                    y      = ivp_DIVISIONHEIGHT*ivpIndex, 
                                                                                                    width  = dWidth,
                                                                                                    height = ivp_DIVISIONHEIGHT,
                                                                                                    color = (self.objectConfig['IVPRAWcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                                            self.objectConfig['IVPRAWcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                                            self.objectConfig['IVPRAWcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                                            self.objectConfig['IVPRAWcolorA%{:s}'.format(self.currentGUITheme)]),
                                                                                                    shapeName = ivpIndex, shapeGroupName = 'IVPRAW', layerNumber = 0)
                    drawn += 0b00001
        #[2]: IVPC Extension
        if (0 < drawSignal&0b00010):
            if (timestamp == self.posHighlight_selectedPos):
                self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].removeGroup(groupName = 'IVPC_EXTENSION')
                if (self.objectConfig['IVPCExtension'] == True):
                    for clusterIndex, cluster in enumerate(ivp_CLUSTERS):
                        self.displayBox_graphics['KLINESPRICE']['RCLCG_XFIXED'].addShape_Line(x  =   0, y  = cluster['cs'], 
                                                                                                x2 = 100, y2 = cluster['cs'],
                                                                                                color   = cluster['cuc'] + (255,),
                                                                                                width_y = 2,
                                                                                                shapeName = clusterIndex, shapeGroupName = 'IVPC_EXTENSION', layerNumber = 0)
                    drawn += 0b00010
        #[3]: #IVPC Positional
        if (0 < drawSignal&0b00100):
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeGroup(groupName = 'IVPC_POSITIONAL_{:d}'.format(timestamp))
            if (self.objectConfig['IVPCPositional'] == True):
                #Draw Positional Cluster Graphics
                for clusterIndex, cluster in enumerate(ivp_CLUSTERS):
                    self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = cluster['cs'], 
                                                                                    x2 = ts_close, y2 = cluster['cs'],
                                                                                    color = cluster['cuc'] + (255,),
                                                                                    width_y = 2,
                                                                                    shapeName = clusterIndex, shapeGroupName = 'IVPC_POSITIONAL_{:d}'.format(timestamp), layerNumber = 0)
                drawn += 0b00100
        #[4]: #IVPC Anchor
        if (0 < drawSignal&0b01000):
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'IVPC_POSITIONALCURRENTANCHOR')
            if (self.objectConfig['IVPCCURRENTANCHORDisplay'] == True):
                ivp_CURRENTANCHORCLUSTERINDEX = self.klines[analysisCode][timestamp]['anchorClusterIndex']
                if (ivp_CURRENTANCHORCLUSTERINDEX != None):
                    self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = ivp_CLUSTERS[ivp_CURRENTANCHORCLUSTERINDEX]['cs'],
                                                                                    x2 = ts_close, y2 = ivp_CLUSTERS[ivp_CURRENTANCHORCLUSTERINDEX]['cs'],
                                                                                    color = (self.objectConfig['IVPCCURRENTANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCCURRENTANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCCURRENTANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCCURRENTANCHORcolorA%{:s}'.format(self.currentGUITheme)]),
                                                                                    width_y = 10,
                                                                                    shapeName = timestamp, shapeGroupName = 'IVPC_POSITIONALCURRENTANCHOR', layerNumber = 11)
                    drawn += 0b01000
        #[5]: IVPC Anchor Previous
        if (0 < drawSignal&0b10000):
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'IVPC_POSITIONALPREVANCHOR')
            if (self.objectConfig['IVPCPREVANCHORDisplay'] == True):
                ivp_PREVANCHORCLUSTERINDEX = self.klines[analysisCode][timestamp]['anchorClusterIndex_prev']
                if (ivp_PREVANCHORCLUSTERINDEX != None):
                    self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Line(x  = ts_open,  y  = ivp_CLUSTERS[ivp_PREVANCHORCLUSTERINDEX]['cs'],
                                                                                    x2 = ts_close, y2 = ivp_CLUSTERS[ivp_PREVANCHORCLUSTERINDEX]['cs'],
                                                                                    color = (self.objectConfig['IVPCPREVANCHORcolorR%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCPREVANCHORcolorG%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCPREVANCHORcolorB%{:s}'.format(self.currentGUITheme)],
                                                                                            self.objectConfig['IVPCPREVANCHORcolorA%{:s}'.format(self.currentGUITheme)]),
                                                                                    width_y = 10,
                                                                                    shapeName = timestamp, shapeGroupName = 'IVPC_POSITIONALPREVANCHOR', layerNumber = 11)
                    drawn += 0b10000
        return drawn

    def __klineDrawer_PIP(self, drawSignal, timestamp, analysisCode):
        kline_raw = self.klines['raw'][timestamp]
        ts_open  = kline_raw[0]
        ts_close = kline_raw[1]
            
        pipResult = self.klines[analysisCode][timestamp]
            
        self.displayBox_graphics['KLINESPRICE']['RCLCG'].removeShape(shapeName = timestamp, groupName = 'PIP_PIP')
        if (pipResult['type'] == 'buy'):
            body_y      = pipResult['entrancePoint']
            body_height = pipResult['exitPoint']-pipResult['entrancePoint']
            lineColor = (self.objectConfig['PIPBUYPOScolorR%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPBUYPOScolorG%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPBUYPOScolorB%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPBUYPOScolorA%{:s}'.format(self.currentGUITheme)])
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Rectangle(x = ts_open, y = body_y, width = ts_close-ts_open-1, height = body_height, color = lineColor, shapeName = timestamp, shapeGroupName = 'PIP_PIP', layerNumber = 0)
        elif (pipResult['type'] == 'sell'):
            body_y      = pipResult['exitPoint']
            body_height = pipResult['entrancePoint']-pipResult['exitPoint']
            lineColor = (self.objectConfig['PIPSELLPOScolorR%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPSELLPOScolorG%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPSELLPOScolorB%{:s}'.format(self.currentGUITheme)],
                            self.objectConfig['PIPSELLPOScolorA%{:s}'.format(self.currentGUITheme)])
            self.displayBox_graphics['KLINESPRICE']['RCLCG'].addShape_Rectangle(x = ts_open, y = body_y, width = ts_close-ts_open-1, height = body_height, color = lineColor, shapeName = timestamp, shapeGroupName = 'PIP_PIP', layerNumber = 0)

        return True

    def __klineDrawer_VOL(self, drawSignal, timestamp, analysisCode):
        viewerNumber = self.siTypes_siViewerAlloc['VOL']
            
        kline_raw = self.klines['raw'][timestamp]
        ts_open  = kline_raw[0]
        ts_close = kline_raw[1]
            
        volResult = self.klines[analysisCode][timestamp]
        valueType = volResult['valueType']

        if (valueType == 0): #Raw Volume Value
            vol = volResult['value']
            p_open  = kline_raw[2]
            p_close = kline_raw[5]
            if   (p_open < p_close): candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_INCREMENTAL'.format(self.objectConfig['KlineColorType'])) #Incremental
            elif (p_open > p_close): candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_DECREMENTAL'.format(self.objectConfig['KlineColorType'])) #Decremental
            else:                    candleColor = self.visualManager.getFromColorTable('CHARTDRAWER_KLINECOLOR_TYPE{:d}_NEUTRAL'.format(self.objectConfig['KlineColorType']))     #Neutral
            self.displayBox_graphics['SIVIEWER{:d}'.format(viewerNumber)]['RCLCG'].addShape_Rectangle(x = ts_open, y = 0, width = ts_close-ts_open-1, height = vol, color = candleColor, shapeName = ts_open, shapeGroupName = analysisCode, layerNumber = 0)

        elif (valueType == 1): #Volume MA
            volMA = volResult['value']
            lineNumber = self.klines_analysisParams[analysisCode]['lineNumber']
            if (self.objectConfig['VOL{:d}Display'.format(lineNumber)] == True):
                self.displayBox_graphics['SIVIEWER{:d}'.format(viewerNumber)]['RCLCG'].addShape_Line(x  = ts_open,  y  = volMA,
                                                                                                        x2 = ts_close, y2 = volMA,
                                                                                                        color = (self.objectConfig['VOL{:d}colorR%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                                self.objectConfig['VOL{:d}colorG%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                                self.objectConfig['VOL{:d}colorB%{:s}'.format(lineNumber, self.currentGUITheme)],
                                                                                                                self.objectConfig['VOL{:d}colorA%{:s}'.format(lineNumber, self.currentGUITheme)]),
                                                                                                        width_y = self.objectConfig['VOL{:d}Width'.format(lineNumber)]*2,
                                                                                                        shapeName = timestamp, shapeGroupName = analysisCode, layerNumber = lineNumber)
            
        return True

    def __klineDrawer_MMACD(self, drawSignal, timestamp, analysisCode):
        viewerNumber = self.siTypes_siViewerAlloc['MMACD']; siViewerCode = 'SIVIEWER{:d}'.format(viewerNumber)
        kline_raw = self.klines['raw'][timestamp]
        ts_open  = kline_raw[0]
        ts_close = kline_raw[1]
        mmacdResult = self.klines['MMACD'][timestamp]

        if (drawSignal == None): drawSignal = 0b111
        drawn = 0b000
        #[1]: MMACD
        if (0 < drawSignal&0b001):
            self.displayBox_graphics[siViewerCode]['RCLCG'].removeShape(shapeName = timestamp, groupName = 'MMACD_MMACD')
            if (self.objectConfig['MMACDMMACDDisplay'] == True):
                lineColor = (self.objectConfig['MMACDMMACDcolorR%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDMMACDcolorG%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDMMACDcolorB%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDMMACDcolorA%{:s}'.format(self.currentGUITheme)])
                self.displayBox_graphics[siViewerCode]['RCLCG'].addShape_Line(x = ts_open, x2 = ts_close, y = mmacdResult['mmacd'], y2 = mmacdResult['mmacd'], color = lineColor, width_y = 3, shapeName = timestamp, shapeGroupName = 'MMACD_MMACD', layerNumber = 1)
                drawn += 0b001
        #[2]: SIGNAL
        if (0 < drawSignal&0b010):
            self.displayBox_graphics[siViewerCode]['RCLCG'].removeShape(shapeName = timestamp, groupName = 'MMACD_SIGNAL')
            if (self.objectConfig['MMACDSIGNALDisplay'] == True):
                lineColor = (self.objectConfig['MMACDSIGNALcolorR%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDSIGNALcolorG%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDSIGNALcolorB%{:s}'.format(self.currentGUITheme)],
                                self.objectConfig['MMACDSIGNALcolorA%{:s}'.format(self.currentGUITheme)])
                self.displayBox_graphics[siViewerCode]['RCLCG'].addShape_Line(x = ts_open, x2 = ts_close, y = mmacdResult['signal'], y2 = mmacdResult['signal'], color = lineColor, width_y = 3, shapeName = timestamp, shapeGroupName = 'MMACD_SIGNAL', layerNumber = 1)
                drawn += 0b010
        #[3]: HISTOGRAM
        if (0 < drawSignal&0b100):
            self.displayBox_graphics[siViewerCode]['RCLCG'].removeShape(shapeName = timestamp, groupName = 'MMACD_HISTOGRAM')
            if (self.objectConfig['MMACDHISTOGRAMDisplay'] == True):
                if (0 <= mmacdResult['msDeltaMAMomentum']):
                    lineColor = (self.objectConfig['MMACDHISTOGRAM+colorR%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM+colorG%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM+colorB%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM+colorA%{:s}'.format(self.currentGUITheme)])
                    body_y      = 0
                    body_height = mmacdResult['msDeltaMAMomentum']
                else:
                    lineColor = (self.objectConfig['MMACDHISTOGRAM-colorR%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM-colorG%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM-colorB%{:s}'.format(self.currentGUITheme)],
                                    self.objectConfig['MMACDHISTOGRAM-colorA%{:s}'.format(self.currentGUITheme)])
                    body_y      = mmacdResult['msDeltaMAMomentum']
                    body_height = -mmacdResult['msDeltaMAMomentum']
                self.displayBox_graphics[siViewerCode]['RCLCG'].addShape_Rectangle(x = ts_open, y = body_y, width = ts_close-ts_open-1, height = body_height, color = lineColor, shapeName = timestamp, shapeGroupName = 'MMACD_HISTOGRAM', layerNumber = 0)
                drawn += 0b100
        print("Drawn MMACD", bin(drawn))
        return drawn

    def __klineDrawer_DMIxADX(self, drawSignal, timestamp, analysisCode):
        pass

    def __klineDrawer_MFI(self, drawSignal, timestamp, analysisCode):
        pass
    #Kline Drawing End ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    #View Control ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #[1]: Horizontal Position and Magnification
    #---Horizontal Position
    def __editHPosition(self, delta_drag = None, delta_scroll = None, updateType = 0):
        if   (delta_drag   != None): effectiveDelta = -delta_drag*(self.horizontalViewRange[1]-self.horizontalViewRange[0])/self.displayBox_graphics['KLINESPRICE']['DRAWBOX'][2]
        elif (delta_scroll != None): effectiveDelta = -delta_scroll*self.expectedKlineTemporalWidth
        hVR_new = [round(self.horizontalViewRange[0]+effectiveDelta), round(self.horizontalViewRange[1]+effectiveDelta)]
        #Above-Zero Container
        if (hVR_new[0] < 0): hVR_new = [0, hVR_new[1]-hVR_new[0]]
        self.horizontalViewRange = hVR_new
        self.__onHViewRangeUpdate(updateType)
        
    #---Horizontal Magnification
    def __editHMagFactor(self, delta_drag = None, delta_scroll = None):
        if   (delta_drag   != None): newMagnitudeFactor = self.horizontalViewRange_magnification - delta_drag*200/self.displayBox_graphics['KLINESPRICE']['DRAWBOX'][2]
        elif (delta_scroll != None): newMagnitudeFactor = self.horizontalViewRange_magnification + delta_scroll
        #Rounding
        newMagnitudeFactor = round(newMagnitudeFactor, 1)
        if   (newMagnitudeFactor < _GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE): newMagnitudeFactor = _GD_DISPLAYBOX_KLINESPRICE_HVR_MINMAGNITUDE
        elif (_GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE < newMagnitudeFactor): newMagnitudeFactor = _GD_DISPLAYBOX_KLINESPRICE_HVR_MAXMAGNITUDE
        #Variation Check and response
        if (newMagnitudeFactor != self.horizontalViewRange_magnification):
            self.horizontalViewRange_magnification = newMagnitudeFactor
            hVR_new = (round(self.horizontalViewRange[1]-(self.horizontalViewRange_magnification*self.horizontalViewRangeWidth_m+self.horizontalViewRangeWidth_b)), self.horizontalViewRange[1])
            if (hVR_new[0] < 0): hVR_new = [0, hVR_new[1]-hVR_new[0]]
            self.horizontalViewRange = hVR_new
            self.__onHViewRangeUpdate(1)
            
    #---Post Horizontal View-Range Update
    def __onHViewRangeUpdate(self, updateType):
        #Horizontal Projection Update
        if (self.apiSymbol != None):
            #Update timestampsInViewRange and BufferZone
            self.horizontalViewRange_timestampsInViewRange = set(ATM_Zeta_Auxillaries.getTimestampList_byRange(self.intervalID, self.horizontalViewRange[0], self.horizontalViewRange[1], lastTickInclusive = True))
            nTSinViewRange = len(self.horizontalViewRange_timestampsInViewRange)
            if (self.horizontalViewRange_backwardBufferSamples < nTSinViewRange): fbf_effective = nTSinViewRange
            else:                                                                 fbf_effective = self.horizontalViewRange_backwardBufferSamples

            timestampsInBufferZone1 = set(ATM_Zeta_Auxillaries.getTimestampList_byNTicks(self.intervalID, self.horizontalViewRange[0], nTicks = fbf_effective *self.horizontalViewRange_backwardBufferFactor+1, direction = False, mrktReg = self.mrktRegTS)[1:])
            timestampsInBufferZone2 = set(ATM_Zeta_Auxillaries.getTimestampList_byNTicks(self.intervalID, self.horizontalViewRange[1], nTicks = nTSinViewRange*self.horizontalViewRange_forwardBufferFactor +1, direction = True,  mrktReg = self.mrktRegTS)[1:])
            self.horizontalViewRange_timestampsInBufferZone = timestampsInBufferZone1.union(timestampsInBufferZone2)

            #Update Process and Kline Draw Queue
            for timestamp in self.horizontalViewRange_timestampsInViewRange.union(self.horizontalViewRange_timestampsInBufferZone):
                if (timestamp in self.klines_processed):
                    #Find which analysis targets to process and add to queue
                    analysisCodesToProcess = self.klines_analysisTargets_keySet - self.klines_processed[timestamp]
                    if (0 < len(analysisCodesToProcess)): self.klines_toProcess[timestamp] = dict.fromkeys(analysisCodesToProcess, 0)
                    #Find which analysis targets are already processed and add to the drawing queue if not drawn
                    if (timestamp in self.klines_drawn): analysisCodesToDraw = [analysisCode for analysisCode in self.klines_processed[timestamp] if analysisCode not in self.klines_drawn[timestamp]]
                    else:                                analysisCodesToDraw = self.klines_processed[timestamp]
                    if (0 < len(analysisCodesToDraw)):
                        if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp].update(dict.fromkeys(analysisCodesToDraw, None))
                        else:                                    self.klines_drawQueue[timestamp] = dict.fromkeys(analysisCodesToDraw, None)
                else: self.klines_toProcess[timestamp] = self.klines_analysisTargets.copy()
                if (timestamp in self.klines_drawQueue): self.klines_drawQueue[timestamp]['KLINE'] = None
                else:                                    self.klines_drawQueue[timestamp] = {'KLINE': None}
            self.klines_drawRemovalQueue = [ts for ts in self.klines_drawn if ts not in self.horizontalViewRange_timestampsInViewRange and ts not in self.horizontalViewRange_timestampsInBufferZone]

        #--- Update RCLCG Projections
        self.displayBox_graphics['KLINESPRICE']['RCLCG'].updateProjection(projection_x0 = self.horizontalViewRange[0], projection_x1 = self.horizontalViewRange[1])
        self.displayBox_graphics['KLINESPRICE']['RCLCG_YFIXED'].updateProjection(projection_x0 = self.horizontalViewRange[0], projection_x1 = self.horizontalViewRange[1])
        for displayBoxName in self.displayBox_graphics_visibleSIViewers:
            self.displayBox_graphics[displayBoxName]['RCLCG'].updateProjection(projection_x0=self.horizontalViewRange[0], projection_x1=self.horizontalViewRange[1])
            self.displayBox_graphics[displayBoxName]['RCLCG_YFIXED'].updateProjection(projection_x0=self.horizontalViewRange[0], projection_x1=self.horizontalViewRange[1])

        #Find new vertical extrema within the new horizontalViewRange
        if (self.apiSymbol != None):
            self.__checkVerticalExtremas_KLINES()
            for siViewerCode in self.displayBox_graphics_visibleSIViewers: self.checkVerticalExtremas_SIs[self.objectConfig['SIVIEWER{:d}SIAlloc'.format(int(siViewerCode[8:]))]]()

        #Vertical Grid Lines
        #--- Determine Vertical Grid Intervals
        gridContentsUpdateFlag = False
        if (updateType == 1):
            for gridIntervalID in ATM_Zeta_Auxillaries.GRID_INTERVAL_IDs[self.intervalID:]:
                rightEnd = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp_GRID(gridIntervalID, self.horizontalViewRange[1], mrktReg = self.mrktRegTS, nTicks = 1)
                verticalGrid_intervals = ATM_Zeta_Auxillaries.getTimestampList_byRange_GRID(gridIntervalID, self.horizontalViewRange[0], rightEnd, mrktReg = self.mrktRegTS, lastTickInclusive = True)
                if (len(verticalGrid_intervals)+1 < self.nMaxVerticalGridLines): break
            self.verticalGrid_intervalID = gridIntervalID
            gridContentsUpdateFlag = True
        elif (updateType == 0):
            rightEnd = ATM_Zeta_Auxillaries.getNextIntervalTickTimestamp_GRID(self.verticalGrid_intervalID, self.horizontalViewRange[1], mrktReg = self.mrktRegTS, nTicks = 1)
            verticalGrid_intervals = ATM_Zeta_Auxillaries.getTimestampList_byRange_GRID(self.verticalGrid_intervalID, self.horizontalViewRange[0], rightEnd, mrktReg = self.mrktRegTS, lastTickInclusive = True)
            if ((self.verticalGrid_intervals[0] != verticalGrid_intervals[0]) or (self.verticalGrid_intervals[-1] != verticalGrid_intervals[-1])): gridContentsUpdateFlag = True

        #--- Update Grid Position & Text
        pixelPerTS = self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][2]*self.scaler / (self.horizontalViewRange[1]-self.horizontalViewRange[0])
        if (gridContentsUpdateFlag == True):
            self.verticalGrid_intervals = verticalGrid_intervals
            for index in range (self.nMaxVerticalGridLines):
                if (index < len(self.verticalGrid_intervals)):
                    timestamp = self.verticalGrid_intervals[index]
                    timestamp_display = timestamp + self.timezoneDelta
                    xPos_Line = round((timestamp-self.verticalGrid_intervals[0])*pixelPerTS, 1)
                    #[1]: KLINESPRICE
                    self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].x       = xPos_Line; self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].x2 = xPos_Line
                    if (self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].visible       == False): self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].visible = True
                    #[2]: MAINGRID_TEMPORAL
                    #---GridLines
                    self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].x = xPos_Line; self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].x2 = xPos_Line
                    if (self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].visible == False): self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].visible = True
                    #---Grid Texts
                    if (self.verticalGrid_intervalID <= 10):
                        if (timestamp_display % 86400 != 0): dateStrFormat = "%H:%M"
                        else:                                dateStrFormat = "%m/%d"
                    else:
                        if (ATM_Zeta_Auxillaries.isNewMonth(timestamp_display) == True): dateStrFormat = "%Y/%m"
                        else:                                                            dateStrFormat = "%m/%d"
                    self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].setText(datetime.fromtimestamp(timestamp_display, tz = timezone.utc).strftime(dateStrFormat))
                    self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].moveTo(x = round((xPos_Line)/self.scaler-_GD_DISPLAYBOX_GRID_VERTICALTEXTWIDTH/2))
                    if (self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].hidden == True): self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].show()
                    #[3]: SIVIEWERs (If Display == True)
                    for siViewerNumber in range (1, len(_SITYPES)+1):
                        if (self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)] == True):
                            self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].x = xPos_Line; self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].x2 = xPos_Line
                            if (self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].visible == False): self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].visible = True
                else:
                    #[1]: KLINESPRICE
                    if (self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].visible       == True): self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_LINES'][index].visible       = False
                    #[2]: MAINGRID_TEMPORAL
                    if (self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].visible == True): self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_LINES'][index].visible = False
                    if (self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].hidden == False): self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_TEXTS'][index].hide()
                    #[3]: SIVIEWERs (If Display == True)
                    for siViewerNumber in range (1, len(_SITYPES)+1):
                        if (self.objectConfig['SIVIEWER{:d}Display'.format(siViewerNumber)] == True):
                            if (self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].visible == True): self.displayBox_graphics['SIVIEWER{:d}'.format(siViewerNumber)]['VERTICALGRID_LINES'][index].visible = False

        #Update Grid CamGroup Projections
        projectionX0 = (self.horizontalViewRange[0]-self.verticalGrid_intervals[0])*pixelPerTS
        projectionX1 = projectionX0+self.displayBox_graphics['MAINGRID_TEMPORAL']['DRAWBOX'][2]*self.scaler
        #--- KLINESPRICE
        self.displayBox_graphics['KLINESPRICE']['VERTICALGRID_CAMGROUP'].updateProjection(projection_x0=projectionX0, projection_x1=projectionX1)
        #--- SIVIEWERS
        for displayBoxName in self.displayBox_graphics_visibleSIViewers: self.displayBox_graphics[displayBoxName]['VERTICALGRID_CAMGROUP'].updateProjection(projection_x0=projectionX0, projection_x1=projectionX1)
        #--- MAINGRID_TEMPORAL
        self.displayBox_graphics['MAINGRID_TEMPORAL']['VERTICALGRID_CAMGROUP'].updateProjection(projection_x0=projectionX0, projection_x1=projectionX1)

        #Update PosSelection
        self.__updatePosSelection(updateType = 1)
        
    def __checkVerticalExtremas_KLINES(self):
        valMin = float('inf')
        valMax = float('-inf')
        for ts in self.horizontalViewRange_timestampsInViewRange:
            if (ts in self.klines['raw']):
                if (self.klines['raw'][ts][4] < valMin): valMin = self.klines['raw'][ts][4]
                if (valMax < self.klines['raw'][ts][3]): valMax = self.klines['raw'][ts][3]
        if (((valMin != float('inf')) and (valMax != float('-inf'))) and ((self.verticalValue_min['KLINESPRICE'] != valMin) or (self.verticalValue_max['KLINESPRICE'] != valMax))): #The found extremas are different
            self.verticalValue_min['KLINESPRICE'] = valMin
            self.verticalValue_max['KLINESPRICE'] = valMax
            self.__onVerticalExtremaUpdate('KLINESPRICE')
            
    def __checkVerticalExtremas_VOL(self):
        #SI Viewer Allocation
        siViewerCode = "SIVIEWER{:d}".format(self.siTypes_siViewerAlloc['VOL'])

        #Extrema Value Init
        valMax = float('-inf')
        
        #Find new vertical extremas
        if (self.siTypes_analysisCodes['VOL'] != None):
            for ts in self.horizontalViewRange_timestampsInViewRange:
                for analysisCode in self.siTypes_analysisCodes['VOL']:
                    if ((analysisCode in self.klines) and (ts in self.klines[analysisCode])):
                        value = self.klines[analysisCode][ts]['value']
                        if (valMax < value): valMax = value
                    
        #If the extremas within the horizontalViewRange are updated
        if ((valMax != float('-inf')) and ((self.verticalValue_loaded[siViewerCode] == False) or (self.verticalValue_max[siViewerCode] != valMax))): #The found extremas are different
            self.verticalValue_loaded[siViewerCode] = True
            self.verticalValue_min[siViewerCode] = 0
            self.verticalValue_max[siViewerCode] = valMax
            self.__onVerticalExtremaUpdate(siViewerCode)
            self.__editVVR_toExtremaCenter(siViewerCode, 0, 0.2)

    def __checkVerticalExtremas_MMACD(self):
        #SI Viewer Allocation
        siViewerCode = "SIVIEWER{:d}".format(self.siTypes_siViewerAlloc['MMACD'])
        
        #Extrema Value Init
        valMin = float('inf')
        valMax = float('-inf')
        
        #Find new vertical extremas
        if (self.siTypes_analysisCodes['MMACD'] != None):
            for ts in self.horizontalViewRange_timestampsInViewRange:
                for analysisCode in self.siTypes_analysisCodes['MMACD']:
                    if ((analysisCode in self.klines) and (ts in self.klines[analysisCode])):
                        analysisResult = self.klines['MMACD'][ts]
                        values = []
                        if (self.objectConfig['MMACDMMACDDisplay'] == True):     values.append(analysisResult['mmacd'])
                        if (self.objectConfig['MMACDSIGNALDisplay'] == True):    values.append(analysisResult['signal'])
                        if (self.objectConfig['MMACDHISTOGRAMDisplay'] == True): values.append(analysisResult['msDeltaMAMomentum'])
                        if (0 < len(values)):
                            value_min = min(values)
                            value_max = max(values)
                            if (value_min < valMin): valMin = value_min
                            if (valMax < value_max): valMax = value_max
                    
        #If the extremas within the horizontalViewRange are updated
        if (((valMin != float('inf')) and (valMax != float('-inf'))) and ((self.verticalValue_loaded[siViewerCode] == False) or (self.verticalValue_min[siViewerCode] != valMin) or (self.verticalValue_max[siViewerCode] != valMax))): #The found extremas are different
            self.verticalValue_loaded[siViewerCode] = True
            self.verticalValue_min[siViewerCode] = valMin
            self.verticalValue_max[siViewerCode] = valMax
            self.__onVerticalExtremaUpdate(siViewerCode)
            self.__editVVR_toExtremaCenter(siViewerCode, 0.1, 0.1)

    def __checkVerticalExtremas_DMIxADX(self):
        #SI Viewer Allocation
        siViewerCode = "SIVIEWER{:d}".format(self.siTypes_siViewerAlloc['DMIxADX'])
        
        #Extrema Value Init
        valMin = float('inf')
        valMax = float('-inf')
        
        #Find new vertical extremas
        if (self.siTypes_analysisCodes['DMIxADX'] != None):
            for ts in self.horizontalViewRange_timestampsInViewRange:
                for analysisCode in self.siTypes_analysisCodes['DMIxADX']:
                    if ((analysisCode in self.klines) and (ts in self.klines[analysisCode])):
                        analysisResult = self.klines['DMIxADX'][ts]
                        values = []
                        if (0 < len(values)):
                            value_min = min(values)
                            value_max = max(values)
                            if (value_min < valMin): valMin = value_min
                            if (valMax < value_max): valMax = value_max
                    
        #If the extremas within the horizontalViewRange are updated
        if (((valMin != float('inf')) and (valMax != float('-inf'))) and ((self.verticalValue_loaded[siViewerCode] == False) or (self.verticalValue_min[siViewerCode] != valMin) or (self.verticalValue_max[siViewerCode] != valMax))): #The found extremas are different
            self.verticalValue_loaded[siViewerCode] = True
            self.verticalValue_min[siViewerCode] = valMin
            self.verticalValue_max[siViewerCode] = valMax
            self.__onVerticalExtremaUpdate(siViewerCode)
            self.__editVVR_toExtremaCenter(siViewerCode, 0.1, 0.1)

    def __checkVerticalExtremas_MFI(self):
        #SI Viewer Allocation
        siViewerCode = "SIVIEWER{:d}".format(self.siTypes_siViewerAlloc['MFI'])
        
        #Extrema Value Init
        valMin = float('inf')
        valMax = float('-inf')
        
        #Find new vertical extremas
        if (self.siTypes_analysisCodes['MFI'] != None):
            for ts in self.horizontalViewRange_timestampsInViewRange:
                for analysisCode in self.siTypes_analysisCodes['MFI']:
                    if ((analysisCode in self.klines) and (ts in self.klines[analysisCode])):
                        analysisResult = self.klines['MFI'][ts]
                        values = []
                        if (0 < len(values)):
                            value_min = min(values)
                            value_max = max(values)
                            if (value_min < valMin): valMin = value_min
                            if (valMax < value_max): valMax = value_max
                    
        #If the extremas within the horizontalViewRange are updated
        if (((valMin != float('inf')) and (valMax != float('-inf'))) and ((self.verticalValue_loaded[siViewerCode] == False) or (self.verticalValue_min[siViewerCode] != valMin) or (self.verticalValue_max[siViewerCode] != valMax))): #The found extremas are different
            self.verticalValue_loaded[siViewerCode] = True
            self.verticalValue_min[siViewerCode] = valMin
            self.verticalValue_max[siViewerCode] = valMax
            self.__onVerticalExtremaUpdate(siViewerCode)
            self.__editVVR_toExtremaCenter(siViewerCode, 0.1, 0.1)

    def __onVerticalExtremaUpdate(self, displayBoxName):
        previousViewRangeHeight = self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0]
        previousViewRangeCenter = (self.verticalViewRange[displayBoxName][0]+self.verticalViewRange[displayBoxName][1])/2
        verticalExtremaDelta = self.verticalValue_max[displayBoxName]-self.verticalValue_min[displayBoxName]
        newViewRangeHeight_min = verticalExtremaDelta
        newViewRangeHeight_max = verticalExtremaDelta*100/_GD_DISPLAYBOX_VVR_MAGNITUDE_MIN[displayBoxName]
        if (previousViewRangeHeight < newViewRangeHeight_min):   vVR_effective = [previousViewRangeCenter-newViewRangeHeight_min*0.5, previousViewRangeCenter+newViewRangeHeight_min*0.5]; self.verticalViewRange_magnification[displayBoxName] = 100
        elif (newViewRangeHeight_max < previousViewRangeHeight): vVR_effective = [previousViewRangeCenter-newViewRangeHeight_max*0.5, previousViewRangeCenter+newViewRangeHeight_max*0.5]; self.verticalViewRange_magnification[displayBoxName] = _GD_DISPLAYBOX_VVR_MAGNITUDE_MIN[displayBoxName]
        else:                                                    vVR_effective = self.verticalViewRange[displayBoxName];                                                                   self.verticalViewRange_magnification[displayBoxName] = round(verticalExtremaDelta/previousViewRangeHeight*100, 1)
        if (displayBoxName == 'KLINESPRICE'): self.verticalViewRange[displayBoxName] = [round(vVR_effective[0], self.verticalViewRange_precision['KLINESPRICE']), round(vVR_effective[1], self.verticalViewRange_precision['KLINESPRICE'])]
        else:                                 self.verticalViewRange[displayBoxName] = vVR_effective
        if (previousViewRangeHeight != self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0]): self.__onVViewRangeUpdate(displayBoxName, 1)
        
    #[2]: Vertical Position and Magnification
    #---Vertical Position
    def __editVPosition(self, displayBoxName, delta_drag = None, delta_scroll = None):
        if   (delta_drag   != None): effectiveDelta = -delta_drag  *(self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0])/self.displayBox_graphics[displayBoxName]['DRAWBOX'][3]
        elif (delta_scroll != None): effectiveDelta = -delta_scroll*(self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0])/50
        vVR_effective = [self.verticalViewRange[displayBoxName][0]+effectiveDelta, self.verticalViewRange[displayBoxName][1]+effectiveDelta]
        self.verticalViewRange[displayBoxName] = vVR_effective
        self.__onVViewRangeUpdate(displayBoxName, 0)
        
    #---Vertical Magnification
    def __editVMagFactor(self, displayBoxName, delta_drag = None, delta_scroll = None, anchor = 'CENTER'):
        if   (delta_drag   != None): newMagnitudeFactor = self.verticalViewRange_magnification[displayBoxName] + delta_drag*200/self.displayBox_graphics[displayBoxName]['DRAWBOX'][3]
        elif (delta_scroll != None): newMagnitudeFactor = self.verticalViewRange_magnification[displayBoxName] + delta_scroll
        #Rounding
        newMagnitudeFactor = round(newMagnitudeFactor, 1)
        #Boundary Control
        if   (newMagnitudeFactor < _GD_DISPLAYBOX_VVR_MAGNITUDE_MIN[displayBoxName]): newMagnitudeFactor = _GD_DISPLAYBOX_VVR_MAGNITUDE_MIN[displayBoxName]
        elif (_GD_DISPLAYBOX_VVR_MAGNITUDE_MAX[displayBoxName] < newMagnitudeFactor): newMagnitudeFactor = _GD_DISPLAYBOX_VVR_MAGNITUDE_MAX[displayBoxName]
        #Variation Check and response
        if (newMagnitudeFactor != self.verticalViewRange_magnification[displayBoxName]):
            #Calculate new viewRange
            self.verticalViewRange_magnification[displayBoxName] = newMagnitudeFactor
            verticalExtremaDelta = self.verticalValue_max[displayBoxName]-self.verticalValue_min[displayBoxName]
            verticalExtremaDelta_magnified = verticalExtremaDelta*100/self.verticalViewRange_magnification[displayBoxName]
            if (anchor == 'CENTER'):
                vVRCenter = (self.verticalViewRange[displayBoxName][0]+self.verticalViewRange[displayBoxName][1])/2
                vVR_effective = [vVRCenter-verticalExtremaDelta_magnified*0.5, vVRCenter+verticalExtremaDelta_magnified*0.5]
            elif (anchor == 'BOTTOM'): vVR_effective = [self.verticalViewRange[displayBoxName][0], self.verticalViewRange[displayBoxName][0]+verticalExtremaDelta_magnified]
            elif (anchor == 'TOP'):    vVR_effective = [self.verticalViewRange[displayBoxName][1]-verticalExtremaDelta_magnified, self.verticalViewRange[displayBoxName][1]]
            self.verticalViewRange[displayBoxName] = [round(vVR_effective[0], self.verticalViewRange_precision[displayBoxName]), round(vVR_effective[1], self.verticalViewRange_precision[displayBoxName])]
            self.__onVViewRangeUpdate(displayBoxName, 1)
            
    #---Reset vVR_price
    def __editVVR_toExtremaCenter(self, displayBoxName, extension_b = 0.1, extension_t = 0.1):
        #Extension Limit Control
        if (extension_b < 0): extension_b = 0
        if (extension_t < 0): extension_t = 0
        extensionLimit_min = (100/_GD_DISPLAYBOX_VVR_MAGNITUDE_MAX[displayBoxName])-1
        extensionLimit_max = (100/_GD_DISPLAYBOX_VVR_MAGNITUDE_MIN[displayBoxName])-1
        extensionSum = extension_b + extension_t
        if ((extensionLimit_min <= extensionSum) and (extensionSum <= extensionLimit_max)):
            extension_b = extension_b
            extension_t = extension_t
        else:
            extensionSumScaler = extensionSum / extensionLimit_max
            extension_b = extension_b / extensionSumScaler
            extension_t = extension_t / extensionSumScaler
        #ViewRange and new Magnification Computation
        verticalExtremaCenter = (self.verticalValue_min[displayBoxName]+self.verticalValue_max[displayBoxName])/2
        verticalExtremaDelta = self.verticalValue_max[displayBoxName]-self.verticalValue_min[displayBoxName]
        verticalExtremaDelta_b = verticalExtremaDelta*(0.5+extension_b)
        verticalExtremaDelta_t = verticalExtremaDelta*(0.5+extension_t)
        vVR_effective = [verticalExtremaCenter-verticalExtremaDelta_b, verticalExtremaCenter+verticalExtremaDelta_t]
        self.verticalViewRange[displayBoxName] = [round(vVR_effective[0], self.verticalViewRange_precision[displayBoxName]), round(vVR_effective[1], self.verticalViewRange_precision[displayBoxName])]
        self.verticalViewRange_magnification[displayBoxName] = round(verticalExtremaDelta/(vVR_effective[1]-vVR_effective[0])*100, 1)
        self.__onVViewRangeUpdate(displayBoxName, 1)
        
    #---Post Vertical View-Range Update - Price
    def __onVViewRangeUpdate(self, displayBoxName, updateType):
        self.displayBox_graphics[displayBoxName]['RCLCG'].updateProjection(projection_y0 = self.verticalViewRange[displayBoxName][0], projection_y1 = self.verticalViewRange[displayBoxName][1])
        self.displayBox_graphics[displayBoxName]['RCLCG_XFIXED'].updateProjection(projection_y0 = self.verticalViewRange[displayBoxName][0], projection_y1 = self.verticalViewRange[displayBoxName][1])

        #Horizontal Grid Lines
        gridContentsUpdateFlag = False
        if (updateType == 1):
            viewRangeHeight = self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0]
            viewRangeHeight_OOM = math.floor(math.log(viewRangeHeight, 10))

            for intervalFactor in (0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5):
                intervalHeight = round(intervalFactor*pow(10, viewRangeHeight_OOM), self.verticalViewRange_precision[displayBoxName])
                bottomEnd = round(int(self.verticalViewRange[displayBoxName][0]/intervalHeight)    *intervalHeight, self.verticalViewRange_precision[displayBoxName])
                topEnd    = round((int(self.verticalViewRange[displayBoxName][1]/intervalHeight)+1)*intervalHeight, self.verticalViewRange_precision[displayBoxName])
                nIntervals = int((topEnd-bottomEnd)/intervalHeight)+1
                if (nIntervals+1 <= self.nMaxHorizontalGridLines[displayBoxName]): 
                    horizontalGridIntervals = list()
                    value = bottomEnd
                    while (value <= topEnd): horizontalGridIntervals.append(value); value += intervalHeight
                    self.horizontalGridIntervalHeight[displayBoxName] = intervalHeight
                    break
            gridContentsUpdateFlag = True

        elif (updateType == 0):
            bottomEnd = int(self.verticalViewRange[displayBoxName][0]/self.horizontalGridIntervalHeight[displayBoxName])*self.horizontalGridIntervalHeight[displayBoxName]
            topEnd    = (int(self.verticalViewRange[displayBoxName][1]/self.horizontalGridIntervalHeight[displayBoxName])+1)*self.horizontalGridIntervalHeight[displayBoxName]
            if ((self.horizontalGridIntervals[displayBoxName][0] != bottomEnd) or (self.horizontalGridIntervals[displayBoxName][-1] != topEnd)):
                horizontalGridIntervals = list()
                value = bottomEnd
                while (value <= topEnd): horizontalGridIntervals.append(value); value += self.horizontalGridIntervalHeight[displayBoxName]
                gridContentsUpdateFlag = True
                
        pixelPerUnitHeight = self.displayBox_graphics[displayBoxName]['DRAWBOX'][3]*self.scaler / (self.verticalViewRange[displayBoxName][1]-self.verticalViewRange[displayBoxName][0])

        if (gridContentsUpdateFlag == True):
            self.horizontalGridIntervals[displayBoxName] = horizontalGridIntervals

            for index in range (self.nMaxHorizontalGridLines[displayBoxName]):
                if (index < len(self.horizontalGridIntervals[displayBoxName])):
                    verticalValue = self.horizontalGridIntervals[displayBoxName][index]
                    yPos_Line = round((verticalValue-self.horizontalGridIntervals[displayBoxName][0])*pixelPerUnitHeight, 1)

                    #Grid Lines
                    self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].y             = yPos_Line; self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].y2             = yPos_Line
                    self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].y = yPos_Line; self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].y2 = yPos_Line
                    if (self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].visible == False):             self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].visible             = True
                    if (self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].visible == False): self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].visible = True

                    #Grid Text
                    verticalValue_rounded   = round(verticalValue, self.verticalViewRange_precision[displayBoxName])
                    verticalValue_formatted = ATM_Zeta_Auxillaries.simpleValueFormatter(verticalValue_rounded, 3)

                    self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].setText(verticalValue_formatted)
                    self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].moveTo(y = round((yPos_Line)/self.scaler-_GD_DISPLAYBOX_GRID_HORIZONTALTEXTHEIGHT/2))
                    if (self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].hidden == True): self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].show()
                else:
                    if (self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].visible == True):             self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_LINES'][index].visible             = False
                    if (self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].visible == True): self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_LINES'][index].visible = False
                    if (self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].hidden == False): self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_TEXTS'][index].hide()
                
        projectionY0 = (self.verticalViewRange[displayBoxName][0]-self.horizontalGridIntervals[displayBoxName][0])*pixelPerUnitHeight
        projectionY1 = projectionY0+self.displayBox_graphics[displayBoxName]['DRAWBOX'][3]*self.scaler
        self.displayBox_graphics[displayBoxName]['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_y0=projectionY0, projection_y1=projectionY1)
        self.displayBox_graphics['MAINGRID_'+displayBoxName]['HORIZONTALGRID_CAMGROUP'].updateProjection(projection_y0=projectionY0, projection_y1=projectionY1)
    #View Control END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def getGroupRequirement(): return 30
#'chartDrawer_typeA' END ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
    def _process_Klines(self, mei_beg):
        if ((self.mouse_Event_currentlyPressed == False)):
            elapsedSoFar = time.perf_counter_ns() - mei_beg

            if (0 < len(self.klines_drawQueue)):
                if (elapsedSoFar < _TIMELIMIT_KLINESDRAW_NS):
                    #Determine timestamps to draw
                    if (len(self.klines_drawQueue) < len(self.horizontalViewRange_timestampsInViewRange)): drawQueueTimestamps = [ts for ts in self.klines_drawQueue if ts in self.horizontalViewRange_timestampsInViewRange]
                    else:                                                                                  drawQueueTimestamps = [ts for ts in self.horizontalViewRange_timestampsInViewRange if ts in self.klines_drawQueue]
                    if (len(drawQueueTimestamps) == 0):
                        if (len(self.klines_drawQueue) < len(self.horizontalViewRange_timestampsInBufferZone)): drawQueueTimestamps = [ts for ts in self.klines_drawQueue if ts in self.horizontalViewRange_timestampsInBufferZone]
                        else:                                                                                   drawQueueTimestamps = [ts for ts in self.horizontalViewRange_timestampsInBufferZone if ts in self.klines_drawQueue]
                    #Draw
                    while (0 < len(drawQueueTimestamps)):
                        self.__processKlineDrawQueue(drawQueueTimestamps.pop(0))
                        if ((_TIMELIMIT_KLINESDRAW_NS < time.perf_counter_ns()-mei_beg) or (self.mouse_Event_currentlyPressed == True) or (self.mouse_Scrolled == True) or (self.posHighlight_updatedPositions != None)): break

            #If there exist any spare time for the processing, process drawRemovalQueues if ther exist any
            if ((0 < len(self.klines_drawRemovalQueue)) and (time.perf_counter_ns() - mei_beg < _TIMELIMIT_KLINESDRAWREMOVAL_NS)):
                while (0 < len(self.klines_drawRemovalQueue)):
                    self.__processKlineDrawRemovalQueue(self.klines_drawRemovalQueue.pop())
                    if ((_TIMELIMIT_KLINESDRAWREMOVAL_NS <= time.perf_counter_ns()-mei_beg) or (self.mouse_Event_currentlyPressed == True) or (self.mouse_Scrolled == True) or (self.posHighlight_updatedPositions != None)): break
"""

"""
    def __processKlineDrawQueue(self, timestamp):
        #Drawn Dictionary Preparation
        if (timestamp not in self.klines_drawn): self.klines_drawn[timestamp] = dict()

        #Process DrawQueues at the corresponding timestamp
        for analysisCode in self.klines_drawQueue[timestamp]:
            try:
                drawn = self.__klines_drawerFunctions[analysisCode.split("_")[0]](self.klines_drawQueue[timestamp][analysisCode], timestamp, analysisCode)
                if (0 < drawn):
                    if (analysisCode in self.klines_drawn[timestamp]): self.klines_drawn[timestamp][analysisCode] |= drawn
                    else:                                              self.klines_drawn[timestamp][analysisCode] = drawn
            except Exception as e:
                print(termcolor.colored("An unexpected error occured while attempting to draw {:s} at {:d}\n *".format(analysisCode, timestamp), 'light_yellow'), termcolor.colored(e, 'light_yellow'))
                if (timestamp in self.klines_toProcess): self.klines_toProcess[timestamp][analysisCode] = 0
                else:                                    self.klines_toProcess[timestamp] = {analysisCode: 0}

        #Descriptor Update
        if (timestamp == self.posHighlight_hoveredPos[0]): self.posHighlight_updatedPositions = [True, True]; self.__onPosHighlightUpdate()

        #Remove the timestamp from the queue
        del self.klines_drawQueue[timestamp]
"""