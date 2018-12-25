## faq(持续更新中)

- faq1.如何查看wehub与 回调接口之间的数据通讯?
```
方法1:安装fiddler,该软件可以很直接的观察到wehub 的所有的http通讯
    在本机上开发和部署回调接口服务的开发者,需下载最新版wehub,打开设置界面,切换到"其他设置"-->设置http代理为127.0.0.1:8888(保持和fiddler默认的代理设置一致),
    然后就可以在fiddler中查看wehub发送的http request和接收到的respone
	
方法2:Wehub在 C:\Users\xxxxxx\AppData\Roaming\WeHub\system\log 目录下会产生log文件,   log的配置文件为C:\Users\xxxxx\AppData\Roaming\WeHub\system\cfg\log4cxx.properties,    
若要看很详细的log,请提高loglevel:
用记事本打开log配置文件,将第1行"log4j.rootLogger = DEBUG,logFile"中的"DEBUG" 修改为"TRACE",
将第6行的"log4j.appender.logFile.Threshold = DEBUG"中的"DEBUG" 修改为"TRACE",然后重启wehub.
之后log文件会详细记录wehub 发送出去的http request和回调接口返回的respone
```

log文件中记录的常见的错误列举
```
错误1:log中出现  "unknow format reply data,error = xxxxx"
原因: 回调接口收到wehub发送的http request后,返回的http respone不是json格式,wehub无法解析或解析出错

错误2:log中出现"HubLogic OnReplyError, replay error = xxx", xxx的值是下方表格中的网络错误码
原因:回调接口的服务端运行不正常(比如服务没有开启,回调接口的域名无法解析等等)

```
网络错误码|Description
:----:|--
1|the remote server refused the connection (the server is not accepting requests)
2|the remote server closed the connection prematurely, before the entire reply was received and processed
3|the remote host name was not found (invalid hostname)
4|the connection to the remote server timed out
5|the operation was canceled  before it was finished.
6|the SSL/TLS handshake failed and the encrypted channel could not be established
7|the connection was broken due to disconnection from the network, however the system has initiated roaming to another access point. The request should be resubmitted and will be processed as soon as the connection is re-established.
8|the connection was broken due to disconnection from the network or failure to start the network.
9|the background request is not currently allowed due to platform policy.
10|while following redirects, the maximum limit was reached. 
11|while following redirects, the network access  detected a redirect from a encrypted protocol (https) to an unencrypted one (http). 
99|an unknown network-related error was detected
101|the connection to the proxy server was refused (the proxy server is not accepting requests)
102|the proxy server closed the connection prematurely, before the entire reply was received and processed
103|the proxy host name was not found (invalid proxy hostname)
104|the connection to the proxy timed out or the proxy did not reply in time to the request sent
105|the proxy requires authentication in order to honour the request but did not accept any credentials offered (if any)
199|an unknown proxy-related error was detected
201|the access to the remote content was denied (similar to HTTP error 403)
202|the operation requested on the remote content is not permitted
203|the remote content was not found at the server (similar to HTTP error 404)
204|the remote server requires authentication to serve the content but the credentials provided were not accepted (if any)
205|the request needed to be sent again, but this failed for example because the upload data could not be read a second time.
206|the request could not be completed due to a conflict with the current state of the resource.
207|the requested resource is no longer available at the server.
299|an unknown error related to the remote content was detected
301|the Network Access  cannot honor the request because the protocol is not known
302|the requested operation is invalid for this protocol
399|a breakdown in protocol was detected (parsing error, invalid or unexpected responses, etc.)
401|the server encountered an unexpected condition which prevented it from fulfilling the request.
402|the server does not support the functionality required to fulfill the request.
403|the server is unable to handle the request at this time.
499|an unknown error related to the server response was detected

- faq2 wehub和回调接口的交互数据的编码方式
```
wehub 将utf-8编码的json格式的request以post方式发往回调接口(http 的ContentType 为application/json)
回调接口的respone也必须为utf-8的编码的json格式数据,否则wehub无法正确解析
```

- faq3.为什么我的代码里按照你的文档里的json格式来写,下发的任务却没有执行?
```
请先检查你的代码逻辑是否正确,书写格式是否规范,执行起来是否按照预想的流程在走.
最最最重要的一点:你的代码执行到最后返回给wehub的json格式是否和文档中的一致,
注意你的代码中出现的各种trace,你的服务器可能会把这些trace全部返回给了wehub,请打开wehub的log,
看是否有异常(参考faq1)
```

