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
	from iso_http_basic import index
	from iso_http_basic import message
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
from data_check import http_check


datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

FrontDomain = baseinfo.BG8010FrontDomain
BackDomain = baseinfo.BG8010BackDomain
proxy_ip = baseinfo.BG8010FrontOpeIp
rbmExc = baseinfo.rbmExc
http_url = index.http_url
http_content = baseinfo.http_content


class Test_iso_http_basic():

    def setup_method(self):
        clr_env.data_check_setup_met(dut='FrontDut')
        clr_env.data_check_setup_met(dut='BackDut')

    def teardown_method(self):
        clr_env.iso_setup_class(dut='FrontDut')
        clr_env.iso_setup_class(dut='BackDut')

    def setup_class(self):
        # 获取参数
        fun.ssh_FrontDut.connect()
        fun.ssh_BackDut.connect()
        self.case1_step1 = index.case1_step1
        self.case1_step11 = index.case1_step11
        self.case2_step1 = index.case2_step1
        self.case2_step11 = index.case2_step11
        self.case3_step1 = index.case3_step1
        self.case3_step11 = index.case3_step11
        self.http_url = index.http_url
        self.downfile_url = index.downfile_url
        self.downlocalPath = index.downlocalPath
        self.upfile_url = index.upfile_url
        self.upfilename = index.upfilename
        self.uplocalPath = index.uplocalPath
        self.upMIME_type = index.upMIME_type


        clr_env.iso_setup_class(dut='FrontDut')
        clr_env.iso_setup_class(dut='BackDut')

    @pytest.mark.skip(reseason="skip")
    @allure.feature('验证隔离下的http代理策略')
    def test_iso_http_basic_a1(self):

        # 下发配置
        fun.send(rbmExc, message.addhttp_front['AddCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.addhttp_back['AddCustomAppPolicy'], BackDomain, base_path)
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

        # 发送get请求，验证隔离下的http策略
        print('请求地址为{}'.format(self.http_url))
        content = http_check.http_get(self.http_url)
        print('验证隔离下的http策略请求内容为：{}'.format(content))
        assert content == http_content

    @pytest.mark.skip(reseason="skip")
    @allure.feature('验证隔离下的http策略下载一个10M大小的文件')
    def test_iso_http_basic_a2(self):

        # 下发配置
        fun.send(rbmExc, message.addhttp_front['AddCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.addhttp_back['AddCustomAppPolicy'], BackDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        # 检查配置下发是否成功
        for key in self.case2_step1:
            re = fun.wait_data(self.case2_step1[key][0], 'FrontDut', self.case2_step1[key][1], '配置', 100)
            print(re)
            assert self.case2_step1[key][1] in re

        for key in self.case2_step11:
            re = fun.wait_data(self.case2_step11[key][0], 'FrontDut', self.case2_step11[key][1], '配置', 100)
            print(re)
            assert self.case2_step11[key][1] in re

        # 发送get请求，验证get请求是否正常
        print('请求地址为{}'.format(http_url))
        content = http_check.http_get(http_url)
        print('验证隔离下的get请求内容为：{}'.format(content))

        # 发送get请求，验证隔离下的http策略下载一个10M大小的文件
        print('下载的服务器地址为{}'.format(self.downfile_url))
        result = http_check.http_download(self.downfile_url, self.downlocalPath)
        assert result == 1


    # @pytest.mark.skip(reseason="skip")
    @allure.feature('验证隔离下的http策略上传一个10M大小的文件')
    def test_iso_http_basic_a3(self):

        # 下发配置
        fun.send(rbmExc, message.addhttp_front_post['AddCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.addhttp_back_post['AddCustomAppPolicy'], BackDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        # 检查配置下发是否成功
        for key in self.case3_step1:
            re = fun.wait_data(self.case3_step1[key][0], 'FrontDut', self.case3_step1[key][1], '配置', 100)
            print(re)
            assert self.case3_step1[key][1] in re

        for key in self.case3_step11:
            re = fun.wait_data(self.case3_step11[key][0], 'FrontDut', self.case3_step11[key][1], '配置', 100)
            print(re)
            assert self.case3_step11[key][1] in re

        #服务器端开启post上传服务

        #发送post请求，验证post请求是否正常
        print('请求地址为{}'.format(self.http_url))
        content = http_check.http_post(self.http_url)
        print('post普通请求的请求内容为：{}'.format(content))

        # 发送post请求，验证隔离下的http策略上传一个10M大小的文件
        print('上传的服务器地址为{}'.format(self.upfile_url))
        result = http_check.http_upload(self.upfile_url, self.upfilename, self.uplocalPath, self.upMIME_type)
        assert result == 1

        #检查文件是否生成




    def teardown_class(self):
        # 回收环境
        clr_env.iso_teardown_met('http', base_path)
        clr_env.iso_teardown_met('http_post', base_path)
        clr_env.iso_setup_class(dut='FrontDut')
        clr_env.iso_setup_class(dut='BackDut')

        fun.rbm_close()
        fun.ssh_close('FrontDut')
        fun.ssh_close('BackDut')
