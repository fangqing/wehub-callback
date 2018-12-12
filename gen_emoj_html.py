# -*- coding: utf-8 -*-
import codecs
import os
import sys
import re

def gen_emoj_html():
	fsave = open("emoji_index.html",'w',encoding='gbk')

	with open("emo_config.txt","r",encoding='utf-8') as f:
		lines = f.readlines()

		fsave.writelines(r'''<html><meta http-equiv="Content-Type" content="text/html; charset=gb2312">''')
		fsave.writelines(r'''<style>
	        table { width: 200px; min-height: 25px; line-height: 25px; text-align: center; border-color:#b6ff00; border-collapse: collapse;}   
	    </style>''')
		fsave.writelines(r'''<body><h2>微信文本消息静态表情转义对照表</h2>''')
		fsave.writelines(r'''<div><table border="1"><tr><th width="100">编号</th><th width="100">转义值</th><th width="100">描述</th><th width="200">实际效果</th></tr>''')
		index = 0
		for line in lines:
			index = index+1
			nfirst = line.find('(\"')
			nfirst_1 = line.find('\")')

			name = line[nfirst+2:nfirst_1]
			print (name)
			nsecond = line.find('(\"',nfirst_1)
			nsecond_2 = line.find('\")',nsecond)
			tip = line[nsecond+2:nsecond_2]
			print(tip)

			emj_png = "<img src=\"./Emoji/%03d.png\"</>"%(index)
			print (emj_png)
			fsave.writelines(str("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>").format(index,name,tip,emj_png))

		fsave.writelines("</table></div></body></html>")


if __name__ =='__main__':
	gen_emoj_html()