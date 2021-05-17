#!/usr/bin/env python
# coding: utf-8
# @TIME : 2021/4/9 10:25
import datetime
import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_test_platform.settings')
django.setup()

from 测试计划.models import GitCase

base_dir = r'E:\Projects_Py\auto_test_0317\auto_test'


def read_case(base_dir):
    case_module = ''
    case_list = []
    rbm_dir = ''
    ssh_dir = ''
    gateway_ip = ''
    iso_ip = ''
    base_dirs = os.listdir(base_dir)
    for i in base_dirs:
        if 'common' == i:
            common_dir = base_dir + '\\' + i
            baseinfo = common_dir + '\\' + 'baseinfo.py'
            with open(baseinfo, 'r', encoding='utf-8') as f:
                for line in f:
                    if r"DeviceObject['gateway', 'manageIp'] = " in line:
                        ips1 = line.split('=')
                        ips = ips1[1].split('"')
                        print('设备ip: ', ips[1])
                        gateway_ip = ips[1]
                    elif r"BG8010['front_dut', 'manageIp'] = " in line:
                        ips1 = line.split('=')
                        ips = ips1[1].split('"')
                        print('隔离设备前置ip: ', ips[1])
                        iso_ip = ips[1]
                    elif r"BG8010['back_dut', 'manageIp'] = " in line:
                        ips1 = line.split('=')
                        ips = ips1[1].split('"')
                        print('隔离设备后置ip: ', ips[1])
                        iso_ip = iso_ip + '--' + ips[1]
        elif 'Case_rbm' in i:
            rbm_dir = base_dir + '\\' + i
            print(rbm_dir)
        elif 'Case_ssh' in i:
            ssh_dir = base_dir + '\\' + i
            print(ssh_dir)

    # SSH模块脚本
    if ssh_dir:
        ssh_dirs = os.listdir(ssh_dir)
        for i in ssh_dirs:
            if '.' not in i:  # 排除带.的文件
                case_title = i
                run_env = '【' + gateway_ip + '】'
                if i.startswith('tupleacl_'):
                    case_module = 'tupleacl'
                elif i.startswith('qos_'):
                    case_module = 'qos'
                elif i.startswith('vxlan_'):
                    case_module = 'vxlan'
                priority = '2'  # ssh模块的优先级暂时设置成2
                case_type = ' SSH '
                test_type = '功能测试'
                owner = 'lwq'
                Last_Modified = 'wq'
                Modified_date = datetime.datetime.now()
                # print(case_title + '\t' + case_type + '\t' + case_module + '\t' + priority + '\t'
                #       + run_env + '\t' + test_type + '\t' + owner + '\t' + Last_Modified + '\t'
                #       + str(Modified_date))
                if not GitCase.objects.filter(case_title=case_title):
                    case_list.append(
                        GitCase(case_title=case_title, case_type=case_type, case_module=case_module, priority=priority,
                                run_env=run_env, test_type=test_type, owner=owner, Last_Modified=Last_Modified,
                                Modified_date=Modified_date))
                else:
                    print('已存在用例：', case_title)
                    pass

    # RBM模块脚本
    if rbm_dir:
        rbm_dirs = os.listdir(rbm_dir)
        for i in rbm_dirs:
            if '.' not in i:  # 排除带.的文件
                case_title = i
                # print(case_title)
                if i.startswith('iso'):  # 以iso开头的为隔离环境下的脚本
                    run_env = '隔离【' + iso_ip + '】'
                else:
                    run_env = '网关【' + gateway_ip + '】'

                if 'http' in i:
                    case_module = 'HTTP'
                elif 'ftp' in i:
                    case_module = 'FTP'
                elif 'mail' in i:
                    case_module = 'MAIL'
                else:
                    case_module = 'other'

                priority = '1'
                case_type = ' rabbitMQ '
                test_type = '功能测试'
                owner = 'lwq'
                Last_Modified = 'wq'
                Modified_date = datetime.datetime.now()
                # print(case_title + '\t' + case_type + '\t' + case_module + '\t' + priority + '\t'
                #       + run_env + '\t' + test_type + '\t' + owner + '\t' + Last_Modified + '\t'
                #       + str(Modified_date))
                if not GitCase.objects.filter(case_title=case_title):
                    case_list.append(
                        GitCase(case_title=case_title, case_type=case_type, case_module=case_module, priority=priority,
                                run_env=run_env, test_type=test_type, owner=owner, Last_Modified=Last_Modified,
                                Modified_date=Modified_date))
                else:
                    print('已存在用例：', case_title)
                    pass

    return case_list


