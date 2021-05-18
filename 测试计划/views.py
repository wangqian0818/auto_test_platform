# Create your views here.
import datetime
import json
import os
import time

import django
from django.contrib import messages

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_test_platform.settings')
django.setup()
from auto_test.common import baseinfo
from auto_test.run import main
from ftp_dir_tools import ftpconnect, upload_file_tree, download_file_tree
from django.http import HttpResponseRedirect
from django.shortcuts import render
from 测试计划.models import Plan, Report
from 测试计划.models import GitCase

ftp_host = "10.10.88.193"
ftp_port = 21
ftp_username = "test"
ftp_password = "1q2w3e"
ftp_remote_path = '/home/ftp/自动化测试_日志记录/自动化平台_测试日志'
download_local_path = r'E:\ftp_test'
version = baseinfo.version

MESSAGE_TAGS = {
    messages.INFO: '',
    50: 'critical',
}
# 自动化测试脚本的运行状态：0就是非运行状态，1正在运行中
case_run_status = 0


# 测试用
def dump(request):
    return render(request, '测试计划/test_ajax.html')


# 测试用
def dump_checkbox(request):
    plans = Plan.objects.all()
    return render(request, '测试计划/checkbox.html', {'plans': plans})


# 展示测试计划
def plans(request):
        print('-------------------------------plans: ', request.method)
        print('------------- case_run_status: ', case_run_status)
        plans = Plan.objects.all()
        return render(request, '测试计划/plan_list.html', {'plans': plans, 'case_run_status': case_run_status})


# 新增测试计划
def add_plan(request):
    print('-------------------------------add_plan:', request.method)
    if 'POST' == request.method:
        # 新增或者更新页面选中的case
        titles = request.POST.getlist('gitCase_title')
        # 选中的用例个数
        case_num = len(titles)
        # 用-连接选中的用例id
        case_list = '-'.join(titles)
        print('--- case_list: ', case_list)
        plan_name = request.POST.get('plan_name')
        purpose = request.POST.get('purpose')
        cycle_num = request.POST.get('cycle_num')
        if '' == cycle_num:
            cycle_num = 1  # 如果没有指定循环次数，默认一次
        # 新建测试计划，结果分析这一块应该是空的
        # result_type = request.POST.get('result_type')
        # analysis_result = request.POST.get('analysis_result')
        Plan.objects.get_or_create(plan_name=plan_name, case_list=case_list, case_num=case_num, purpose=purpose,
                                   result_type='', analysis_result='', component_version=version,
                                   last_run='', last_plan='', cycle_num=cycle_num)
        return HttpResponseRedirect('/plans')
    elif 'GET' == request.method:
        print('---add_plan:get')
        # 查询所有用例，显示到计划页面，便于多选
        gitCases = GitCase.objects.all()
        return render(request, '测试计划/plan_add.html', {'gitCases': gitCases})


