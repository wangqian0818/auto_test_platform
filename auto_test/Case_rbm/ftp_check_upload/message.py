import time
from common import baseinfo
from ftp_check_upload import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
ftp_ip = baseinfo.ftp_ip
case1_upload = index.case1_upload
case2_upload = index.case2_upload
case2_allow_upload = index.case2_allow_upload

addftp = {
'AddAgent':{
"MethodName":"AddAgent",
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
}]
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
ftpcheck1 = {'SetFtpCheck':{
"MethodName":"SetFtpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"upload","DataCheck":case1_upload}
]}
}
ftpcheck2 = {'SetFtpCheck':{
"MethodName":"SetFtpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"upload","DataCheck":f'{case2_upload};{case2_allow_upload}'}
]}
}

