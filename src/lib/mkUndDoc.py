import os, re
from PIL import Image
import pandas as pd

FIX_RESOLUTION = 130 #解像度
MAX_FIG_RATE = 70 #最大倍率
NEW_PAGE_SEC_NUM = 3 #改ページする章の数
A4_SIZE = {"width":8.27 , "heigt":11.69}


### Set figure size ###
def chapTitleStr(row, chapNo, preTitle):
    title =""

    ## Extract file name form table and title
    curFile = re.search(r"[^\\]+$", row.file).group()
    if preTitle: preFile = re.search(r"[^\\\s]+$", preTitle).group()
    else       : preFile = ""

    ## Make title strings
    if (row.cls == "func"): # Section title (C function) 
        if (not(preTitle) or curFile != preFile): 
            title = "## " + str(chapNo+1) + ". "\
                    + row.file  +"\n" # Set Class or file name

    else: # Section title (Cpp class)
        if (not(preTitle) or curFile != preFile): 
            title = "## " + str(chapNo+1) + ". "\
                    + row.file + "\n" # Set Class or file name
    return title


### Set figure size(rate) for document ###
def figRatio(path):
    img = Image.open(path)
    rate = int(img.width/(A4_SIZE["width"]*FIX_RESOLUTION) * 100)
    if rate > MAX_FIG_RATE: rate = MAX_FIG_RATE
    return rate


### Check file exist and open mode ###
def chkOpeMode(path, mode):
    isFile = os.path.isfile(path)
    if not(isFile):
        if mode != "w": mode = "w"
        else          : pass
    return mode
    

### write file ###
def writeMdTxt(txt, outDir, mdName, opMode):
    ## Write *.md file
    outPath = os.path.join(outDir, mdName)
    opMode = chkOpeMode(outPath, opMode) # Check file exist and open mode    
    f = open(outPath, mode=opMode, encoding="UTF-8")
    f.write(txt)
    f.close()


### Make Called by graph Mark-down txt ###
def writeCallByMdTxt(table, outDir, mdName, opMode="w"):
    chapNo = 0
    SecCnt = 0
    txt ="" # The body text (for output)
    title= preTitle = "" #The body titel and previous chapter title

    for row in table.itertuples():
        if (row.cls != "macro" and row.fig):
            ## Initalize new page flag
            newpageFlg = False

            ## Set chapter title and initial No.
            title = chapTitleStr(row, chapNo, preTitle)
            if title:
                txt += title
                preTitle = title
                chapNo += 1
                secNo = 1

            ## Set figure relative path
            figPath = os.path.join(outDir, row.fig)
            rate = figRatio(figPath)
            relatPath = figPath.replace(outDir, "").replace(os.path.sep, './')

            ## Make output markdown txt
            secNoStr = str(chapNo) + "."+ str(secNo) + ". "
            txt +=  "### " + secNoStr + row.func + "\n"
            txt +=  "#### " + "解析結果 (Analysis result)" + "\n"
            txt +=  "<img src=\""+ relatPath +"\" width=\""+ str(rate)\
                        +"%\" title=\"Called by"+ row.func +"\"> \n\n"
            txt +=  "#### " + "確認内容 (Confirmation details)" + "\n"
            txt +=  "ここに確認内容を記入してください。(Please write your confirmation details.) \n\n"

            if SecCnt >= NEW_PAGE_SEC_NUM:
                txt += "<div style=\"page-break-before:always\"></div>\n\n"
                newpageFlg = True
                SecCnt = 0

            ## Update each counter
            secNo += 1
            SecCnt += 1

    if not(newpageFlg):
        txt += "<div style=\"page-break-before:always\"></div>\n\n"
    writeMdTxt(txt, outDir, mdName, opMode)


### Make Called by graph Mark-down txt ###
def writeMacroyMdTxt(table, outDir, mdName, opMode="a"):
    ## section title and table head
    txt = "## 変更マクロ一覧 \n"
    txt += "|" + "|".join(table) + "|\n"

    ## table setting
    txt += "|"
    for i in table: txt += "---|" 
    txt += "\n"

    ## Macro information
    for row in table.itertuples(name=None):
        txt += "|"
        txt += "|".join(row[1:])
        txt += "|\n"
    writeMdTxt(txt, outDir, mdName, opMode)