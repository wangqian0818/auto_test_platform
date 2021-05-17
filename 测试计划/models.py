from django.db import models


# Create your models here.
class Plan(models.Model):
    env_list = [('1', '网关'), ('2', '隔离')]

    cases_list = [('1', '功能测试'), ('2', '性能测试'), ('3', '稳定性测试')]
    # cases_list = [[('功能测试1','test1'),('功能测试1','test1')],[('功能测试1','test1'),('功能测试1','test1')]]

    purpose_list = [('1', '冒烟测试'), ('2', '回归bug'), ('3', '回归版本'), ('4', '出厂测试'), ('5', '功能测试'), ('6', '性能测试'),
                    ('7', '稳定性测试')]
    result_type_list = [('1', '版本问题'), ('2', '环境问题'), ('3', '脚本问题')]

    # id = models.IntegerField(primary_key=True)
    plan_name = models.CharField(verbose_name='计划名称', max_length=100, default=None)
    run_env = models.CharField(verbose_name='运行环境', max_length=100, choices=env_list, default=env_list[0])
    case_num = models.IntegerField(verbose_name='用例条数', blank=True, null=True, default=0)
    pass_num = models.IntegerField(verbose_name='成功条数', blank=True, null=True, default=0)
    fail_num = models.IntegerField(verbose_name='失败条数', blank=True, null=True, default=0)
    case_list = models.CharField(verbose_name='用例id列表', blank=True, null=True, default='', max_length=1000)
    pass_list = models.CharField(verbose_name='成功id列表', blank=True, null=True, default='', max_length=1000)
    fail_list = models.CharField(verbose_name='失败id列表', blank=True, null=True, default='', max_length=1000)
    time = models.CharField(verbose_name='耗时', blank=True, null=None, default='', max_length=100)
    purpose = models.CharField(verbose_name='测试目的', max_length=100, choices=purpose_list, default=purpose_list[0])
    executor = models.CharField(verbose_name='执行者', max_length=32, blank=True)
    analyst = models.CharField(verbose_name='分析者', max_length=32, blank=True)
    label = models.CharField(verbose_name='标签', max_length=32, blank=True)
    result_type = models.CharField(verbose_name='结果类型', max_length=32, choices=result_type_list,
                                   default=result_type_list[0])
    analysis_result = models.TextField(verbose_name='分析结果', blank=True)
    cycle_num = models.IntegerField(verbose_name='循环次数', blank=True, default=0)
    component_version = models.CharField(verbose_name='组件版本', max_length=32, blank=True)
    last_run = models.CharField(verbose_name='最后一次运行时间', blank=True, default='', max_length=100)
    last_plan = models.CharField(verbose_name='下次计划', blank=True, default='', max_length=100)

    def __unicode__(self):
        return self.plan_name


class Report(models.Model):
    plan_name = models.CharField(verbose_name='计划名称', max_length=100, default=None)
    run_env = models.CharField(verbose_name='运行环境', max_length=100, default=None)
    case_num = models.IntegerField(verbose_name='用例条数', blank=True, null=True, default=0)
    pass_num = models.IntegerField(verbose_name='成功条数', blank=True, null=True, default=0)
    fail_num = models.IntegerField(verbose_name='失败条数', blank=True, null=True, default=0)
    case_list = models.CharField(verbose_name='用例id列表', blank=True, null=True, default='', max_length=1000)
    pass_list = models.CharField(verbose_name='成功id列表', blank=True, null=True, default='', max_length=1000)
    fail_list = models.CharField(verbose_name='失败id列表', blank=True, null=True, default='', max_length=1000)
    time = models.CharField(verbose_name='耗时', blank=True, null=None, default='', max_length=100)
    purpose = models.CharField(verbose_name='测试目的', max_length=100, default=None)
    executor = models.CharField(verbose_name='执行者', max_length=32, blank=True)
    analyst = models.CharField(verbose_name='分析者', max_length=32, blank=True)
    label = models.CharField(verbose_name='标签', max_length=32, blank=True)
    result_type = models.CharField(verbose_name='结果类型', max_length=32, default=None)
    analysis_result = models.TextField(verbose_name='分析结果', blank=True)
    cycle_num = models.IntegerField(verbose_name='循环次数', blank=True, default=0)
    component_version = models.CharField(verbose_name='组件版本', max_length=32, blank=True)
    last_run = models.CharField(verbose_name='最后一次运行时间', blank=True, default='', max_length=100)
    last_plan = models.CharField(verbose_name='下次计划', blank=True, default='', max_length=100)
    report_path = models.CharField(verbose_name='报告路径', max_length=100, blank=True, default='')
    plan_id = models.CharField(verbose_name='计划id', max_length=10, blank=True, default='')

    def __unicode__(self):
        return self.plan_name



