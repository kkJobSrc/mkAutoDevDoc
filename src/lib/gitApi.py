# -*- coding: utf-8 -*-

from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from unicodedata import name

from sympy import true
from . import common
import re, subprocess, git, os
import numpy as np

#############################
### Git Operating class #####
############################# 
class GITDIFF():
    def __init__(self, repoPath, branch, rtNum):
        self.repoPath = repoPath # The local repository path
        self.branch = branch     # The branchName
        self.rtNum = rtNum       # The number of retun from head 
        self.repo = git.Repo(self.repoPath) # The local repsitory information
        self.curBranch = self.repo.active_branch.name # Get the current baranch name.
        self.mthdList = [] # Fixed method List
        self.glbVarList =[] # Fixed global variable List
        self.fixfileList= [] # Fixed fixed files
        self.cFuncList =[] # C language functions 
        self.curHash = "" # New branch SHA-1
        self.srcHash = "" # Old branch SHA-1


    ## Returen to current branch
    def returenCurBranch(self):
        self.repo.git.checkout(self.curBranch)


    ### Checkout to target branch
    def chkout2TarBranch(self):
        try:
            self.repo.git.checkout(self.branch)
        except:
            self.repo.git.checkout(self.curBranch)


    ### Get the source branch SHA-1 ###
    def getSrcHash(self):
        try:
            chkoutFlg = False

            ## Checkout to the target baranch  
            if not(self.curBranch == self.branch):# The target branch is not the current branch.
                self.repo.git.checkout(self.branch)
                chkoutFlg = True
            elif not("HEAD" in self.branch):# The target branch is not HEAD.
                self.curBranch = self.branch
            else: # The target branch is HEAD.
                pass # Do nothing

            ## Get the source branch name.
            branchList = subprocess.run(["git", "show-branch"], cwd=self.repoPath, check=True,\
                shell=True, stdout=subprocess.PIPE).stdout.decode(encoding="utf-8").split('\n')

            # Match pattern: ++ * [BRANCH_NAME] or -- -[BRANCH_NAME] (+:Belong branch ,-:Merged commit)
            branchAst =[b for b in branchList if re.match(r'[\s\+\-]+[\*\-].*\[.*', b)]
            branchHead = [b for b in branchAst if not(self.curBranch in b)] # Remove current branch

            # Extract branch name
            origBranch = branchHead[0].split("[")[-1].split("]")[0]
            origBranch = origBranch.split("~")[0].split("^")[0]

            ## Get the source branch SHA-1 
            sha1List = subprocess.run(["git", "show-branch", "--sha1-name", self.curBranch, origBranch],\
                cwd=self.repoPath, check=True, shell=True, stdout=subprocess.PIPE).stdout.decode(encoding="utf-8").split('\n')
            # for s in sha1List:print(s)
            for s in sha1List[::-1]:
                if s:
                    origSha1 = s
                    break
        
            if chkoutFlg: self.repo.git.checkout(self.curBranch)
            return origSha1.split("[")[-1].split("]")[0]

        ## Checkout to current branch when occure error.
        except:
            print("Some error occured in getSrcHash() !!") 
            self.repo.git.checkout(self.curBranch)


    ### Get the target commit SHA-1 ###
    def getTrgHash(self):
        trgCommit = self.repo.iter_commits(self.branch, max_count=self.rtNum+1)# Get the HEAD~2 SHA-1  when setting "self.rtNum = 1"
        for i, c in enumerate(trgCommit):
            if(i == self.rtNum): return c.hexsha


    ### Get the unified diff from the local repository ###
    def getHash(self):
        ## The latest commit SHA-1 of the target branch 
        self.curHash = self.repo.git.rev_parse(self.branch) 

        ## The old version commit SHA-1
        if self.rtNum is None: self.srcHash = self.getSrcHash()
        else                 : self.srcHash = self.getTrgHash()
        print("Compare :", self.curHash, "and", self.srcHash)


    ### Get the unified diff from the local repository ###
    def getUdiff(self, ext=["*.c", "*.h", "*.cpp"] ):
        ## Run "git diff" command on Powershell
        cmd = ["git", "diff", self.srcHash, self.curHash] + ext
        diff = subprocess.run(cmd, cwd=self.repoPath,
                                                    check=True, shell=True, stdout=subprocess.PIPE)
        diff = diff.stdout.decode(encoding="shift-jis", errors='ignore').split('\n')
        return diff


    ### Extract some information from the unified diff ### 
    def srchUniDiff(self, diff, rgxp, lineHead, headFlg=False):
        resList = np.array([], dtype=object) # The serach result for return
        lNumList =np.array([], dtype=int) # The row num. in unidiff
        extrPtn = re.compile(rgxp) #The extra patarn in regxp

        for i, l in enumerate(diff): #Search all lines
            if lineHead in l:
                if headFlg: chkStr = extrPtn.match(l[1:])
                else      : chkStr = extrPtn.search(l)
                if not(chkStr is None):
                    if headFlg: res=("".join(chkStr.group().split(" ")[-1] ))
                    else      : res=("".join(chkStr.group()))
                    resList = np.append(resList ,res.replace(" ",""))
                    lNumList = np.append(lNumList, i)
        resList = np.hstack((lNumList[:,np.newaxis], resList[:,np.newaxis]))
        # resList = list(set(resList)) # Delete overlapping componets
        # resList = sorted(resList)
        # for m in resList: print(m)
        return resList


    ### Extract changes and row no. from the unified diff ###
    def getChgDetale(self):
        diff = self.getUdiff()
        self.mthdList = self.srchUniDiff(diff, "(?<=\s)[\w]+::[\w]+(?=\()", "@@")   # Calass method
        self.glbVarList = self.srchUniDiff(diff, "(?<=#define)\s+[\w]+", "+")       # Macro
        self.fixfileList = self.srchUniDiff(diff, "[\w]+\.[\w]+", "diff")           # fileName

        self.cFuncList = self.srchUniDiff(diff, "[\w]+\s*(?=\()", "@@")
        self.cFuncList = np.vstack((self.cFuncList, self.srchUniDiff(diff, "[\w]+\s+[\w]+(?=\()", "+", True)))


    ### Identify changes  ###
    def idnetchgFile(self):
        chgDetail = []
        for i, fl in enumerate(self.fixfileList):# **List = [row no., ** name] 
            for j, mthd in enumerate(self.mthdList):
                if (i < self.fixfileList.shape[0] - 1):
                    row = [fl[1], mthd[1].split("::")[0], mthd[1].split("::")[-1]]
                    if(fl[0] <= mthd[0] and mthd[0] < self.fixfileList[i+1,0] ):
                        if not(row in chgDetail): chgDetail.append(row) 
                else:
                    if(fl[0] <= mthd[0]): # Final fixed file 
                        if not(row in chgDetail): chgDetail.append(row)

            for k, glb in enumerate(self.glbVarList):
                if (i < self.fixfileList.shape[0] - 1):
                    if(fl[0] <= glb[0] and glb[0] < self.fixfileList[i+1,0] ):
                        chgDetail.append([fl[1], "-", glb[1]]) 
                else:
                    if(fl[0] <= glb[0]):
                        chgDetail.append([fl[1], "-", glb[1]])
            
            for cFunc in self.cFuncList:
                if (i < self.fixfileList.shape[0] - 1):
                    if(fl[0] <= cFunc[0] and cFunc[0] < self.fixfileList[i+1,0] ):
                        if not(cFunc[0] in self.mthdList[:,0]): 
                            chgDetail.append([fl[1], "--", cFunc[1]]) 
                else:
                    if(fl[0] <= cFunc[0]):
                        chgDetail.append([fl[1], "--", cFunc[1]])
        return chgDetail


    def getChgFileRows(self):
        diff = self.getUdiff()
        diffInfoList=[]
        for i, info in enumerate(self.fixfileList):
            sL = self.fixfileList[i,0] #File start line
            if i < len(self.fixfileList)-1:
                eL = self.fixfileList[i+1,0] #File end line
                fileRows = diff[sL:eL]
            else:
                fileRows = diff[sL:]
            rowList =[]
            for j, row in enumerate(fileRows):
                rNo = re.match(r'@@.*@@', row.strip())
                if None != rNo:
                    startRow = int(rNo.group().split(' ')[2].split(',')[0])
                    chgChnk = int(rNo.group().split(' ')[2].split(',')[1])
                    enDiff = [ f for f in fileRows[j+1: (j+1)+chgChnk] if not(f.startswith('-'))]
                    tmpRows = [k + startRow for k, r in enumerate(enDiff) if r.startswith('+')]
                    rowList.extend(tmpRows)
            
            diffInfoList.append([info[1], rowList])
        return diffInfoList


    ### Get changed file relative path ##
    def getChgFilePath(self, hash1, hash2):  
        cmd = ["git", "diff", "--irreversible-delete", "--diff-filter=d", "--name-only"]
        fileList = subprocess.run(cmd+[hash1, hash2], cwd=self.repoPath, shell=True, stdout=subprocess.PIPE)
        fileList = fileList.stdout.decode(encoding="shift-jis", errors='ignore').split('\n')
        return [n for n in fileList if n]


    ### Create diff. file archives(*.zip)  ###
    def getChgFileArchiveZip(self, hash1, files, outDir):
        outPath = os.path.join(outDir, "archive.zip")
        outPath = os.path.join(os.getcwd(), outPath)
        cmd = ["git", "archive", "--format=zip", "--prefix=root/", hash1]
        cmd.extend(files)
        cmd.extend(["-o", outPath])
        subprocess.run(cmd, cwd=self.repoPath, shell=True)
        return outPath

