#coding=utf-8
#
"""
作者版权所有:www.unionnets.com
作者邮箱:110410524@qq.com
@2019-03-13

#--windows------------------------------
E:
CD E:\\WorkStation\\_GPROJECT\\codedoc_unionnets_com\\python0\\

#python目录 make1.py 配置文件名
C:\Python34\python make1.py conf1







#--linux------------------------------
cd /data/python/codedoc/

#python目录 make1.py 配置文件名
/usr/Python_3_4_1/python make1.py conf1




"""




import os,sys,json,datetime,subprocess,smtplib,urllib,re,threading,time,pymysql,urllib.parse
from urllib.request import urlopen
from urllib.parse import urlencode

from email.mime.text import MIMEText
from email.header import Header
sys.path.append(".")

from Inc.Common.File.netsError import netsError
from Inc.Common.File.netsFile import netsFile
from Inc.netsFunc.Func.netsCode import netsCode


###################读取并赋值数据配置
tmpSTR_charset="utf-8"
tmpSTR_fixdir="\\run\\codedoc"
tmpCOUNT_charreplace=15 #脏字任重复替换次数
tmpJSON_save={}

tmpCONF_fileroot="E:\\WorkStation\\_GPROJECT\\codedoc_unionnets_com\\python0\\run\\codedoc\\testfile"
tmpCONF_language="php"
tmpCONF_format="json"
tmpCONF_urlroot="http://127.0.0.1:8072/"
tmpCONF_urlextend="&uname=core@unionnets.com&upxd=123123"
#{d}{dt}
tmpCONF_output="D:\\_Down\\output_doc\\"

tmpCONFAR_fileroot=tmpCONF_fileroot.split(netsCode.sysSPLIT1)
tmpCONFAR_language=tmpCONF_language.split(netsCode.sysSPLIT1)




tmpAR_Filepath=[
	"/log/t_{0}.log",

	]





###################从配置文件读取配置
if len(sys.argv)>=2 :
	tmpSTR_config=sys.argv[1]
	tmpFilepath_config=os.path.split(os.path.realpath(__file__))[0]+"/"+tmpSTR_config+".json"
	tmpCONTENT_config=netsFile.readFile(tmpFilepath_config)
	tmpJSON_config=json.loads(tmpCONTENT_config)
	
	tmpCONFAR_fileroot=tmpJSON_config["loadpaths"]
	tmpCONFAR_language=tmpJSON_config["language"]
	tmpCONF_urlroot=tmpJSON_config["urlroot"]
	tmpCONF_urlextend=tmpJSON_config["urlextend"]
	tmpCONF_output=tmpJSON_config["output"]








###################开发配置日志文件
tmpSTR_now=datetime.datetime.now().strftime('%Y%m%d')
tmpSTR_now_min=datetime.datetime.now().strftime('%Y%m%d%H%M')
tmpSTR_now_sec_int=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
tmpSTR_now_sec=datetime.datetime.now().strftime('datetime:%Y-%m-%d_%H:%M:%S')

tmpFilepath=os.path.split(os.path.realpath(__file__))[0]+tmpAR_Filepath[0].replace("{0}",tmpSTR_now)

tmpOBJ_file=netsFile.openFile(tmpFilepath)
print("###################################################################\r\n")
netsFile.appendFile(tmpOBJ_file,"\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n/* -- ------ #Info# ------ -- ............................................... */ - "+tmpSTR_now_sec+"\r\n");

tmpTIME_start=time.time()






###################遍历目录，取得所有文件地址
tmpAR_dir=tmpCONFAR_fileroot
tmpAR_file=[]
tmpDIR=os.listdir(tmpCONF_fileroot)
for Row_dir in tmpDIR :
	if os.path.isdir(tmpCONF_fileroot+"\\"+Row_dir) :
		tmpAR_dir.append(tmpCONF_fileroot+"\\"+Row_dir)

