#encoding='utf-8'
try:
	import os,sys,pytest,allure,time,re,time
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
print(base_path)
try:
	from iso_tcp import index
	from iso_tcp import message
	from common import fun
	import common.ssh as c_ssh
except Exception as err:
	print(
		'导入基础函数库失败!请检查相关文件是否存在.\n文件位于: ' + str(base_path) + '/common/ 目录下.\n分别为:pcap.py  rabbitmq.py  ssh.py\n错误信息如下:')
	print(err)
	sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
else:
	del sys.path[0]  # 及时删除导入的环境变量,避免重复导入造成的异常错误
# import index
# del sys.path[0]
#dir_dir_path=os.path.abspath(os.path.join(os.getcwd()))
#sys.path.append(os.getcwd())

from common import clr_env
from common import baseinfo
from common.rabbitmq import *
from data_check import send_smtp
from data_check import recv_pop3

datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

FrontDomain = baseinfo.BG8010FrontDomain
BackDomain = baseinfo.BG8010BackDomain
proxy_ip = baseinfo.BG8010FrontOpeIp
rbmExc = baseinfo.rbmExc


class Test_iso_tcp():

    def setup_method(self):
        clr_env.data_check_setup_met(dut='FrontDut')
        clr_env.data_check_setup_met(dut='BackDut')

    def teardown_method(self):
        clr_env.iso_teardown_met('mail', base_path)

    def setup_class(self):
        # 获取参数
        fun.ssh_FrontDut.connect()
        fun.ssh_BackDut.connect()
        self.case1_step1 = index.case1_step1
        self.case1_step11 = index.case1_step11
        self.mail_sender = index.mail_sender
        self.mail_receivers = index.mail_receivers
        self.mail_cc = index.mail_cc
        self.mail_bcc = index.mail_bcc
        self.mail_host = index.mail_host
        self.mail_port = index.mail_port
        self.mail_user = index.mail_user
        self.mail_pass = index.mail_pass
        self.pop3_email = index.pop3_email
        self.pop3_pwd = index.pop3_pwd
        self.pop3_proxy_port = index.pop3_proxy_port
        self.title = index.title
        self.file = index.file
        self.attach_path = index.attach_path
        self.context = index.context

        clr_env.iso_setup_class(dut='FrontDut')
        clr_env.iso_setup_class(dut='BackDut')

    # @pytest.mark.skip(reseason="skip")
    @allure.feature('验证基于主题关键字过滤的邮件策略')
    def test_iso_tcp_a1(self):

        # 下发配置
        fun.send(rbmExc, message.addsmtp_front['AddCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.addsmtp_back['AddCustomAppPolicy'], BackDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.send(rbmExc, message.addpop3_front['AddCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.addpop3_back['AddCustomAppPolicy'], BackDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        # 检查配置下发是否成功
        for key in self.case1_step1:
            re = fun.wait_data(self.case1_step1[key][0], 'FrontDut', self.case1_step1[key][1], '配置', 100)
            print(re)
            assert self.case1_step1[key][1] in re

        for key in self.case1_step11:
            re = fun.wait_data(self.case1_step11[key][0], 'FrontDut', self.case1_step11[key][1], '配置', 100)
            print(re)
            assert self.case1_step11[key][1] in re

        # 发送邮件，检测隔离代理是否生效
        result = send_smtp.post_email(self.mail_sender, self.mail_receivers, self.mail_cc, self.mail_bcc,
                                       self.mail_host, self.mail_port, self.mail_user, self.mail_pass,
                                       self.attach_path, self.file, self.title, self.context, 0, 0)
        print('隔离下的邮件代理{}结果为:{}'.format(self.title,result))
        assert result == 1

        # 接收邮件
        msg = recv_pop3.get_email(self.pop3_email, self.pop3_pwd, proxy_ip, self.pop3_proxy_port)
        print(msg)
        mail_list = recv_pop3.print_info(msg)  # 解析
        print('接收邮件解析到的列表为{}'.format(mail_list))
        assert self.title, self.context in mail_list


    def teardown_class(self):
        # 回收环境
        clr_env.iso_setup_class(dut='FrontDut')
        clr_env.iso_setup_class(dut='BackDut')

        fun.rbm_close()
        fun.ssh_close('FrontDut')
        fun.ssh_close('BackDut')
