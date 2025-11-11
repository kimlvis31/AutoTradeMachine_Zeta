# AutoTradeMachine_Zeta

This is the sixth version of the **Auto Trade Machine** project.

The main aspects of this version are:

**1. GUI Platform Transition (Tkinter -> Pyglet)**  
    Due to its dependence only on CPU, tkinter showed clear limitations as a foundation for building a *ChartDrawer* GUI object, which handles large datasets and requires fast view transitions.  
    Its event-driven mechanism also proved to be inadequate for constructing a generalized GUI management framework, as seperate event-hadling control functions were often required to prevent over-computation in cases where display data updates occur frequently.  
  
**2. Modularized GUI Subsystem**  
    A fully modular GUI subsystem has been established. To simplify GUI resource management, the GUI system now includes three dedicated submanagers:  
        1. **Visual Manager**: Allows the main GUI manager to update and retrieve GUI components variables such as language-dependent string data, object colors, etc in a formatted form through a single pipeline.  
        2. **Image Manager**: Identifies and loads or creates image files used for GUI upon initialization and during run-time.  
        3. **Audio Manager**: Identifies and loads audio files used by GUI objects.  
    While simple GUI components are written in a single file named *'ATM_Zeta_GUIO_Generals.py'*, more advanced GUI components like ChartDrawers are now written in their own seperate files for easier maintenance.  
  
**3. Multi-Language Support**  
    Text display data for GUI objects was previously hard-coded in the source code. Now they are managed using 'keys' in a seperate textpack file called *'ATM_Zeta-GUI_TextPack.py'* as a python dictionary type. Each item has both English and Korean version, which allows easy runtime language switching through the *Visual Manager*.  
  
**4. Audio**  
    Thanks to *pyglet* for providing its own easy-to-use audio playing features, this version can now play sounds.  
  
**5. Configuration-based Launch System**  
    Currently used primarily for storing GUI user-interface data, the application now uses external configuration files to setup GUI system and components, and determines number of *RTAs (Real-Time Analyzer)* and market asset subscription list.  
  
**6. Mutiple RTAs (Real-Time Analyzer)**  
    Upon application launch, the system environment is analyzed (currently only the number of CPU cores) to determine the number of *RTAs (Real-Time Analyzer)*.  
  
**7. Market Data Management Using Sqlite3 '.db' formats**  
    Local market data are now stored in '.db' formats using *Sqlite3*.  
    Efficient and selective data retrieval is essential for an automated trading system. *Sqlite3* provided light yet heavy enough resources to build a database system for such a system.  
  
**8. Improved and Generalized IPC Module**  
    The inter-process communication module has been updated for flexibility and robustness.  
        1. Decentralized inter-process communication  
        2. [REMOVED] DAR (Data Acquisition Request)  
        3. Updated message queue control mechanism  
  
**9. [REMOVED] Logger Class**  
    Logger class has been removed. Even though it proved to be useful in generated unified logs and messages, its implementation was limited for at this starge of development. It will be reintroduced in the future once event and data-flow schemes become more clear.  
  
---

### 🗓️ Project Duration
**March 2024 – September 2024**

---

### 📄 Document Info
**Last Updated:** November 12th, 2025  
**Author:** Bumsu Kim  
**Email:**  kimlvis31@gmail.com  
