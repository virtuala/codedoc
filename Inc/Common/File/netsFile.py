#coding=utf-8

import os,urllib
from urllib.request import urlopen
from urllib.parse import urlencode

class netsFile():
	
	sysSPLIT1=","
	
	#def __init__(self):
	#	self.data=""
	
	#Р§зг
	#tmpData={}
	#tmpData['a']=tmpSTR_title
	#tmpHTML=netsFile.readURL2(tmpAR_URL_poriginal[0],tmpData,"")
	#tmpSTR_title=tmpHTML.decode("utf-8").split("<html>")[0];
	def createDir(pPath):
		pPath=pPath.strip()
		pPath=pPath.rstrip("\\")
		if not os.path.exists(pPath) :
			os.makedirs(pPath)

		return True

	def createDir_ByFilepath(pFilepath):
		pFilepath=pFilepath.replace("\\","/")
		tmpAR0=pFilepath.split("/")
		tmpSTR=""
		Coun0=0
		while (len(tmpAR0)-1)>Coun0 :
			tmpSTR=tmpSTR+tmpAR0[Coun0]+"/"
			Coun0+=1
		tmpSTR=tmpSTR.strip()
		tmpSTR=tmpSTR.rstrip("\\")
		if not os.path.exists(tmpSTR):
			os.makedirs(tmpSTR)

		return True

	def readURL2(pURL,pPOST,pCOOKIE):
		tmpSTR_HTML=""
		try :
			tmpResponse=urlopen(pURL,urlencode(pPOST).encode('utf-8'))
			tmpSTR_HTML=tmpResponse.read()
		except EOFError:
			tmpSTR_HTML="urlopen/error"
			tmpSTR_HTML=EOFError
		return tmpSTR_HTML

	def readURL(pURL):
		tmpSTR_HTML=""
		try :
			tmpResponse=urlopen(pURL)
			tmpSTR_HTML=tmpResponse.read()
		except EOFError:
			tmpSTR_HTML=EOFError
		return tmpSTR_HTML
	
	def readURL_Collection(pURL):
		tmpSTR_HTML=""
		try :
			tmpREQ=urllib.request.Request(pURL)
			tmpREQ.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
			tmpResponse=urllib.request.urlopen(tmpREQ)
			tmpSTR_HTML=tmpResponse.read()
		except EOFError:
			tmpSTR_HTML=EOFError
		
		return tmpSTR_HTML
	
	def readFile(pFilepath):
		all_the_text=""
		file_object=open(pFilepath,encoding="utf-8")
		try:
			all_the_text=file_object.read()
		finally:
			file_object.close()
		return all_the_text
	
	def readFile_HasCharset(pFilepath,pCharset):
		all_the_text=""
		file_object=open(pFilepath,encoding=pCharset)
		try:
			all_the_text=file_object.read()
		finally:
			file_object.close()
		return all_the_text
	
	def writeFile(pFilepath,pContent):
		__class__.createDir_ByFilepath(pFilepath)
		
		file_object=open(pFilepath,'w',encoding="utf-8")
		file_object.write(pContent)
		file_object.close()
		return 0

	def appendFile(pFilepath,pContent):
		__class__.createDir_ByFilepath(pFilepath)
		
		file_object=open(pFilepath,'a')
		file_object.write(pContent)
		file_object.close()
		return 0
		
	def downloadFile(pURL,pFilepath):
		tmpResponse=urlopen(pURL)
		tmpIMG=tmpResponse.read()
		with open(pFilepath) as f:
			f.write(tmpIMG)
		f.close()
		return 0
		
	def getFileName(pFilename):
		tmpAR0=pFilename.split("/")
		return tmpAR0[len(tmpAR0)-1]





	def openFile(pFilepath):
		__class__.createDir_ByFilepath(pFilepath)
		
		file_object=open(pFilepath,'a')
		return file_object
	def appendFile(pOBJ,pContent):
		pOBJ.write(pContent)
		return 0
	def closeFile(pOBJ):
		pOBJ.close()
		return 0