def import_db(case_list):
    for case in case_list:
        print(
            case.case_title + '\t' + case.case_type + '\t' + case.case_module + '\t' + case.priority + '\t'
            + case.run_env + '\t' + case.test_type + '\t' + case.owner + '\t' + case.Last_Modified + '\t'
            + str(case.Modified_date))
    GitCase.objects.bulk_create(case_list)
    print('已成功插入{}条数据'.format(len(case_list)))


def tree_case_data():
    function_rbm_http = GitCase.objects.filter(test_type='功能测试', case_type=' rabbitMQ ', case_module='HTTP',
                                               run_env__contains="网关")
    function_rbm_ftp = GitCase.objects.filter(test_type='功能测试', case_type=' rabbitMQ ', case_module='FTP',
                                              run_env__contains="网关")
    function_rbm_mail = GitCase.objects.filter(test_type='功能测试', case_type=' rabbitMQ ', case_module='MAIL',
                                               run_env__contains="网关")
    p1 = {"id": 1, "text": "function"}
    # json的第二层，rbm,ssh和接口层
    p21 = {"id": 11, "text": "rabbitMQ"}
    p22 = {"id": 12, "text": "SSH"}
    p23 = {"id": 13, "text": "interface"}
    case_type_list = []
    case_type_list.append(p21)
    case_type_list.append(p22)
    case_type_list.append(p23)
    # json的第三层，http,ftp,mail层
    # rbm下的一层
    p311 = {"id": 111, "text": "HTTP"}
    p312 = {"id": 112, "text": "FTP"}
    p313 = {"id": 113, "text": "MAIL"}
    # ssh下的一层
    # p221 = {"id": 121, "text": "vxlan"}
    # p222 = {"id": 122, "text": "tupleacl"}
    # p223 = {"id": 123, "text": "qos"}
    case_module_list = []
    case_module_list.append(p311)
    case_module_list.append(p312)
    case_module_list.append(p313)
    # json的第四层，具体用例名称
    function_rbm_http_title_list = []
    for function_rbm_http_obj in function_rbm_http:
        title_dict = {}
        title_dict['case_id'] = function_rbm_http_obj.pk
        title_dict['text'] = function_rbm_http_obj.case_title
        function_rbm_http_title_list.append(title_dict)
    # print(function_rbm_http_title_list)

    function_rbm_ftp_title_list = []
    for function_rbm_ftp_obj in function_rbm_ftp:
        title_dict = {}
        title_dict['case_id'] = function_rbm_ftp_obj.pk
        title_dict['text'] = function_rbm_ftp_obj.case_title
        function_rbm_ftp_title_list.append(title_dict)
    # print(function_rbm_http_title_list)

    function_rbm_mail_title_list = []
    for function_rbm_mail_obj in function_rbm_mail:
        title_dict = {}
        title_dict['case_id'] = function_rbm_mail_obj.pk
        title_dict['text'] = function_rbm_mail_obj.case_title
        function_rbm_mail_title_list.append(title_dict)
    # print(function_rbm_mail_title_list)
    # function_rbm_title
    p311['children'] = function_rbm_http_title_list
    p312['children'] = function_rbm_ftp_title_list
    p313['children'] = function_rbm_mail_title_list

    p21['children'] = case_module_list

    # 第一父级
    p1['children'] = case_type_list
    # 写入json文件
    json_str = json.dumps(p1, indent=2)
    json_file = 'jeasyui-tree-tree4/data/tree_test_data.json'
    with open(json_file, 'w') as json_file:
        json_file.write('[' + json_str + ']')
    # print('---------------------------------')
    # print(p311['children'])
    # print(p311)
    # print('---------------------------------')
    # print(p21['children'])
    # print(p21)
    # print('---------------------------------')
    # print(p1['children'])
    # print(p1)


if __name__ == '__main__':
    case_list = read_case(base_dir)
    import_db(case_list)
    # tree_case_data()
    # html_logs_paths = [
    #     'E:\\Projects_Py\\django_prctice\\django_test03\\auto_test\\Logs\\test1.0.0\\20210428_10-53-02\\',
    #     'E:\\Projects_Py\\django_prctice\\django_test03\\auto_test\\Logs\\test1.0.0\\20210428_10-53-29\\']
    # log_paths = []
    # for path in html_logs_paths:
    #     dirname = path.split('\\')[-2]
    #     version_dir = path.split('\\')[-3]
    #     log_path = '【' + version_dir + '\\' + dirname + '】'
    #     print('log_path: ', log_path)
    #     log_paths.append(log_path)
    # report_path = '-'.join(log_paths)
    # print('report_path: ', report_path)