- faq4.wehub是否可以多开?
```
0.1.4之前的wehub不支持多开微信,之后的wehub已支持多开微信,请升级到最新版的微信.
多开方式:先开启一个wehub和微信并登陆;再开启第二个wehub和微信并登陆;重复以上步骤
如果这个过程中wehub没有自动开启新的微信客户端,手动点击wehub界面上的"打开微信"按钮.
```

- faq5.回调接口该如何处理上报的聊天消息?
```
wehub提供基础的微信聊天消息上报的能力,不过滤发送者的wxid(但会过滤公众号推送的内容)
因此回调接口在做自动回复的时候,需要过滤自己的微信号发的消息.否则会陷入"回调接口下发自动 
回复内容--->wehub发消息--->微信消息事件回调--->wehub上报刚才自己发的消息--->回调接口又下发聊天任务"的死循环
```
```
一旦陷入死循环,容易导致wehub高频率地发消息,这极易触发微信系统的安全提醒甚至被封号
如何过滤自己发的消息?
若使用的wehub版本<0.1.4,回调接口在收到report_new_msg时,判断msg中的wxid是否为这个wehub上登陆的wxid. 若是,则不要下发task_type=1的发消息的任务
若使用的wehub版本>=0.1.4,回调接口在收到report_new_msg时,判断msg中的wxid_from是否为这个wehub上登陆的wxid.若是,则不要下发task_type=1的发消息的任务
```

- faq6.为什么有时候wehub无法监测到微信?
```
1. 确定当前wehub 支持的微信版本号:
   方法:  打开wehub的安装目录,进入WeChatVersion 子目录,会发现有以微信版本号命名的子文件夹如2.6.xx.xx等等,
   他们分别代表着wehub所支持的微信的版本号. 若你当前正在使用的微信的版本号不在上述之列,则表示你当前使用的wehub无法支持你当前运行的微信版本,
   请下载安装最新版的WeHub.目前最新的WeHub(0.3.3)支持2.6.4.56|2.6.5.38|2.6.6.28 等3个版本的微信.
   注意:360等软件可能会把wehub当成不安全的进程,从而误删除WeChatVersion目录下的文件,
   请使用wehub时退出360进程或将wehub加入到360的信任名单.(很重要,很重要,很重要)

2. 看系统中是否有僵死的微信进程:
   方法: 打开系统的任务管理器,对所有的进程按"名称" 排序查看,查看当前有多少个微信进程(只有名称为Wechat的进程才是微信进程,其他的如WeChatweb, WeChatStore都不是微信的主进程),同时查看你的任务栏里有多少个微信的聊天或登陆窗口. 比如你的任务管理器中显示有4个"Wechat"进程而在任务栏上你只看到了3个微信的窗口,说明有一个微信进程是僵死的.
    若出现这种情况,请杀掉所有的微信进程,然后重新开启wehub登陆微信
    
3. 看系统是否安装了360等安全软件,或者其他的类似于wehub的微信辅助软件.
   360会干扰wehub的正常的行为甚至会删除wehub的某些关键dll文件,其他的微信辅软件可能会和wehub冲突.
   请彻底卸载掉这些软件(保险起见,最好重新安装wehub)
```

- faq7.为什么有时候wehub发图片很慢很慢?
```
目前已知的情况是,运行在阿里云主机上的wehub发图片很慢很慢(猜测可能微信对运行阿里云的微信客户端有某些特殊的行为处理),
更换成腾讯云的主机后一切都正常了
```

- faq8.为什么wehub 开启后,appid无法验证成功?
```
   appid验证失败后会弹出设置界面,并用红色文字标识失败的原因. 
  一般 appid验证失败有两种情况:
  1.appid 过期了需要续费, 这种情况请在微信群里资讯我们的工作人员
  2.wehub 发给回调接口的 login 请求没有正确地返回: 
  	可能你的网络问题,可能你的服务器没有正常启动(看wehub的log). 
  	若开启了安全验证,回调接口在处理logIn时可能没有正确地返回签名.
```

- faq9:我在服务端代码里打了log,登陆后为什么没有收到 report_contact?
```
report_contact每次post的数据量会比较大(好友/群越多,post的数据就越大),请将服务端能接受的post_max_size 调整成至少10M.
由于很多服务器比如ngix 默认的接收的最大量会比较小(比如1M),当report_contact的数据量超过这个上限时,服务端会无法接收这个request.
请参考这个网页:https://www.jianshu.com/p/7797b200e1f4
```

- faq 10: 关于json中的数据类型
```
  task_id字段 必须为字符串
  error_code,task_typ,msg_type字段必须为数字
```