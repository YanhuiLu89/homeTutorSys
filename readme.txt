#graduationDesignSys
����django�ı�ҵ���ѡ��ϵͳ
# django-python
���в���
1����װpython3.7,�����õ���������

2����װmysql���ݿ⣨5.7�����ϰ汾�������������ݿ����

3����װ����ģ��:������������ִ����������
	pip install django
	pip install mysqlclient
	pip install Pillow
(ע��	1�����ִ�еڶ���ʱ�������ơ�����������pip install --upgrade pip���Ĵ��󣬰���ʾִ���������pip install --upgrade pip
	2�����pip install mysqlclient���ִ����ִ��pip install mysqlclient-1.4.4-cp37-cp37m-win_amd64.whl)

4�������������ݿ⣬ע������ʽ����Mysql������������������
create database home_tutor_sys_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
	
5��ͬ�����ݿ⣬�������н���graduationDesignSys·��������ִ���������
    python manage.py makemigrations
    python manage.py migrate

6����������Ա�˻�������Ա�ǲ���ע��ġ��������н���graduationDesignSys·��������ִ����������
	python manage.py shell
	>>> from pages.models import Users
	>>> admin=Users(usertype=1,name='admin01',password='123456',email="296932576@qq.com")
	>>> admin.save()
	ctrl-z�˳� shell����
7��ͬ�����ݿ�
    python manage.py makemigrations
    python manage.py sqlmigrate pages 0001
    python manage.py migrate

8���������н��뵽graduationDesignSys·����ִ���������
	python manage.py runserver,
	����Starting development server at http://127.0.0.1:8000/
	Quit the server with CTRL-BREAK.��
	���ˣ�ϵͳ�ɹ�����

9�� �����������ַ����http://127.0.0.1:8000/pages/index,�򿪵�½ҳ���Ե�7�������Ĺ���Ա��ݵ�½������Ա��½���������ʦ����ѧ���������ɾ����ʦ��ѧ��������ͳ�ƿ��⣬��˿��⣬�������档
��ע�⣺Ŀǰ�˺�ֻ�������֣�ѧ������ѧ�ţ���ʦ��ʦ��ţ�

10����ʦ��½����Կ������棬������ѡ�������ӿ��⣬�������ѧ����������⡣

11��ѧ����½����Կ��Կ������棬ѡ�⣬���⣬������Ա���ԡ�

12����ʦ��ѧ���������޸��Լ�����Ϣ���鿴��Ϣ����ѡ��״̬��
	
   

