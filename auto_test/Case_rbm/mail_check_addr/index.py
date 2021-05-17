#coding:utf-8
from common import baseinfo

proxy_ip = baseinfo.gwServerIp
mail_attach = baseinfo.mail_attach

#smtp相关参数设置
mail_sender = 'liwanqiu66@163.com'  # 发件人
mail_receivers = ['m53667987@163.com','liwanqiu66@163.com']  # 收件人
mail_cc = ['liwanqiu66@163.com', 'm53667987@163.com']  # 抄送人
mail_bcc = ['liwanqiu66@163.com', 'm53667987@163.com']  # 暗送人
mail_host = proxy_ip  # 设置服务器,发件人的服务器代理
mail_port = baseinfo.mail_proxy_port  # 设置服务器端口
mail_user = "liwanqiu66@163.com"  # 邮件登录地址
mail_pass = "lwq5945"  # 授权码
deny_mail = 'jusontest@163.com'
deny_pwd = 'UMXDELUQAPUWQFNU'

#pop3相关参数设置
# 获取邮箱密码和对应邮箱POP3服务器,邮件地址跟收件人相同
pop3_email = "m53667987@163.com"
pop3_pwd = "GWCARVNCOYZWYHYB"   # 授权码
pop3_server_host = proxy_ip
pop3_server_port = baseinfo.pop3_server_port

title = '关于mail_check_addr'
context = '测试内容-content'
file = '1.xls'
attach_path = mail_attach + file

mail_ip = proxy_ip + ':' + str(mail_port)
pop3_ip = proxy_ip + ':' + str(pop3_server_port)

#配置检查
#列表里面的顺序依次为：查询命令，预期结果
case1_step1={
"step1":["cat /etc/jsac/protocol.stream","smtp8885"],
"step2":["cat /etc/jsac/protocol.stream","pop38886"]
}
case1_step11={
"step1":["netstat -anp |grep tcp",mail_ip],
"step2":["netstat -anp |grep tcp",pop3_ip]
}
case1_step2={
"step1":["cat /etc/jsac/filter.json","allow-from"],
"step2":["cat /etc/jsac/filter.json",mail_sender]
}


case2_step1={
"step1":["cat /etc/jsac/protocol.stream","smtp8885"],
"step2":["cat /etc/jsac/protocol.stream","pop38886"]
}
case2_step11={
"step1":["netstat -anp |grep tcp",mail_ip],
"step2":["netstat -anp |grep tcp",pop3_ip]
}
case2_step2={
"step1":["cat /etc/jsac/filter.json","allow-from"],
"step2":["cat /etc/jsac/filter.json",mail_sender],
"step3":["cat /etc/jsac/filter.json",mail_receivers[0]]
}
