
from common import baseinfo
import time

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
front_ifname = baseinfo.BG8010FrontOpeIfname
back_ifname = baseinfo.BG8010BackOpeIfnameOutside
windows_sip = baseinfo.windows_sip
front_cardid = baseinfo.BG8010FrontCardid
back_cardid = baseinfo.BG8010BackCardid
http_server = baseinfo.http_server
http_server_port = baseinfo.http_server_port
http_proxy_port = baseinfo.http_proxy_port
http_server_port_file = baseinfo.http_server_port_file

addhttp_front = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":http_server,
"Sip":windows_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":20,
"L3protocol":"ipv4",
"Dport":http_server_port,
"SeLabel":{},
"Module":"http",
"File":"off",
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

addhttp_back = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":http_server,
"Sip":windows_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":20,
"L3protocol":"ipv4",
"Dport":http_server_port,
"SeLabel":{},
"Module":"http",
"File":"off",
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

addhttp_front_post = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":http_server,
"Sip":windows_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":21,
"L3protocol":"ipv4",
"Dport":http_server_port_file,
"SeLabel":{},
"Module":"http",
"File":"off",
"Lport":http_server_port_file,
"L4protocol":"tcp"}]
}]}
}

addhttp_back_post = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":http_server,
"Sip":windows_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":21,
"L3protocol":"ipv4",
"Dport":http_server_port_file,
"SeLabel":{},
"Module":"http",
"File":"off",
"Lport":http_server_port_file,
"L4protocol":"tcp"}]
}]}
}
