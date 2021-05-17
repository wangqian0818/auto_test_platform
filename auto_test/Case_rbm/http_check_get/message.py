import time
from common import baseinfo
from http_check_get import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
proxy_port = index.proxy_port
server_ip = baseinfo.http_server
server_port = baseinfo.http_server_port
check1_data1 = index.check1_data1
check2_data1 = index.check2_data1
check2_data2 = index.check2_data2

addhttp = {
'AddAgent':{
"MethodName":"AddAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"http",
"Type":2,
"InPort":proxy_port,
"domain":"all",
"SyncId":27,
"OutAddr":[{
"OutPort":server_port,
"OutIp":server_ip}],
"InIp":proxy_ip}]
}}
delhttp = {
'DelAgent':{
"MethodName":"DelAgent",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"InProtocol":"http",
"Type":2,
"InPort":proxy_port,
"domain":"all",
"SyncId":27,
"OutAddr":[{
"OutPort":server_port,
"OutIp":server_ip}],
"InIp":proxy_ip}]
}}
httpcheck1 = {
'SetHttpCheck':{
"MethodName":"SetHttpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"content",
"DataCheck":[{"method":"get","DataType":"re","Data":check1_data1}]}]
}}
httpcheck2 = {
'SetHttpCheck':{
"MethodName":"SetHttpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"content",
"DataCheck":[{"method":"get","DataType":"re","Data":f'{check2_data1};{check2_data2}'}]}]
}}