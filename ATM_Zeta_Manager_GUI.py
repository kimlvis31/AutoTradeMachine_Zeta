from GUIs import ATM_Zeta_GUIO_Generals, ATM_Zeta_GUI_PageSetup, ATM_Zeta_GUI_ImageManager, ATM_Zeta_GUI_VisualManager, ATM_Zeta_GUI_AudioManager

from random import randint
import pyglet
import time
import os
import pprint
import termcolor
import numpy
import datetime

path_PROJECT = os.path.dirname(os.path.realpath(__file__))

#Screen Aspect Ratio Table, only supports the resolutions listed below (16:9H, 21:9H, 32:9H)
_SCREENASPECTRATIOTABLE = {'1920x1080': {'resolutionX': 1920, 'resolutionY': 1080, 'ratio': '16:9H', 'scaler': 0.12}, # 16:9 FHD HORIZONTAL
                           '2560x1440': {'resolutionX': 2560, 'resolutionY': 1440, 'ratio': '16:9H', 'scaler': 0.16}, # 16:9 QHD HORIZONTAL
                           '3840x2160': {'resolutionX': 3840, 'resolutionY': 2160, 'ratio': '16:9H', 'scaler': 0.24}, # 16:9 UHD HORIZONTAL
                                  
                           '2520x1080': {'resolutionX': 2520, 'resolutionY': 1080, 'ratio': '21:9H', 'scaler': 0.12}, # 21:9 FHD HORIZONTAL
                           '3360x1440': {'resolutionX': 3360, 'resolutionY': 1440, 'ratio': '21:9H', 'scaler': 0.16}, # 21:9 QHD HORIZONTAL
                                 
                           '3840x1080': {'resolutionX': 3840, 'resolutionY': 1080, 'ratio': '32:9H', 'scaler': 0.12}, # 32:9 FHD HORIZONTAL
                           '5120x1440': {'resolutionX': 5120, 'resolutionY': 1440, 'ratio': '32:9H', 'scaler': 0.16}} # 32:9 QHD HORIZONTAL

_PAGESTOINITIALIZE            = ("PROGRAMLOADING", "DASHBOARD", "APIKEY", "ASSET", "MARKET", "SIMULATION", "SIMULATIONRESULT", "AUTOTRADE", "SETTINGS")
_PAGESTOINITIALIZE_EXPERIMENT = ("EXPERIMENT0", "EXPERIMENT1", "EXPERIMENT2", "EXPERIMENT3", "EXPERIMENT4")
_PAGESINITIALIZATIONMODE = 0b11

