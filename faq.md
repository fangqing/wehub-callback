## faq(持续更新中)

如何查看wehub与 回调接口之间的数据通讯?
```
方法1:安装fiddler,该软件可以很直接的观察到wehub 的所有的http通讯
方法2:Wehub在 C:\Users\xxxxxx\AppData\Roaming\WeHub\system\log 目录下会产生log文件   
log的配置文件为C:\Users\xxxxx\AppData\Roaming\WeHub\system\cfg\log4cxx.properties,    
若要看很详细的log,请提高loglevel:
用记事本打开log配置文件,将第1行"log4j.rootLogger = DEBUG,logFile"中的"DEBUG" 修改为"TRACE",
将第6行的"log4j.appender.logFile.Threshold = DEBUG"中的"DEBUG" 修改为"TRACE",然后重启wehub.
之后log文件会详细记录wehub 发送出去的http request和回调接口返回的respone
```

数据的编码方式
```
wehub 将utf-8编码的json格式的request以post方式发往回调接口(http 的ContentType 为application/json)
回调接口的respone也必须为utf-8的编码的json格式数据,否则wehub无法正确解析
```

wehub是否可以多开?
```
wehub是可以多开的,但不会主动帮你多开微信.
你必须首先多开微信,再多开wehub才有意义
```

回调接口该如何处理上报的聊天消息?
```
wehub提供基础的微信聊天消息上报的能力,不过滤发送者的wxid(但会过滤公众号推送的内容)
因此回调接口在做自动回复的时候,需要过滤自己的微信号发的消息.否则会陷入"回调接口下发自动 
回复内容--->wehub发消息--->微信消息事件回调--->wehub上报刚才自己发的消息--->回调接口又下发聊天任务"的死循环
```
