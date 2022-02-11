# aliyun_ddns_ros
# 阿里云DNS动态解

```
docker run -itd --name='aliyun_flask_ddns' \
-e TZ="Asia/Shanghai" \
-e ACCESS_KEY_ID='' \ #阿里云ACCESS_KEY_ID
-e ACCESS_KEY_SECRET='' \ #阿里云ACCESS_KEY_ID
-e DOMAIN='' \ #主域名，如:baidu.com
-e SUBDOMAINS='' \ 子域名，如:www,new,blog,多个子域名中间用英文逗号隔开
-e AUTH_TOKEN='' \ 任意字符串，用于连接验证
-p 2000:80/tcp \
yangyang202107/aliyun_flask_ddns:latest
```
# 添加ros脚本
```
:local token "XXXXXX" #docker中设置的AUTH_TOKEN
:local url "http://10.10.10.3" #请求url地址
:local port 2000 #请求端口
:local pppoe "pppoe-out1"
:local ipaddr [/ip address get [/ip address find interface=$pppoe] address]
:set ipaddr [:pick $ipaddr 0 ([len $ipaddr] -3)]

:global aliip

if ($ipaddr != $aliip) do={
:local result [/tool fetch url="$url/?token=$token&ip=$ipaddr" mode=http port=$port as-value output=user];
:if ($result->"status" = "finished") do={
:set aliip $ipaddr
:log info ($result->"data")
}
}
```
