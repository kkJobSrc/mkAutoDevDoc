import os, glob, json

def json2GuiMbr(gui, path):
    jFile = open(path, "r")
    conf = json.load(jFile)
    gui.repoPath   = str(conf["repository_path"])
    gui.branchName     = str(conf["branch_name"])
    gui.comNum     = int(conf["commit_num"])
    gui.outPath     = str(conf["output_path"])
    gui.codeDiffFlg    = bool(conf["code_diff_flg"])
    gui.pgrDir     = str(conf["pgr_dir_path"])
    gui.pgrFlg     = bool(conf["pgr_flg"])
    gui.undProcFlg = bool(conf["und_proc_flg"])
    gui.undFigFlg  = bool(conf["und_fig_flg"])


def guiMbr2Json(gui):
    conf = dict()
    conf["repository_path"] = gui.repoPath.get()   
    conf["branch_name"]     = gui.branchName.get()     
    conf["commit_num"]      = gui.comNum.get()     
    conf["output_path"]     = gui.outPath.get()     
    conf["code_diff_flg"]   = gui.codeDiffFlg.get()    
    conf["pgr_dir_path"]    = gui.pgrDir.get()     
    conf["pgr_flg"]         = gui.pgrFlg.get()      
    conf["und_proc_flg"]    = gui.undProcFlg.get() 
    conf["und_fig_flg"]     = gui.undFigFlg.get()   
    confPath = os.path.join("./conf/", gui.branchName.get().split("/")[-1]+".json")
    jFile = open(confPath, "w", encoding="utf-8")
    json.dump(conf, jFile, indent=2)

    return confPath

def mapPnlFlg(gui, dflt, jsn):
    gui.pnlDict["dflt"]["flg"] = dflt
    gui.pnlDict["json"]["flg"] = jsn


def mapJson2DfltPnl(gui):
    jFile = open(gui.jsonPath , "r")
    conf = json.load(jFile)

    gui.repoPath.set(str(conf["repository_path"]))
    gui.branchName.set( str(conf["branch_name"]))
    gui.comNum.set(int(conf["commit_num"]))
    gui.outPath.set(str(conf["output_path"]))
    gui.codeDiffFlg.set(bool(conf["code_diff_flg"]))
    gui.pgrDir.set(str(conf["pgr_dir_path"]))
    gui.pgrFlg.set(bool(conf["pgr_flg"]))
    gui.undProcFlg.set(bool(conf["und_proc_flg"]))
    gui.undFigFlg.set(bool(conf["und_fig_flg"]))