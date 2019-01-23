# -*- coding: utf-8 -*-
import codecs
import os
import sys
import re
from emoj_data import emj_datebase

def gen_emoj_html():
	with open("emoji_index.html","w",encoding='gbk') as fsave:
		fsave.writelines(r'''<html><meta http-equiv="Content-Type" content="text/html; charset=gb2312">''')
		fsave.writelines(r'''<style>
	        table { width: 200px; min-height: 25px; line-height: 25px; text-align: center; border-color:#b6ff00; border-collapse: collapse;}   
	    </style>''')
		fsave.writelines(r'''<body><h2>微信文本消息静态表情转义对照表</h2>''')
		fsave.writelines(r'''<div><table border="1"><tr><th width="100">编号</th><th width="100">转义值</th><th width="100">描述</th><th width="200">实际效果</th></tr>''')
		for key,value in emj_datebase.items():
			index = key
			name = value.get("value")
			print (name)
			tip = value.get("tip")
			image = value.get("image")
			emj_png = "<img src=\"./Emoji/%s\"</>"%(image)
			fsave.writelines(str("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>").format(index,name,tip,emj_png))

		fsave.writelines("</table></div></body></html>")


if __name__ =='__main__':
	gen_emoj_html()