# 更新测试计划
def update_plan(request, id):
    print('-------------------------------update_plan:', request.method)
    print('--- update_plan: id=', id)
    plan_obj = Plan.objects.filter(pk=id)
    lp = list(plan_obj)
    plan = lp[0]
    if 'GET' == request.method:
        # 获取该plan对象选择的case
        print('--- plan_name: ', plan.plan_name)
        print('--- case_list: ', plan.case_list)
        checked_cases = None
        if '' != plan.case_list:
            case_id_list = plan.case_list.split('-')
            ls = []
            # 转成数字的list,用于查询，已被选择的blog
            for case_id in case_id_list:
                ls.append(int(case_id))
            checked_cases = GitCase.objects.filter(pk__in=ls)
        # 获取所有case，展示后用于重新选择
        all_cases = GitCase.objects.all()
        return render(request, '测试计划/plan_update.html',
                      {'plan': plan, 'all_cases': all_cases, 'checked_cases': checked_cases})
    elif 'POST' == request.method:
        # 从修改页面的表单提交转到此逻辑
        # 新增或者更新页面选中的case
        titles = request.POST.getlist('gitCase_title')
        # 选中的用例个数
        case_num = len(titles)
        # 用-连接选中的用例id
        case_list = '-'.join(titles)
        print('--- case_list: ', case_list)
        plan_name = request.POST.get('plan_name')
        purpose = request.POST.get('purpose')
        result_type = request.POST.get('result_type')
        analysis_result = request.POST.get('analysis_result')
        # 如果结果类型或者分析结果不为空了，则表示有分析，需要更新当前的用户为分析者
        if '' != result_type or '' != analysis_result:
            # 获取当前用户名，作为分析者
            username = request.user.username
            Plan.objects.filter(pk=id).update(analyst=username)
        cycle_num = request.POST.get('cycle_num')
        # 每次更新，需要清空pass_list和fail_list
        # 获取该plan对象选择的case
        print('--- plan_name: ', plan_name)
        print('--- case_list: ', case_list)
        Plan.objects.filter(pk=id).update(plan_name=plan_name, case_list=case_list, case_num=case_num,
                                          pass_list='', fail_list='', pass_num=0, fail_num=0, purpose=purpose,
                                          result_type=result_type, analysis_result=analysis_result,
                                          component_version=version, cycle_num=cycle_num)
        return HttpResponseRedirect('/plans')


def delete_plan(request, id):
    print('-------------------------------delete_plan: id=', id)
    if 'GET' == request.method:
        print('--- delete_plan:get')
        Plan.objects.filter(pk=id).delete()
    elif 'POST' == request.method:
        print('--- delete_plan:post')
    return HttpResponseRedirect('/plans')


# 点击执行按钮，执行该id的测试计划
def exec(request, id):
    print('-------------------------------exec: ', request.method)
    this_plan = list(Plan.objects.filter(pk=id))
    plan = this_plan[0]
    # 该plan选中的用例
    case_list = plan.case_list
    # 如果有选择用例
    case_title_list = []
    if case_list:
        messages.info(request, "正在执行")
        cirNum = plan.cycle_num
        case_ids = case_list.split('-')
        print('--- case_ids: ', case_ids)
        for case_id in case_ids:
            case = GitCase.objects.filter(pk=case_id)
            case_title = case[0].case_title
            case_title_list.append(case_title)
        print('--- case_title_list: ', case_title_list)
        # ===============================================================
        # 根据该测试计划中选中的case，更改selected.py文件
        change_selected(case_title_list=case_title_list)
        # 执行用例，计算耗时
        start_time = time.time()
        # 执行自动化测试脚本，因为存在循环多次执行，所以返回值是本地日志路径list
        html_logs_paths = run_auto_test(cirNum)
        waste_time = format(time.time() - start_time, '.3f') + ' s '
        print('--- 运行耗时：', waste_time)
        # ===============================================================
        # # 模拟数据
        # # html_logs_paths = [
        # #     'E:\\Projects_Py\\django_prctice\\auto_test_platform\\auto_test\\Logs\\test1.0.0\\20210119_19-39-20\\',
        # #     'E:\\Projects_Py\\django_prctice\\auto_test_platform\\auto_test\\Logs\\test1.0.0\\20210506_11-54-57\\']
        # html_logs_paths = [
        #     'E:\\Projects_Py\\django_prctice\\auto_test_platform\\auto_test\\Logs\\test1.0.0\\20210518_16-26-10\\']
        # waste_time = '20.213 s '
        # print('--- 运行耗时：', waste_time)
        # ===============================================================
        messages.success(request, "执行结束，耗时" + waste_time)
        # 获取当前时间
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取当前用户
        django_username = request.user.username
        print('--- 当前用户：', )
        Plan.objects.filter(pk=id).update(time=waste_time, last_run=now, executor=django_username)
        # 读取此次执行后的html日志，得出执行情况，并更新测试计划的数据
        read_logs(html_logs_paths=html_logs_paths, plan_id=id)
        # 每执行一次，产生一次新的测试报告，新建测试报告实例
        # 因为执行结束后，会更新pass_list和fail_list，所以需要重新查询
        this_plan = list(Plan.objects.filter(pk=id))
        plan = this_plan[0]
        # 跑自动化脚本的结果为日志绝对路径的list，页面显示可能会导致表格变形，需要处理数据，【版本号\日期时间】
        log_paths = []
        for path in html_logs_paths:
            dirname = path.split('\\')[-2]
            version_dir = path.split('\\')[-3]
            log_path = '【' + version_dir + '\\' + dirname + '】'
            log_paths.append(log_path)
        report_path = '-'.join(log_paths)
        # report_path = '<br>'.join(log_paths)
        try:
            Report.objects.create(plan_name=plan.plan_name, run_env=plan.run_env,
                                  case_list=plan.case_list, case_num=plan.case_num,
                                  pass_list=plan.pass_list, pass_num=plan.pass_num,
                                  fail_list=plan.fail_list, fail_num=plan.fail_num,
                                  purpose=plan.purpose, result_type=plan.result_type,
                                  analysis_result=plan.analysis_result, time=waste_time,
                                  report_path=report_path, plan_id=str(id), last_run=now,
                                  component_version=version, executor=django_username,
                                  analyst=plan.analyst)
        except Exception as err:
            print('测试报告新建失败：', err)
        # 每执行一次新产生的测试报告，上传到ftp
        ftp = ftpconnect(ftp_host, ftp_username, ftp_password, ftp_port)
        if ftp:
            for html_logs_path in html_logs_paths:
                ''' 上传整个路径下的文件 '''
                # 加上本地日志时间的文件夹名称，类似【20210421_16-56-59】
                remote_path = ftp_remote_path + r'/' + html_logs_path.split('\\')[-2]
                # 递归传输本地所有文件包括目录
                upload_file_tree(local_path=html_logs_path, remote_path=remote_path, ftp=ftp)
            # 关闭ftp
            ftp.quit()
            print(
                '--------- ftp断开连接：host[{}]-port[{}]-username[{}]-password[{}]'.format(ftp_host, ftp_port, ftp_username,
                                                                                       ftp_password))
        else:
            print('--------- ftp主机{} 连接失败'.format(ftp_host))
    else:
        print('该测试计划没有选择用例')
        messages.error(request, "该测试计划没有选择用例")
    return HttpResponseRedirect('/plans')


