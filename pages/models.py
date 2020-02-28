from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)#0-学生，1-老师，2-管理员
    name = models.CharField(max_length=30)#账户名
    fullname = models.CharField(max_length=30,default='')#姓名
    gender = models.CharField(max_length=10,default='')
    password = models.CharField(max_length=50)
    email = models.EmailField(default='')
    phone=models.CharField(max_length=50,default='')
    address=models.CharField(max_length=200,default='')

class StudentInfos(models.Model):#学生信息，与user一对一关系
    student = models.OneToOneField(Users, on_delete=models.CASCADE)
    grade = models.CharField(max_length=40,default='')

class TeacherInfos(models.Model):#老师信息，与user一对一关系
    teacher = models.OneToOneField(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default="")
    mark = models.IntegerField(default=0 )#打分0-5
    introduce= models.IntegerField(max_length=300,default=0 )#自我介绍

class TeacherCourse(models.Model):#开售的课程
    name=models.CharField(max_length=50)#课程名称
    teacher = models.ManyToManyField(TeacherInfos)#有哪些老师可以上这个课
    student = models.ManyToManyField(StudentInfos)#有哪些学生预约了这个课程
    grade = models.CharField(max_length=40,default=u"高三")#年级
    subject = models.CharField(max_length=200,default=u"英语")#科目
    introduce = models.CharField(max_length=200)#c课程简介

class StudentCourses(models.Model):#学生发布的所需课程
    student = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    grade = models.CharField(max_length=40,default=u"高三")
    subject = models.CharField(max_length=200,default=u"英语")
    introduce = models.CharField(max_length=500)

class Notices(models.Model):#新闻公告
    text = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)

class Messages(models.Model):#留言
    fromuser = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInfos,default=(None),on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    updatetime = models.DateTimeField(auto_now=True)

class Recruit(models.Model):#招聘信息
    name = models.CharField(max_length=30)#职位名称
    minage = models.IntegerField(default=20)#最小年龄要求
    maxage = models.IntegerField(default=65)#最大年前要求
    wages = models.IntegerField(default=7000)#工资
    education= models.IntegerField(default=0)#0-大专,1-本科，2-研究生，3-硕士
    description = models.CharField(max_length=500)
    updatetime = models.DateTimeField(auto_now=True)#

class Courseflow(models.Model):#课程审批流程
    course = models.OneToOneField(TeacherCourse, on_delete=models.CASCADE)
    state = models.IntegerField(default=0)#0-提交 1-通过 2-打回
    updatetime = models.DateTimeField(auto_now=True)#
