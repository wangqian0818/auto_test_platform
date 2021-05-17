
from common import baseinfo
import time


datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
front_ifname = baseinfo.BG8010FrontOpeIfname
back_ifname = baseinfo.BG8010BackOpeIfnameOutside
smtp_ip = baseinfo.smtp_ip
pop3_ip = baseinfo.pop3_ip
mail_sip = baseinfo.mail_sip
front_cardid = baseinfo.BG8010FrontCardid
back_cardid = baseinfo.BG8010BackCardid
smtp_proxy_port = baseinfo.mail_proxy_port
pop3_proxy_port = baseinfo.pop3_server_port


addsmtp_front = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":smtp_ip,
"Sip":mail_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":1,
"L3protocol":"ipv4",
"Dport":25,
"SeLabel":{},
"Module":"smtp",
"File":"off",
"Lport":smtp_proxy_port,
"L4protocol":"tcp"}]
}]
}
}

addsmtp_back = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":smtp_ip,
"Sip":mail_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":2,
"L3protocol":"ipv4",
"Dport":25,
"SeLabel":{},
"Module":"smtp",
"File":"off",
"Lport":smtp_proxy_port,
"L4protocol":"tcp"}]
}]
}
}


addpop3_front = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":pop3_ip,
"Sip":mail_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":3,
"L3protocol":"ipv4",
"Dport":110,
"SeLabel":{},
"Module":"pop3",
"File":"off",
"Lport":pop3_proxy_port,
"L4protocol":"tcp"}]
}]
}
}

addpop3_back = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":pop3_ip,
"Sip":mail_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":4,
"L3protocol":"ipv4",
"Dport":110,
"SeLabel":{},
"Module":"pop3",
"File":"off",
"Lport":pop3_proxy_port,
"L4protocol":"tcp"}]
}]
}
}


delsmtp_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":smtp_ip,
"Sip":mail_sip,
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
"Sip":mail_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":2,
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
"Sip":mail_sip,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":3,
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
"Sip":mail_sip,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Appid":4,
"L3protocol":"ipv4",
"Dport":110,
"Module":"pop3",
"Lport":pop3_proxy_port,
"L4protocol":"tcp"}]
}]
}
}