# Git用例对象
class GitCase(models.Model):
    # id = models.IntegerField(verbose_name="用例编号", primary_key=True)  # 设置主键后，就会代替原来默认的自增id列
    case_title = models.TextField(verbose_name="用例标题", max_length=100)
    case_type = models.CharField(verbose_name="用例类型", max_length=100, null=True)
    case_module = models.CharField(verbose_name="所属模块", max_length=100)
    priority = models.IntegerField(verbose_name="优先级", null=True)
    run_env = models.CharField(verbose_name="运行环境", max_length=100)
    test_type = models.CharField(verbose_name="测试类型", max_length=100)
    owner = models.CharField(verbose_name="所属人", max_length=100, null=True)
    Last_Modified = models.CharField(verbose_name="最后修改者", max_length=100)
    Modified_date = models.DateTimeField(verbose_name="更新日期", auto_now=True)

    def __unicode__(self):
        return self.case_title



# 禅道用例对象
'''
['用例编号', '所属产品', '所属模块', '相关需求', '用例标题', '前置条件', '步骤', '预期', '实际情况',
'关键词', '优先级', '用例类型', '适用阶段', '用例状态', 'B', 'R', 'S', '结果', '由谁创建', '创建日期',
'最后修改者', '修改日期', '用例版本', '相关用例']
'''
class Case(models.Model):
    # 用例编号
    id = models.IntegerField(verbose_name="用例编号", primary_key=True)  # 设置主键后，就会代替原来默认的自增id列
    # 所属产品
    product = models.CharField(verbose_name="所属产品", max_length=100)
    # 所属模块
    case_module = models.CharField(verbose_name="所属模块", max_length=100)
    # 相关需求
    relate_requirement = models.CharField(verbose_name="相关需求", max_length=10000)
    # 用例标题
    case_title = models.TextField(verbose_name="用例标题", max_length=100)
    # 前置条件
    Preconditions = models.TextField(verbose_name="前置条件", max_length=100)
    # 步骤
    step = models.TextField(verbose_name="步骤", max_length=10000)
    # 预期
    Expected = models.TextField(verbose_name="预期", max_length=100)
    # 实际情况
    actual_situation = models.TextField(verbose_name="实际情况", max_length=10000)
    # 关键词
    key_word = models.CharField(verbose_name="关键词", max_length=100, null=True)
    # 优先级
    priority = models.IntegerField(verbose_name="优先级")
    # 用例类型
    case_type = models.CharField(verbose_name="用例类型", max_length=100)
    # 适用阶段
    Applicable_stage = models.CharField(verbose_name="适用阶段", max_length=100, null=True)
    # 用例状态
    case_status = models.CharField(verbose_name="用例状态", max_length=100)
    # B：是Bug的缩写，指该用例产生的Bug数
    bug_num = models.IntegerField(verbose_name="B")
    # R：是指该用例执行的结果数
    result_num = models.IntegerField(verbose_name="R")
    # S：是指该用例的步骤数
    step_num = models.IntegerField(verbose_name="S")
    # 结果
    result = models.CharField(verbose_name="结果", max_length=100, null=True)
    # 由谁创建
    creater = models.CharField(verbose_name="由谁创建", max_length=100, default=None)
    # 创建日期
    # create_date = models.DateTimeField()
    create_date = models.CharField(verbose_name="创建日期", max_length=100, default='', null=True)
    # 最后修改者
    Last_Modified = models.CharField(verbose_name="最后修改者", max_length=100)
    # 修改日期
    # Modified_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    Modified_date = models.CharField(verbose_name="修改日期", max_length=100, default='', null=True)
    # 用例版本
    case_version = models.CharField(verbose_name="用例版本", max_length=10, default='')
    # 相关用例
    relate_case = models.CharField(verbose_name="相关用例", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.case_title
