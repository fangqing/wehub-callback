## faq(持续更新中)

如何查看wehub与 回调接口之间的数据通讯?
```
方法1:安装fiddler,该软件可以很直接的观察到wehub 的所有的http通讯
    在本机上开发和部署回调接口服务的开发者,需下载最新版wehub,打开设置界面,切换到"其他设置"-->设置http代理为127.0.0.1:8888(保持和fiddler默认的代理设置一致),然后就可以在fiddler中查看wehub发送的http request
	
方法2:Wehub在 C:\Users\xxxxxx\AppData\Roaming\WeHub\system\log 目录下会产生log文件   
log的配置文件为C:\Users\xxxxx\AppData\Roaming\WeHub\system\cfg\log4cxx.properties,    
若要看很详细的log,请提高loglevel:
用记事本打开log配置文件,将第1行"log4j.rootLogger = DEBUG,logFile"中的"DEBUG" 修改为"TRACE",
将第6行的"log4j.appender.logFile.Threshold = DEBUG"中的"DEBUG" 修改为"TRACE",然后重启wehub.
之后log文件会详细记录wehub 发送出去的http request和回调接口返回的respone
```

通过log文件来排查常见的问题
```
错误1:log中出现  "unknow format reply data,error = xxxxx"
原因: 回调接口收到wehub发送的http request后,返回的http respone不是json格式,wehub无法解析或解析出错

错误2:log中出现"HubLogic OnReplyError, replay error = xxx", xxx的值是下方NetworkError枚举类型的值
原因:回调接口的服务端运行不正常(比如服务没有开启,回调接口的域名无法解析等等)

enum  NetworkError {
        NoError = 0,
// network layer errors [relating to the destination server] (1-99):
        ConnectionRefusedError = 1,
        RemoteHostClosedError,
        HostNotFoundError,
        TimeoutError,
        OperationCanceledError,
        SslHandshakeFailedError,
        TemporaryNetworkFailureError,
        NetworkSessionFailedError,
        BackgroundRequestNotAllowedError,
        TooManyRedirectsError,
        InsecureRedirectError,
        UnknownNetworkError = 99,

        // proxy errors (101-199):
        ProxyConnectionRefusedError = 101,
        ProxyConnectionClosedError,
        ProxyNotFoundError,
        ProxyTimeoutError,
        ProxyAuthenticationRequiredError,
        UnknownProxyError = 199,

        // content errors (201-299):
        ContentAccessDenied = 201,
        ContentOperationNotPermittedError,
        ContentNotFoundError,
        AuthenticationRequiredError,
        ContentReSendError,
        ContentConflictError,
        ContentGoneError,
        UnknownContentError = 299,

        // protocol errors
        ProtocolUnknownError = 301,
        ProtocolInvalidOperationError,
        ProtocolFailure = 399,

        // Server side errors (401-499)
        InternalServerError = 401,
        OperationNotImplementedError,
        ServiceUnavailableError,
        UnknownServerError = 499
    };
```


数据的编码方式
```
wehub 将utf-8编码的json格式的request以post方式发往回调接口(http 的ContentType 为application/json)
回调接口的respone也必须为utf-8的编码的json格式数据,否则wehub无法正确解析
```

wehub是否可以多开?
```
0.1.4之前的wehub不支持多开微信,之后的wehub已支持多开微信.
多开方式:先开启一个wehub和微信并登陆;再开启第二个wehub和微信并登陆;重复以上步骤
如果这个过程中wehub没有自动开启新的微信客户端,手动点击wehub界面上的"打开微信"按钮.
```

回调接口该如何处理上报的聊天消息?
```
wehub提供基础的微信聊天消息上报的能力,不过滤发送者的wxid(但会过滤公众号推送的内容)
因此回调接口在做自动回复的时候,需要过滤自己的微信号发的消息.否则会陷入"回调接口下发自动 
回复内容--->wehub发消息--->微信消息事件回调--->wehub上报刚才自己发的消息--->回调接口又下发聊天任务"的死循环
```