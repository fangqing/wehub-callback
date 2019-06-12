#                                                        WeHub API接口规范v2

## 修改记录
修改时间|对应的客户端版本|协议修改内容
----|---|---
2018.9.28|v0.2.0| 简化ack_type类型,"发消息任务"的字段有调整 
2018.10.12|v0.2.2|回调地址改为到wehub后台网页里进行配置,增加secret key进行安全性验证
2018.10.17|v0.2.3|login中增加"local_ip"字段
2018.10.23|v0.2.6|增加 report_contact_update ;   userInfo 结构新增sex,country,province,city等字段
2018.11.16|v0.2.15|login,logout中增加 machine_id 字段(起辅助作用);新增task_type 为14的任务类型
2018.11.29|v0.3.0|在report_contact 中增加对当前账号关注的公众号信息的上报;开始支持语音消息中的语音数据上传;支持下发扩展的gif表情任务
2018.12.11|v0.3.3|上报的文本消息中新增atuserlist字段;支持发文件消息中的文件数据上传;report_room_member_info有新增字段
2018.12.27|v0.3.6|客户端增加缓存清理设置(接口协议无修改)
2019.1.18|v0.3.8|增加report_friend_removed
2019.3.15|v0.4.0|客户端新增升级功能并强制在登陆时做安全验证.  新增检查僵尸粉的任务类型(task_type为15), report_contact_update 的userInfo 结构中新增is_friend字段.
2019.4.4|v0.4.2|上报的个人微信号的信息中(城市,省份,国家等信息已准确),新增100,101两种本地打标签的任务类型.  wehub已支持websocket方式的通讯(见文档最下方的描述).   在发消息任务中增加at_style字段,可以把@符号放在文本中的任意位置 (见该任务类型的详细描述)

## 概述

```
- 什么是WeHub?
  WeHub是杭州推宝科技研发的一款针对微信windows客户端的辅助工具,它能监测微信中的各种事件,
  并辅助微信执行各种操作.它同时提供了对接企业服务的能力, 这需要第三方企业(以下简称为第三方)
  开发一套符合WeHub数据应答格式的webserver接口(以下简称为回调接口)

  WeHub所包含的能力分为两大类:
   一.截获微信内部发生的各种事件,并主动向回调接口发送这些事件的详细信息.
  这些事件的种类有:
  1.微信登陆事件(login)
  2.微信登出事件(logout)
  3.好友列表和群列表的信息及更新(report_contact,report_contact_update)
  4.收到新消息,包含私聊消息和群聊消息(report_new_msg)
  5.群成员的变化(report_room_member_change)
  6.发现了新的群(report_new_room)
  7.收到新的加好友请求(report_friend_add_request)
  8.好友被删除(report_friend_removed)
  9.新的好友(report_new_friend)
    
  二. 执行回调接口下发的指令:
  这些指令包括:
  1.发送一条具体的消息(包括发送文字,发送图片,发送链接,发送视频,发送个人名片)
  2.将其他人踢出群
  3.向其他人发送入群邀请
  4.获取群成员信息
  5.加群成员为好友
  6.修改好友备注
  7.修改群昵称(修改当前微信号在某个群里的群昵称)
  8.退群(退出某个群)
  9.发送群公告
  10.自动收账(自动收取其他微信号对当前微信号的某笔转账)
  11.删除某个好友
  12.通过好友验证(当其他账号给当前微信号发送加好友请求时,同意这次请求)
  13.上报当前好友列表和群列表 
  14.检测某个微信号是否是僵尸好友
  15.上传文件:上传某条聊天信息中的图片/语音/视频

- 什么是appid? 
  appid是一段字符串,WeHub使用它来区分不同的第三方.任何想使用wehub服务的第三方首先向推宝科技申请,
  申请时需提交自己的回调接口地址,推宝科技会对该地址做审核.第三方在使用WeHub时首先要在WeHub中
  配置appid,WeHub验证通过后才会post数据到第三方的回调接口地址上.

- 什么是wxid?
  就如同每个人都有一个身份证号一样,每一个微信号/微信群都有唯一的标识字符串用来做区分.
  对于微信群,其唯一标识格式为xxxxxx@chatroom(如8680025352@chatroom);
  对于个人微信号,其格式wxid_xxxxxxx(以wxid_开头,如wxid_p9597egc5j1c21)
  或者 xxxxxxx(不以wxid_开头,在注册微信号时由注册者指定,如fangqing_hust).
  本文档中所有数据结构中的"wxid"/"room_wxid"字段即代表微信号/群的唯一的标识字符串.

- 如何获取当前微信号的wxid?
  登陆微信PC客户端,点击当前微信号的头像(位于主界面左上角),弹出的界面中会显示"微信号:xxxxxxx", 
  "xxxxx" 即为当前微信号的wxid

- WeHub和第三方回调接口是如何通讯的?
  WeHub和回调接口之间采用http的方式进行通讯,双方都采用json格式的数据,utf-8编码. 
  当微信中有相关的事件发生时,WeHub会主动Post http request到回调接口,
  该http request中包含了解释具体微信事件的数据,回调接口返回
  http respone,respone中包含第三方需要WeHub执行的任务(任务的格式见文档中描述)
```

微信-wehub-回调接口 三者之间的数据流如下
![image](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/img/wehub_flow.png)

--------------
## 数据结构(request/respone)
wehub发送的数据(简称为:request)json格式为:
```
{
    "action": "具体业务名",
    "appid": "第三方申请的id",
    "wxid": "当前登录的wxid",
    "data": {具体业务的相关数据}
}
```
>wehub用"action"字段来区分发送的数据/事件的种类.
>比如当前微信收到一条新消息时,wehub会发送action为"report_new_msg"的json数据, "data"中的数据为一条具体的消息(包含的消息发送者的wxid和消息的内容)
>不同种类的action,对应的data的数据格式也不一样(接下来文档中会有详细描述)

