# encoding='utf-8'
try:
    import os, sys, time
except Exception as err:
    print('导入CPython内置函数库失败!错误信息如下:')
    print(err)
    sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 获取当前项目文件夹
base_path = base_path.replace('\\', '/')
sys.path.insert(0, base_path)  # 将当前目录添加到系统环境变量,方便下面导入版本配置等文件
try:
    import common.pcap as c_pacp
    import common.rabbitmq as c_rbm
    import common.ssh1 as c_ssh
    import common.baseinfo as info
except Exception as err:
    print(
        '导入基础函数库失败!请检查相关文件是否存在.\n文件位于: ' + str(base_path) + '/common/ 目录下.\n分别为:pcap.py  rabbitmq.py  ssh.py\n错误信息如下:')
    print(err)
    sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
else:
    del sys.path[0]  # 及时删除导入的环境变量,避免重复导入造成的异常错误

pcap_sip = info.clientOpeIp
pcap_dip = info.serverOpeIp
qos_port = info.qos_port

ssh_gw = c_ssh.ssh(info.gwManageIp, info.gwUser, info.gwPwd)
ssh_c = c_ssh.ssh(info.clientIp, info.clientUser, info.clientPwd)
ssh_s = c_ssh.ssh(info.serverIp, info.serverUser, info.serverPwd)
rbm = c_rbm.rabbitmq(info.rbmIp, info.rbmWebUser, info.rbmWebPwd, base_path)
ssh_FrontDut = c_ssh.ssh(info.BG8010FrontIp, info.BG8010FrontUser, info.BG8010FrontPwd)
ssh_BackDut = c_ssh.ssh(info.BG8010BackIp, info.BG8010BackUser, info.BG8010BackPwd)
ssh_BG8010Client = c_ssh.ssh(info.BG8010ClientIp, info.BG8010ClientUser, info.BG8010ClientPwd)
ssh_BG8010Server = c_ssh.ssh(info.BG8010ServerIp, info.BG8010ServerUser, info.BG8010ServerPwd)
# ssh_gw.connect()
# ssh_c.connect()
# ssh_s.connect()
print('base_path: ' + str(base_path))
# rbm.connect()
# mac=['gw']
mac = ['gw', 'c', 's', 'gw2', 'FrontDut', 'BackDut', 'ssh_BG8010Client', 'ssh_BG8010Server']


def cmd(cmd='', domain='', thread=0, timeout=None):  # cmd执行函数
    if not cmd:
        print('请输入cmd指令!')
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    if domain not in mac:
        print('请输入有效的ssh主机代号!')
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    ssh_name = 'ssh_' + str(domain)
    fun_cmd = globals()[ssh_name].cmd(cmd, thread, timeout)
    print(' ------------ fun_{}:{}'.format(cmd, fun_cmd))
    print(' ------------ fun_{} ------------ '.format(cmd))
    return fun_cmd  # 调用globals()把文本名变成object对象


def ssh_close(domain=1):  # ssh连接关闭
    if domain not in mac:
        print('请输入有效的ssh主机代号!')
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    ssh_name = 'ssh_' + str(domain)
    return globals()[ssh_name].close()  # 调用globals()把文本名变成object对象


def search(path, end, domain=1):  # 查找文件
    if domain not in mac:
        print('请输入有效的ssh主机代号!')
        sys.exit(0)
    ssh_name = 'ssh_' + str(domain)
    return globals()[ssh_name].search(path, end)


# 从远程服务器读取文件到本地
def read(path='', fun='read', mode='r', text='', domain=1):
    if domain not in mac:
        print('请输入有效的ssh主机代号!')
        sys.exit(0)
    ssh_name = 'ssh_' + str(domain)
    return globals()[ssh_name].open(path, fun, mode, text)


def send(exc, method, domain, path):  # 向Rabbitmq发送信息
    if (not exc) or (not method) or (not domain):
        print('请输入有效的Rabbitmq发送信息参数!')
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    rbm.send(exc, method, domain, path)


def rbm_close():  # 关闭Rabbitmq连接
    rbm.close()


def pkt_capture(iface, filter_, num, pkt_name):  # 开启抓包，只获取命令，不运行
    capture_pkt = "python3 /opt/pkt/sniff.py %s %s %d /opt/pkt/%s" % (iface, filter_, num, pkt_name)
    # capture_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/sniff.py %s %s %d %s'%(iface, filter_, num, pkt_name))
    return capture_pkt


def pkt_send(iface, num, pkt_name):  # 发包命令
    # proto=pkt_name.split('__')
    # send_pkt="tcpreplay -i %s -l %d /opt/pkt/%s/%s"%(iface,num,proto,pkt_name)
    send_pkt = "tcpreplay -i %s -l %d /opt/pkt/%s" % (iface, num, pkt_name)
    return send_pkt


def pkt_read(pkt_name, pkt_id):  # 解析报文，返回标记字段，只获取命令，不运行
    read_pkt = "python3 /opt/pkt/read.py /opt/pkt/%s %d" % (pkt_name, pkt_id)
    # read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
    return read_pkt


