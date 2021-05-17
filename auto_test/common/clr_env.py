# coding:utf-8
import time

from common import baseinfo
from common import fun
from common import message

rbmDomain = baseinfo.rbmDomain
FrontDomain = baseinfo.BG8010FrontDomain
BackDomain = baseinfo.BG8010BackDomain
proxy_ip = baseinfo.BG8010FrontOpeIp
rbmExc = baseinfo.rbmExc

card_list = [0]


def clear_env(dut='gw'):
    start = time.time()
    clear_env = []
    env_list = [
        "switch-jsac --set --switch on",
        'switch-jsac --set --module 12 --switch off',
        'switch-jsac --set --module 13 --switch off',
        'switch-jsac --set --module 15 --switch off',
        'switch-jsac --set --module 16 --switch off',
        "defconf  --action forward",
        "defconf --selabel on",
        "defconf --cycle 15",
        "defconf --ipv4aclcycle 30",
        'defconf --domain off',
        'defconf --netflow off',
        'defconf --ipv4acl off',
        'defconf --syncookie off',
        'defconf --ckoption off',
        'defconf --noflow off',
        'defconf --droperr off',
        'defconf --tcpmss 0'
    ]

    for i in card_list:
        for j in env_list:
            cmd = f'export cardid={i}&&{j}'
            clear_env.append(cmd)
    for i in clear_env:
        print(i)
        dd = fun.cmd(i, dut)
        print(dd)
    print("=========================== clear_env 结束 耗时：{}s ==================================".format(
        time.time() - start))


def clear_met_acl(dut='gw'):
    start = time.time()
    clear_met = []

    met_list = [
        "tupleacl --clear",
        "selabel --clear",
        "qos-jsac --clear"
    ]

    for i in card_list:
        for j in met_list:
            cmd = f'export cardid={i}&&{j}'
            clear_met.append(cmd)
    for i in clear_met:
        print(i)
        dd = fun.cmd(i, dut)
        print(dd)
    print("=========================== clear_met_acl 结束 耗时：{}s ==================================".format(
        time.time() - start))


def data_check_setup_met(dut='gw'):
    start = time.time()
    fun.wait_data('ps -ef |grep agentjsac', dut, '/usr/bin/agentjsac -c /etc/jsac/agentjsac.config')
    fun.nginx_worker('ps -ef |grep nginx', dut, 'nginx: worker process')
    print("=========================== data_check_setup_met 结束 耗时：{}s ==================================".format(
        time.time() - start))


def data_check_teardown_met(protocol, base_path, dut='gw'):
    start = time.time()
    if protocol == 'mail':
        fun.send(rbmExc, message.delsmtp['DelAgent'], rbmDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', dut, 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', dut, 'nginx: worker process')
        fun.send(rbmExc, message.delpop3['DelAgent'], rbmDomain, base_path)
    elif protocol == 'ftp':
        fun.send(rbmExc, message.delftp['DelAgent'], rbmDomain, base_path)
    elif protocol == 'http':
        fun.send(rbmExc, message.delhttp['DelAgent'], rbmDomain, base_path)
    else:
        pass
    fun.wait_data('ps -ef |grep nginx', dut, 'nginx: worker process')
    fun.nginx_worker('ps -ef |grep nginx', dut, 'nginx: worker process')
    print("=========================== data_check_teardown_met 结束 耗时：{}s ==================================".format(
        time.time() - start))

def iso_setup_class(dut):
    start = time.time()
    fun.wait_data('ps -ef |grep jsac', dut, 'jsac_master')
    for i in range(4):
        fun.wait_data('ps -ef |grep jsac', dut, f'jsac_worker{i}')
    print("=========================== 设备{}iso_setup_class 结束 耗时：{}s ==================================".format(dut, (time.time() - start)))


def iso_teardown_met(protocol, base_path):
    start = time.time()
    if protocol == 'mail':
        fun.send(rbmExc, message.delsmtp_front['DelCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.delsmtp_back['DelCustomAppPolicy'], BackDomain, base_path)
        fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
        fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
        fun.send(rbmExc, message.delpop3_front['DelCustomAppPolicy'], FrontDomain, base_path)
        fun.send(rbmExc, message.delpop3_back['DelCustomAppPolicy'], BackDomain, base_path)
    elif protocol == 'ftp':
        fun.send(rbmExc, message.delftp['DelAgent'], rbmDomain, base_path)
    elif protocol == 'http':
        fun.send(rbmExc, message.delhttp['DelAgent'], rbmDomain, base_path)
    else:
        pass
    fun.wait_data('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
    fun.nginx_worker('ps -ef |grep nginx', 'FrontDut', 'nginx: worker process')
    fun.wait_data('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
    fun.nginx_worker('ps -ef |grep nginx', 'BackDut', 'nginx: worker process')
    print("=========================== data_check_teardown_met 结束 耗时：{}s ==================================".format(
        time.time() - start))
