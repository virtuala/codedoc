#coding=utf-8

import sys,re
from urllib.request import urlopen

from Inc.Common.File.netsFile import netsFile

class netsCode(netsFile):
	
	#def __init__(self):
	#	self.data=""
	
	def getDataByString(pSTR,pSTR_Start,pSTR_End,pFlag_Mode):
		tmpSTR=""
		
		if pFlag_Mode==0 :
			tmpAR0=pSTR.split(pSTR_Start)
			if len(tmpAR0)>1 :
				tmpAR1=tmpAR0[1].split(pSTR_End)
				tmpSTR=tmpAR1[0]
		else:
			tmpAR0=pSTR.split(pSTR_End)
			if len(tmpAR0)>1 :
				tmpAR1=tmpAR0[0].split(pSTR_Start)
				tmpSTR=tmpAR1[len(tmpAR1)-1]
		
		return tmpSTR

	def getSystemVersion():
		tmpSTR="win"
		tmpSTR_0=str(sys.platform)
		if tmpSTR_0=="win32" :
			tmpSTR="win"
		elif tmpSTR_0=="linux" :
			tmpSTR="linux"
				
		return tmpSTR

	def illegal_char(pSTR,pSTR_replaceto):
		pSTR=re.compile(
			u"[^"
			u"\u4e00-\u9fa5"
			u"\u0041-\u005A"
			u"\u0061-\u007A"
			u"\u0030-\u0039"
			u"\u3002\uFF1F\uFF01\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2018\u2019\u201C\u201D\uFF08\uFF09\u3014\u3015\u3010\u3011\u2014\u2026\u2013\uFF0E\u300A\u300B\u3008\u3009"
			u"\!\@\#\$\%\^\&\*\(\)\-\=\[\]\{\}\\\|\;\'\:\"\,\.\/\<\>\?\/\*\+"
			u"]+").sub(pSTR_replaceto,pSTR)
		return pSTR
    