Coun0=0
while len(tmpAR_dir)>Coun0 :
	tmpDIR=os.listdir(tmpAR_dir[Coun0])
	for Row_now in tmpDIR :
		tmpSTR=tmpAR_dir[Coun0]+"\\"+Row_now
		if os.path.isdir(tmpSTR) :
			tmpAR_dir.append(tmpSTR)
		if os.path.isfile(tmpSTR) :
			tmpAR_ext=tmpSTR.split(".")
			if len(tmpAR_ext)>=2 :
				for Row_ext in tmpCONFAR_language :
					if tmpAR_ext[len(tmpAR_ext)-1]==Row_ext :
						tmpAR_file.append(tmpSTR)
	Coun0+=1;








#REPORT
print("共扫描"+str(len(tmpAR_dir))+"个目录，共有"+str(len(tmpAR_file))+"个文件")




###################解析文件并导出到JSON
#设置导出文件的名称，并打开文件流
tmpCONF_save=tmpCONF_output
tmpCONF_save=tmpCONF_save.replace("{d}",tmpSTR_now)
tmpCONF_save=tmpCONF_save.replace("{dt}",tmpSTR_now_sec_int)

tmpSAVE_indexcontent=""

for Row_file in tmpAR_file :
	#初始化最终保存变量
	tmpJSON_save={"Info":{},"Function":{},"Interface":{}}
	#生成单一文件名
	tmpAR0=Row_file.split("\\")
	tmpAR0.pop(len(tmpAR0)-1)
	tmpSTR_filepath="\\".join(tmpAR0)

	tmpSTR_filename=Row_file.replace(tmpCONF_fileroot,"")
	tmpAR0=tmpSTR_filename.split(".")
	tmpSTR_filenamesingle=tmpAR0[0]
	tmpSTR_filenamesingle=tmpSTR_filenamesingle.replace("\\","")
	tmpSTR_filenamesingle=tmpSTR_filenamesingle.replace("/","")
	tmpSTR_filename=tmpSTR_filename.replace("."+tmpAR0[len(tmpAR0)-1],"")
	tmpSTR_filename=tmpSTR_filename.replace("\\","_")
	tmpSTR_filename=tmpSTR_filename.replace(".","_")
	tmpSTR_filename=tmpSTR_filename.replace("/","_")
	if tmpSTR_filename[0:1]=="_" :
		tmpSTR_filename=tmpSTR_filename[1:len(tmpSTR_filename)]
	tmpSTR_extendname=tmpAR0[len(tmpAR0)-1]

	tmpAR_filepath=Row_file.split("\\")
	tmpSTR_name=tmpAR_filepath[len(tmpAR_filepath)-1]
	
	tmpSTR_classname=""
	
	#根据文件类型设置方法最后字符串
	tmpSTR_funclast="{"
	tmpSTR_funcre1="function \w*"
	tmpSTR_funcre2="function \w*"
	if tmpSTR_extendname=="php" or tmpSTR_extendname=="java" :
		tmpSTR_funclast="{"
	if tmpSTR_extendname=="java" :
		tmpSTR_funcre1="\w* \w*"
		tmpSTR_funcre2="\w* \w* \w*"
	
	
	
	#读出文件
	tmpCONTENT_2=tmpCONTENT=netsFile.readFile(Row_file)
	#文件内容预处理

	#取得所有注释块
	tmpAR_comment=re.findall("/\*{1,2}[\s\S]*?\*/",tmpCONTENT_2)
	#取得所有注释块下的类名或方法名，并拼接成最终字符段
	Coun_comment=0
	while len(tmpAR_comment)>Coun_comment :
		tmpAR0=tmpCONTENT_2.split(tmpAR_comment[Coun_comment])
		if len(tmpAR0)>=2 :
			tmpAR1=tmpAR0[1].split("/*")
			tmpAR1=tmpAR1[0].split(tmpSTR_funclast)
			if len(tmpAR1)>=2 :
				tmpAR_comment[Coun_comment]+=tmpAR1[0]
		Coun_comment+=1
	
	for Row_comment in tmpAR_comment :
		tmpSTR_comment=Row_comment
		Coun_filter=0
		while Coun_filter<tmpCOUNT_charreplace :
			tmpSTR_comment=tmpSTR_comment.replace(" 	"," ")#SPACE+TAB
			Coun_filter+=1
		Coun_filter=0
		while Coun_filter<tmpCOUNT_charreplace :
			tmpSTR_comment=tmpSTR_comment.replace("	 "," ")#TAB+SPACE
			Coun_filter+=1
		Coun_filter=0
		while Coun_filter<tmpCOUNT_charreplace :
			tmpSTR_comment=tmpSTR_comment.replace("		"," ")#TAB+TAB
			Coun_filter+=1
		Coun_filter=0
		while Coun_filter<tmpCOUNT_charreplace :
			tmpSTR_comment=tmpSTR_comment.replace("	"," ")#TAB
			Coun_filter+=1
		Coun_filter=0
		while Coun_filter<tmpCOUNT_charreplace :
			tmpSTR_comment=tmpSTR_comment.replace("  "," ")#SPACE+SPACE
			Coun_filter+=1
		
		#class name
		tmpAR_class=re.findall("class \w* ",tmpSTR_comment)
		for Row_class in tmpAR_class :
			if len(Row_class)>0 :
				tmpAR0=Row_class.split(" ")
				if len(tmpAR0)>=2 :
					tmpSTR_classname=tmpAR0[1]

		#function name
		tmpSTR_function="???"
		tmpAR0=tmpSTR_comment.split("*/")
		if len(tmpAR0)>=2 :
			tmpAR_function=re.findall(tmpSTR_funcre1,tmpAR0[len(tmpAR0)-1])
			for Row_function in tmpAR_function :
				if len(Row_function)>0 :
					tmpAR0=Row_function.split(" ")
					if len(tmpAR0)>=2 :
						tmpSTR_function=tmpAR0[len(tmpAR0)-1]
		if tmpSTR_function.lower()=="String" or tmpSTR_function.lower()=="int" or tmpSTR_function.lower()=="void" :
			if len(tmpAR0)>=2 :
				tmpAR_function=re.findall(tmpSTR_funcre2,tmpAR0[len(tmpAR0)-1])
				for Row_function in tmpAR_function :
					if len(Row_function)>0 :
						tmpAR0=Row_function.split(" ")
						if len(tmpAR0)>=2 :
							tmpSTR_function=tmpAR0[len(tmpAR0)-1]

		#取得所有注释块
		tmpJSON_section={}
		if len(tmpSTR_comment)>0 :
			try:
				tmpAR0=tmpSTR_comment.split("/*")
				if len(tmpAR0)>=2 :
					tmpAR0=tmpAR0[1].split("*/")
				tmpJSON_section=json.loads(tmpAR0[0])
			except:
				tmpJSON_section={}

		if ("@Info" in tmpJSON_section) :
			tmpJSON_save["Info"]=tmpJSON_section["@Info"]
			
		if ("@Interface" in tmpJSON_section) :
			tmpJSON_save["Interface"][len(tmpJSON_save["Interface"])]=tmpJSON_section["@Interface"]
		
		if ("@Function" in tmpJSON_section) :
			tmpJSON_save["Function"][len(tmpJSON_save["Function"])]=tmpJSON_section["@Function"]

		#REPLACE
		tmpAR_col=[
			"title", #标题
			"grouppath", #分类文件路径
			"path", #文件路径
			"urlroot", #项目测试域名（前段）
			"urlextend", #项目测试附加字符（后段）
			"uidescpath", #界面描述表保存路径
			"savepath", #生成的文件保存路径
			"description", #文字描述
			"author_update", #作者与更新时间
			"version" #版本
			]
		Coun_col=0
		while len(tmpAR_col)>Coun_col :
			if (tmpAR_col[Coun_col] in tmpJSON_save["Info"]) :
				tmpSTR=tmpJSON_save["Info"][tmpAR_col[Coun_col]]
				
				Coun_filepath=2
				while Coun_filepath<9 :
					if len(tmpAR_filepath)>=Coun_filepath :
						tmpINT=Coun_filepath-2
						tmpSTR=tmpSTR.replace("{d"+str(tmpINT)+"}",tmpAR_filepath[len(tmpAR_filepath)-Coun_filepath])
					Coun_filepath+=1
				tmpSTR=tmpSTR.replace("{class}",tmpSTR_classname)
				tmpSTR=tmpSTR.replace("{filename}",tmpSTR_name)
				tmpSTR=tmpSTR.replace("{filenamesingle}",tmpSTR_filenamesingle)
				tmpSTR=tmpSTR.replace("{fileextend}",tmpSTR_extendname)
				
				tmpJSON_save["Info"][tmpAR_col[Coun_col]]=tmpSTR
			
			elif tmpAR_col[Coun_col]=="urlroot" :
				tmpJSON_save["Info"][tmpAR_col[Coun_col]]=tmpCONF_urlroot
			elif tmpAR_col[Coun_col]=="urlextend" :
				tmpJSON_save["Info"][tmpAR_col[Coun_col]]=tmpCONF_urlextend
				
			elif tmpAR_col[Coun_col]=="title" or tmpAR_col[Coun_col]=="grouppath" or tmpAR_col[Coun_col]=="uidescpath" or tmpAR_col[Coun_col]=="description" or tmpAR_col[Coun_col]=="version" :
				tmpJSON_save["Info"][tmpAR_col[Coun_col]]=""
				
			Coun_col+=1



		tmpAR_col=[
			"title", #标题
			"method", #传入方法GET或POST
			"function", #方法名称（类方法）
			"type", #接口类型REST或RPC
			"description", #描述
			"author_update", #作者与更新时间
			"path", #路径
			"urlroot", #项目测试域名（前段）
			"urlextend", #项目测试附加字符（后段）
			"uidescpath", #界面描述表保存路径
			"version", #版本
			"parameterfilepath" #读取参数配置文件路径，生成参数
			]
			#Parameter #参数
		Coun_row=0
		while len(tmpJSON_save["Interface"])>Coun_row :
			Coun_col=0
			while len(tmpAR_col)>Coun_col :
				###
				if (tmpAR_col[Coun_col] in tmpJSON_save["Interface"][Coun_row]) :
					tmpSTR=tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]
					
					Coun_filepath=2
					while Coun_filepath<9 :
						if len(tmpAR_filepath)>=Coun_filepath :
							tmpINT=Coun_filepath-2
							tmpSTR=tmpSTR.replace("{d"+str(tmpINT)+"}",tmpAR_filepath[len(tmpAR_filepath)-Coun_filepath])
						Coun_filepath+=1
					tmpSTR=tmpSTR.replace("{class}",tmpSTR_classname)
					tmpSTR=tmpSTR.replace("{function}",tmpSTR_function)
					tmpSTR=tmpSTR.replace("{filename}",tmpSTR_name)
					tmpSTR=tmpSTR.replace("{filenamesingle}",tmpSTR_filenamesingle)
					tmpSTR=tmpSTR.replace("{fileextend}",tmpSTR_extendname)
					
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpSTR

				elif tmpAR_col[Coun_col]=="type" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]="REST"
				elif tmpAR_col[Coun_col]=="method" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]="GET"
				elif tmpAR_col[Coun_col]=="function" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpSTR_function
				elif tmpAR_col[Coun_col]=="uidescpath" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpJSON_save["Info"][tmpAR_col[Coun_col]]
				elif tmpAR_col[Coun_col]=="author_update" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpJSON_save["Info"][tmpAR_col[Coun_col]]
				elif tmpAR_col[Coun_col]=="urlroot" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpCONF_urlroot
				elif tmpAR_col[Coun_col]=="urlextend" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpCONF_urlextend

				elif tmpAR_col[Coun_col]=="title" or tmpAR_col[Coun_col]=="description" or tmpAR_col[Coun_col]=="version" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=""

				Coun_col+=1

			#Parameter
			if not ("Parameter" in tmpJSON_save["Interface"][Coun_row]) :
				tmpJSON_save["Interface"][Coun_row]["Parameter"]=[]

			Coun_row+=1

		tmpAR_col=[
			"title", #标题
			"function", #方法名称（类方法）
			"description", #描述
			"author_update", #作者与更新时间
			"path", #路径
			"version", #版本
			]
			#Parameter #参数
		Coun_row=0
		while len(tmpJSON_save["Function"])>Coun_row :
			Coun_col=0
			while len(tmpAR_col)>Coun_col :
				if (tmpAR_col[Coun_col] in tmpJSON_save["Function"][Coun_row]) :
					tmpSTR=tmpJSON_save["Function"][Coun_row][tmpAR_col[Coun_col]]
					
					Coun_filepath=2
					while Coun_filepath<9 :
						if len(tmpAR_filepath)>=Coun_filepath :
							tmpINT=Coun_filepath-2
							tmpSTR=tmpSTR.replace("{d"+str(tmpINT)+"}",tmpAR_filepath[len(tmpAR_filepath)-Coun_filepath])
						Coun_filepath+=1
					tmpSTR=tmpSTR.replace("{class}",tmpSTR_classname)
					tmpSTR=tmpSTR.replace("{function}",tmpSTR_function)
					tmpSTR=tmpSTR.replace("{filename}",tmpSTR_name)
					tmpSTR=tmpSTR.replace("{filenamesingle}",tmpSTR_filenamesingle)
					tmpSTR=tmpSTR.replace("{fileextend}",tmpSTR_extendname)
					
					tmpJSON_save["Function"][Coun_row][tmpAR_col[Coun_col]]=tmpSTR

				elif tmpAR_col[Coun_col]=="function" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpSTR_function
				elif tmpAR_col[Coun_col]=="author_update" :
					tmpJSON_save["Interface"][Coun_row][tmpAR_col[Coun_col]]=tmpJSON_save["Info"][tmpAR_col[Coun_col]]

				elif tmpAR_col[Coun_col]=="title" :
					tmpJSON_save["Function"][Coun_row][tmpAR_col[Coun_col]]=""
				elif tmpAR_col[Coun_col]=="description" :
					tmpJSON_save["Function"][Coun_row][tmpAR_col[Coun_col]]=""
				elif tmpAR_col[Coun_col]=="version" :
					tmpJSON_save["Function"][Coun_row][tmpAR_col[Coun_col]]=""
				
				Coun_col+=1

			Coun_row+=1











	tmpSTR=json.dumps(tmpJSON_save)
	tmpSTR=tmpSTR
	tmpSTR_savefile=tmpCONF_save+tmpJSON_save["Info"]["savepath"]+tmpSTR_filename+".json"
	netsFile.writeFile(tmpSTR_savefile,tmpSTR);












	###################开始生成测试文件

	#读出index.htm
	tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\template.htm"
	tmpCONTENT_template=tmpCONTENT=netsFile.readFile(tmpFilename)

	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.title}",tmpJSON_save["Info"]["title"])
	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.description}",tmpJSON_save["Info"]["description"])
	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.version}",tmpJSON_save["Info"]["version"])
	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.author_update}",tmpJSON_save["Info"]["author_update"])
	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.urlroot}",tmpJSON_save["Info"]["urlroot"])
	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Info.urlextend}",tmpJSON_save["Info"]["urlextend"])

	#写Inteface
	tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\template_list.htm"
	tmpTEMP_Link=netsFile.readFile(tmpFilename)
	tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\template_content.htm"
	tmpTEMP_Content=netsFile.readFile(tmpFilename)
	tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\template_contentparameter.htm"
	tmpTEMP_Parameter=netsFile.readFile(tmpFilename)
	
	tmpSTR_List=""
	tmpSTR_Content=""
	Coun_inter=0
	while len(tmpJSON_save["Interface"])>Coun_inter :
		Row_inter=tmpJSON_save["Interface"][Coun_inter]
		
		tmpSTR=tmpTEMP_Link
		tmpSTR=tmpSTR.replace("{title}",Row_inter["title"])
		tmpSTR_Content=tmpSTR_Content+tmpSTR

		tmpSTRCONTENT=tmpTEMP_Content
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{title}",Row_inter["title"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{method}",Row_inter["method"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{function}",Row_inter["function"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{type}",Row_inter["type"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{description}",Row_inter["description"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{author_update}",Row_inter["author_update"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{version}",Row_inter["version"])
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{path}",Row_inter["path"])
		
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{Info.path}",tmpJSON_save["Info"]["path"])
		
		#Parameter
		tmpSTR_Parameter=""
		tmpSTRPARA=""
		Coun_para=0
		while len(tmpJSON_save["Interface"][Coun_inter]["Parameter"])>Coun_para :
			Row_para=tmpJSON_save["Interface"][Coun_inter]["Parameter"][Coun_para]
			tmpSTRPARA=tmpTEMP_Parameter
			
			tmpSTRPARA=tmpSTRPARA.replace("{title}",Row_para["title"])
			tmpSTRPARA=tmpSTRPARA.replace("{name}",Row_para["name"])
			tmpSTRPARA=tmpSTRPARA.replace("{dbtype}",Row_para["dbtype"])
			tmpSTRPARA=tmpSTRPARA.replace("{testvalue}",Row_para["testvalue"])
			
			tmpSTR_Parameter+=tmpSTRPARA
			Coun_para+=1
		
		tmpSTRCONTENT=tmpSTRCONTENT.replace("{Parameter}",tmpSTR_Parameter)
		
		tmpSTR_Content=tmpSTR_Content+tmpSTRCONTENT
		Coun_inter+=1

	tmpCONTENT_template=tmpCONTENT_template.replace("{Nets.Content}",tmpSTR_List+tmpSTR_Content)
	
	tmpAR0=tmpJSON_save["Info"]["savepath"].split("\\")
	tmpSTR_back=""
	Coun0=0
	while (len(tmpAR0))>Coun0 :
		tmpSTR_back+="..\\"
		Coun0+=1
	
	tmpCONTENT_template=tmpCONTENT_template.replace("{back}",tmpSTR_back)
	
	
	
	
	tmpSTR_savefile=tmpCONF_save+tmpJSON_save["Info"]["savepath"]+tmpSTR_filename+".htm"
	netsFile.writeFile(tmpSTR_savefile,tmpCONTENT_template);
	
	tmpSAVE_indexcontent=tmpSAVE_indexcontent+"<a href="+tmpJSON_save["Info"]["savepath"]+tmpSTR_filename+".htm>"+tmpJSON_save["Info"]["title"]+".htm"+"</a>"







###保存INDEX.HTM文件
tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\index.htm"
tmpCONTENT_template=tmpCONTENT=netsFile.readFile(tmpFilename)
tmpSTR=tmpCONTENT_template.replace("{Nets.Content}",tmpSAVE_indexcontent)

tmpSTR_savefile=tmpCONF_save+"index.htm"
netsFile.writeFile(tmpSTR_savefile,tmpSTR);

###保存CSS文件
tmpFilename=os.path.split(os.path.realpath(__file__))[0]+tmpSTR_fixdir+"\\template\\Common.css"
tmpSTR_savefile=tmpCONF_save+"Common.css"
netsFile.writeFile(tmpSTR_savefile,tmpSTR);




###################结束处理
tmpTIME_now=time.time()
print("\r\n............总用时(total):"+str(tmpTIME_now-tmpTIME_start))

netsFile.closeFile(tmpOBJ_file)















