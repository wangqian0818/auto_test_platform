# encoding='utf-8'
'''
allure支持的定制形式如下:
Feature: 标注主要功能模块
Story: 标注Features功能模块下的分支功能
Severity: 标注测试用例的重要级别
Step: 标注测试用例的重要步骤
Issue和TestCase: 标注Issue、Case，可加入URL
attach: 标注增加附件
Environment: 标注环境Environment字段
本程序对单元测试例下的函数测试定制,强制要求使用Story定制,否则会导致程序程序出现逻辑复杂,不便于阅读以及后期维护
'''

import time

# from common import baseinfo

try:
    import os, sys, json, shutil, pytest, allure
except Exception as err:
    msg = '''
	第三方库导入失败!
	如果提示pytest库不存在,请执行:sudo pip3 install pytest 安装pytest库
	如果提示allure库不存在,请执行:sudo pip3 install allure-pytest 安装allure库
	错误信息如下:'''
    print(msg)
    print(err)
    sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序


def main(cirNum=1):
    '''
    为了便于区分单元测试例与测试总目录,强制要求,单元测试总目录以大写字母开头:Case
    如果python的执行目录不是当前目录,递归查找的时候,容易出现异常错误,避免出现异常,写死查找路径
    '''
    base_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前项目文件夹
    base_path = base_path.replace('\\', '/')
    sys.path.insert(0, base_path)  # 将当前目录添加到系统环境变量,方便下面导入版本配置等文件

    try:  # 导入版本配置等文件
        import common.baseinfo as info
        import common.email_send as email_s
    except Exception as err:
        print('版本配置文件导入失败!请检查: ' + base_path + '/common/baseinfo.py 文件是否存在.\n错误信息如下:')
        print(err)
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    else:
        del sys.path[0]  # 及时删除导入的环境变量,避免重复导入造成的异常错误
        try:
            version = info.version  # 获取版本号
            controlIp = info.controlIp
            mode = info.mode  # 获取测试模式，ssh还是rabbitmq等等
            print(version)
        # print(clientIp)
        except Exception as err:
            print('版本号获取失败!请检查是否设置了版本号.错误信息如下:')
            print(err)
            sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

    try:
        with open(base_path + '/common/caseselect_' + str(mode) + '.py', 'r', encoding='utf-8') as f:  # 读取选取的单元测试例
            case = json.loads(f.read())
    except Exception as err:
        print('读取单元测试例文件失败!请检查文件: ' + str(base_path + '/common/caseselect_' + str(mode) + '.py') + ' 是否存在.\n错误信息如下:')
        print(err)
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

    if not isinstance(case, dict):  # 判断单元测试例选择文件是否是字典形式,是的话就继续执行
        msg = '''被选择的单元测试例的文件格式为:\n{"case1":['Story1','Story2'],"case2":['Story2','Story3']}'''
        print(msg + '\n		单元测试例选择文件位于: ' + base_path + '/common/caseselect_' + str(mode) + '.py')
        sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
    else:
        try:
            case_name = case.keys()  # 获取所有的单元测试例文件目录
            print('-----------------------')
            print(case_name)
        except Exception as err:
            print('单元测试例文件读取成功,但单元测试例目录读取失败!请检查单元测试例命名格式是否有误.\n单元测试例选择文件位于: ' + base_path + '/common/caseselect_' + str(
                mode) + '.py')
            sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

    case_list = ''  # 定义单元测试例文件夹保存变量
    for i in case_name:  # 判断所选择的单元测试例目录是否真实存在,如果不存在就直接报错,结束程序运行
        print('--------------', i)
        if os.path.exists(base_path + '/Case_' + str(mode) + '/' + str(i) + '/function.py'):
            case_list = case_list + base_path + '/Case_' + str(mode) + '/' + str(i) + '/function.py' + ' '
        else:
            print('单元测试例目录: ' + str(i) + ' 不存在!请检查后重试.')
            sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

    # cirStr = input("请输入循环次数（非零正整数）：")
    try:
        if not isinstance(cirNum, int) or 0 >= cirNum:
            print("程序友好退出，请输入整数。")
            sys.exit(0)
    except Exception as err:
        print("程序友好退出，请输入整数({})".format(err))
        sys.exit(0)
    print('循环{}次'.format(cirNum))
    log_dirs = []  # 此次循环产生的日志路径
    exist_faileds = []  # 存在failed的case文件夹名称
    for num in range(cirNum):
        print('================================== 开始第{}次循环 =================================='.format(num + 1))
        # 验证并创建log保存目录
        current_time = time.strftime('%Y%m%d_%H-%M-%S', time.localtime(time.time()))
        if not os.path.exists(base_path + '/Logs/' + str(version) + '/' + current_time):  # 如果保存当前版本的logs目录不存在,就创建
            try:
                os.makedirs(base_path + '/Logs/' + str(version) + '/' + current_time)
            except Exception as err:
                print('保存当前版本的Logs目录创建失败!请检查文件夹是否有操作权限.\n错误信息如下:')
                print(err)
                sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
        else:  # 如果logs目录已存在
            msg = '''当前版本测试例的Logs目录已存在,继续运行将删除已存在的Logs文件\n是否继续运行?继续运行请输入y\n输入其他任何字符都将直接结束程序运行'''
            msg = input(msg)
            msg = msg.strip()
            if msg.lower() == 'y':
                try:
                    shutil.rmtree(base_path + '/Logs/' + str(version) + '/' + current_time)  # 删除当前logs目录
                    os.makedirs(base_path + '/Logs/' + str(version) + '/' + current_time)
                except Exception as err:
                    print('保存当前版本的Logs目录创建失败!请检查文件夹是否有操作权限.\n错误信息如下:')
                    print(err)
                    sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
            else:
                print('已选择结束程序运行!如需查看已存在的Logs文件,请进入: ' + base_path + '/Logs/' + str(version) + ' 目录查看对应的Log文件')
                sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
        try:
            try:
                list = str(case_list).strip().split(" ")
                left = '['
                right = ']'
                mid = '-'
                log_name = mid + left + info.gwManageIp + right + mid + left
                result_file = base_path + '/Logs/' + str(version) + '/result_temp.txt'

                # 清空文件： result_temp.txt
                with open(result_file, 'w') as f1:
                    f1.seek(0)
                    f1.truncate()
                for i in list:
                    file = open(result_file, 'a+')
                    file.write("\n--------------------- 开始执行 case：%s" % i)
                    file.flush()
                    c = i.split("/")[-2]
                    log = left + c + right + log_name + time.strftime('%Y%m%d_%H-%M-%S',
                                                                      time.localtime(time.time())) + right
                    abs_path = os.path.dirname(os.path.abspath(__file__))
                    # print('abs_path: ', abs_path)
                    os.system('pytest ' + i + ' --html=' + abs_path + '/Logs/' + str(
                        version) + '/' + current_time + '/' + log + '.html --self-contained-html')
                    file.write("\n--------------------- 执行结束 case：%s\n\n\n" % i)
                    file.flush()

                    # 读取执行结果文件，更改文件名
                    result = get_result(result_file, i)
                    log_dir = abs_path + '\\Logs\\' + str(version) + '\\' + current_time + '\\'
                    src_log = log_dir + log + '.html'
                    des_log = log_dir + log + result + '.html'
                    os.rename(src_log, des_log)

                log_dirs.append(log_dir)
                print('当前第{}次循环生成的报告文件夹名为：{}'.format(cirNum, log_dir))
                print('log_dirs：{}'.format(log_dirs))
                if 'failed' in result:
                    exist_faileds.append(current_time)

                print('###################################################')
            except Exception as err1:
                print('执行Pytest测试失败!错误信息如下:')
                print(err1)
                sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
        except Exception as error:
            print('pytest测试调用失败!错误内容如下:')
            print(error)
            sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

    print('自动化测试完成！')
    if 0 != len(log_dirs):
        # print("日志路径为：", log_dirs)
        if 0 == len(exist_faileds):
            print('========================== 恭喜，此次循环执行用例{}次，全部成功！！！棒棒~'.format(cirNum))
        else:
            print('========================== 此次循环执行用例{}次，存在失败的用例，如下: \n{}'.format(cirNum, exist_faileds))
        return log_dirs
    else:
        print("========================== 日志路径不存在，测试报告尚未生成 ========================== ")
        return None


