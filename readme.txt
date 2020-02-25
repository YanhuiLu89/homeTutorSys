#graduationDesignSys
基于django的毕业设计选题系统
# django-python
运行步骤
1、安装python3.7,并配置到环境变量

2、安装mysql数据库（5.7及以上版本），并启动数据库服务

3、安装所需模块:在命令行依次执行以下输入
	pip install django
	pip install mysqlclient
	pip install Pillow
(注意	1、如果执行第二步时出现类似“。。。。。pip install --upgrade pip”的错误，按提示执行以下命令：pip install --upgrade pip
	2、如果pip install mysqlclient出现错误就执行pip install mysqlclient-1.4.4-cp37-cp37m-win_amd64.whl)

4、创建数据数据库，注意编码格式：在Mysql命令行输入以下命令
create database home_tutor_sys_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
	
5、同步数据库，从命令行进入graduationDesignSys路径，依次执行以下命令：
    python manage.py makemigrations
    python manage.py migrate

6、创建管理员账户，管理员是不能注册的。从命令行进入graduationDesignSys路径，依次执行以下命令
	python manage.py shell
	>>> from pages.models import Users
	>>> admin=Users(usertype=1,name='admin01',password='123456',email="296932576@qq.com")
	>>> admin.save()
	ctrl-z退出 shell命令
7、同步数据库
    python manage.py makemigrations
    python manage.py sqlmigrate pages 0001
    python manage.py migrate

8、从命令行进入到graduationDesignSys路径，执行以下命令：
	python manage.py runserver,
	出现Starting development server at http://127.0.0.1:8000/
	Quit the server with CTRL-BREAK.，
	至此，系统成功启动

9、 打开浏览器，网址输入http://127.0.0.1:8000/pages/index,打开登陆页，以第7步创建的管理员身份登陆，管理员登陆后可以在老师管理、学生管理添加删除老师和学生，可以统计课题，审核课题，发布公告。
（注意：目前账号只能是数字，学生就是学号，老师老师编号）

10、老师登陆后可以看到公告，可以在选题管理添加课题，可以审核学生的自拟课题。

11、学生登陆后可以可以看到公告，选题，拟题，给管理员留言。

12、老师和学生都可以修改自己的信息，查看消息，看选题状态。
	
   