回调接口返回的数据(简称为:respone)json格式为:
```
{
    "error_code": 0,            //0代表没有错误,其他的第三方自定义
    "error_reason": "",         //如果出错,这里写出错原因的描述,否则留空
    "ack_type":"xxxx_ack",      //ack_type 字段不能缺失                         
    "data":{
        xxxxx:xxxxxx    //具体的附带的数据,不同的ack_type对应不同的data格式
    }
}

对于respone中带双引号的数据域,如果其语义为字符串,则双引号不可缺少
如:"ack_type":"login_ack"
	ack_type字段其值代表具体的业务名称(字符串), 因此login_ack前后的""符号不能省略
又如: "error_code": 0, 
	error_code其值语义为一个具体的错误码(数字),因此0前后不需要""符号
```
>wehub发送的request 以utf-8编码,回调接口返回的respone 中的json格式数据 wehub 也以utf-8编码来解析 ,文档的示例代码中出现的  "$xxx"  符号代表这里应该出现一个名为"xxx"结构的数据对象,如 <a href="#memberInfo">$memberInfo</a>,  <a href="#task">$task</a>,  <a   href ="#report_msgunit">$report_msgunit</a>等

request中的action 类型|respone中的ack_type
----|----
login|login_ack
logout|logout_ack
pull_task|pull_task_ack
report_contact|common_ack
report_contact_update|common_ack
report_new_friend|common_ack
report_new_msg|common_ack
report_task_result|common_ack
report_room_member_info|common_ack
report_room_member_change|common_ack
report_friend_add_request|common_ack
report_new_room|common_ack
report_friend_removed|common_ack  
report_zoom_check_status|common_ack
**上述action中,回调接口必须实现对login的正确处理,否则使用相应appid的wehub 客户端将无法使用**
**对于其他不感兴趣/不想处理的action,可简单返回一个空的json**{}

### login(微信登录通知)
这是appid验证通过并且微信登陆后向回调接口发送的第一个request
<b>回调接口必须对这个request做出正确的响应,否则wehub 会提示登陆失败/安全验证失败</b>

<p>自0.2.2版本开始,wehub引进了"安全性验证"机制. 第三方的管理员请登录<a href="http://wehub.weituibao.com">WeHub后台</a>
对回调参数进行配置, 系统会自动为每一个appID生成了"secret key".</p>

<p><b>WeHub的计费策略是每月按appid统计登陆wehub的微信号的数量,
因此登陆wehub的微信号数量直接影响第三方的wehub使用费用.
为了使登陆的微信号处于可控状态,第三方必须在服务端建立微信号(wxid)的白名单,
在处理login请求时对白名单之外的微信号返回错误,这样没有列入
第三方白名单的微信无法用第三方申请的appid登陆wehub,也不会计入当月的使用量</b></p>
![image](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/img/wehub_s1.png)
![image](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/img/wehub_s2.png)

若"任务轮询间隔" <=0 ,则wehub 不会向回调接口轮询任务.


request格式为

```
{
    "action" : "login",				 //登录的业务名为"login"
    "appid": "xxxx",					 //申请的appid
    "wxid" : "wxid_fo1039029348sfj",    //当前登陆的微信账号的wxid
    "data" : {
      "nickname": "Bill",              //微信昵称
      "wx_alias": "mccbill",           //微信号(有可能为空)
      "head_img": "http://xxxxxx",     //微信的头像地址
      "client_version":"xxxxxx"		 //wehub的版本号
      "nonce":"xxxxxxxxxxxxxxx"     //回调接口在计算签名时用到这个nonce值
      								//有这个字段时服务端必须返回正确的签名
      								//没有这个字段时回调接口无需做签名处理
      "local_ip":"192.168.0.104|211.168.0.104"
      //当前wehub所在系统中的网卡ip,如有多个以'|'分隔, 该字段是在0.2.3 版本中新加入的
       "machine_id":"xxxxxx"    //wehub客户端的标识(由计算机名+进程id生成)0.2.15版本中加入
    }
}
```
回调接口返回(respone):
```
{
    "error_code": 0,                       
    "error_reason": "",                    
    "ack_type":"login_ack",
    "data":{
        "signature":"xxxxxxxxxxx"   //返回给wehub客户端的签名
    }
}
签名算法:
将login request中的wxid和nonce两个字段的值取出
然后将wxid,nonce,secretkey用'#'符号拼接成字符串,计算出md5值,该md5值的32位编码字符串即为签名值.

比如wxid为"fangqing_hust",nonce值为"helloworld",secretkey为"112233",
则signature = md5("fangqing_hust#helloworld#112233") = "4B8D798F8B34A7BD2CD3B4CBFA309D9C"
```

<p><b>从0.4.0版本开始,wehub客户端已强制要求做安全验证(无论后台是否取消了安全验证,request中都会有nonce 字段).对于服务端而言,只需判断受到的request中是否有nonce 字段, 有这个字段时服务端必须返回正确的签名!!! 没有这个字段时回调接口无需做签名处理(signature可以置空)</b></p>


###  logout(微信退出通知)
request格式:
```
{
    "action":"logout",
    "appid": "xxxxxx",				//申请的appid
    "wxid": "wxid_xxxxxxx",
    "data":{
       "client_version":"xxxxxx"		//wehub的版本号 
        "machine_id":"xxxxxx"    //wehub客户端的标识(由计算机名+进程id生成)0.2.15版本中加入
    }
}
```
respone格式
```
{
    "error_code": 0,                   
    "error_reason": "",                
    "ack_type":"logout_ack",                
    "data":{}
}
```
### report_contact(上报当前好友列表和群列表)
<p>这是紧接login之后发送的request, 如果微信的好友/群的数量比较多,这个request post的数据将会非常大.
由于微信客户端对联系人的信息加载是个lazy load 的过程,因此在report_contact 中上报的联系人信息可能不全,比如有的头像信息没有获取到,wehub会通过 report_contact_update的方式进行增量更新,详情见[上报成员信息变化]</p>
<b>report_contact 这个http请求Post的数据量会比较大(好友/群越多,post的数据就越大),请将服务端能接受的**post_max_size** 调整成至少10M </b>

