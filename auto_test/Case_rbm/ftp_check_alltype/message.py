import time
from common import baseinfo
from ftp_check_alltype import index

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
proxy_ip = baseinfo.gwServerIp
ftp_ip = baseinfo.ftp_ip
allow_user = index.username
case1_upload = index.case1_upload
case1_downfile = index.case1_downfile

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
"Type":"user","DataCheck":allow_user},
{"Type":"cmd","DataCheck":"ABOR;ACCT;ADAT;ALLO;APPE;AUTH;CCC;CDUP;CONF;CWD;DELE;ENC;EPRT;EPSV;FEAT;HELP;LANG;LIST;LPRT;LPSV;MDTM;MIC;MKD;MLSD;MLST;MODE;NLST;NOOP;OPTS;PASS;PASV;PBSZ;PORT;PROT;PWD;QUIT;REIN;REST;RMD;RNFR;RNTO;SITE;SIZE;SMNT;STAT;STOR;STOU;STRU;SYST;TYPE;USER;XCUP;XMKD;XPWD;XRCP;XRMD;XRSQ;XSEM;XSEN"},
{"Type":"upload","DataCheck":case1_upload},
{"Type":"download","DataCheck":case1_downfile}
]}
}


