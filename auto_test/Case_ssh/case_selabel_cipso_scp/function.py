#encoding='utf-8'
try:
	import os,sys,pytest,allure,time
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
try:
	from case_selabel_cipso_scp import index
	import common.baseinfo as info
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
sys.path.append(os.getcwd())
from common import fun
from common import clr_env
#del sys.path[0]
from common import baseinfo


pcap_sip = baseinfo.clientOpeIp
pcap_dip = baseinfo.serverOpeIp

class Test_selabel_cipso_scp():

	def setup_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

	def teardown_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

		fun.pid_kill(self.cap_pcap1)

	def setup_class(self):
		#获取参数
		fun.ssh_gw.connect()
		fun.ssh_c.connect()
		fun.ssh_s.connect()
		self.clr_env = clr_env.clear_env
		#self.pre_env=index.pre_env
		# self.case1_step=index.case1_step
		self.pkt1_cfg=index.pkt1_cfg
		self.cap_pcap1 = self.pkt1_cfg["capture"][3]

		for i in self.clr_env:
			print(i)
			dd=fun.cmd(i,'gw')
			print(dd)

	#@pytest.mark.skip(reseason="skip")
	@allure.feature('验证标记系统tcp上传功能')
	def test_selabel_category_cipso_scp(self):

		#下发配置并检查结果
		# for key in self.case1_step:
		# 	fun.cmd(self.case1_step[key][0],'gw')
		# 	re = fun.cmd(self.case1_step[key][1],'gw')
		# 	assert self.case1_step[key][2] in re

		#服务端抓取报文
		cap_iface, cap_filter, cap_num, cap_pcap=self.pkt1_cfg['capture'][0], self.pkt1_cfg['capture'][1],self.pkt1_cfg['capture'][2],self.pkt1_cfg['capture'][3]
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		#发送文件
		c_scp,c_dip = self.pkt1_cfg["scp"][0],self.pkt1_cfg["scp"][1]
		scp_cmd = fun.pkt_scp(c_scp,c_dip)
		fun.cmd(scp_cmd,'c')


		#检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file

		#读包
		# read_name, read_id = self.pkt1_cfg["read"][0], self.pkt1_cfg["read"][1]
		# read_cmd = fun.pkt_read(read_name, read_id)
		# print(read_cmd)
		# read_re = fun.cmd(read_cmd, 's')
		# print(read_re)
		#获取期望结果
		# exp = self.pkt1_cfg["expect"][0]
		# assert exp == read_re

	def teardown_class(self):
		#回收环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw')
		for i in fun.mac:
			fun.ssh_close(i)

