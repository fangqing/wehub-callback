## faq(持续更新中)

如何查看wehub与 回调接口之间的数据通讯?
```
方法1:安装fiddler,该软件可以很直接的观察到wehub 的所有的http通讯
方法2:Wehub在 C:\Users\xxxxxx\AppData\Roaming\WeHub\system\log 目录下会产生log文件,
log的配置文件为 C:\Users\xxxxx\AppData\Roaming\WeHub\system\cfg\log4cxx.properties ,
若要看很详细的log,请提高loglevel:用记事本打开log配置文件,将第1行的"log4j.rootLogger = DEBUG, logFile"中的"DEBUG" 修"TRACE,将第6行的"log4j.appender.logFile.Threshold = DEBUG"中的"DEBUG" 修改为"TRACE" ,然后重启wehub.之后log文件会详细记录wehub 发送出去的http request和回调接口返回的respone
```

数据的编码方式
```
wehub 将utf-8编码的json格式的request以post方式发往回调接口(http 的ContentType 为application/json)
回调接口的respone也必须为utf-8的编码的json格式数据,否则wehub无法正确解析
```
