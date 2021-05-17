# encoding='utf-8'

# 以下参数配置仅与执行环境有关，与用例无关
version = 'test1.0.0'  # 版本信息
controlIp = '10.10.88.6'
'''
mode：代表的是执行ssh类型的链接还是其他的，例如：rabbitmq或其他类型的
需要在common同级目录建立Case_ssh文件夹，其中的ssh是mode变量的值，这个可以根据需要随意进行设置
为了便于理解与书写方便，建议ssh链接的定义为ssh；Rabbitmq链接的定义为rbm
同时，需要在common目录下建议caseselect_ssh.py文件，对Case_ssh目录中的单元测试例文件夹进行选择
其中的ssh是一一对应的
'''
mode = 'rbm'  # 要测试的类型
strip = '[]\n'
qos_port = '8888'

# 发件设置
smtp_server = "smtphz.qiye.163.com"  # 发包服务器
sender_passwd = "Js1234"  # 发件箱密码
sender_addr = "baotest@jusontech.com"  # 发件箱
receiver_addr = ["wangqian@jusontech.com"]  # 收件人

# 数据结构检查相关ip
smtp_ip = '220.181.12.11'
pop3_ip = '220.181.12.110'
ftp_ip = '192.168.50.4'
windows_sip = '10.10.100.136'

# server的/usr/local/nginx/html路径下需要有get或者post需要的文件：test.php、juson.php、123.php（.php为post需要的）
http_url = 'http://10.10.88.55:2287'
http_proxy_port = 2287
http_server = '10.10.100.201'
http_content = 'You got right!'
http_server_port = 80
http_server_port_file = 9999

# mail相关参数设置
mail_proxy_port = 8885
pop3_server_port = 8886
mail_sip = '10.10.100.136'  # 发送邮件的源ip，即运行环境的ip，即电脑的本机ip

# ftp相关参数设置
ftp_proxy_host = "192.168.50.47"
ftp_proxy_port = 8887

# vxlan等封装报文的内层ip和port设置
vxlan_sip = '172.16.1.243'
vxlan_dip = '172.16.1.196'
vxlan_sp = 42982
vxlan_dp = 8889

# 定制应用（隔离）相关配置
iso_timeout = 10
ssh_proxy_port = 5555

# dns协议相关配置
dns_domain = 'www.test.com'
dns_port = 53
dns_proxy_port = 5353

# 定义字典类型
DeviceObject = {}
# client端设置
DeviceObject['client', 'manageIp'] = "10.10.88.23"  # 设备的管理ip
DeviceObject['client', 'loginUser'] = "root"  # 登入的用户名
DeviceObject['client', 'loginPwd'] = "3e2b6e75b403c492"  # 登入的密码
DeviceObject['client', 'operationIp'] = "192.168.30.23"  # 设备间通信的业务ip

# server端设置
DeviceObject['server', 'manageIp'] = "10.10.88.27"  # 设备的管理ip
DeviceObject['server', 'loginUser'] = "root"  # 登入的用户名
DeviceObject['server', 'loginPwd'] = "3e2b6e75b403c492"  # 登入的密码
DeviceObject['server', 'operationIp'] = "192.168.50.27"  # 设备间通信的业务ip

# dut的设置
DeviceObject['gateway', 'manageIp'] = "10.10.88.55"  # 设备的管理ip，若管理ip无法直连，则添加路由使其通信
DeviceObject['gateway', 'loginUser'] = "root"  # 登入的用户名
DeviceObject['gateway', 'loginPwd'] = "1q2w3e"  # 登入的密码
DeviceObject['gateway', 'operationIpClient'] = "192.168.30.47"  # 设备间通信的业务ip（client）
DeviceObject['gateway', 'operationIpServer'] = "10.10.88.55"  # 设备间通信的业务ip（server）   //http & mail
# DeviceObject['gateway', 'operationIpServer'] = "192.168.50.47"  # 设备间通信的业务ip（server）   //ftp
DeviceObject['gateway', 'card0'] = "CS807304LV200A1N042"  # cardid为0的网卡序列号
DeviceObject['gateway', 'card1'] = "CS807304LV2008CN003"  # cardid为1的网卡序列号
DeviceObject['gateway', 'card2'] = "807102F02CV11099N006"  # cardid为2的网卡序列号