def mss_read(pkt_name, pkt_id):  # 解析报文，返回标记字段，只获取命令，不运行
    read_mss = "python3 /opt/pkt/read_mss.py /opt/pkt/%s %d" % (pkt_name, pkt_id)
    # read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
    return read_mss


def vxlan_read(pkt_name, pkt_id):  # 解析报文，返回标记字段，只获取命令，不运行
    read_vxlan = "python3 /opt/pkt/read_vxlan.py /opt/pkt/%s %d" % (pkt_name, pkt_id)
    # read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
    return read_vxlan


# def pid_kill(cap_pcap):
# 	# 判断抓包程序是否停止，如果进程还在则停止
# 	pid = cmd(f'ps -ef | grep python | grep {pcap_dip}', 's')
# 	print(pid)
# 	if (cap_pcap in pid):
# 		# 获取进程ID
# 		pid = pid.split()[1]
# 		print(pid)
# 		cmd("kill -9 %s" % pid, "s")

def pid_kill(content, process='python', gw='s'):
    # 判断抓包程序是否停止，如果进程还在则停止
    cmd1 = f'ps -ef | grep {process}'
    if process == 'python':
        cmd1 = f'ps -ef | grep {process} | grep {pcap_dip} | grep {content}'
    while True:
        a = cmd(cmd1, gw)
        print('pid_kill_a: ', a)
        if content in a:
            # 获取进程ID
            kpid = a.split()[1]
            print('kpid: ', kpid)
            cmd("kill -9 %s" % kpid, gw)
        else:
            break


def iperf_kill():
    # 判断抓包程序是否停止，如果进程还在则停止
    pid = cmd(f'ps -ef | grep iperf3 | grep {qos_port}', 's')
    print(pid)
    if ('iperf3' in pid):
        # 获取进程ID
        pid = pid.split()[1]
        print(pid)
        cmd("kill -9 %s" % pid, "s")


def cipso_category(a, b):
    value = ''
    for i in range(a, b):
        value = value + ' ' + str(i)
        if i == b - 1:
            return value


def pkt_scp(scp_name, scp_dip):  # 上传命令
    scp_pkt = f"sshpass -p {info.serverPwd} scp /opt/pkt/%s root@%s:/opt/pkt" % (scp_name, scp_dip)
    return scp_pkt


def pkt_wget(wget_name, wget_dip):
    wget_pkt = "wget %s /opt/pkt/%s" % (wget_name, wget_dip)
    return wget_pkt


def qos_speed(file, s_txt, qbucket='p'):
    with open(file, 'w') as f:
        f.write(s_txt)

    result = []
    with open(file, 'r') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))

    if qbucket == 'p':
        result1 = result[-24:-28]
        speed_list = []
        for i in result1:
            str_i = str(i)
            p_speed = str_i.split()[6]
            speed_list.append(p_speed)
            print(speed_list)
        return speed_list
    elif qbucket == 's':
        result1 = str(result[-30])
        s_speed = result1.split()[5]
        return s_speed


def wait_data(command, device, context, name='进程', number=300, timeout=0.1, flag='存在'):
    print('当前时间为{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    a = cmd(command, device)
    tmp = 0
    # time.sleep(2)
    print('wait_data_command: ', command)
    print('wait_data_device: ', device)
    print('wait_data_context: ', context)
    print('wait_data_a0: ', a)
    if flag == '存在':
        while a is None or context not in a:
            if tmp < number:
                time.sleep(timeout)
                tmp += 1
                print('这是{}的第{}次等待'.format(name, tmp))
                a = cmd(command, device)
                print(a)
            else:
                print('{}检查结果失败'.format(name))
                return 0
    else:
        while context in a:
            if tmp < number:
                print(a)
                time.sleep(timeout)
                tmp += 1
                print('这是{}的第{}次等待'.format(name, tmp))
                a = cmd(command, device)
            else:
                print('{}检查结果失败'.format(name))
                return 0
    return a


def nginx_worker(command, device, context, non_context='nginx: worker process is shutting down', name='进程', number=300,
                 timeout=0.1):
    time.sleep(5)
    print('当前时间为{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    tmp = 0
    num = 0
    while num != 24:
        if tmp < number:
            num = 0  # 每次循环，进程数需重新置为0
            time.sleep(timeout)
            tmp += 1
            print('这是{}的第{}次等待'.format(name, tmp))
            a = cmd(command, device)
            print('wait_data_command: ', command)
            print('wait_data_device: ', device)
            print('wait_data_context: ', context)
            print('wait_data_non_context: ', non_context)
            if a is not None:
                a = a.split('\n')
                print('nginx_worker_a: ', a)
                for i in a:
                    if context in i and non_context not in i:
                        num += 1
                print('当前有{}个{}启动成功'.format(num, name))
                if num == 24:
                    print('{}个{}全部启动成功'.format(num, name))
                    break
        else:
            print('{}启动失败'.format(name))
            break