# 根据该测试计划中选中的case，更改selected_rbm.py文件
def change_selected(test_type='rbm', case_title_list=None):
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # base_path：E:/Projects_Py/django_prctice/django_test03
    base_path = base_path.replace('\\', '/')
    # selected_path：E:/Projects_Py/django_prctice/django_test03/auto_test/common/caseselect_rbm.py
    selected_path = base_path + '/auto_test/common/caseselect_rbm.py'
    # print('------------------ base_path: ', base_path)
    print('--- selected_path: ', selected_path)
    logs_path = base_path + '/auto_test/Logs/test1.0.0/'
    list_values = []
    for i in range(len(case_title_list)):
        list_values.append([])
    selected_json = json.dumps(dict(zip(case_title_list, list_values)))
    with open(selected_path, 'w') as f1:
        f1.seek(0)
        f1.truncate()
        print("--- 清空{}文件数据".format(test_type))
        f1.write(selected_json)
        print("--- 插入{}文件数据".format(test_type))


def read_logs(html_logs_paths='', plan_id=None):
    pass_num = 0
    pass_case_ids = []
    fail_num = 0
    fail_case_ids = []
    skip_num = 0
    for html_logs_path in html_logs_paths:
        files = os.listdir(html_logs_path)  # 得到文件夹下的所有文件名称
        for file in files:  # 遍历文件夹
            if not os.path.isdir(file) and os.path.splitext(file)[1] == ".html":  # 非文件夹，并且是html格式的文件才读取
                file_name = os.path.splitext(file)[0]
                # print('file_name:', file_name)
                # 存在一个fail的用例都算失败
                if 'fail' in file_name:
                    fail_num += 1
                    log_list = file.split('-')
                    # 去掉首尾的[]符号
                    case_name = log_list[0].replace('[', '').replace(']', '')
                    gitCase = GitCase.objects.filter(case_title=case_name)
                    fail_case_id = gitCase[0].id
                    print('--- fail_case_id:', fail_case_id)
                    fail_case_ids.append(fail_case_id)
                # 没有成功失败，只有skip的用例，就算skip
                elif 'pass' not in file_name and 'fail' not in file_name and 'skip' in file_name:
                    skip_num += 1
                # 剩下的都是成功的，或者pass+skip
                else:
                    pass_num += 1
                    log_list = file.split('-')
                    # 去掉首尾的[]符号
                    case_name = log_list[0].replace('[', '').replace(']', '')
                    gitCase = GitCase.objects.filter(case_title=case_name)
                    pass_case_id = gitCase[0].id
                    # print('----- pass_case_id:', pass_case_id)
                    pass_case_ids.append(pass_case_id)
                    # result = log_list[-1].split('.')[0].replace('[', '').replace(']', '')
                    # print('result:', result)
    print('--- pass_case_ids: ', pass_case_ids)
    print('--- fail_case_ids: ', fail_case_ids)
    print('--- pass_num:{} \t fail_num:{} \t skip_num:{}'.format(pass_num, fail_num, skip_num))
    Plan.objects.filter(pk=plan_id).update(pass_num=pass_num, fail_num=fail_num, pass_list=str(pass_case_ids),
                                           fail_list=str(fail_case_ids))