# 读取执行结果文件，将执行结果追加到日志文件名
def get_result(result_file, case_path):
    file = open(result_file, 'r')
    lines = file.read().split('\n')
    str1 = '开始执行 case：' + case_path
    str2 = '执行结束 case：' + case_path
    start_index = 0
    end_index = 0
    for i in range(len(lines)):
        if str1 in lines[i]:
            start_index = i
        elif str2 in lines[i]:
            end_index = i
    result_list = []
    for i in range(len(lines)):
        if i > start_index and i < end_index:
            result_list.append(lines[i])
    # 统计总的成功失败次数
    # pass_num = 0
    # skip_num = 0
    # fail_num = 0
    # print("-------------result_list:",result_list)
    # for i in result_list:
    #     if 'passed' in i:
    #         pass_num += 1
    #     if 'skipped' in i:
    #         skip_num += 1
    #     if 'failed' in i:
    #         fail_num += 1
    # result = '-[pass-%d_skip-%d_fail-%d]' % (pass_num, skip_num, fail_num)

    # 按照用例执行顺序来列出pass，skip,fail
    re = '-['
    for i in range(len(result_list)):
        if 'passed' in result_list[i]:
            re = re + 'passed'
        if 'skipped' in result_list[i]:
            re = re + 'skipped'
        if 'failed' in result_list[i]:
            re = re + 'failed'
        if i == len(result_list) - 1:
            re = re + ']'
        elif i < len(result_list):
            re = re + '_'
    return re


if __name__ == '__main__':
    main()
