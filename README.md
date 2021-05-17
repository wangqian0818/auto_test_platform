## 自动化测试平台操作指南
自动化平台的数据增删改查是在django的框架之上开发的，测试计划和用例执行，以及测试报告的查看只用了
django的前后端调用方式，没有用django的前端和后端，所以暂时页面纯用HTML垒起来的，没有用到任何的CSS样式，
比较丑，后面有时间再考虑优化页面。

#### 以下是环境的搭建和基本操作介绍
1、 安装django  
`pip install django==2.2.18`  
查看Django版本号：`python -m django --version`  

2、 运行  
`python3 manage.py runserver`  

3、界面登录  
首页URL：http://127.0.0.1:8000/  
**超级管理员账密【admin:@!juson1203】**  
新建测试计划，并执行用例的URL：http://127.0.0.1:8000/plans/    

4、 django的基本命令介绍【了解即可】    
* 创建项目  
```shell script
django-admin startproject 项目名称
``` 
* 创建APP  
```shell script
python manage.py startapp 应用名
``` 
* 运行项目  
```shell script
cd 项目名称  
python3 manage.py runserver        
```
* 创建超级管理员  
```shell script
python manage.py createsuperuser         # 创建超管用户
python manage.py changepassword username  # 修改密码
```
* 新建对象，或者修改过对象的字段、字段属性后，需要手动应用到数据库
```shell script
python manage.py makemigrations (appname)
python manage.py migrate (appname)
# 查看sql语句：
python3 manage.py sqlmigrate appname 文件ID
# eg：python3 manage.py sqlmigrate app02_db 0001
```
