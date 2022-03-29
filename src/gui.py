import os, glob
import tkinter as tk
from tkinter import ttk, filedialog
from unittest import result

from .und import UND
from .pgr import PGR
from .codeDiff import CODEDIFF

from . import lib

class GUI():
    def __init__(self):
        # Panael base dict
        self.pnlDict = {
            "init":{"bdy":None, "flg":False}, 
            "dflt":{"bdy":None, "flg":False},
            "json":{"bdy":None, "flg":False}
        }

        # User parameters(default panel)
        self.repoPath    = "" # tk.StringVar()
        self.branchName  = "" # tk.StringVar()
        self.comNum      = "" # tk.StringVar()
        self.outPath     = "" # tk.StringVar()
        self.codeDiffFlg = False # tk.BooleanVar()
        self.pgrDir      = "" # tk.StringVar()
        self.pgrFlg      = False # tk.BooleanVar()
        self.undProcFlg  = False # tk.BooleanVar()
        self.undFigFlg   = False # tk.BooleanVar()
        self.jsonPath    = "" # tk.StringVar()

    # =+=+=+ Set up GUI panels  +=+=+= #
    ### Seting panel layout ###
    def setPnlGrd(self, components):
        for i, cmp in enumerate(components):
            if isinstance(cmp, list):
                for j, c in enumerate(cmp):
                    c.grid(row=i, column=j+2, sticky="W")
            else:
                cmp.grid(row=i, column=2, sticky="W")


    ### Delete GUI panle ###
    def delPnl(self, pnl):
        self.pnlDict[pnl]["bdy"].destroy()
        self.pnlDict[pnl]["bdy"] = None
        self.pnlDict[pnl]["flg"] = False


    ### Set initial panel ###
    def setInitPnl(self):
        ## Inital panel root
        self.pnlDict["init"]["bdy"] = tk.Tk()
        self.pnlDict["init"]["bdy"].geometry('300x100') # windwo size
        self.pnlDict["init"]["bdy"].title('') # window title

        ## User parameters
        self.pnlDict["dflt"]["flg"] = tk.BooleanVar()
        self.pnlDict["json"]["flg"] = tk.BooleanVar()

        ## Initial panel commponents
        self.initPnlCmp =[
            tk.Label(self.pnlDict["init"]["bdy"], text=" Select parameter setting mode..."),
            tk.Checkbutton(self.pnlDict["init"]["bdy"],  variable=self.pnlDict["dflt"]["flg"], text='with manual input'),
            tk.Checkbutton(self.pnlDict["init"]["bdy"],  variable=self.pnlDict["json"]["flg"], text='with JSON file'),
            [# Controll button
                tk.Button(self.pnlDict["init"]["bdy"], text="Exsit", command=self.exitBtn),
                tk.Button(self.pnlDict["init"]["bdy"], text="Next>>", command=self.nextBtn)
            ]
        ]

        ## Draw Initial 
        self.pnlDict["init"]["flg"] = True
        self.setPnlGrd(self.initPnlCmp)
        self.pnlDict["init"]["bdy"].mainloop()


    def defDfltPnlParam(self):
        ## User parameters  
        self.repoPath    = tk.StringVar()
        self.branchName  = tk.StringVar()
        self.comNum      = tk.StringVar()
        self.outPath     = tk.StringVar()
        self.codeDiffFlg = tk.BooleanVar()
        self.pgrDir      = tk.StringVar()
        self.pgrFlg      = tk.BooleanVar()
        self.undProcFlg  = tk.BooleanVar()
        self.undFigFlg   = tk.BooleanVar()


    ### Set default panel ###
    def setDfltPnl(self, jsonSetFlg=False):
        ## Default panel root
        self.pnlDict["dflt"]["bdy"] = tk.Tk() # Init. Tk
        self.pnlDict["dflt"]["bdy"].geometry('350x300') # windwo size
        self.pnlDict["dflt"]["bdy"].title('Setting manually analysis conf.') # window title

        self.defDfltPnlParam()
        if jsonSetFlg: 
            lib.guiMod.mapJson2DfltPnl(self)

        ## Default panel commponents
        self.dfltPnlCmp = [
                tk.Label(self.pnlDict["dflt"]["bdy"], text="Local repository path"), # Entry box for laocal repository path 
                [
                    ttk.Entry(self.pnlDict["dflt"]["bdy"], textvariable=self.repoPath),
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="Browse", command = self.setRepoPath)
                ],
                tk.Label(self.pnlDict["dflt"]["bdy"], text="Branch - Num."),        # Entry box for branch name
                [
                    ttk.Entry(self.pnlDict["dflt"]["bdy"], textvariable=self.branchName),
                    ttk.Entry(self.pnlDict["dflt"]["bdy"], textvariable=self.comNum),
                ],
                tk.Label(self.pnlDict["dflt"]["bdy"], text="Output folder"), # Entry box for output directory
                [
                    ttk.Entry(self.pnlDict["dflt"]["bdy"], textvariable=self.outPath),
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="Browse", command=self.setOutpath)
                ],
                tk.Checkbutton(self.pnlDict["dflt"]["bdy"], variable=self.codeDiffFlg, text='Create code-diff PDF'),# Check box for create code-diff PDF file
                tk.Checkbutton(self.pnlDict["dflt"]["bdy"], variable=self.pgrFlg, text='Analysis PG-Relife result '),# Entry and check box for PG-Relife result analysis
                [
                    ttk.Entry(self.pnlDict["dflt"]["bdy"], textvariable=self.pgrDir),
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="Browse", command=self.setPgrDir)
                ],
                tk.Checkbutton(self.pnlDict["dflt"]["bdy"], variable=self.undProcFlg, text='Create understand DB'),
                tk.Checkbutton(self.pnlDict["dflt"]["bdy"], variable=self.undFigFlg, text='Analysis understand DB'),
                [# Controll button
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="<< Back", command=self.backBtn),
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="Exsit", command=self.exitBtn),
                    tk.Button(self.pnlDict["dflt"]["bdy"], text="Excute", command=self.excuteBtn)
                ]
            ]

        ## Draw default panel
        self.setPnlGrd(self.dfltPnlCmp)
        self.pnlDict["dflt"]["bdy"].mainloop()


    ### Set json mode panel ###
    def setJsonPnl(self):
        ## Json mode panel root
        self.pnlDict["json"]["bdy"] = tk.Tk()
        self.pnlDict["json"]["bdy"].geometry('300x80') # windwo size
        self.pnlDict["json"]["bdy"].title('') # window title

        ## User parameters
        self.jsonPath    = tk.StringVar()

        ## Json mode panel commponents
        self.jsonPnlCmp =[
            tk.Label(self.pnlDict["json"]["bdy"], text="Select config. json file."),
            [
                ttk.Entry(self.pnlDict["json"]["bdy"], textvariable=self.jsonPath),
                tk.Button(self.pnlDict["json"]["bdy"], text="Browse", command=self.setJsonPath)
            ],
            [# Controll button
                tk.Button(self.pnlDict["json"]["bdy"], text="<< Back", command=self.backBtn),
                tk.Button(self.pnlDict["json"]["bdy"], text="Exsit", command=self.exitBtn),
                tk.Button(self.pnlDict["json"]["bdy"], text="Next >>", command=self.setBtn)
            ]
        ]
        ## Draw json mode panle 
        self.setPnlGrd(self.jsonPnlCmp)
        self.pnlDict["json"]["bdy"].mainloop()


    # =+=+=+ Set file or Directory name to gui-variable. +=+=+= #
    ### Selscet folder ####
    def dirDialogClick(self):
        iDir = os.getcwd()
        iDirPath = filedialog.askdirectory(initialdir = iDir)
        return iDirPath


    ### Select json file ###
    def jsonDialogClick(self):
        fTyp = [("", "*.json")]
        iFile = os.getcwd()
        iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
        return iFilePath

    def setRepoPath(self) : self.repoPath.set(self.dirDialogClick())
    def setOutpath(self)  : self.outPath.set(self.dirDialogClick())
    def setPgrDir(self)   : self.pgrDir.set(self.dirDialogClick())
    def setJsonPath(self) : self.jsonPath.set(self.jsonDialogClick())
    

    # =+=+=+ Define button action +=+=+= #
    ### "Exit" button action ###
    def exitBtn(self, pnl=""):
        if not(pnl):
            for k in self.pnlDict:  
                if not(self.pnlDict[k]["bdy"] is None):
                    self.delPnl(k)
        else:
            self.delPnl(pnl)


    ### "Back" button action ###
    def nextBtn(self):
        dfltFlg = self.pnlDict["dflt"]["flg"].get()
        jsonFlg = self.pnlDict["json"]["flg"].get()
        
        if ((dfltFlg and jsonFlg) or (not(dfltFlg) and not(jsonFlg)) ):
            pass
            #tk.messagebox.showinfo("Nofitication", "Please select either of one manual or json mode.")

        else:
            lib.guiMod.mapPnlFlg(self, dfltFlg, jsonFlg)
            self.delPnl("init")

            if(self.pnlDict["dflt"]["flg"]): # Select manula setting mode(default)
                self.setDfltPnl()

            if(self.pnlDict["json"]["flg"]): # Select json mode
                self.setJsonPnl()


    ### "Next" button action ###
    def backBtn(self):
        self.exitBtn()
        self.setInitPnl()

    ### "Set" button action ##
    def setBtn(self):
        if self.jsonPath.get():
            self.jsonPath = self.jsonPath.get()
            self.delPnl("json")
            self.pnlDict["dflt"]["flg"] = True
            self.setDfltPnl(jsonSetFlg=True)
        else:
            pass

    ### "Excute" button action ###
    def excuteBtn(self):
        ## Read config JSON file.
        if self.pnlDict["json"]["flg"]:
            lib.guiMod.json2GuiMbr(self, self.jsonPath.get())
        if self.pnlDict["dflt"]["flg"]:
            #lib.guiMod.map2guiMbr(self)
            self.jsonPath = lib.guiMod.guiMbr2Json(self)

        if self.repoPath == None:
            pass
            #tk.messagebox.showinfo("Nofitication", "Please input local repository path.")

        ## Initalize gitApi 
        gitApi = lib.gitApi.GITDIFF(self.repoPath.get(), # Repository path
                                    self.branchName.get(), # Branch name
                                    int(self.comNum.get()) ) # Numbaer of return
        gitApi.getHash() # Get target SHA-1's
        gitApi.getChgDetale() # Analysis Git unidiff (chg. file names, mehtd etc..)
        
        ## Clean up and create Output directory
        lib.common.cleanUpOutDir(self.outPath.get())
        lib.common.createOutDir(self.outPath.get())

        ### Exract PGR
        if not(self.pgrDir is None): # Input directory name
            if self.pgrFlg.get(): # Option flg. is Ture
                pgrResList = glob.glob(os.path.join(self.pgrDir.get(), "*.csv"))
                if pgrResList: #Exist PRG result csv
                    pgrAna = PGR(pgrResList, self.outPath.get())
                    pgrAna.mainProc(gitApi)

        ###  Processing understand analysis ###
        if (self.undProcFlg.get() or self.undFigFlg.get()):
            und = UND(self.repoPath.get(), self.outPath.get())
            if self.undProcFlg.get(): # Create undestand data-base
                und.createDB(gitApi)
            if self.undFigFlg.get(): # Affection analysis by understand
                und.mainProc(gitApi)

        ### Create code diff PDF
        if self.codeDiffFlg.get():
            code = CODEDIFF(self.outPath.get())
            code.maniProc(gitApi)