# 执行pytest,auto_test的run.py
def run_auto_test(cirNum):
    main_return = main(cirNum)
    # 返回：./Logs/test1.0.0/20210416_16-47-58/   需要以下过滤
    # last_log_dir = main_return.split('/')[3]
    # version = main_return.split('/')[2]
    # print(version + '/' + last_log_dir)
    # main_log_path = r'E:\Projects_Py\django_prctice\django_test03\auto_test\Logs' + version + '\\' + last_log_dir
    # print('main_log_path: ', main_log_path)
    # 执行结束，脚本运行状态改为0
    case_run_status = 0
    return main_return


def history_report(request, id):
    this_plan = list(Plan.objects.filter(pk=id))
    plan = this_plan[0]
    history_reports = Report.objects.filter(plan_id=plan.pk)
    return render(request, '测试计划/plan_report.html', {'history_reports': history_reports})


def download_report(request, report_id):
    this_report = list(Report.objects.filter(pk=report_id))
    report = this_report[0]
    ftp = ftpconnect(ftp_host, ftp_username, ftp_password, ftp_port)
    ftp_remote_path = '/home/ftp/自动化测试_日志记录/自动化平台_测试日志'
    ftp_remote_path = ftp_remote_path + r'/' + str(report.report_path).split('\\')[-2]
    print('--- ftp_remote_path:', ftp_remote_path)
    if ftp:
        download_file_tree(local_path=download_local_path, remote_path=ftp_remote_path, ftp=ftp)
        # 关闭ftp
        ftp.quit()
        print(
            '--- ftp断开连接：host[{}]-port[{}]-username[{}]-password[{}]'.format(ftp_host, ftp_port, ftp_username,
                                                                             ftp_password))
    else:
        print('--- ftp主机{} 连接失败'.format(ftp_host))
    # 通过该report_id，查出同组其他历史report
    history_reports = Report.objects.filter(plan_id=report.plan_id)
    return render(request, '测试计划/plan_report.html', {'history_reports': history_reports})


def delete_report(request, report_id):
    # 查出此条report，用它的plan_id查找出同组的其他report
    this_report = list(Report.objects.filter(pk=report_id))
    report = this_report[0]
    history_reports = Report.objects.filter(plan_id=report.plan_id)
    # 根据report的主键id删除report
    Report.objects.filter(pk=report_id).delete()
    return render(request, '测试计划/plan_report.html', {'history_reports': history_reports})


if __name__ == '__main__':
    run_auto_test()