request格式
```
{
    "action": "report_contact",
    "appid": "xxxxxx",
    "wxid": "wxid_xxxxxxx",
    "data":{
        "group_list":[$groupinfo,$groupinfo, $groupinfo,......],  //群
        "friend_list":[$userInfo,$userInfo,$userInfo,...],		//好友
        "public_list":[$publicinfo,$publicinfo,$publicinfo,....]  //公众号
    }
}
data中相关字段描述
- groupinfo(群信息结构):
{
    "wxid": "xxxxxxx",                  //群的wxid,格式为 xxxxx@chatroom
    "name": "xxxxxx",                   //群名称
    "owner_wxid": "xxxxxxxx",           //群主的wxid
    "member_count":  100,               //该群成员总数
    "head_img":"http://xxxxxxxx"        //群的头像的url地址
    "member_wxid_list" :['wxid_xxx1','wxid_xxx2',...]  //当前群的成员wxid的列表
}

- userInfo(好友信息结构)
{
    "wxid":  "wxid",                //wxid
    "wx_alias": "xxxxx",            //微信号(有可能为空)
    "nickname":"xxxxx",             //微信昵称
    "remark_name" :"xxxx",          //好友备注
    "head_img":"http://xxxxxxxx"    //头像的url地址
    "sex" : xx ,    				//性别:0或者1,默认是0,1代表女性
    "country":"xxx",				//祖国(可能为空)
    "province":"xxxx",				//省份(可能为空)
    "city":"xxxxx"					//城市(可能为空)
}

- publicinfo(公众号信息)
{
    "wxid":  "gh_xxxxx",   //某些公众号也可能以wxid_ 开头
    "nickname":"xxxxx",    //公众号名称
    "head_img":"http://xxxxxxxxxx"  //头像
}

```

respone格式为:common_ack格式

####  <a name="common_ack">[common_ack格式]</a>
```
{
    "error_code": 0,                      
    "error_reason": "",         
    "ack_type":"common_ack",                
    "data":{
         "reply_task_list": [$task,$task,...]  
        //回复的任务列表,如果没有要回复的任务,则列表为空
    }
}
```
注:每个$task都是一个json对象,代表一个要下发给wehub执行的任务,格式见<a href="#task"> [任务类型格式]</a>

**<u>示例</u>**
通过common_ack 向wehub回复两个任务,第一个任务让wehub向一个群发送3条消息(1条文本消息(同时@了两个群成员),1条图片消息,1条链接消息),第二个任务让wehub上报两个微信群的群成员信息

```
{
   "error_code": 0,                      
   "error_reason": "",         
    "ack_type":"common_ack",                
    "data":
    {
       "reply_task_list": 
        [
           {
              "task_type": 1,  
              "task_dict":
               {
                  "wxid_to":"wxid_test@chatroom",   		
                  "at_list":["wxid_b1","wxid_b2"], 
                  "msg_list":
                  [
                     {
                       "msg_type":1,
                        "msg":"自动回复,test"
                     },
                     {
                        "msg_type":3,
                         "msg":"https://www.baidu.com/img/bd_logo1.png"
                     },
                     {
                        'msg_type':49,
                        'link_url':"http://httpd.apache.org/",
                         "link_title":"apache",
                         "link_desc":"apache官网",		
                          "link_img_url":"http://httpd.apache.org/images/httpd_logo_wide_new.png"
                     }
                  ]  
               }
            },
            {
               "task_type":4,
               "task_dict":
               {
                  "room_wxid_list":["wxid_test1@chatroom","wxid_test2@chatroom"]
               }
            }
       ]  
    }
}
```
### report_contact_update(上报成员信息变化)
触发时机:
wehub探测到联系人列表中的信息有更新(如昵称,头像等)."联系人"可能是我的好友,也可能是某个群里的成员,也可能是某个陌生人---总之这个联系人不表述好友关系);
亦或是在上报report_contact时尚未获取到的联系人/群信息.
为节省流量,wehub 会每隔10s检查这些变化,然后上传这些变化的信息.

