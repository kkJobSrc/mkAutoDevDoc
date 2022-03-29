# -*- coding: utf-8 -*-
from . import lib
import os, zipfile, glob, subprocess


class CODEDIFF():
    def __init__(self, outDir):
        contextNum = lib.common.getEnvConf("winmrg", "contesxt")  #コンテキストの行数
        self.optContext= "Settings/DiffContextV2=" + str(contextNum)

        self.outDir = outDir
        self.codeDir = os.path.join(self.outDir, "code")
        self.oldCode = os.path.join(self.codeDir, "old")
        self.curCode = os.path.join(self.codeDir, "cur")
        self.htmlDir = os.path.join(self.codeDir, "html")
   
        lib.common.createOutDir(self.codeDir)
        lib.common.createOutDir(self.oldCode)
        lib.common.createOutDir(self.curCode)
        lib.common.createOutDir(self.htmlDir)


    def createArchves(self, gitApi):
        ## Get old src. code archives
        files = gitApi.getChgFilePath(gitApi.curHash, gitApi.srcHash)
        zipPath = gitApi.getChgFileArchiveZip(gitApi.srcHash, files, self.oldCode)
        with zipfile.ZipFile(zipPath) as tarZip:
            tarZip.extractall(self.oldCode)
        os.remove(zipPath)

        ## Get current src. code archives
        files = gitApi.getChgFilePath(gitApi.srcHash, gitApi.curHash)
        zipPath = gitApi.getChgFileArchiveZip(gitApi.curHash, files, self.curCode)
        with zipfile.ZipFile(zipPath) as tarZip:
            tarZip.extractall(self.curCode)
        os.remove(zipPath)


    def procWinmrg(self):
        curPathList = glob.glob(os.path.join(self.curCode, "**/*.*"), recursive=True)
        oldPathList = glob.glob(os.path.join(self.oldCode, "**/*.*"), recursive=True)

        for cur, old in zip(curPathList, oldPathList):
            name = cur.split(os.sep)[-3:]
            name= "_".join(name)
            htmlName = os.path.join(self.htmlDir, name + ".html")

            cmd = [ "winmergeu.exe", old, cur, "-cfg", self.optContext, 
                    "-minimize", "-noninteractive", "-u", "-or", htmlName]
            subprocess.run(cmd, shell=True)
            print("Output HTML::", name)


    def maniProc(self, gitApi):
        try:
            print("== Star creating code diff. ==")
            self.createArchves(gitApi)
            self.procWinmrg()

            htmls = glob.glob(os.path.join(self.htmlDir, "*.html"))
            driver = lib.convPdf.initDriver()
            for html in htmls:
                print(os.path.basename(html).split(".")[0])
                lib.convPdf.html2Pdf(html, self.htmlDir, driver)
            lib.convPdf.endDriver(driver)
            lib.convPdf.joinPdfs(self.htmlDir, self.outDir)

        except:
            print("** Create code diff. fault. **")

        finally:
            print("== End creating code diff. ==")





