#encoding='utf-8'
try:
	import os,sys,pytest,allure,time,re
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
print(base_path)
try:
	from case1 import index
	from common import fun
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
#del sys.path[0]
from common import baseinfo

pcap_sip = baseinfo.clientOpeIp
pcap_dip = baseinfo.serverOpeIp


class Test_case1():

	def setup_method(self):

		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

	def teardown_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

		# 判断抓包程序是否停止，如果进程还在则停止
		fun.pid_kill(self.cap_pcap1)
		fun.pid_kill(self.cap_pcap2)

	def setup_class(self):
		# 获取参数
		fun.ssh_gw.connect()
		fun.ssh_c.connect()
		fun.ssh_s.connect()
		self.clr_env = clr_env.clear_env
		self.case1_step = index.case1_step
		self.case2_step = index.case2_step
		self.pkt1_cfg = index.pkt1_cfg
		self.pkt2_cfg = index.pkt2_cfg
		self.cap_pcap1 = self.pkt1_cfg["capture"][3]
		self.cap_pcap2 = self.pkt2_cfg["capture"][3]

		for i in self.clr_env:
			print(i)
			dd = fun.cmd(i, 'gw')
			print(dd)

	@allure.feature('测试1')
	def test_rabbitmq(self):
		#清空环境
		for i in self.clr_env:
			fun.cmd(i,'gw_s')

		agent_config = fun.cmd('cat /etc/jsac/agentjsac.config','gw_s')
		print(agent_config)

		agent_list = agent_config.split('\n')

		for i in agent_list:
			str_domain = re.findall("DeviceDomain = (\w*\d*.\w*\d*.\w*\d*.\w*\d*.\w*\d*)", i)
			if str_domain:
				domain = str_domain

		print(domain)

		#下发配置
		fun.send('ManageExchange','AddAclPolicy',domain,base_path)
		
		#检查配置下发是否成功
		re=fun.cmd(self.case_step['step1'][0],'gw_s')
		print(re)
		assert self.case_step['step1'][1] in re
		'''
		#开启接收端抓包
		fun.cmd(command.pre_env[0],'gw_c',thread=1)
		time.sleep(3)
		
		#客户端发送报文
		fun.cmd(command.case_step_c[0],'gw_s')
		
		#解析接收端抓包
		re=fun.cmd(command.result_check_c[0],'gw_c')
		assert command.case_result_c[0] in re
		'''

	def teardown_class(self):
		# 回收环境
		for i in clr_env.clear_env:
			fun.cmd(i, 'gw')

		for i in fun.mac:
			fun.ssh_close(i)

