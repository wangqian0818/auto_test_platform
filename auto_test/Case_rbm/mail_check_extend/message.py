import time
from common import baseinfo
from mail_check_extend import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
smtp_ip = baseinfo.smtp_ip
pop3_ip = baseinfo.pop3_ip
case1_extend1 = index.case1_extend1
case2_extend1 = index.case2_extend1
case2_extend2 = index.case2_extend2

addsmtp = {
'AddAgent':{
"MethodName":"AddAgent",
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
addpop3 = {
'AddAgent':{
"MethodName":"AddAgent",
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
mailcheck1 = {
'SetMailCheck':{
"MethodName":"SetMailCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"attachment",
"DataCheck":{"ext":f'{case1_extend1}'}}]
}}
mailcheck2 = {
'SetMailCheck':{
"MethodName":"SetMailCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"attachment",
"DataCheck":{"ext":f'{case2_extend1};{case2_extend2}'}}]
}}