class manager_GUI:
    #Initialization ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, ipcA_MAIN_AUX, ipcA_MAIN_ATM, ipcA_MAIN_AUX_Thread, ipcA_MAIN_ATM_Thread, process_AUX, process_ATM):
        print(termcolor.colored("\nInitializing", 'green'), termcolor.colored("GUI", 'light_blue'), termcolor.colored("Manager --------------------------------------------------------------------------------------------------------------------------", 'green'))
        self.ipcA_AUX = ipcA_MAIN_AUX
        self.ipcA_ATM = ipcA_MAIN_ATM
        self.ipcAThread_AUX = ipcA_MAIN_AUX_Thread
        self.ipcAThread_ATM = ipcA_MAIN_ATM_Thread
        self.process_AUX = process_AUX
        self.process_ATM = process_ATM
        
        self.displaySpaceDefiner = None

        #GUI Config File Read
        self.guiConfig = {"fullscreen": True,                                                    #Fullscreen
                          "windowSize": (1920, 1080),                                            #Window Size
                          "resolution": (1920, 1080),                                            #Resolution
                          "windowTitle": "AUTO TRADE MACHINE ZETA",                              #Window Title
                          "windowIcon": os.path.join(path_PROJECT, 'config', "windowIcon.png"),  #Window Icon
                          "maxFPS": 60,                                                          #Frames per second
                          "maxPPS": 120,                                                         #Processes per second
                          "MSAA": 2,                                                             #Multisample Anti-Aliasing
                          "VSync": False,                                                        #VSync
                          "Language": 'ENG',                                                     #Language
                          "ImageGenMSAA": 4,                                                     #Image Generation Multisample Anti-Aliasing
                          "GUITheme": 'Dark',                                                    #GUI Theme
                          "AudioMute": False,                                                    #Audio Mute
                          "AudioVolume": 100}                                                    #Audio Volume
        self.__readGUIConfig()

        #GUIO Config File Read
        self.guioConfig = dict()
        self.__readGUIOConfig()

        #Image & Audio Manager Initialization
        self.imageManager  = ATM_Zeta_GUI_ImageManager.imageManager(self.guiConfig)
        self.audioManager  = ATM_Zeta_GUI_AudioManager.audioManager(self.guiConfig)
        self.visualManager = ATM_Zeta_GUI_VisualManager.visualManager(self.guiConfig)

        #Analyze Monitor Information
        print("\nAnalyzing Monitor Information...")
        self.allowFullscreen = False
        display = pyglet.canvas.get_display(); screens = display.get_screens()
        print("<Detected Monitors>")
        for index, screen in enumerate(screens): print(" [DISPLAY{:d}] {:s}".format(index, str(screen)))
        if ((str(screens[0].width) + "x" + str(screens[0].height)) in _SCREENASPECTRATIOTABLE.keys()):
            print(" * Primary screen specification is supported by the program, fullscreen mode is allowed")
            self.allowFullscreen = True
        else: print(" * Primary screen specification is not supported by the program, fullscreen mode is disallowed")
        print("Monitor Information Analysis Complete!")

        #Window Object Initialization
        config = pyglet.gl.Config(sample_buffers = 1, samples = self.guiConfig["MSAA"])
        self.window = pyglet.window.Window(width      = self.guiConfig["windowSize"][0], 
                                           height     = self.guiConfig["windowSize"][1],
                                           caption    = self.guiConfig["windowTitle"],
                                           config     = config,
                                           vsync      = self.guiConfig["VSync"])

        self.windowIcon = pyglet.image.load(self.guiConfig["windowIcon"])
        self.window.set_icon(self.windowIcon)
        #self.window.set_icon(pyglet.image.load(self.windowIcon))
        if ((self.allowFullscreen == True) and (self.guiConfig["fullscreen"] == True)): self.window.set_fullscreen(True); self.window.activate()
        else:                                                                           self.window.set_location(100, 100)
        
        #GUIO Called System Functions
        self.GUIOCallSysFunc = {'TERMINATEPROGRAM':  self.sysFunc_terminateProgram,
                                'TOGGLE_FULLSCREEN': self.sysFunc_toggleFullscreen,
                                'ISFULLSCREEN':      self.sysFunc_isFullScreen,
                                'LOADPAGE':          self.sysFunc_loadPage,
                                'SAVEGUICONFIG':     self.sysFunc_saveGUIConfig,
                                'CHANGEGUITHEME':    self.sysFunc_changeGUITheme,
                                'CHANGELANGUAGE':    self.sysFunc_changeLanguage,
                                'EDITGUIOCONFIG':    self.sysFunc_editGUIOConfig}

        #Pages Initialization
        self.pages = dict()
        pagesToInit = tuple()
        if (0 < _PAGESINITIALIZATIONMODE&0b01): pagesToInit += _PAGESTOINITIALIZE
        if (0 < _PAGESINITIALIZATIONMODE&0b10): pagesToInit += _PAGESTOINITIALIZE_EXPERIMENT
        for pageName in pagesToInit: self.__addPage(pageName)
        self.currentPage = "PROGRAMLOADING"

        #Window Events Handler Functions
        @self.window.event
        def on_draw(): self.__draw()
        @self.window.event
        def on_key_press(symbol, modifiers):
            self.__InputHandler_KeyPress(symbol, modifiers)
            if (symbol == 65307): return pyglet.event.EVENT_HANDLED
        @self.window.event
        def on_key_release(symbol, modifiers): self.__InputHandler_KeyRelease(symbol, modifiers)
        @self.window.event
        def on_mouse_motion(x, y, dx, dy): self.__InputHandler_MouseMotion(x, y, dx, dy)
        @self.window.event
        def on_mouse_press(x, y, button, modifiers): self.__InputHandler_MousePress(x, y, button, modifiers)
        @self.window.event
        def on_mouse_release(x, y, button, modifiers): self.__InputHandler_MouseRelease(x, y, button, modifiers)
        @self.window.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers): self.__InputHandler_MouseDrag(x, y, dx, dy, button, modifiers)
        @self.window.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y): self.__InputHandler_MouseScroll(x, y, scroll_x, scroll_y)

        #System Clock Variables
        self.processUpdates = list(); self.lastProcessTime_ns = 0
        self.frameUpdates = list()

        self.printPPS = False
        self.printFPS = False

        print(termcolor.colored("GUI", 'light_blue'), termcolor.colored("Manager Initialization Complete! --------------------------------------------------------------------------------------------------------------", 'green'))
    def postInitialization(self):
        pyglet.clock.schedule_interval(func = self.__process, interval = 1/self.guiConfig['maxPPS'])
        self.ipcA_AUX.sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        self.ipcA_ATM.sendPRDEDIT("PROCSTATUS", "PROCESSING", nMaxDispatch = 'INF')
        self.ipcA_AUX.sendPRDEDIT("PROCCTRL_INITGO", True, nMaxDispatch = 'INF')
        pyglet.app.run(1/self.guiConfig['maxFPS'])
    #Initialization END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #Manager Internal Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __process(self, functionCallInterval):
        currentTime_ns = time.perf_counter_ns()

        #Page Processing and Process Reports Analysis
        sinceLastProcess_ns = currentTime_ns - self.lastProcessTime_ns; self.lastProcessTime_ns = currentTime_ns
        self.pages[self.currentPage].process(sinceLastProcess_ns)

        #FAR/FARR Processing
        self.ipcA_ATM.processFARs()
        self.ipcA_AUX.processFARs()
        self.ipcA_ATM.processFARRs()
        self.ipcA_AUX.processFARRs()

        #PPS Calculation
        self.processUpdates.append(currentTime_ns / 1e9)
        while (True):
            try:
                if (1 < (currentTime_ns / 1e9 - self.processUpdates[0])): self.processUpdates.pop(0)
                else: break
            except: break
        if (self.printPPS == True): print("{:d} PPS".format(self.__getCurrentPPS()))



    def __draw(self):
        #Graphics Drawing
        self.window.clear()
        self.pages[self.currentPage].draw()

        #FPS Calculation
        currentTime = time.time()
        self.frameUpdates.append(currentTime)
        while (True):
            try:
                if (1 < (currentTime - self.frameUpdates[0])): self.frameUpdates.pop(0)
                else: break
            except: break
        if (self.printFPS == True): print("{:d} FPS".format(self.__getCurrentFPS()))





    def __addPage(self, pageName):
        self.pages[pageName] = ATM_Zeta_GUIO_Generals.guiPage(self.window, self.GUIOCallSysFunc, self.displaySpaceDefiner, self.guioConfig, self.imageManager, self.audioManager, self.visualManager, pageName, self.ipcA_AUX, self.ipcA_ATM)
        ATM_Zeta_GUI_PageSetup.setupPage(self.pages[pageName], self.window, self.GUIOCallSysFunc, self.displaySpaceDefiner, self.guioConfig, self.imageManager, self.audioManager, self.visualManager, self.ipcA_AUX, self.ipcA_ATM)

    #Read GUI Configuration File located at 'path_PROJECT/config/guiConfig.txt
    def __readGUIConfig(self):
        print("Reading GUIO Configuration...")
        configFile = open(os.path.join(path_PROJECT, 'config', 'guiConfig.txt'))
        configFileContents = configFile.readlines()
        configFile.close()
        for i in range (len(configFileContents)):
            try:
                configFileContents[i] = configFileContents[i].strip()
                contentLineContents = configFileContents[i].split("=")
                contentName = contentLineContents[0].strip(); contentData = contentLineContents[1].strip()
                if (contentName == "fullscreen"):  
                    if   ((contentData == "True") or (contentData == "true") or (contentData == "1")): self.guiConfig[contentName] = True
                    else:                                                                              self.guiConfig[contentName] = False
                elif (contentName == "resolution"):
                    contentData = contentData.split("x"); screenSizeX = int(contentData[0]); screenSizeY = int(contentData[1])
                    self.guiConfig[contentName] = (screenSizeX, screenSizeY)
                elif (contentName == "windowTitle"):
                    self.guiConfig[contentName] = contentData
                elif (contentName == "windowIcon"):
                    self.guiConfig[contentName] = os.path.join(path_PROJECT, 'config', contentData)
                elif (contentName == "maxFPS"):
                    self.guiConfig[contentName] = int(contentData)
                elif (contentName == "maxPPS"):
                    self.guiConfig[contentName] = int(contentData)
                elif (contentName == "MSAA"):
                    self.guiConfig[contentName] = int(contentData)
                elif (contentName == "VSync"):
                    if   ((contentData == "True") or (contentData == "true") or (contentData == "1")): self.guiConfig[contentName] = True
                    else:                                                                              self.guiConfig[contentName] = False
                elif (contentName == "Language"):
                    self.guiConfig[contentName] = contentData
                elif (contentName == "ImageGenMSAA"):
                    self.guiConfig[contentName] = int(contentData)
                elif (contentName == "GUITheme"):
                    self.guiConfig[contentName] = contentData
                elif (contentName == "AudioMute"):
                    if   ((contentData == "True") or (contentData == "true") or (contentData == "1")): self.guiConfig[contentName] = True
                    else:                                                                              self.guiConfig[contentName] = False
                elif (contentName == "AudioVolume"):
                    self.guiConfig[contentName] = round(float(contentData), 1)
                else: print("Unrecognizable Content Name Detected During 'guiConfig.txt' Read: < {:s} >".format(configFileContents[i]))
            except Exception as e: print("Unrecognizable Content Detected During 'guiConfig.txt' Read: <{:s}> <{:s}>".format(configFileContents[i], str(e)))

        #Contents Verification
        #---Check and select Display Space Definer
        resolution_str = str(self.guiConfig['resolution'][0]) + "x" + str(self.guiConfig['resolution'][1])
        if resolution_str in _SCREENASPECTRATIOTABLE.keys(): 
            self.displaySpaceDefiner = _SCREENASPECTRATIOTABLE[resolution_str]
            self.guiConfig['windowSize'] = self.guiConfig['resolution']
            print(" * Using Display Space Definer for {:s}: {:s}".format(resolution_str, str(self.displaySpaceDefiner)))
        else:                                                    
            self.guiConfig['resolution'] = (1920, 1080); self.displaySpaceDefiner = _SCREENASPECTRATIOTABLE['1920x1080']
            print(" * Using Display Space Definer for {:s}: {:s}".format(resolution_str, str(self.displaySpaceDefiner)))
        #---Verify GUITheme Value
        if not(self.guiConfig['GUITheme'] in ('DARK', 'LIGHT')): self.guiConfig['GUITheme'] = 'DARK'

        #Console Print
        print("<self.guiConfig>")
        pprint.pprint(self.guiConfig)
        print("GUI Configuration Read Complete!")
        
        self.sysFunc_saveGUIConfig()

    def __readGUIOConfig(self):
        print("Reading GUI Configuration...")
        configFile = open(os.path.join(path_PROJECT, 'config', 'guioConfig.txt'))
        configFileContents = configFile.readlines()
        configFile.close()
        
        for i in range (len(configFileContents)):
            try:
                configFileContents[i] = configFileContents[i].strip()
                contentLineContents = configFileContents[i].split("=")
                contentName = contentLineContents[0].strip(); contentData = contentLineContents[1].strip()
                contentNameSplit = contentName.split("_")
                contentNameA = contentNameSplit[0]; contentNameB = contentNameSplit[1]
                if contentNameA in self.guioConfig: self.guioConfig[contentNameA][contentNameB] = contentData
                else:                               self.guioConfig[contentNameA] = {contentNameB: contentData}
            except Exception as e: print("Unrecognizable Content Detected During 'guioConfig.txt' Read: <{:s}> <{:s}>".format(configFileContents[i], str(e)))
            
        #Console Print
        #print("<self.guioConfig>")
        #pprint.pprint(self.guioConfig)
        print("GUI Configuration Read Complete!")

    def __toggleFullscreen(self):
        if (self.allowFullscreen == True):
            self.window.set_fullscreen(not(self.guiConfig["fullscreen"]))
            self.guiConfig["fullscreen"] = not(self.guiConfig["fullscreen"])

    def __getCurrentFPS(self): return (len(self.frameUpdates))
    def __getCurrentPPS(self): return (len(self.processUpdates))

    #System Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def sysFunc_terminateProgram(self):
        #AUX Process Termination Handling
        #---Send termination signal and confirm process termination for AUX process
        self.ipcA_AUX.sendFAR(functionID = "PROCCTRLFUNC_TERMINATE", nMaxDispatch = 'INF')
        self.process_AUX.join()
        print(termcolor.colored("AUX Process Terminated!", 'light_cyan'))
        #---Send termination signal and confirm thread termination for AUX IPCA thread
        self.ipcAThread_AUX.terminate()
        self.ipcAThread_AUX.join()
        
        #ATM Process Termination Handling
        #---Send termination signal and confirm process termination for ATM process
        self.ipcA_ATM.sendFAR(functionID = "PROCCTRLFUNC_TERMINATE", nMaxDispatch = 'INF')
        self.process_ATM.join()
        print(termcolor.colored("AUX Process Terminated!", 'light_cyan'))
        #---Send termination signal and confirm thread termination for ATM IPCA thread
        self.ipcAThread_ATM.terminate()
        self.ipcAThread_ATM.join()

        #Exit Pyglet App
        pyglet.app.exit()

    def sysFunc_toggleFullscreen(self): self.__toggleFullscreen()
    def sysFunc_isFullScreen(self):     return self.guiConfig['fullscreen']

    def sysFunc_loadPage(self, pageName):
        if pageName in self.pages.keys(): 
            self.currentPage = pageName
            self.pages[self.currentPage].on_PageLoad()

    def sysFunc_saveGUIConfig(self):
        configFile = open(os.path.join(path_PROJECT, 'config', 'guiConfig.txt'), 'w')
        configFile.write('fullscreen = {:s}\n'.format(str(self.guiConfig['fullscreen'])))
        configFile.write('resolution = {:d}x{:d}\n'.format(self.guiConfig['resolution'][0],self.guiConfig['resolution'][1]))
        configFile.write('windowTitle = {:s}\n'.format(self.guiConfig['windowTitle']))
        configFile.write('windowIcon = {:s}\n'.format(self.guiConfig['windowIcon'].split("\\")[-1]))
        configFile.write('maxFPS = {:d}\n'.format(self.guiConfig['maxFPS']))
        configFile.write('maxPPS = {:d}\n'.format(self.guiConfig['maxPPS']))
        configFile.write('MSAA = {:d}\n'.format(self.guiConfig['MSAA']))
        configFile.write('VSync = {:s}\n'.format(str(self.guiConfig['VSync'])))
        configFile.write('Language = {:s}\n'.format(self.guiConfig['Language']))
        configFile.write('ImageGenMSAA = {:d}\n'.format(self.guiConfig['ImageGenMSAA']))
        configFile.write('GUITheme = {:s}\n'.format(self.guiConfig['GUITheme']))
        configFile.write('AudioMute = {:s}\n'.format(str(self.guiConfig['AudioMute'])))
        configFile.write('AudioVolume = {:d}'.format(int(self.guiConfig['AudioVolume'])))
        configFile.close()

    def sysFunc_changeGUITheme(self, guiTheme):
        if (((guiTheme == 'LIGHT') and (self.guiConfig['GUITheme'] == 'DARK')) or ((guiTheme == 'DARK') and (self.guiConfig['GUITheme'] == 'LIGHT'))): self.guiConfig['GUITheme'] = guiTheme
        self.imageManager.on_GUIThemeUpdate()
        self.visualManager.on_GUIThemeUpdate()
        for pageName in self.pages.keys(): self.pages[pageName].on_GUIThemeUpdate()

    def sysFunc_changeLanguage(self, language):
        if (language in self.visualManager.availableLanguages): self.guiConfig['Language'] = language
        self.visualManager.on_LanguageUpdate()
        for pageName in self.pages.keys(): self.pages[pageName].on_LanguageUpdate()

    def sysFunc_editGUIOConfig(self, targetName, targetContent):
        try:
            self.guioConfig[targetName] = targetContent
            toWrite = list()
            for targetName1 in self.guioConfig:
                for targetName2 in self.guioConfig[targetName1]:
                    targetNameCombined = "{:s}_{:s}".format(targetName1, targetName2)
                    toWrite.append("{:s} = {:s}".format(targetNameCombined, str(self.guioConfig[targetName1][targetName2])))
            configFile = open(os.path.join(path_PROJECT, 'config', 'guioConfig.txt'), 'w')
            for index, line in enumerate(toWrite):
                if (index < len(toWrite)-1): configFile.write(line+"\n")
                else:                        configFile.write(line)
            configFile.close()
            print("CONFIG FILE SAVED!")
        except Exception as e: print(termcolor.colored("An unexpected error ocrrued while attempting to edit guioConfig.txt\n *", 'light_red'), termcolor.colored(e, 'light_red'))

    #System Functions END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Manager Internal Functions END -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






    #Input Hanlder Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __InputHandler_KeyPress(self, symbol, modifiers):
        if (symbol == 65480): self.__toggleFullscreen() #F11, no shift
        self.pages[self.currentPage].handleKeyEvent({'eType': "PRESSED", 'symbol': symbol, 'modifiers': modifiers})
    def __InputHandler_KeyRelease(self, symbol, modifiers):              self.pages[self.currentPage].handleKeyEvent({'eType': "RELEASED", 'symbol': symbol, 'modifiers': modifiers})
    def __InputHandler_MouseMotion(self, x, y, dx, dy):                  self.pages[self.currentPage].handleMouseEvent({'eType': "MOVED",    'x': x/self.displaySpaceDefiner['scaler'], 'y': y/self.displaySpaceDefiner['scaler'], 'dx': dx/self.displaySpaceDefiner['scaler'], 'dy': dy/self.displaySpaceDefiner['scaler']}) 
    def __InputHandler_MousePress(self, x, y, button, modifiers):        self.pages[self.currentPage].handleMouseEvent({'eType': "PRESSED",  'x': x/self.displaySpaceDefiner['scaler'], 'y': y/self.displaySpaceDefiner['scaler'], 'button': button, 'modifiers': modifiers})
    def __InputHandler_MouseRelease(self, x, y, button, modifiers):      self.pages[self.currentPage].handleMouseEvent({'eType': "RELEASED", 'x': x/self.displaySpaceDefiner['scaler'], 'y': y/self.displaySpaceDefiner['scaler'], 'button': button, 'modifiers': modifiers})
    def __InputHandler_MouseDrag(self, x, y, dx, dy, button, modifiers): self.pages[self.currentPage].handleMouseEvent({'eType': "DRAGGED",  'x': x/self.displaySpaceDefiner['scaler'], 'y': y/self.displaySpaceDefiner['scaler'], 'dx': dx/self.displaySpaceDefiner['scaler'], 'dy': dy/self.displaySpaceDefiner['scaler'], 'button': button, 'modifiers': modifiers})
    def __InputHandler_MouseScroll(self, x, y, scroll_x, scroll_y):      self.pages[self.currentPage].handleMouseEvent({'eType': "SCROLLED", 'x': x/self.displaySpaceDefiner['scaler'], 'y': y/self.displaySpaceDefiner['scaler'], 'scroll_x': scroll_x, 'scroll_y': scroll_y}) 
    #Input Hanlder Functions END --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------