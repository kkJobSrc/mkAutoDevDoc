# -*- coding: utf-8 -*-

from ast import arg
from encodings import utf_8
import src
from src import lib

import argparse, os, glob, json

def getGitInfo(repoPath,  branch, rtNum):
    gitInfo = lib.gitApi.GITDIFF(repoPath,  branch, rtNum)
    gitInfo.getHash() # Get target SHA-1's
    gitInfo.getChgDetale() # Analysis Git unidiff (chg. file names, mehtd etc..)
    
    return gitInfo


def setUpOutDir(outDir):
    lib.common.cleanUpOutDir(outDir)
    lib.common.createOutDir(outDir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--repoPath', '-r',      	type=str,   default=None, 	help='Local repository path.')
    parser.add_argument('--branch', '-b',   type=str,	default="HEAD", help='Target branch name.')
    parser.add_argument('--rtnNum', '-n',   type=int,	default=None, 	help='The number of commit.')
    parser.add_argument('--output', '-o',   type=str,   default="./result/default", 	help='Output directory path.')
    parser.add_argument('--codeFlg', '-c',  action='store_true', 	help='Analysis code diff. flag.')
    parser.add_argument('--pgrDir', '-d',   type=str,	default=None, help='Target branch name.')
    parser.add_argument('--pgrFlg', '-s',   action='store_true',	help='Extract PGR result flag.')
    parser.add_argument('--undProcFlg', '-p',   action='store_true', 	help='Create understand Data-base flag.')
    parser.add_argument('--undFigFlg', '-f',   action='store_true', 	help='Affection analysis flag.')
    parser.add_argument('--jsonFlg', '-j',   action='store_true', 	help='Read conf/setup.json flag.')
    parser.add_argument('--jsonPath', '-jp',   type=str, default="./conf/default.json", help='Read .JSON path.')


    args = parser.parse_args()
    
    ### Read config JSON file.
    if args.jsonFlg:
        args = lib.common.getAnaConf(args)
    else:
        lib.common.setAnaConf(args)

    if not(args.jsonFlg) and args.repoPath == None:
        print("Please enter your options")
        exit()


    ### Initalize gitApi and output directory ###
    setUpOutDir(args.output)
    gitApi = getGitInfo(args.repoPath, args.branch, args.rtnNum)

    ### Exract PGR
    if not(args.pgrDir is None): # Input directory name
        if args.pgrFlg: # Option flg. is Ture
            pgrResList = glob.glob(os.path.join(args.pgrDir, "*.csv"))
            if pgrResList: #Exist PRG result csv
                pgrAna = src.PGR(pgrResList, args.output)
                pgrAna.mainProc(gitApi)

    ###  Processing understand analysis ###
    if (args.undProcFlg or args.undFigFlg):
        und = src.UND(args.repoPath, args.output)
        if args.undProcFlg: # Create undestand data-base
            und.createDB(gitApi)
        if args.undFigFlg: # Affection analysis by understand
            und.mainProc(gitApi)

    ### Create code diff PDF
    if args.codeFlg:
        code = src.CODEDIFF(args.output)
        code.maniProc(gitApi)
