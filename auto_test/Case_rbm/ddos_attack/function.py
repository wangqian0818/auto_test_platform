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
	from ddos_attack import index
	from ddos_attack import message
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
domain_rmb=baseinfo.rbmDomain
Exc_rmb=baseinfo.rbmExc
port_d=index.dport
port_attack=index.attack_port

class Test_ddos_attack():

	def setup_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

	def teardown_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

		fun.pid_kill(self.cap_pcap1,'pyhton','s')
		fun.pid_kill(self.hping3_1,'hping3','c')
		fun.pid_kill(self.http_1,'python2.7','s')
		fun.pid_kill(self.cap_pcap2, 'pyhton', 's')
		fun.pid_kill(self.hping3_2, 'hping3', 'c')
		fun.pid_kill(self.http_2, 'python2.7', 's')
		fun.pid_kill(self.cap_pcap3, 'pyhton', 's')
		fun.pid_kill(self.hping3_3, 'hping3', 'c')
		fun.pid_kill(self.http_3, 'python2.7', 's')
		fun.pid_kill(self.cap_pcap4, 'pyhton', 's')
		fun.pid_kill(self.hping3_4, 'hping3', 'c')
		fun.pid_kill(self.http_4, 'python2.7', 's')


	def setup_class(self):
		#获取参数
		fun.ssh_gw.connect()
		#fun.rbm.connect()
		fun.ssh_c.connect()
		fun.ssh_s.connect()
		self.clr_env = clr_env.clear_env
		self.case1_step = index.case1_step
		self.pkt1_cfg = index.pkt1_cfg
		self.pkt2_cfg = index.pkt2_cfg
		self.pkt3_cfg = index.pkt3_cfg
		self.pkt4_cfg = index.pkt4_cfg
		self.cap_pcap1 = self.pkt1_cfg["capture"][3]
		self.cap_pcap2 = self.pkt2_cfg["capture"][3]
		self.cap_pcap3 = self.pkt3_cfg["capture"][3]
		self.cap_pcap4 = self.pkt4_cfg["capture"][3]
		self.hping3_1 = self.pkt1_cfg["hping3"][0]
		self.hping3_2 = self.pkt2_cfg["hping3"][0]
		self.hping3_3 = self.pkt3_cfg["hping3"][0]
		self.hping3_4 = self.pkt4_cfg["hping3"][0]
		self.http_1 = self.pkt1_cfg["http"][0]
		self.http_2 = self.pkt2_cfg["http"][0]
		self.http_3 = self.pkt3_cfg["http"][0]
		self.http_4 = self.pkt4_cfg["http"][0]
		self.read_1 = self.pkt1_cfg["read"][0]
		self.read_2 = self.pkt2_cfg["read"][0]
		self.read_3 = self.pkt3_cfg["read"][0]
		self.read_4 = self.pkt4_cfg["read"][0]



		for i in self.clr_env:
			print(i)
			dd=fun.cmd(i,'gw')
			print(dd)

	#@pytest.mark.skip(reseason="skip")
	@allure.feature('边界保护系统开启DDoS防御，RST FLOOD攻击测试')
	def test_ddos_rst_flood(self):

		# 下发配置并检查结果
		fun.send(Exc_rmb,message.setddos_open['SetDdosEnable'], domain_rmb, base_path)
		for key in self.case1_step:
			re0 = fun.cmd(self.case1_step[key][0], 'gw')
			re1 = fun.cmd(self.case1_step[key][1], 'gw')
			assert self.case1_step[key][2] in re0
			assert self.case1_step[key][2] in re1

		# 服务端抓取报文
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt1_cfg['capture'][0], self.pkt1_cfg['capture'][1], \
												   self.pkt1_cfg['capture'][2], self.pkt1_cfg['capture'][3]
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 服务端开启http服务
		fun.cmd(f"python2.7 -m  SimpleHTTPServer {port_d}",'s',thread=1)

		# 客户端发送攻击命令
		fun.cmd(f"hping3 -i u1000 -R -p {port_attack} {pcap_dip} --rand-source --tcp-timestamp", 'c', thread=1)
		fun_result = fun.cmd('ps -ef | grep hping3', 'c')
		print(fun_result)

		# 检查hping3命令是否发送成功
		assert self.pkt1_cfg["hping3"][0] in fun_result
		print('hping3攻击命令下发成功')
		# if self.pkt1_cfg["hping3"][0] in fun_result:
		# 	print('hping3攻击命令下发成功')
		# else:
		# 	print('!!!hping3攻击命令下发失败!!!')
		# 	exit()

		# 客户端发送http请求
		fun.cmd(f"curl http://{pcap_dip}:{port_d}", 'c', thread=1)
		time.sleep(5)

		# 检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file
		print('服务端抓到报文：{}'.format(self.read_1))



	#@pytest.mark.skip(reseason="skip")
	@allure.feature('边界保护系统开启DDoS防御，FIN FLOOD攻击测试')
	def test_ddos_fin_flood(self):

		# 下发配置并检查结果
		fun.send(Exc_rmb, message.setddos_open['SetDdosEnable'], domain_rmb, base_path)
		for key in self.case1_step:
			re0 = fun.cmd(self.case1_step[key][0], 'gw')
			re1 = fun.cmd(self.case1_step[key][1], 'gw')
			assert self.case1_step[key][2] in re0
			assert self.case1_step[key][2] in re1

		# 服务端抓取报文
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt2_cfg['capture'][0], self.pkt2_cfg['capture'][1], \
													   self.pkt2_cfg['capture'][2], self.pkt2_cfg['capture'][3]
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 服务端开启http服务
		fun.cmd(f"python2.7 -m  SimpleHTTPServer {port_d}", 's', thread=1)

		# 客户端发送攻击命令
		fun.cmd(f"hping3 -i u1000 -F -A -p {port_attack} {pcap_dip} --rand-source --tcp-timestamp", 'c', thread=1)
		fun_result = fun.cmd('ps -ef | grep hping3', 'c')
		print(fun_result)

		# 检查hping3命令是否发送成功
		assert self.pkt2_cfg["hping3"][0] in fun_result
		print('hping3攻击命令下发成功')
		# if self.pkt2_cfg["hping3"][0] in fun_result:
		# 	print('hping3攻击命令下发成功')
		# else:
		# 	print('!!!hping3攻击命令下发失败!!!')
		# 	exit()

		# 客户端发送http请求
		fun.cmd(f"curl http://{pcap_dip}:{port_d}", 'c', thread=1)
		time.sleep(5)

		# 检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file
		print('服务端抓到报文：{}'.format(self.read_2))



	#@pytest.mark.skip(reseason="skip")
	@allure.feature('边界保护系统开启DDoS防御，ACK FLOOD攻击测试')
	def test_ddos_ack_flood(self):

		# 下发配置并检查结果
		fun.send(Exc_rmb, message.setddos_open['SetDdosEnable'], domain_rmb, base_path)
		for key in self.case1_step:
			re0 = fun.cmd(self.case1_step[key][0], 'gw')
			re1 = fun.cmd(self.case1_step[key][1], 'gw')
			assert self.case1_step[key][2] in re0
			assert self.case1_step[key][2] in re1

		# 服务端抓取报文
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt3_cfg['capture'][0], self.pkt3_cfg['capture'][1], \
												   self.pkt3_cfg['capture'][2], self.pkt3_cfg['capture'][3]
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 服务端开启http服务
		fun.cmd(f"python2.7 -m  SimpleHTTPServer {port_d}", 's', thread=1)

		# 客户端发送攻击命令
		fun.cmd(f"hping3 -i u1000 -A -p {port_attack} {pcap_dip} --rand-source --tcp-timestamp", 'c', thread=1)
		fun_result = fun.cmd('ps -ef | grep hping3', 'c')
		print(fun_result)

		# 检查hping3命令是否发送成功
		assert self.pkt3_cfg["hping3"][0] in fun_result
		print('hping3攻击命令下发成功')
		# if self.pkt3_cfg["hping3"][0] in fun_result:
		# 	print('hping3攻击命令下发成功')
		# else:
		# 	print('!!!hping3攻击命令下发失败!!!')
		# 	exit()

		# 客户端发送http请求
		fun.cmd(f"curl http://{pcap_dip}:{port_d}", 'c', thread=1)
		time.sleep(5)

		# 检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file
		print('服务端抓到报文：{}'.format(self.read_3))



	#@pytest.mark.skip(reseason="skip")
	@allure.feature('边界保护系统开启DDoS防御，SYN-ACK FLOOD攻击测试')
	def test_ddos_syn_ack_flood(self):

		# 下发配置并检查结果
		fun.send(Exc_rmb, message.setddos_open['SetDdosEnable'], domain_rmb, base_path)
		for key in self.case1_step:
			re0 = fun.cmd(self.case1_step[key][0], 'gw')
			re1 = fun.cmd(self.case1_step[key][1], 'gw')
			assert self.case1_step[key][2] in re0
			assert self.case1_step[key][2] in re1

		# 服务端抓取报文
		cap_iface, cap_filter, cap_num, cap_pcap = self.pkt4_cfg['capture'][0], self.pkt4_cfg['capture'][1], \
												   self.pkt4_cfg['capture'][2], self.pkt4_cfg['capture'][3]
		pre_cfg = fun.pkt_capture(cap_iface, cap_filter, cap_num, cap_pcap)
		fun.cmd(pre_cfg, 's', thread=1)
		print('step wait')
		time.sleep(20)

		# 服务端开启http服务
		fun.cmd(f"python2.7 -m  SimpleHTTPServer {port_d}", 's', thread=1)

		# 客户端发送攻击命令
		fun.cmd(f"hping3 -i u1000 -SA -p {port_attack} {pcap_dip} --rand-source --tcp-timestamp", 'c', thread=1)
		fun_result = fun.cmd('ps -ef | grep hping3', 'c')
		print(fun_result)

		# 检查hping3命令是否发送成功
		assert self.pkt4_cfg["hping3"][0] in fun_result
		print('hping3攻击命令下发成功')
		# if self.pkt4_cfg["hping3"][0] in fun_result:
		# 	print('hping3攻击命令下发成功')
		# else:
		# 	print('!!!hping3攻击命令下发失败!!!')
		# 	exit()

		# 客户端发送http请求
		fun.cmd(f"curl http://{pcap_dip}:{port_d}", 'c', thread=1)
		time.sleep(5)

		# 检查报文是否存在
		pcap_file = fun.search('/opt/pkt', 'pcap', 's')
		assert cap_pcap in pcap_file
		print('服务端抓到报文：{}'.format(self.read_4))



	def teardown_class(self):
		#回收环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw')
		for i in fun.mac:
			fun.ssh_close(i)

		fun.rbm_close()