# 定义隔离组网

BG8010 = {}
# 隔离client的设置
BG8010['client', 'manageIp'] = "10.10.88.11"  # 隔离测试客户端管理IP
BG8010['client', 'loginUser'] = "root"  # 登录账户
BG8010["client", "loginPwd"] = "3e2b6e75b403c492"  # 登录密码
BG8010["client", "operationIp"] = "192.168.30.11"  # 设备间通信用的业务IP

# 隔离server端的设置
BG8010['server', 'manageIp'] = "10.10.88.27"  # 隔离测试服务器端管理IP
BG8010['server', 'loginUser'] = "root"  # 登录账户
BG8010["server", "loginPwd"] = "3e2b6e75b403c492"  # 登录密码
BG8010["server", "operationIp"] = "192.168.50.27"  # 设备间通信用的业务IP

# 隔离设备端的设置
BG8010['front_dut', 'manageIp'] = "10.10.88.54"  # 隔离测试前置机管理IP
BG8010['front_dut', 'loginUser'] = "root"  # 登录账户
BG8010["front_dut", "loginPwd"] = "1q2w3e"  # 登录密码
BG8010["front_dut", "operationIp"] = "192.168.30.54"  # 设备间通信用的业务IP
BG8010["front_dut", "operationIfname"] = "enp60s0f00"  # 设备接口名
BG8010["front_dut", "domain"] = "hf.f1203.g01.cs_17.a54"  # 前置机domain
BG8010["front_dut", "cardid"] = "CS807304LV2008CN017"  # 前置机domain

BG8010['back_dut', 'manageIp'] = "10.10.88.57"  # 隔离测试后置机管理IP
BG8010['back_dut', 'loginUser'] = "root"  # 登录账户
BG8010["back_dut", "loginPwd"] = "1q2w3e"  # 登录密码
BG8010["back_dut", "operationIpInside"] = "192.168.50.57"  # 设备间通信用的业务IP
BG8010["back_dut", "operationIfnameInside"] = "enp60s0f00"  # 设备接口名
BG8010["back_dut", "operationIpOutside"] = "10.10.88.57"  # 设备间通信用的业务IP
BG8010["back_dut", "operationIfnameOutside"] = "enp60s0f01"  # 设备接口名
BG8010["back_dut", "domain"] = "hf.f1203.g01.cs_17.wg57"  # 后置机domain
BG8010["back_dut", "cardid"] = "CS807304LV2008CN014"  # 安全卡的网卡序列号

# rabbitmq相关的设置
DeviceObject['rabbitmq', 'manageIp'] = "10.10.88.32"  # rabbitmq server所在服务器地址
DeviceObject['rabbitmq', 'loginUser'] = "root"  # 登入的用户名
DeviceObject['rabbitmq', 'loginPwd'] = "3e2b6e75b403c492"  # 登入的密码
DeviceObject['rabbitmq', 'rbmUser'] = "admin"  # rabbitmq登录用户名
DeviceObject['rabbitmq', 'rbmPwd'] = "1qazxsw2#"  # rabbitmq登录密码
DeviceObject['rabbitmq', 'DeviceDomain'] = 'hf.f1203.g01.xn_17.gw47'  # 设备domain代码
DeviceObject['rabbitmq', 'exchanges'] = 'ManageExchange'  # 交换机名称

# 报文相关的设置(网口与执行环境有关)
DeviceObject['packet', 'sendIface'] = "ens9"  # 报文发送时的出接口
DeviceObject['packet', 'gwIface'] = "enp59s0f00"  # 报文发送时的出接口
DeviceObject['packet', 'readIface'] = "ens9"  # 抓取报文时的接口

# 文件路径设置

