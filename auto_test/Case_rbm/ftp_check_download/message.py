import time
from common import baseinfo
from ftp_check_download import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
ftp_ip = baseinfo.ftp_ip
case1_downfile = index.case1_downfile
case2_downfile = index.case2_downfile
case2_allow_downfile = index.case2_allow_downfile

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
"Type":"download","DataCheck":case1_downfile}
]}
}
ftpcheck2 = {'SetFtpCheck':{
"MethodName":"SetFtpCheck",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Type":"download","DataCheck":f'{case2_downfile};{case2_allow_downfile}'}
]}
}

