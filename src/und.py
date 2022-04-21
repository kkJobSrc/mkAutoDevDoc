# -*- coding: utf-8 -*-

from . import lib
import os, sys, glob, subprocess
import pandas as pd
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
        self.chgLstTab = pd.DataFrame()


    ### Draw callby graphs with undarstand ###
    def drawCallbyGraph(self, chgList):
        if(len(chgList) != 0):
            ## Set change list table
            self.chgLstTab = pd.DataFrame(chgList, columns =["file","cls","func"])
            self.chgLstTab["fig"] = ""

            print("-- Draw called by Graph")
            for row in self.chgLstTab.itertuples(): # chgLst = [file name, typ or class, func. name]
                if row.cls != "macro":
                    if row.cls == "func": #C function
                        ## Undesrstand unique name
                        uniName = "c"+ row.func\
                                + "@file=RELATIVE:" + row.file

                        ## Graph figure name 
                        graphName = os.path.basename(row.file).split(".")[0]
                        graphName += "_" + row.func+".png"
                        ent = self.db.lookup_uniquename(uniName) # Get entity wiht unique name
                        
                    else: #Cpp method
                        ## Understand  reference name
                        name = row.cls + "::" +row.func
                        
                        ## Graph figure name 
                        graphName = row.cls + "_" + row.func + ".png"
                        ent = self.db.lookup(name)[0]# Get entity wiht name
    
                    ## Output called by fig
                    if not(ent is None):
                        print(ent.longname())
                        path = os.path.join(self.outDir, graphName).replace(os.path.sep, '/')
                        ent.draw("Called By", path, OPTIONS)
                        self.chgLstTab.iloc[row[0], 3] = graphName
                    else:
                        print("Draw graph fault: ", row.func, "(", row.cls, ")")
            print("-- END")


    ### Get global variavle info ###
    def getGlbVarInfo(self, macroList):
        if (macroList.shape[0] > 0):
            dfList = [["Name", "Ref.", "Ent.", "File", "Row", "Col."]]
            print("--Get fixed macro information")
            for ent in self.db.ents("Macro"):
                #print(ent)
                if ent.name() in macroList:
                    print(ent.name(), ent.uniquename())
                    for ref in ent.refs():
                        dfList.append(list(map(str, [ent.name(), ref.kindname(), ref.ent(), # Macro name, def. or use, ent. name 
                                                ref.file(), ref.line(), ref.column()]))) # File name, row number, colum number 
            print("--End")
            return dfList


    ### Arrange output table ###
    def outputChgTable(self):
        outTable = self.chgLstTab
        outTable = outTable[outTable["cls"] != "macro"]
        outTable["file"] = outTable["file"].replace(r"^.*\\", "", regex=True)
        del outTable["fig"]

        path = os.path.join(self.outDir, "chang_file_list.csv")
        outTable.to_csv(path)


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
            lib.mkUndDoc.writeMdTxt(self.chgLstTab, self.outDir)
            self.outputChgTable()
            lib.common.outList2Csv(chgMacros, self.outDir, "change_macro_list.csv")

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

