# aliyun_flask_ddns_ros
# 阿里云DNS动态解
# 添加ros脚本
```
:local id "***********"  #阿里云ID
:local secret "FOrrT2HVWtkM3IPApm413CdR1qxv8c" #阿里云secret
:local domain "baidu.com" #填入主域名，不要带www
:local record "www" #填入需要解析的域名前缀 
:local pppoe "pppoe-out1"
:local ipaddr [/ip address get [/ip address find interface=$pppoe] address]
:set ipaddr [:pick $ipaddr 0 ([len $ipaddr] -3)]
:global aliip
:if ($ipaddr != $aliip) do={
:local result [/tool fetch url="http://10.10.10.9:8080/alidns?domain=$domain&record=$record&id=$id&secret=$secret&ip=ipaddr" as-value output=user]; #ip地址和端口号根据实际填写
:if ($result->"status" = "finished") do={
:if ($result->"data" = "0") do={
:set aliip $ipaddr
:log info "alidns update ok";
} else={
:log info "alidns update error";
}
}
}
```
