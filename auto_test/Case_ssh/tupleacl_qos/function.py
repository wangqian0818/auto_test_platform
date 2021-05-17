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
	import index
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
qos_port = baseinfo.qos_port

class Test_acl_qos():

	def setup_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')

	def teardown_method(self):
		self.clr_met = clr_env.clear_met

		for i in self.clr_met:
			fun.cmd(i, 'gw')
		fun.iperf_kill()

	def setup_class(self):
		# 获取参数
		fun.ssh_gw.connect()
		fun.ssh_c.connect()
		fun.ssh_s.connect()
		self.clr_env = clr_env.clear_env
		self.case1_step = index.case1_step
		self.case2_step = index.case2_step

		for i in self.clr_env:
			print(i)
			dd = fun.cmd(i, 'gw')
			print(dd)

	# @pytest.mark.skip(reseason="skip")
	@allure.feature('验证ACL的上下行限速功能，多桶')
	def test_acl_qos_a1(self):

		#初始化
		fun.iperf_kill()

		#下发配置并检查结果
		for key in self.case1_step:
			fun.cmd(self.case1_step[key][0],'gw')
			re=fun.cmd(self.case1_step[key][1],'gw')
			assert self.case1_step[key][2] in re

		# 服务端占用端口
		fun.cmd(f'iperf3 -s -p {qos_port} --logfile s.txt', 's', thread=1)
		time.sleep(5)

		# 发送报文
		c_cmd = fun.cmd(f'iperf3 -c {pcap_dip} -p {qos_port} -i 1 -u -t 5 -b 30M -P 5', 'c')
		print(c_cmd)

		# 检查速率是否正确
		s_txt = fun.cmd('cat s.txt', 's')
		speed_list = fun.qos_speed('s.txt',s_txt)
		for i in speed_list:
			print(i)
			assert 9.0 <= float(i) <= 10.0

	# @pytest.mark.skip(reseason="skip")
	@allure.feature('关闭selabel开关再开启，验证ACL限速情况')
	def test_acl_qos_a2(self):

		# 初始化
		fun.iperf_kill()

		# 下发配置并检查结果
		for key in self.case2_step:
			fun.cmd(self.case2_step[key][0], 'gw')
			re = fun.cmd(self.case2_step[key][1], 'gw')
			assert self.case2_step[key][2] in re

		# 服务端占用端口
		fun.cmd(f'iperf3 -s -p {qos_port} --logfile s.txt', 's', thread=1)
		time.sleep(5)

		# 发送报文
		c_cmd = fun.cmd(f'iperf3 -c {pcap_dip} -p {qos_port} -i 1 -u -t 5 -b 30M -P 5', 'c')
		print(c_cmd)

		# 检查速率是否正确
		s_txt = fun.cmd('cat s.txt', 's')
		speed_list = fun.qos_speed('s.txt', s_txt)
		for i in speed_list:
			print(i)
			assert 9.0 <= float(i) <= 10.0

		#关闭selabel开关再开启
		fun.cmd('export cardid=0&&defconf --selabel off', 'gw')
		fun.cmd('export cardid=1&&defconf --selabel off', 'gw')
		fun.iperf_kill()
		fun.cmd('export cardid=0&&defconf --selabel on', 'gw')
		fun.cmd('export cardid=1&&defconf --selabel on', 'gw')

		# 服务端占用端口
		fun.cmd(f'iperf3 -s -p {qos_port} --logfile s.txt', 's', thread=1)
		time.sleep(5)

		# 发送报文
		c_cmd = fun.cmd(f'iperf3 -c {pcap_dip} -p {qos_port} -i 1 -u -t 5 -b 30M -P 5', 'c')
		print(c_cmd)

		# 检查速率是否正确
		s_txt = fun.cmd('cat s.txt', 's')
		speed_list = fun.qos_speed('s.txt', s_txt)
		for i in speed_list:
			print(i)
			assert 9.0 <= float(i) <= 10.0

	def teardown_class(self):
		#回收环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw')
		for i in fun.mac:
			fun.ssh_close(i)

