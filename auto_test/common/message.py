import time
from common import baseinfo

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
smtp_ip = baseinfo.smtp_ip
pop3_ip = baseinfo.pop3_ip
ftp_ip = baseinfo.ftp_ip
http_server = baseinfo.http_server
http_server_port = baseinfo.http_server_port
iso_timeout = baseinfo.iso_timeout
serverIp = baseinfo.BG8010ServerOpeIp
clientIp = baseinfo.BG8010ClientOpeIp
dns_port = baseinfo.dns_port
dns_proxy_port = baseinfo.dns_proxy_port
ssh_proxy_port = baseinfo.ssh_proxy_port

front_ifname = baseinfo.BG8010FrontOpeIfname
back_ifname = baseinfo.BG8010BackOpeIfnameOutside
windows_sip = baseinfo.windows_sip
front_cardid = baseinfo.BG8010FrontCardid
back_cardid = baseinfo.BG8010BackCardid
smtp_proxy_port = baseinfo.mail_proxy_port
pop3_proxy_port = baseinfo.pop3_server_port
ftp_proxy_port = baseinfo.ftp_proxy_port
http_proxy_port = baseinfo.http_proxy_port
http_server_port_file = baseinfo.http_server_port_file


delsmtp = {'DelAgent':{
"MethodName":"DelAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"smtp",
"Type":2,
"InPort":8885,
"domain":"all",
"SyncId":85,
"OutAddr":[{"OutPort":25,"OutIp":smtp_ip}],
"InIp":proxy_ip
}]
}}
delpop3 = {
'DelAgent':{
"MethodName":"DelAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"pop3",
"Type":2,
"InPort":8886,
"domain":"all",
"SyncId":86,
"OutAddr":[{"OutPort":110,"OutIp":pop3_ip}],
"InIp":proxy_ip
}]
}}
delhttp = {
'DelAgent':{
"MethodName":"DelAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"http",
"Type":2,
"InPort":2287,
"domain":"all",
"SyncId":27,
"OutAddr":[{
"OutPort":http_server_port,
"OutIp":http_server}],
"InIp":proxy_ip}]
}}
delftp = {
'DelAgent':{
"MethodName":"DelAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"ftp",
"Type":2,
"InPort":8887,
"domain":"all",
"SyncId":87,
"OutAddr":[{"OutPort":21,"OutIp":ftp_ip}],
"InIp":proxy_ip
}]}
}



delsmtp_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":smtp_ip,
"Sip":windows_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":1,
"L3protocol":"ipv4",
"Dport":25,
"Module":"smtp",
"Lport":smtp_proxy_port,
"L4protocol":"tcp"}]
}]
}
}
delsmtp_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":smtp_ip,
"Sip":windows_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":1,
"L3protocol":"ipv4",
"Dport":25,
"Module":"smtp",
"Lport":smtp_proxy_port,
"L4protocol":"tcp"}]
}]
}
}
delpop3_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":pop3_ip,
"Sip":windows_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":2,
"L3protocol":"ipv4",
"Dport":110,
"Module":"pop3",
"Lport":pop3_proxy_port,
"L4protocol":"tcp"}]
}]
}
}
delpop3_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":pop3_ip,
"Sip":windows_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":2,
"L3protocol":"ipv4",
"Dport":110,
"Module":"pop3",
"Lport":pop3_proxy_port,
"L4protocol":"tcp"}]
}]
}
}

delftp_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":ftp_ip,
"Sip":windows_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":3,
"L3protocol":"ipv4",
"Dport":21,
"Module":"ftp",
"Lport":ftp_proxy_port,
"L4protocol":"tcp"}]
}]}
}

delftp_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":ftp_ip,
"Sip":windows_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":3,
"L3protocol":"ipv4",
"Dport":21,
"Module":"ftp",
"Lport":ftp_proxy_port,
"L4protocol":"tcp"}]
}]}
}

deltcp_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Action":"allow",
"Appid":4,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":http_server_port,
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

deltcp_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Action":"allow",
"Appid":4,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":http_server_port,
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

deltcp_ssh_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":30,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":22,
"Lport":ssh_proxy_port,
"L4protocol":"tcp"}]}
]}
}

deltcp_ssh_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":30,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":22,
"Lport":ssh_proxy_port,
"L4protocol":"tcp"}]
}]}
}


deludp_dns_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}

deludp_dns_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}

delhttp_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Module":"http",
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

delhttp_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Module":"http",
"Lport":http_proxy_port,
"L4protocol":"tcp"}]
}]}
}

delhttp_front_post = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Module":"http",
"Lport":http_server_port_file,
"L4protocol":"tcp"}]
}]}
}

delhttp_back_post = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
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
"Module":"http",
"Lport":http_server_port_file,
"L4protocol":"tcp"}]
}]}
}

