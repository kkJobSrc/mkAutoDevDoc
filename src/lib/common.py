import os, glob, json, csv


### Delete figures in an output directory ### 
def cleanUpOutDir(outDir):
    if(os.path.isdir(outDir)):
        pathList = glob.glob(os.path.join(outDir,"**/*.*"), recursive=True)
        for p in pathList: # Remove files
            if os.path.isfile(p): os.remove(p)

        for p in pathList: # Remove directoris
            if os.path.isdir(p): os.rmdir(p)
        print("Clean up the old files!!")


### Create an outpur directory ###
def createOutDir(outDir):
    if(not(os.path.isdir(outDir))):
        os.makedirs(outDir)
        print("Create the output directory!!")


### Output list  to CSV file ###
def outList2Csv(lst, outDir=None, name=None):
    if(lst != None):
        if outDir!= None and name!= None:
            path = os.path.join(outDir, name)
        else:
            path = outDir

        with open(path, "w", encoding="SHIFT-JIS") as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            csvWriter.writerows(lst)


def setAnaConf(args):
    conf = dict()
    conf["repository_path"] = args.repoPath   
    conf["branch_name"]     = args.branch     
    conf["commit_num"]      = args.rtnNum     
    conf["output_path"]     = args.output      
    conf["code_diff_flg"]   = args.codeFlg    
    conf["pgr_dir_path"]    = args.pgrDir     
    conf["pgr_flg"]         = args.pgrFlg      
    conf["und_proc_flg"]    = args.undProcFlg 
    conf["und_fig_flg"]     = args.undFigFlg   
    confPath = os.path.join("./conf/", args.branch.split("/")[-1]+".json")
    jFile = open(confPath, "w", encoding="utf-8")
    json.dump(conf, jFile, indent=2)
    return args


def getAnaConf(args):
    jFile = open(args.jsonPath, "r")
    conf = json.load(jFile)
    args.repoPath   = str(conf["repository_path"])
    args.branch     = str(conf["branch_name"])
    args.rtnNum     = int(conf["commit_num"])
    args.output     = str(conf["output_path"])
    args.codeFlg    = bool(conf["code_diff_flg"])
    args.pgrDir     = str(conf["pgr_dir_path"])
    args.pgrFlg     = bool(conf["pgr_flg"])
    args.undProcFlg = bool(conf["und_proc_flg"])
    args.undFigFlg  = bool(conf["und_fig_flg"])
    return args


def getEnvConf(sec, subSec=None):
    confPath = "./conf/setup.json"
    jFile = open(confPath, "r", encoding="utf-8")
    jWhole = json.load(jFile)
    if subSec==None: conf = jWhole[sec]
    else           : conf = jWhole[sec][subSec]
    return conf



