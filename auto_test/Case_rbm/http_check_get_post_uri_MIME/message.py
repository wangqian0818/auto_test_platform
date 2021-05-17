import time
from common import baseinfo
from http_check_get_post_uri_MIME import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
proxy_port = index.proxy_port
server_ip = baseinfo.http_server
server_port = baseinfo.http_server_port
get1_data1 = index.get1_data1
get1_data2 = index.get1_data2
post1_data1 = index.post1_data1
post1_data2 = index.post1_data2
check1_uri1 = index.check1_uri1
check1_uri2 = index.check1_uri2
MIME1_uri1 = index.MIME1_uri1
MIME1_uri2 = index.MIME1_uri2

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
"Type":"uri","DataCheck":[{"DataType":"re","Data":f"{check1_uri1};{check1_uri2}"}]},
{"Type":"mime","DataCheck":[{"Action":0,"Data":f"{MIME1_uri1};{MIME1_uri2}"}]},
{"Type":"content","DataCheck":[
{"method":"get","DataType":"re","Data":f"{get1_data1};{get1_data2}"},
{"method":"post","DataType":"re","Data":f"{post1_data1};{post1_data2}"}
]}]
}}
httpcheck2 = {
'SetHttpCheck':{
"MethodName":"SetHttpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"uri","DataCheck":[{"DataType":"re","Data":f"{check1_uri1};{check1_uri2}"}]},
{"Type":"mime","DataCheck":[{"Action":1,"Data":f"{MIME1_uri1};{MIME1_uri2}"}]},
{"Type":"content","DataCheck":[
{"method":"get","DataType":"re","Data":f"{get1_data1};{get1_data2}"},
{"method":"post","DataType":"re","Data":f"{post1_data1};{post1_data2}"}
]}]
}}
