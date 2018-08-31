本project 包含以下内容:

wehub 回调接口开发文档: 见 wehub-api-doc.md  
faq:在与第三方企业在对接过程中遇到的相关的问题的记录(整理中)     
		
WeHub对接企业交流qq群: 830137009         

官方网站: https://www.wxb.com/wetool   
对接的demo(php版) : https://gitee.com/chinalu/codes/hxreqplwf0ydi4gjokz7292   
对接的demo(python版): https://github.com/fangqing/wehub_callback_server
版本更新记录:

当前最新版wehub

http://wxbs.oss-cn-hangzhou.aliyuncs.com/wetool/WeHub_release_20180831.zip

```
2018.8.31
http://wxbs.oss-cn-hangzhou.aliyuncs.com/wetool/WeHub_release_20180831.zip
1.新增文件上传功能:在wehub上可以配置上传的文件类型,目前只支持上传图片)
  需要第三方开发一个文件上传的接口并在wehub上进行设置,wehub_callback_server项目中有文件上传的示范代码.  图片消息增加file_index 字段,该字段用来标识图片文件的索引值
2.groupinfo 结构增加member_wxid_list字段(这会导致report_contact 的包比较大)
3.群成员发生变化时增量上报 (action为report_room_member_change)
4.wehub和回调接口之间的http连接可设置http代理,方便调试
	在本机上开发和部署回调接口服务的开发者,需下载最新版wehub,打开设置界面,切换到"其他设置",  
	设置http代理为127.0.0.1:8888(保持和fiddler默认的代理设置一致),然后就可以在fiddler中查看wehub  发送的http request
```
```
2018.8.22
pull task的定时轮询时间可在wehub上设置;上报链接消息;修正wehub 多实例运行中的bug
http://wxbs.oss-cn-hangzhou.aliyuncs.com/wetool/WeHub_release_20180823.zip
```


