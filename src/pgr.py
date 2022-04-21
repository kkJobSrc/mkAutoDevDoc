# -*- coding: utf-8 -*-
from . import lib
import os
import pandas as pd
import numpy as np

class PGR():
	def __init__(self, csvList, ouputDir):
		self.csvList = csvList
		self.OutDir = ouputDir
		self.resFileName = "extract_prg_result.csv"


	### Reference PGR results ###
	def check_pg_relief_results(self, diffInfo):
		allPrgRes = dict() # dict for target PRG results
		
		for info in diffInfo:			
			for name in self.csvList:
				csvName = os.path.splitext(os.path.basename(name))[0]
				csvUsName = csvName.split("_")[-1]

				if  csvUsName in info[0]:
					df = pd.read_csv(name, encoding="SHIFT-JIS")
					resTable = df.values.tolist()

					## Extract change row from PGR result csv
					tarResList = [[os.path.basename(res[0])] + (res[1:]) for res in resTable if res[1] in info[1]]
					allPrgRes[info[0]] = tarResList	
		return allPrgRes


	def output_result(self, prgRes):
		header = ['番号','解析ファイル','行番号','Grp','指摘ID','指摘メッセージ','修正内容／修正不要の理由','最終指摘（○：あり）']
		outTable = []

		for key in prgRes:
			outTable.append(header)
			if 0 == len(prgRes[key]):# No exit code point out
				rows = [""] * len(header)
				rows[0] = 1
				rows[1] = key
				rows[5] = "指摘なし"
				outTable.append(rows)

			else: #Exist code point out
				rows = [[i+1] + r for i, r in enumerate(prgRes[key])]
				outTable.extend(rows)
		lib.common.outList2Csv(outTable, self.OutDir, self.resFileName)


	def mainProc(self, gitApi):
		try:
			print("== Star PGR result analysis ==")
			diffInfoList = gitApi.getChgFileRows()# [ [file name, [chg. row List], ...]
			pgrRes = self.check_pg_relief_results(diffInfoList)
			self.output_result(pgrRes)

		except:
			print("** Error occured  PGR result analysis **")
		
		finally:
			print("== End PGR result analysis ==")

