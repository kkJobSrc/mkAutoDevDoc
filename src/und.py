# -*- coding: utf-8 -*-

from . import lib
import os, sys, glob, subprocess
sys.path.append( lib.common.getEnvConf("und", "path") )
import understand

############# User parameters ######################
### Understand called by graph options ###
LEVELNUM = lib.common.getEnvConf("und", "disp_level")
NAMEOPT = lib.common.getEnvConf("und", "disp_mthd_name")

### Proccessing option strings ###
LEVELSTR = " level" if LEVELNUM == 1 else " levels"
OPTIONLIST = [
                "Name=" + NAMEOPT, 
                "Level="+ str(LEVELNUM) + LEVELSTR
            ]
OPTIONS = ";".join(OPTIONLIST)
##################################################



#####################################
### Understand  Operating class #####
#####################################
class UND():
    def __init__(self, udbDir, outDir):
        self.dbDir = udbDir # The directory existing an udb file
        self.dbPath = glob.glob(os.path.join(self.dbDir, "*.udb")) # An udb file path
        
        if self.dbPath: #Exist UDB file
            self.dbPath = self.dbPath[0]
        else:
            self.dbPath = os.path.join(self.dbDir, "analyze.udb")
        self.outDir = outDir # An output graph directory


    ### Draw callby graphs with undarstand ###
    def drawCallbyGraph(self, chgLst):
        if(len(chgLst) != 0):
            print("-- Draw called by Graph")
            for chg in chgLst: # chgLst = [file name, typ or class, func. name]
                if chg[1] != "macro":
                    if chg[1] == "func": #C function
                        uniName = "c"+ chg[2] + "@file=RELATIVE:" + chg[0]
                        graphName = os.path.basename(chg[0]).split(".")[0]
                        graphName += "_" + chg[2]+".png"
                        ent = self.db.lookup_uniquename(uniName)
                        
                    else: #Cpp method
                        name = chg[1] + "::" + chg[2]
                        graphName = chg[1] + "_" + chg[2] + ".png"
                        ent = self.db.lookup(name)[0]
                    print(ent.longname())
                    path = os.path.join(self.outDir, graphName)
                    ent.draw("Called By", path, OPTIONS)
            print("-- END")


    ### Get global variavle info ###
    def getGlbVarInfo(self, macroList):
        if (macroList.shape[0] > 0):
            dfList = [["Name", "Ref.", "Ent.", "File", "Row", "Col."]]
            print("--Get fixed macro information")
            for ent in self.db.ents("Macro"):
                #print(ent)
                if ent.name() in macroList:
                    print(ent.name())
                    for ref in ent.refs():
                        dfList.append(list(map(str, [ent.name(), ref.kindname(), ref.ent(), # Macro name, def. or use, ent. name 
                                                ref.file(), ref.line(), ref.column()]))) # File name, row number, colum number 
            print("--End")
            return dfList


    ### Main process ###
    def mainProc(self, gitApi):
        #try:
        if 1:
            print("== Star UND result analysis ==")
            self.db = understand.open(self.dbPath)  
            ## Proc git diff analysis
            chgList = gitApi.getAllChgLst()

            ## Proc. understand analysis
            self.drawCallbyGraph(chgList)
            chgMacros = self.getGlbVarInfo(gitApi.macroList ) # Get global variavle info
            lib.common.outList2Csv(chgList, self.outDir, "chgFileList.csv")
            lib.common.outList2Csv(chgMacros, self.outDir, "chgMacroList.csv")

        # except:
        #     print("** UND analysis fault. **")

        # finally:
        #     gitApi.returenCurBranch()
        #     print("== End UND result analysis ==")


    ### Create understand data base ###
    def createDB(self, gitApi):
        if os.path.isfile(self.dbPath):# Del. old UDB file
            os.remove(self.dbPath)

        try:
            print("== Star creating understand data-base ==")
            gitApi.chkout2TarBranch()
            dbName = os.path.basename(self.dbPath)
            subprocess.run(["und", "create", "-db", dbName, "-languages", "c++"], cwd=self.dbDir)
            subprocess.run(["und", "add", ".", dbName], cwd=self.dbDir)
            subprocess.run(["und", "settings", "-AddMode", "Relative", dbName], cwd=self.dbDir)
            subprocess.run(["und", "analyze", "-all", "-db", dbName], cwd=self.dbDir)

        except:
            print("** Understand analysis fault. **")

        finally:
            gitApi.returenCurBranch()
            print("== End creating understand data-base ==")

