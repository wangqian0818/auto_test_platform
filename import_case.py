#!/usr/bin/env python
# coding: utf-8
# @TIME : 2021/4/7 9:48
import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_test_platform.settings')
django.setup()

from 测试计划.models import Case

'''
从禅道导出数据为CSV文件，
'''
csv_file = r'C:\Users\admin\Desktop\禅道1.csv'


def update_csv(csv_file):
    field = []
    rows = []
    with open(csv_file, 'r') as csvfile:
        # 创建 reader 对象
        csvReader = csv.reader(csvfile)  # 每行读数据
        # csvReader = csv.DictReader(csvfile)  # 字典形式的读出数据

        # 在第一行中提取字段名称
        # field = csvReader.next()

        case_list = []
        for row in csvReader:
            if '用例编号' == row[0]:
                continue
            rows.append(row)
            # Case.objects.get_or_create(case_id=row[0], product=row[1], case_module=row[2], relate_requirement=row[3],
            #                            case_title=row[4],
            #                            Preconditions=row[5], step=row[6], Expected=row[7], actual_situation=row[8],
            #                            key_word=row[9], priority=row[10], case_type=row[11], Applicable_stage=row[12],
            #                            case_status=row[13], bug_num=row[14], result_num=row[15], step_num=row[16],
            #                            result=row[17], creater=row[18], create_date=row[19], Last_Modified=row[20],
            #                            Modified_date=row[21], case_version=row[22], relate_case=row[23])
            if not Case.objects.filter(id=row[0]):
                # print('new_id:', row[0])
                case_list.append(Case(id=row[0], product=row[1], case_module=row[2], relate_requirement=row[3],
                                      case_title=row[4], Preconditions=row[5], step=row[6], Expected=row[7],
                                      actual_situation=row[8], key_word=row[9], priority=row[10], case_type=row[11],
                                      Applicable_stage=row[12], case_status=row[13], bug_num=row[14],
                                      result_num=row[15], step_num=row[16], result=row[17], creater=row[18],
                                      create_date=row[19], Last_Modified=row[20], Modified_date=row[21],
                                      case_version=row[22], relate_case=row[23]))
            else:
                # print('id为{}的Case已存在'.format(row[0]))
                continue

    csvfile.close()

    Case.objects.bulk_create(case_list)

    # print(len(row))
    # for i in row:
    #     print('=== ', i)

    for row in rows:
        print(row)
    # all = Case.objects.all()
    # print('============== case_obj:\n', all)


if __name__ == '__main__':
    # 添加Case入库
    update_csv(csv_file)
    print('Done!')
