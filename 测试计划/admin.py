from django.contrib import admin
from django.utils.html import format_html

from 测试计划.models import Plan, Report, GitCase, Case


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'plan_name', 'run_env', 'case_list', 'pass_list', 'fail_list', 'time', 'purpose', 'executor', 'analyst',
        'result_type', 'analysis_result', 'cycle_num', 'component_version', 'last_run',
        'last_plan')  # ,'operation_link'
    search_fields = ('plan_name', 'label', 'result_type')  # 根据计划名称，标签和结果类型搜索
    exclude = ('label', 'case_list', 'pass_list', 'fail_list',)  # 表单中不显示 标签列
    list_filter = ('plan_name', 'label', 'result_type')
    ordering = ['-id']
    list_per_page = 20

    def operation_link(self, obj):
        return format_html(u'<a href="/baidu" target="_blank">执行</a>  '
                           u'<a href="/baidu" target="_blank">修改</a>  '
                           u'<a href="/baidu" target="_blank">删除</a>  '
                           u'<a href="/baidu" target="_blank">查看报告</a>  '
                           u'<a href="/baidu" target="_blank">结果分析</a>', )

    operation_link.short_description = '操作'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'plan_name', 'run_env', 'case_list', 'pass_list', 'fail_list', 'time', 'purpose', 'executor', 'analyst',
        'result_type', 'analysis_result', 'cycle_num', 'component_version', 'last_run',
        'last_plan')  # ,'operation_link'
    search_fields = ('plan_name', 'label', 'result_type')  # 根据计划名称，标签和结果类型搜索
    exclude = ('label', 'case_list', 'pass_list', 'fail_list',)  # 表单中不显示 标签列
    list_filter = ('plan_name', 'label', 'result_type')
    ordering = ['-id']
    list_per_page = 20

    def operation_link(self, obj):
        return format_html(u'  <a href="/download_report" target="_blank">下载</a>  ', )

    operation_link.short_description = '操作'


class GitCaseAdmin(admin.ModelAdmin):
    list_display = (
        'case_title', 'test_type', 'case_type', 'case_module', 'priority', 'run_env', 'owner', 'Last_Modified',
        'Modified_date')
    search_fields = ('case_type', 'case_module', 'priority', 'run_env', 'test_type',)  # 根据标题或者内容搜索
    list_filter = ('case_type', 'case_module', 'priority', 'run_env', 'test_type',)
    ordering = ['-id']
    list_per_page = 20


admin.site.register(GitCase, GitCaseAdmin)


class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'priority', 'case_title', 'case_type', 'creater', 'bug_num', 'result_num', 'step_num', 'case_status')
    search_fields = ('id', 'priority',)  # 根据标题或者内容搜索
    list_filter = ('product', 'case_module', 'case_type',)
    ordering = ['-id']
    list_per_page = 20


admin.site.register(Case, CaseAdmin)