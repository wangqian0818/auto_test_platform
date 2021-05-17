#encoding='utf-8'
try:
	import os,sys,pytest,allure,time
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
sys.path.append(os.getcwd())

base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件

try:
	from tupleacl_priority_quintet_same import index
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


from common import clr_env
from common import baseinfo


pcap_sip = baseinfo.clientOpeIp
pcap_dip = baseinfo.serverOpeIp
#del sys.path[0]


class Test_acl_priority_quintet_same():

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
		fun.pid_kill(self.cap_pcap3)

	def setup_class(self):
		# 获取参数
		fun.ssh_gw.connect()
		fun.ssh_c.connect()
		fun.ssh_s.connect()
		self.clr_env = clr_env.clear_env
		self.case1_step1 = index.case1_step1
		self.case2_step1 = index.case2_step1
		self.case3_step1 = index.case3_step1
		self.pkt1_cfg = index.pkt1_cfg
		self.pkt2_cfg = index.pkt2_cfg
		self.pkt3_cfg = index.pkt3_cfg
		self.cap_pcap1 = self.pkt1_cfg["capture"][3]
		self.cap_pcap2 = self.pkt2_cfg["capture"][3]
		self.cap_pcap3 = self.pkt3_cfg["capture"][3]

		for i in self.clr_env:
			print(i)
			dd = fun.cmd(i, 'gw')
			print(dd)

	
	# @pytest.mark.skip(reseason="skip")
	@allure.feature('验证优先级相同情况下的策略命中规则（五元组数量相同,比较sip和dip）')
	def test_acl_priority_quintet_same_a1(self):

		#初始化
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt1_cfg["capture"][0], self.pkt1_cfg["capture"][1], self.pkt1_cfg["capture"][2], self.pkt1_cfg["capture"][3]
		c_iface, c_num, c_pcap = self.pkt1_cfg["send"][0], self.pkt1_cfg["send"][1], self.pkt1_cfg["send"][2]
		read_name, read_id = self.pkt1_cfg["read"][0], self.pkt1_cfg["read"][1]

		#切换卡面为0,下发配置并检查结果
		for key in self.case1_step1:
			fun.cmd(self.case1_step1[key][0],'gw')
			re = fun.cmd(self.case1_step1[key][1],'gw')
			assert self.case1_step1[key][2] in re

		# # 切换卡面为1,下发配置并检查结果
		# fun.cmd('export cardid=1', 'gw')
		# for key in self.case1_step2:
		# 	fun.cmd(self.case1_step2[key][0], 'gw')
		# 	card1 = fun.cmd(self.case1_step2[key][1], 'gw')
		# 	assert self.case1_step2[key][2] in card1

		# 服务端抓取报文
		# pcap_cmd = f'tcpdump -i {cap_iface} -w /opt/pkt/{cap_pcap} host {cap_filter}'
		# print(pcap_cmd)
		# fun.cmd(pcap_cmd,'s',thread=1)
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		print(pre_cfg)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 发送报文
		send_cmd = fun.pkt_send(c_iface, c_num, c_pcap)
		fun.cmd(send_cmd, 'c')


		#检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file

		# #c从远程服务器读取文件
		# pkt_read = fun.read(f'/opt/pkt/{cap_pcap}','read','r','','s')
		# print(pkt_read)	#b为二进制读取，后面的字符串为读取的内容
		# 读包
		read_cmd = fun.pkt_read(read_name, read_id)
		print(read_cmd)
		read_re = fun.cmd(read_cmd, 's')
		print(read_re)

		# 获取期望结果
		exp = self.pkt1_cfg["expect"][0]
		assert exp == read_re

	# @pytest.mark.skip(reseason="skip")
	@allure.feature('验证优先级相同情况下的策略命中规则（五元组数量相同,比较sip+dip+dp和dip+dp+协议）')
	def test_acl_priority_quintet_same_a2(self):

		#初始化
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt2_cfg["capture"][0], self.pkt2_cfg["capture"][1], self.pkt2_cfg["capture"][2], self.pkt2_cfg["capture"][3]
		c_iface, c_num, c_pcap = self.pkt2_cfg["send"][0], self.pkt2_cfg["send"][1], self.pkt2_cfg["send"][2]
		read_name, read_id = self.pkt2_cfg["read"][0], self.pkt2_cfg["read"][1]

		# 切换卡面为0,下发配置并检查结果
		for key in self.case2_step1:
			fun.cmd(self.case2_step1[key][0], 'gw')
			re = fun.cmd(self.case2_step1[key][1], 'gw')
			assert self.case2_step1[key][2] in re


		# 服务端抓取报文
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 发送报文
		send_cmd = fun.pkt_send(c_iface, c_num, c_pcap)
		fun.cmd(send_cmd, 'c')


		#检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file

		# 读包
		read_cmd = fun.pkt_read(read_name, read_id)
		read_re = fun.cmd(read_cmd, 's')
		print(read_re)

		# 获取期望结果
		exp = self.pkt2_cfg["expect"][0]
		assert exp == read_re

	# @pytest.mark.skip(reseason="skip")
	@allure.feature('验证优先级相同情况下的策略命中规则（五元组数量相同,比较dip+sp和dip+dp）')
	def test_acl_priority_quintet_same_a3(self):

		#初始化
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt3_cfg["capture"][0], self.pkt3_cfg["capture"][1], self.pkt3_cfg["capture"][2], self.pkt3_cfg["capture"][3]
		c_iface, c_num, c_pcap = self.pkt3_cfg["send"][0], self.pkt3_cfg["send"][1], self.pkt3_cfg["send"][2]
		read_name, read_id = self.pkt3_cfg["read"][0], self.pkt3_cfg["read"][1]

		# 切换卡面为0,下发配置并检查结果
		for key in self.case3_step1:
			fun.cmd(self.case3_step1[key][0], 'gw')
			re = fun.cmd(self.case3_step1[key][1], 'gw')
			assert self.case3_step1[key][2] in re

		# 服务端抓取报文
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		print(pre_cfg)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 发送报文
		send_cmd = fun.pkt_send(c_iface, c_num, c_pcap)
		fun.cmd(send_cmd, 'c')

		#检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file

		# 读包
		read_cmd = fun.pkt_read(read_name, read_id)
		read_re = fun.cmd(read_cmd, 's')
		print(read_re)

		# 获取期望结果
		exp = self.pkt3_cfg["expect"][0]
		assert exp == read_re


	def teardown_class(self):
		#回收环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw')
		for i in fun.mac:
			fun.ssh_close(i)

