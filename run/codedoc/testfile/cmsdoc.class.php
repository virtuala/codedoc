<?php

/*
	{
"@Info":{
  	"title":"新闻文档接口:cmsdoc:{filename}",
  	"grouppath":"cmsdoc",
  	"version":"{class}.1.2",
  	"description":"introduct",
  	"author_update":"2019-03-09",
  	"uidescpath":"..\\uidesc\\1.conf",
  	"path":"{d2}/{d1}/{d0}/{filenamesingle}.{fileextend}",
  	"path":"Interface/Common/Cms/{filenamesingle}.{fileextend}",
  	"savepath":"{d0}/"
  	}
  	}
 */
class PaDefault extends CustomPage {
	/*{"@Interface":{"title":"add","path":"?ActionType=NoneJson&ActionTypeF=DAdd","method":"POST"}}*/
	public function PaDefault(){
		$this->CustomPage();
	}

      /*
      {
      "@Interface":{
      		"title":"列表/{class}.{function}",
      		"description":"取得列表数据",
      		"author_update":"110410524@qq.com-2019-03-10",
      		"path":"?ActionType=List&",
      		"type":"REST",
      		"method":"GET",
      		"function":"{function}",
      		"version":"1",
      		"parameterfilepath":"",
      		"Parameter":[
      		{"name":"Name","method":"GET","title":"名称","dbtype":"string","default":"","testvalue":"","ismust":"1"},
      		{"name":"Parid","method":"GET","title":"分类","dbtype":"int","default":"","testvalue":"","ismust":"1"}
      		],
      		"Return":[
      		{"title":"名称","dbtype":"json","description":""}
      		]
      },
      "@Function":{
      }
}
     */
	public function OnList(){

		$this->Message_Fix("SUCCESS","成功取得数据(getdata)","");
		return 0;
	}
      /*
      {
      "@Interface":{
      		"title":"详细内容/{class}.{function}",
      		"description":"取得详细数据",
      		"path":"?ActionType=Normal&",
      		"Parameter":[
      		{"name":"Normal","method":"GET","title":"ID值","dbtype":"int","default":"","testvalue":"1,","ismust":"1"}
      		],
      		"Return":[
      		{"title":"名称","dbtype":"json","description":""}
      		]
      },
      "@Function":{
      }
}
     */
	public function OnNormal(){

		$this->Message_Fix("SUCCESS","成功取得数据","");
		return 0;
	}







}
?>