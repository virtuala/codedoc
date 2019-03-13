#coding=utf-8

from Inc.Common.File.netsFile import netsFile

class netsError(netsFile):
	
	def getError_0(pMessage,pSMessage,pCause,pTrace,pType):
		print(pMessage)

	def wl(pOBJ,pMessage):
		tmpSTR=""+pMessage+"\r\n"
		pOBJ.write(tmpSTR)

	def wlv2(pOBJ,pMessage):
		tmpSTR="/* -- ------ #Info# ------ -- */\r\n"+pMessage+"\r\n\r\n\r\n"
		pOBJ.write(tmpSTR)

	def wlnote(pOBJ,pMessage):
		tmpSTR="/* -- #Comment.Note# -- */\r\n"+pMessage+"\r\n\r\n\r\n"
		pOBJ.write(tmpSTR)