request格式
```
{
    "action":"report_contact_update",
    "appid":"xxxxxxxx",
    "wxid":"xxxxxxx",
    "data":{
        "update_list":[
            $userInfo,$groupbaseInfo,$userInfo,$groupbaseInfo,.....   
            // 群基本信息(groupbaseInfo)和联系人信息(userInfo)的无序列表
            // 如果其wxid字段以@chatroom结尾,其为groupbaseInfo
            // 否则代表联系人信息(userInfo)
    ]
  }
}

$userInfo 
- userInfo(好友信息结构)
{
    "wxid":  "wxid",                //wxid
    "wx_alias": "xxxxx",            //微信号(有可能为空)
    "nickname":"xxxxx",             //微信昵称
    "remark_name" :"xxxx",          //好友备注
    "head_img":"http://xxxxxxxx"    //头像的url地址
    "sex" : xx ,    				//性别:0或者1,默认是0,1代表女性
    "country":"xxx",				//祖国(可能为空)
    "province":"xxxx",				//省份(可能为空)
    "city":"xxxxx"					//城市(可能为空)
    'is_friend': x   			//0:不是我的好友;1:是我的好友     
}

$groupbaseInfo (群基本信息):
{
    "wxid": "xxxxxxx",                  //群的wxid:格式为 xxxxx@chatroom
    "name": "xxxxxx",                   //群名称
    "head_img":"http://xxxxxxxx"        //群头像的url地址
    "owner_wxid":"xxxxxx",				//群主的wxid,0.3.8版本中加入
    "member_count":xx					//群成员总数,0.3.8版本中加入
}


```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### report_room_member_info(上报群成员详细信息)
触发时机: 由回调接口通过下发"任务"来被触发
```
request
{
    "action":"report_room_member_info",
    "appid": "xxxxxxxx",				//申请的appid
    "wxid" : "wxid_fo1039029348sfj",
    "data" : {
   	   room_data_list:[
           {
              "room_wxid":"xxxxx1@chatroom",  //群wxid
              "name":"xxxx",  	     //群名(0.3.3版本中新增) 
              "owner_wxid":"xxxxx",  //群主wxid(0.3.3版本中新增)
              "head_img":"xxxxxxx",  //群头像(0.3.3版本中新增)
              "member_count": xxx,   //群内有多少个成员(0.3.3版本中新增)
              "memberInfo_list":[$memberInfo,$memberInfo.....] 
           	  //群内成员信息
           },
           ........
   	   ]
    }
}
```
####  <a name="memberInfo">$memberInfo格式</a>
```
{
    "wxid":  "wxid",             //wxid
    "wx_alias": "xxxxx",         //微信号(有可能为空)
    "room_nickname":			//这个微信号的群昵称
    "nickname":"xxxxx",             //微信昵称
    "head_img":"http://xxxxxxxx"    //头像的url地址
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### report_room_member_change(上报群成员变化)
触发时机:群成员增加或减少时上报

```
request
{
    "action":"report_room_member_change",
    "appid":"xxxxxxx",
    "wxid": "wxid_xxxxxxx",
      "data":{
        "room_wxid":"xxxxxxx@chatroom",
        "owner_wxid":"xxxxx",	//群主wxid, 0.3.8版本中加入
        "wxid_list";['xxxxxx','xxxxx'],  //变化的成员的wxid列表
        "flag": flag //0,群成员减少;1,群成员增加
      }
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>


### report_new_room(上报新群)
触发时机:当发现新的群时(比如被拉进了新的群或新建了新的群)
```
request
{
    "action":"report_new_room",
    "appid":"xxxxxxx",
    "wxid": "wxid_xxxxxxx",
      "data":{
        "wxid":"xxxxx",   //新群的wxid
        "name:"xxxx",	  //群名(可能为空)
        "owner_wxid":"xxxxx", //群主的wxid
        "head_img":"xxxx",  //群头像的url地址
        "memberInfo_list":[$memberInfo,$memberInfo,.....]  //见memberInfo结构
      }
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>


### report_new_msg(上报新的聊天消息)

触发时机:当收到私聊消息或所在的某个群内有人发言(含自己发送的消息)

**对于做了自动回复功能的第三方接口,需要过滤自己发的消息.否则会陷入"回调接口下发自动回复-->wehub发消息--->微信消息事件回调--->wehub上报刚才自己发的消息--->回调接口又下发聊天任务"的死循环**

```
一旦陷入死循环,容易导致wehub高频率地发消息,这极易触发微信系统的安全提醒甚至被封号
如何过滤自己发的消息?
若使用的wehub版本<0.1.4,回调接口在收到report_new_msg时,判断msg中的wxid是否为这个wehub上登陆的wxid. 若是,则不要下发task_type=1的发消息的任务
若使用的wehub版本>=0.1.4,回调接口在收到report_new_msg时,判断msg中的wxid_from是否为这个wehub上登陆的wxid.若是,则不要下发task_type=1的发消息的任务
```


```
request
{
    "action" : "report_new_msg",
    "appid": "xxxxxxxx",				//申请的appid
    "wxid" : "wxid_fo1039029348sfj",
    "data" : {
      "msg": $report_msgunit       //上报单条消息
      //report_msgunit格式见[上报的消息单元的格式]
      }
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

####   <a name="report_msgunit">上报的消息单元的格式($report_msgunit)</a>

 聊天消息类型|类型值msg_type|是否支持任务下发|是否支持上传消息中的文件
   ----|----|---|----
   文本消息|1|支持|----
   图片消息|3|支持|支持消息中的图片文件上传
   个人名片|42|支持|----
   语音|34|暂不支持|从0.3.0版本开始支持
   视频|43|支持|支持消息中的视频文件上传
   表情消息|47|从0.3.0版本开始支持|不支持
   链接消息 |49|支持|----
   小程序|4901|暂不支持|----
 转账 |4902|暂不支持|----
 文件 |4903|暂不支持|暂不支持
   微信系统通知 |10000|不支持|----

```
- 文本消息
{
    "msg_type": 1,                      //1 代表文本消息
    "room_wxid": "xxxxxxxx@chatroom",   //聊天消息发生在哪个群(如果是私聊则为空)
    "wxid_from":  "wxid_xxxxxx",     	//消息发送者的wxid
                                        //如果是自己发的消息这里的wxid就是自己的微信号
    "wxid_to": 	"wxid_xxxxx",		 //消息的接收者的wxid
                                     //如果发往群的消息,这个值就是群的wxid
                                     //如果是别人私聊给自己的消息,这里就是自己的微信号
    "atUserList": ["xxx","xxx"]        //这条消息@的对象列表                       
    "msg": "xxxxxxxx"                //具体的文本内容
  //如果A在群里面at了B(群昵称为BN),C(群昵称为CN),则msg的格式为"@BN @CN XXXXXX" (@BN @CN之间有空格)
}
例如:
  A用户在B群里发了一条消息:
  "room_wxid": "B群wxid",
  "wxid_from":"A的wxid",
  "wxid_to": "B群wxid",
  A给我私聊了一条消息:
    "room_wxid": "",
    "wxid_from":"A的wxid",
    "wxid_to": "我的wxid",
  我在B群里发了一条消息:
   "room_wxid": "B群wxid",
    "wxid_from":"我的wxid",
    "wxid_to": "B群wxid",
  我向A发了一条私聊消息:
    "room_wxid": "",
    "wxid_from":"我的wxid",
    "wxid_to": "A的wxid",
  
- 图片消息
{
    "msg_type": 3, 					  //3 代表图片消息
    "room_wxid": "xxxxxxxx@chatroom", //同文本消息
    "wxid_from": "wxid_xxxxxx", 	//同文本消息
    "wxid_to": 	"wxid_xxxxx",		//同文本消息
    "file_index":"xxxxxx"   		//图片文件的唯一索引(由wehub生成)
      //该字段在wehub上报消息时有效
      //如果是自己发/转发的图片,file_index为本地的文件路径
}

- 链接消息(分享某个网页链接)
{
    "msg_type":49, 					//49 代表链接消息
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "link_title":"标题", 			  //链接标题
    "link_desc": "副标题",           //链接描述（副标题）
    "link_url":"http://xxxxx", 		//分享链接的url
    "link_img_url": "http://xxxxxxx" //链接的缩略图的的Url,jpg或者png格式
    "raw_msg": "xxxxxxx"		//微信的原始消息,xml格式,0.3.14版本中新增
}
raw_msg 中的关键字段有"title","des","url","thumburl"(分别与link_title,link_desc,link_url,link_img_url值对应),如果link_url值为空,请自行分析raw_msg中的url.


- 表情消息
{
    "msg_type":47, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "emoji_url": "xxxxxxxxx" //表情的url地址(若有需要,请回调接口自行下载该文件)
    "raw_msg": "xxxxxxx"  
}

- 小程序
{
    "msg_type":4901, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "raw_msg": "xxxxxxx"    //微信中的小程序信息的原始数据,xml格式,请自行解析
        //username,nickname 为关键字段
}

- 转账事件 
触发时机:
情况一:我转账给他人
   1.发起转账时:wxid_from='我的wxid',wxid_to='他人的wxid',paysubtype=1
   2.对方确认收账时:wxid_from ='他人的wxid',wxid_to='我的wxid',paysubtype=3
情况二:他人转账给我:
   1.发起转账时:wxid_from ='他人的wxid',wxid_to='我的wxid',paysubtype=1
   (只有这种情况下才能自动收账,格式见自动收账任务)
   2.我确认收账时:wxid_from='我的wxid',wxid_to='他人的wxid',paysubtype=3
{
    "msg_type":4902, 					
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "transferid": "xxxxxxx"   //转账的ID
    "paysubtype":paysubtype,  //这笔账单的状态
    "raw_msg": "xxxxxxx"	  //微信中的转账事件的原始数据,xml格式				
}

- 文件
(从0.3.3版本开始支持文件上传)
{
    "msg_type":4903, 					
    "room_wxid": "xxxxxxxx@chatroom", 	//发生在哪个群里
    "wxid_from": "wxid_xxxxxx", 	  	//文件发送者
    "wxid_to":"wxid_xxxxx",	  			//文件接收者
    "file_index":"xxxxx",  		
    "file_name": "xxxxxx",		//文件名
    "file_size": xxxxx,		//字节数
    "raw_msg": "xxxxxxx"   	//微信中的文件的原始消息,xml格式,请自行解析
}
- 个人名片
{
    "msg_type":42, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "raw_msg": "xxxxxxx"   //微信中的名片信息的原始数据,xml格式,请自行解析
}
- 语音消息
(从0.3.0版本开始支持上传消息中的语音文件,将微信中原始语音数据转化为MP3格式后上报)
{
    "msg_type":34, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "file_index":"xxxxxxx",//0.3.0之前的版本中该值都预留为空
    "raw_msg": "xxxxxxx"   //微信中的原始消息,xml格式
}
- 视频消息
{
    "msg_type":43, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "file_index":"xxxxxx",  //视频文件的索引
    "raw_msg":"xxxxxxx",	//视频文件详细信息(文件大小length,播放时长playlength),需服务端自行解析;可根据文件大小来判断是否要上传
}

- 微信系统通知
{
    "msg_type":10000, 					
    "room_wxid": "xxxxxxxx@chatroom", 
    "wxid_from": "wxid_xxxxxx", 
    "wxid_to": "wxid_xxxxxx", 
    "raw_msg": "xxxxxxxx"     //具体的通知内容,纯文本格式
}
无需对系统通知做自动回复
eg:
1.发消息-被对方拉黑之后,raw_msg 为"消息已发出，但被对方拒收了"
2.有红包出没时:"发出红包，请在手机上查看"
3.修改群名称后:xxxxx修改群名为xxxxxxx
其他:
	群主已恢复默认进群方式。
	群主已启用“群聊邀请确认”，群成员需群主确认才能邀请朋友进群。
	你已成为新群主
	xxxxxx已成为新群主
	你邀请xxxx加入了群聊
	xxxx邀请xxxx加入了群聊
	xxxxx通过扫描你分享的二维码加入群聊"
	xxxxx通过扫描xxxxxx分享的二维码加入群聊"
```

### 文件上传
在<a href="http://wehub.weituibao.com">WeHub后台</a>配置文件上传的接口地址,WeHub会将需要上传的文件(比如聊天消息中的图片,语音,视频等)数据post到该地址上(form-data方式).
```
基本流程:
1.wehub收到图片消息/视频消息,上报基本信息(此时wehub仅仅通过report_new_msg上报该图片的索引file_index值,不上传具体文件的二进制信息)
2.回调接口根据file_index的值查询当前服务端文件存储系统中是否已经存在该索引的文件,若需要wehub上传,在ack中携带上传文件的任务类型:
比如
{
   "error_code": 0,                      
   "error_reason": "",         
    "ack_type":"common_ack",                
    "data":
    {
       "reply_task_list": 
        [
          {
              "task_type": 9,  
              "task_dict":
               {
                  "file_index":"xxxxxxx"
               }
          }
        ]
    }
}

3.wehub收到指令后通过文件上传接口上传文件(post 方式)
4.上传接口返回文件处理的结果
{
    'error_code':0,        
    'error_reason':'',     
    'ack_type':'upload_file_ack',
    'file_index':file_index     //接收到的文件的file_index
}
```
以下为 wehub向上传接口上传图片文件的http request示例
```
Content-Type: multipart/form-data; boundary="boundary_.oOo._OTg2Ng==MzU3Mg==MjEwNzE="
MIME-Version: 1.0
Content-Length: 46718
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en,*
User-Agent: Mozilla/5.0
Host: localhost.:5678

--boundary_.oOo._OTg2Ng==MzU3Mg==MjEwNzE=
Content-Type: text/plain
Content-Disposition: form-data; name="file_index"

3053020100044c304a02010002041cdc709b02032f56c10204a2e5e77302045b87dcfa0425617570696d675f356665376666383735333737623337355f313533353633303538353633390204010400020201000400
--boundary_.oOo._OTg2Ng==MzU3Mg==MjEwNzE=
Content-Type: image/jpeg
Content-Disposition: form-data; name="file";filename="6a0b2e8d81857cd9ac7cf4fcb6ac271fd409fc1d.jpg"

xxxxxxxxxxxxxxx.....  //图片的二进制字节流
xxxxxxxxxxxxxxx.....
```

上传视频
```
Content-Type: multipart/form-data; boundary="boundary_.oOo._MTQ5NDU=Mjg1Nzk=MTAyNzE="
MIME-Version: 1.0
Content-Length: 1351338
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en,*
User-Agent: Mozilla/5.0
Host: localhost.:5678

--boundary_.oOo._MTQ5NDU=Mjg1Nzk=MTAyNzE=
Content-Type: text/plain
Content-Disposition: form-data; name="file_index"

306b0201000464306202010002041cdc709b02032f56c10204cde5e77302045b99fc32043d617570766964656f5f356665376666383735333737623337355f313533363831383232345f3137353730343133303931383637613066633434323433300204010400040201000400
--boundary_.oOo._MTQ5NDU=Mjg1Nzk=MTAyNzE=
Content-Type: video/mp4
Content-Disposition: form-data; name="file";filename="c899cebad9877280af73d4e595f5d1e41e7b1ed8.mp4"

xxxxxxxxxxxxxxx.....  //视频文件的二进制字节流
xxxxxxxxxxxxxxx.....
```
上传语音
```
Content-Type: multipart/form-data; boundary="boundary_.oOo._NDM2NQ==NTkyNQ==MzE1ODQ="
MIME-Version: 1.0
Content-Length: 2993
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en,*
User-Agent: Mozilla/5.0
Host: localhost.:5678

--boundary_.oOo._NDM2NQ==NTkyNQ==MzE1ODQ=
Content-Type: text/plain
Content-Disposition: form-data; name="file_index"

4166303733643135323139616165340028224211291867a0fc48766102
--boundary_.oOo._NDM2NQ==NTkyNQ==MzE1ODQ=
Content-Type: audio/mpeg
Content-Disposition: form-data; name="file";filename="274cfbce78d88c83a9d0bd7d0cda9fe3c2da2d64.mp3"

xxxxxxxxxxxxxxx.....  //mp3文件的二进制字节流
xxxxxxxxxxxxxxx.....
```

注意: 
1.服务端的上传接口接收到wehub的request后需要取出 request中 file_index的值.
2.目前wehub支持上传图片/视频类型的文件,但wehub的文件上传功能并不是一个完全可靠的服务,当微信中的图片/视频没有下载完成时,wehub是无法上传这些文件的.

### report_friend_add_request(新的加好友请求)
收到添加好友的请求(此时对方还不是我的好友,不能给对方发消息)
微信系统对每个账号每天通过的好友请求有限制(每天200左右) 
服务端需要储存(v1,v2) 值, 以便通过任务下发的方式通过好友验证  

```
request
{
    "action" : "report_friend_add_request",
    "appid": "xxxxxxx",
    "wxid" : "wxid_fo1039029348sfj",
    "data" : {
      "v1":"xxxxxx",			  //若要自动通过,请在ack中回传
      "v2":"xxxxxxx",			  //若要自动通过,请在ack中回传
      "notice_word":"xxxxxxx", //新好友加我时的打招呼的内容,可能为空
      "raw_msg":"xxxxxxxxxxx"  //微信中的原始消息,xml格式
    }
}
若要自动通过好友验证,可在reply_task_list字段中加入"通过好友验证"的任务(task_type为13)
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### report_friend_removed(删除好友通知)
当某个好友被删除了会上报该事件
```
request格式
{
    "action":"report_friend_removed",
    "appid": "xxxxxxx",
    "wxid":	"xxxxxxx",
    "data":{
    	"wxid_removed":"xxxxxx"	    //被删除的好友的wxid
	}
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### report_new_friend(新好友通知)

每当有新的好友时,上报新好友的个人信息(此时对方已经成为了我的好友)


```
request格式
{
    "action" : "report_new_friend",
    "appid": "xxxxxxx",
    "wxid" : "xxxxxx",
    "data" : {
      "fans_wxid": "wxid_ljsdlfjslfjl",		 // 新好友的wxid
      "nickname": "Jerry",					// 新好友的昵称
      "wx_alias": "jerry"				// 新好友的微信号,可能为空
      "head_img": "xxxxx",			//头像url
      "notice_word":  "xxxxxxx"  		//新好友加我时的打招呼的内容,可能为空
      "sourceusername": "xxxxx"		//推荐人的wxid,可能为空
      "sourcenickname":"xxxxxxx" 		//推荐人昵称,可能为空
    }
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### <a name="task"> 任务类型格式[$task]</a>

回调接口在 respone中下发的任务格式

任务类型|类型值task_type
   ----|----
 发消息 |1(只支持文字,图片,链接,视频,个人名片)
 踢人 |2
 邀请入群(发送入群邀请) |3
   上报群成员信息 |4
   加群成员为好友|5
   修改好友备注|6
   修改群昵称|7
   退群|8
   上传文件|9
   发群公告|10 
   自动收账|11
   删除好友|12
   通过好友验证|13
   重新上报当前好友列表和群列表|14
   检测某个wxid是否是僵尸|15

[文本消息中静态表情转义对照表](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/Emoji/emoji_index.html)

当你在微信中发送一个的静态的![](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/Emoji/001.png)表情时,其实你只是发送了 "[笑脸]" 这几个文字

#### 发消息任务类型的数据格式
```
(向一个微信群或一个微信号发一组消息单元)
{
    "task_type": 1,  
    "task_dict":
    {
      "wxid_to":"xxxxxx",   		//消息发往的对象(群微信号或者个人微信号)
      "at_list":['xxxx','xxxx'],  //发群消息时,需要@的对象的wxid列表,可以为空
      							  //at_list对msg_list里所有的文本消息生效
      "msg_list":[$push_msgunit,$push_msgunit,....]  //待发送的消息单元列表
      "at_style": xx //0或者1, 默认为0.  该字段在0.4.2中新增.
    }
}

发消息任务中的$push_msgunit格式
⑴文字消息
{
    'msg_type':1,
    'msg': "xxxxxx"  发送的文字(可以嵌入转义的静态表情文字,参阅上方的链接 静态表情转义对照表)
}
关于@符号的位置


⑵图片消息
{
    'msg_type':3,
    'msg':"xxxx"  //图片的url绝对地址:http://xxxxxxx/xx.jpg或png 
}
⑶gif表情         //从0.3.0开始支持
{
    "msg_type":47,
    "msg":"http://xxxxxxx/xx.gif"  //gif的url:必须是gif格式
}
⑷链接消息
{
    "msg_type":49,                    //49 代表链接消息
    "link_url":"http://xxxxx",        //分享链接的url
    "link_title":"标题",              //链接标题
    "link_desc": "副标题",             //链接描述（副标题）
    "link_img_url": "http://xxxxxxx"    //链接的缩略图的的Url,jpg或者png格式
}
⑸视频消息
{
    "msg_type":43, 	
    "video_url":"http://xxxxxxx/xx.mp4" //回调接口推送给用户的视频的url地址, mp4格式 
}
⑹个人名片
{
    "msg_type":42, 	
    "wxid_card":"xxxxxx" 		//发送谁的个人名片
}
```

**关于'@'符号的位置**

```
只针对发往群的文本消息有效
在0.4.2版本之前,wehub是默认把@符号放在文本消息的最前面的.
从0.4.2版本开始,支持把'@'放在文本消息的任意位置,具体操作如下:
1.发消息任务中的at_style字段设置为1
2.文本消息的msg的内容中设置占位字符串 {$@},这些字符的位置就是最终的@符号所在的位置
{
    "task_type": 1,  
    "task_dict":
    {
      "wxid_to":"xxxxxx",   		
      "at_list":["wxid_a","wxid_b"],  //假设这两个被@的微信号的群昵称分别为aa,bb
      "msg_list":[
          {
              'msg_type':1,
              'msg':"test,你好{$@},你好{$@}.早上好"
          }
      ]  
      "at_style": 1  //注意这里必须为1.
    }
}
则wehub收到后,则实际发送的内容为 "test,你好@ aa,你好@ bb.早上好"(占位符被替换了)
注意at_list不能为空,at_style必须为1,占位字符串的数量必须和at_list中的微信数量相等.
当at_style为0时仍然按照以往的方式(@符号放在文本最前面,此时发送文本总即使有{$@}占位符wehub也不会进行替换)进行发送
```

```
- 踢人任务:
(把一个微信号从指定的群踢出,当前微信必须有群主权限)
{
    "task_type":2,
    "task_dict":
    {
      "room_wxid":"xxxxx@chatroom", //被踢者所在的群,如果为空,则从所有的群踢出
      "wxid":"xxxxxxx"              //被踢者的wxid
    }
}
```

```
- 拉群任务:
(向一个好友发入群邀请,注意必须是自己的好友)
{
    "task_type":3,
    "task_dict":
    {
      "room_wxid":"xxxxx@chatroom", //目标群
      "wxid":"xxxxxxx"              //被拉进群的wxid
    }
}
- 上报群成员信息:
(上报某个群里所有的群成员的详细信息,如果群成员比较多,上报的数据量会比较大)
{
    "task_type":4,
    "task_dict":
    {
      //要上报的群列表
      "room_wxid_list":["xxxxx@chatroom","xxxxx2@chatroom"....]  
    }
}
wehub 通过report_room_member_info来主动上报,详情见[上报群成员详细信息]

- 加群成员为好友：
{
    "task_type":5,
    "task_dict":
    {
      "room_wxid":"xxxxx@chatroom", //群wxid,可以留空
      "wxid":"xxxxxxx"              //要加谁为好友,不能为空
      "msg":"xxxxxx"                //打招呼消息,文本
    }
}
- 修改好友备注:
{
    "task_type":6,
    "task_dict":
    {
      "wxid":"xxxxxx",        //好友微信
      "remark_name":"xxxxxx" 	//好友备注
    }
}
- 修改群昵称:
(修改当前微信号在某个群里的群昵称)
{
    "task_type":7,
    "task_dict":
    {
      "room_wxid":"xxxxxx",     //微信群wxid
      "room_nickname":"xxxxxx" 	//我在这个群里的昵称
    }
}
- 退群:
{
    "task_type":8,
    "task_dict":
    {
      "room_wxid":"xxxxxx",   //要退出的微信群wxid
    }
}
- 上传文件
{
    "task_type":9,
    "task_dict":
    {
      "file_index":"xxxxxxx",   //需要上传的文件的file_index
    }
}
//第三方需要将wehub上传的文件保存起来,建立file_index与上传文件的对应关系

- 发群公告
{
    "task_type":10,
    "task_dict":
    {
      "room_wxid":"xxxxxx",   //微信群
      "msg":"xxxxxx"          //群公告的内容
    }
}

- 自动收账 (只能收取别人发给自己的转账)
{
    "task_type":11,
    "task_dict":
    {
      "wxid_from": "xxxxxx"     //转账发起者wxid
      "transferid":"xxxxxx"     //transferid:自动收哪一笔转账
    }
}
- 删除好友
{
    "task_type":12,
    "task_dict":
    {
      "wxid_delete": "xxxxx"  //要被删除的好友的wxid
    }
}
- 通过好友验证
{
    "task_type":13,
    "task_dict":
    {
      "v1": "xxxxx",
      "v2": "xxxxx"
    }
}

- 重新上报联系人 (wehub会重新发送report_contact)
{
    "task_type":14,
    "task_dict":{}
}

- 僵死粉检测 (检测结果通过report_zoom_check_status上报)
 {
     "task_type":15
     "task_dict":
     {
		"wxid":"xxxxx"		//待检测的wxid
	 }
 }

- 操作标签(新增,删除标签)
{
    "task_type":100
    "task_dict":
    {
    	"tag_name":"xxxxx",  //被操作的标签名
    	"wxid_list":["wxid_xxx","wxid_xxx"]    //群或者好友的wxid(不能包含陌生人)
    	"op_code" : xx   // 1:将wxid_list加入到tag_name标签中(如果没有这个标签则新建这个标签)
    					 // 2:将wxid_list中的成员从tag_name标签中删除
    					 // 3:删除tag_name标签(此时会忽略wxid_list参数)  					 
	}
}
- 重命名标签
(将old_tag_name标签重命名为new_tag_name)
{
    "task_type":101
    "task_dict":
    {
    	"old_tag_name": "xxxx",
    	"new_tag_name":"xxxx"
	}
}

```
### 上报僵死粉检测结果(report_zoom_check_status)

触发时机: 无论是操作客户端主动开始检测或者下发任务让客户端被动检测,都会上报检测到的结果.

```
request格式
{
    "action":"report_zoom_check_status",
    "appid": "xxxxxxx",
    "wxid":	"xxxxxxx",
    "data":{
    	"wxid":"xxxxxx",//被检测的wxid
    	"status": x  	//0 :正常状态(不是僵尸粉)
    					//1 :检测为僵尸粉(对方把我拉黑了)
                    	//2 :检测为僵尸粉(对方把我从他的好友列表中删除了)
	}
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>

### pull_task(向回调接口请求一个任务)
wehub在appid验证通过以后,每间隔x秒请求一次(时间间隔可在wehub后台设置.若无需轮询,则设置任务轮询间隔 为0秒)
request格式

```
{
    "action": "pull_task",
    "appid": "xxxxxx",
    "wxid" : "wxid_xxxxxxxx",
    "data":{}
}
```
respone格式
```
{
    "error_code": 0,                    
    "error_reason": "",     
    "ack_type":"pull_task_ack",         
    "data":{
         //wehub通过task_id来识别不同的任务(task_id其值是由回调接口生成的字符串,请保证有唯一性)
        "task_id": "任务id",    //字符串
        "task_data": $task     //单个任务
    }
}
```
注: $task是一个json对象,代表一个要下发给wehub执行的任务,格式见<a href="#task"> [任务类型格式]</a>,wehub接收到任务以后,会立即开始执行,执行完成后会把结果异步地反馈给回调接口(通过report_task_result)

**<u>示例</u>**

通过pull_task_ack 向wehub下发一个任务(该任务将wxid_abc从群bcdef@chatroom 中踢出)

```
{
    "error_code": 0,                    
    "error_reason": "",     
    "ack_type":"pull_task_ack",         
    "data":
    {
        "task_id": "aaaa111222",    
        "task_data": 
        {
           "task_type":2,
           "task_dict":
           {
              "room_wxid":"bcdef@chatroom", 
              "wxid":"wxid_abc"		  
           }
        }
    }
}
```
### report_task_result(向回调接口反馈任务执行的结果)
request格式
```
{
    "action": "report_task_result",
    "appid": "xxxxxxx",         
    "wxid" : "wxid_xxxxxxxx"
    "data":
    {
      "task_id": "任务id",
      "task_result": 1,   //0,任务执行失败,1任务执行成功
      "error_reason": ""  //为什么执行失败,若任务执行成功则为空
    }
}
```
respone格式为<a href="#common_ack">[common_ack格式]</a>


## 其他
### 容易混淆的地方
- wehub主动上报的消息与服务端下发的任务的区别

  (1).前者是在http request中(通过report_xxxxx),数据从wehub流向server;后者是在http respone中(通过common_ack 或者pull_task_ack),数据由服务端流向wehub

  (2).二者的格式不样,前者的消息格式见<a href="#report_msgunit">[上报的消息单元的格式]</a>;后者的任务格式见<a href="#task"> [任务类型格式]</a>

  前者的消息主要是视觉可感知的数据(如文本,图片) ,而后者的任务除了发消息,还包括很多不可感知的事件(如踢人出群,删除好友等)

- common_ack 与 pull_task_ack 的区别:

  common_ack中可携带多个下发的任务(data中有reply_task_list字段),但不会上报任务执行的结果

  pull_task_ack只能下发一个任务(data中没有reply_task_list字段),且必须有task_id字段,通过pull_task_ack 下发的任务会通report_task_result 上报任务执行的结果;

  common_ack 与pull_task_ack中的任务格式都是一样的,见<a href="#task"> [任务类型格式]</a>

  


### 关于websocket的通讯方式
  <div>WeHub默认采用http短连接的方式和回调接口进行数据,这导致了回调接口只能被动的响应wehub,无法主动下发指令给WeHub.从0.4.2版本开始,WeHub支持用websocket的方式和第三方服务器进行通讯.具体流程如下:</div>

![image](http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/img/websocket.png)

>wehub会先发送login request到当前回调地址,然后尝试从respone中寻找extension_protocol字段,
>并获取到要去连接的websocket服务器的真实ws地址(格式为ws://xxxx或者wss://xxxx,和原有的http回调地址不一样).
>这样做的好处是把目前的回调接口当做跳板,并且可以配置多个ws地址进行负载均衡.

回调接口在收到wehub发送的login请求后返回如下(如果测试的话可以只对特定的wxid才返回这个ws地址)
```
{
    "error_code": 0,                       
    "error_reason": "",                    
    "ack_type":"login_ack",
    "data":
    {
        "signature":"xxxxxxxxxxx"    //返回给wehub客户端的签名(同上)
        "extension_protocol":
        {
            "type":"websocket",                     //目前只能是"websocket"
            "param":
             {
                "ws_url":"ws://127.0.0.1:3456/ws",  //ws服务地址
                "heartbeat_interval":30    		      //心跳时间间隔(秒)
             }
        }
    }
}
```
<div>wehub获取到ws地址后,之后就会websocket服务进行连接,不再将数据post到原来回调接口地址上.
websocket连接建立后wehub会主动定时发送心跳包给第三方websocket服务,时间间隔在heartbeat_interval字段中指定</div>

websocket为什么需要心跳? 参考 https://blog.csdn.net/feiwutudou/article/details/80564630 

```
心跳包格式如下
{
    "atcion":"heartbeat",
    "appid": "xxxxx",
    "wxid": "xxxx",
    "data":{}
}
```
<div>双方约定采用json格式的文本进行通讯,所有的数据格式仍然和目前已有的格式保持一致.
由于websocket连接的双方都可以收发数据,因此wehub不再会定时发pull_task,websocket服务端可以直接通过发送common_ack, pull_task_ack格式的指令给wehub(json格式的文本) </div>
关于websocket服务端的demo:https://github.com/fangqing/wehub-callback-websocket

更多的问题请参考<a href="./faq.md">faq</a>

