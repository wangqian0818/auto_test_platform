#!/usr/bin/env python
# coding: utf-8
# @TIME : 2021/3/18 14:24
from time import sleep

import paramiko


# 定义一个类，表示一台ssh连接远端linux主机
class ssh():
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, port=22, timeout=30):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, self.port))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()  # 打开一个通道
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()  # 获取终端
                self.chan.invoke_shell()  # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
                # 如果没有抛出异常说明连接成功，直接返回
                print(u'连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                # print(self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception:
                if self.try_times != 0:
                    print(u'连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试3次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def cmd(self, cmd='', thread=0, timeout=None):
        cmd += '\r'
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            sleep(0.5)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            print(result)
            return result


# 测试linux类代码
if __name__ == '__main__':
    ssh = ssh()
    ssh.connect()
    ssh.send('ps -ef | grep nginx')
    ssh.send('who')
    ssh.close()
