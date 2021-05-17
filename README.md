## �Զ�������ƽ̨����ָ��
�Զ���ƽ̨��������ɾ�Ĳ�����django�Ŀ��֮�Ͽ����ģ����Լƻ�������ִ�У��Լ����Ա���Ĳ鿴ֻ����
django��ǰ��˵��÷�ʽ��û����django��ǰ�˺ͺ�ˣ�������ʱҳ�洿��HTML�������ģ�û���õ��κε�CSS��ʽ��
�Ƚϳ󣬺�����ʱ���ٿ����Ż�ҳ�档

#### �����ǻ����Ĵ�ͻ�����������
1�� ��װdjango  
`pip install django==2.2.18`  
�鿴Django�汾�ţ�`python -m django --version`  

2�� ����  
`python3 manage.py runserver`  

3�������¼  
��ҳURL��http://127.0.0.1:8000/  
**��������Ա���ܡ�admin:@!juson1203��**  
�½����Լƻ�����ִ��������URL��http://127.0.0.1:8000/plans/    

4�� django�Ļ���������ܡ��˽⼴�ɡ�    
* ������Ŀ  
```shell script
django-admin startproject ��Ŀ����
``` 
* ����APP  
```shell script
python manage.py startapp Ӧ����
``` 
* ������Ŀ  
```shell script
cd ��Ŀ����  
python3 manage.py runserver        
```
* ������������Ա  
```shell script
python manage.py createsuperuser         # ���������û�
python manage.py changepassword username  # �޸�����
```
* �½����󣬻����޸Ĺ�������ֶΡ��ֶ����Ժ���Ҫ�ֶ�Ӧ�õ����ݿ�
```shell script
python manage.py makemigrations (appname)
python manage.py migrate (appname)
# �鿴sql��䣺
python3 manage.py sqlmigrate appname �ļ�ID
# eg��python3 manage.py sqlmigrate app02_db 0001
```