ftp_upremotePath = '/home/ftp/ftp_auto/'  # ftp上传的ftp服务器路径
ftp_uplocalPath = 'C:\\Users\\admin\\Desktop\\work\\'  # ftp上传的本地路径
ftp_downremotePath = '/home/ftp/ftp_auto/'  # ftp下载的ftp服务器路径
ftp_downlocalPath = 'C:\\Users\\admin\\Desktop\\work\\downfile\\'  # ftp下载的本地路径
ftp_delePath = '/home/ftp/ftp_auto/ftp_del'
mail_attach = 'C:\\Users\\admin\\Desktop\\work\\'  # 邮件发送的附件路径
http_downlocalPath = 'C:\\Users\\admin\\Desktop\\work\\httpdown\\'  # ftp下载的本地路径
http_uplocalPath = 'C:\\Users\\admin\\Desktop\\work\\'

clientIp = DeviceObject['client', 'manageIp']
clientUser = DeviceObject['client', 'loginUser']
clientPwd = DeviceObject['client', 'loginPwd']
clientOpeIp = DeviceObject['client', 'operationIp']

serverIp = DeviceObject['server', 'manageIp']
serverUser = DeviceObject['server', 'loginUser']
serverPwd = DeviceObject['server', 'loginPwd']
serverOpeIp = DeviceObject['server', 'operationIp']

gwManageIp = DeviceObject['gateway', 'manageIp']
gwUser = DeviceObject['gateway', 'loginUser']
gwPwd = DeviceObject['gateway', 'loginPwd']
gwClientIp = DeviceObject['gateway', 'operationIpClient']
gwServerIp = DeviceObject['gateway', 'operationIpServer']
gwCard0 = DeviceObject['gateway', 'card0']
gwCard1 = DeviceObject['gateway', 'card1']
gwCard2 = DeviceObject['gateway', 'card2']

# 隔离client的设置
BG8010ClientIp = BG8010['client', 'manageIp']
BG8010ClientUser = BG8010['client', 'loginUser']
BG8010ClientPwd = BG8010["client", "loginPwd"]
BG8010ClientOpeIp = BG8010["client", "operationIp"]

# 隔离server端的设置
BG8010ServerIp = BG8010['server', 'manageIp']
BG8010ServerUser = BG8010['server', 'loginUser']
BG8010ServerPwd = BG8010["server", "loginPwd"]
BG8010ServerOpeIp = BG8010["server", "operationIp"]

# 隔离设备端的设置
BG8010FrontIp = BG8010['front_dut', 'manageIp']
BG8010FrontUser = BG8010['front_dut', 'loginUser']
BG8010FrontPwd = BG8010["front_dut", "loginPwd"]
BG8010FrontOpeIp = BG8010["front_dut", "operationIp"]
BG8010FrontOpeIfname = BG8010["front_dut", "operationIfname"]
BG8010FrontDomain = BG8010["front_dut", "domain"]
BG8010FrontCardid = BG8010["front_dut", "cardid"]

BG8010BackIp = BG8010['back_dut', 'manageIp']
BG8010BackUser = BG8010['back_dut', 'loginUser']
BG8010BackPwd = BG8010["back_dut", "loginPwd"]
BG8010BackOpeIpInside = BG8010["back_dut", "operationIpInside"]
BG8010BackOpeIfnameInside = BG8010["back_dut", "operationIfnameInside"]
BG8010BackOpeIpOutside = BG8010["back_dut", "operationIpOutside"]
BG8010BackOpeIfnameOutside = BG8010["back_dut", "operationIfnameOutside"]
BG8010BackDomain = BG8010["back_dut", "domain"]
BG8010BackCardid = BG8010["back_dut", "cardid"]

rbmIp = DeviceObject['rabbitmq', 'manageIp']
rbmUser = DeviceObject['rabbitmq', 'loginUser']
rbmPwd = DeviceObject['rabbitmq', 'loginPwd']
rbmWebUser = DeviceObject['rabbitmq', 'rbmUser']
rbmWebPwd = DeviceObject['rabbitmq', 'rbmPwd']
rbmDomain = DeviceObject['rabbitmq', 'DeviceDomain']
rbmExc = DeviceObject['rabbitmq', 'exchanges']

pcapSendIface = DeviceObject['packet', 'sendIface']
pcapGwIface = DeviceObject['packet', 'gwIface']
pcapReadIface = DeviceObject['packet', 'readIface']
