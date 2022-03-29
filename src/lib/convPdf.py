# 環境構築
# pip install selenium
# 下記URLよりchromeのバージョンにあったドライバーをダウンロード
# https://chromedriver.chromium.org/downloads 
# 変数 driver_path に chromedriver.exe の path を代入
#(参考:
# https://degitalization.hatenablog.jp/entry/2021/03/13/102805,
# https://salamann.com/python_selenium_html_pdf_automation,
# https://qiita.com/memakura/items/20a02161fa7e18d8a693)

# ヘッドレスモードで掃き出し参考:
# https://qiita.com/mochi_yu2/items/a845e52b8aa677f132bf

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import base64, glob, os,  PyPDF2 


TAR_EXT = ["c", "cpp", "h", "hpp", "rc", "INI", "ini"] # 解析の対象となる拡張子
PDF_CONF = {# output PDF config. 
        "printBackground": True, # pinrt backGround
        "paperWidth": 11.69, # A4
        "paperHeight": 8.27,
        # "displayHeaderFooter": True, # 印刷時のヘッダー、フッターを表示
}

### Setting output file paht. ###
def setOutputName(fileName, outDir):
    ### Make string for pdf file name
    name = os.path.basename(fileName).split(".")[0:-1]
    name = ("_").join(name) + ".pdf"
    return os.path.join(outDir, name)


### Get file extension ###
def getFileExt(name):
    return os.path.basename(name).split(".")[0].split("_")[-1]


### Convine multi PDF files ###
def joinPdfs(pdfDir, outDir):
    ### Initialized PDF informations
    merger = PyPDF2.PdfFileMerger()
    pdfs = glob.glob(os.path.join(pdfDir, "*.pdf"))
    sortPdfs = sorted( [ p for p in pdfs if getFileExt(p) in TAR_EXT[0:4] ] )
    sortPdfs.extend(sorted( [ p for p in pdfs if getFileExt(p) in TAR_EXT[5:] ] ))
    sortPdfs.extend(sorted( [ p for p in pdfs if "rc" in getFileExt(p)] ))

    for pdf in sortPdfs: merger.append(pdf)
    merger.write(os.path.join(outDir, "codeDiff.pdf"))
    merger.close()


### Setting conf. for saving as PDF ###
### Convert an opned web page or HTML file to PDF ###
def html2Pdf(html, outdir):
    ## Setting chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=options )

    ## Convert html to PDF
    driver.get("file:///" + html)
    pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", PDF_CONF)
    pdf = base64.b64decode(pdf_base64["data"])
    
    ## Setting output
    path = setOutputName(html, outdir)
    with open(path, 'bw') as f: f.write(pdf)

    ## Quit driver
    driver.close()
    driver.quit()