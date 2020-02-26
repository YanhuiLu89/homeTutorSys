from django.db import models

# Create your models here.
class Users(models.Model):
    usertype = models.IntegerField(default=0)#0-学生，1-老师，2-管理员
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,default='male')
    password = models.CharField(max_length=50)
    email = models.EmailField(default='1@2.com')
    phone=models.CharField(max_length=50,default='')
    address=models.CharField(max_length=200,default='')

class StudentInfos(models.Model):#学生信息，与user一对一关系
    student = models.OneToOneField(Users, on_delete=models.CASCADE)
    grade = models.CharField(max_length=40)

class TeacherInfos(models.Model):#老师信息，与user一对一关系
    teacher = models.OneToOneField(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=200，default="")
    mark = models.IntegerField(default=0 )#打分0-5

class TeacherCourse(models.Model):#老师在开售的课程
    teacher = models.ForeignKey(TeacherInfos,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    grade = models.CharField(max_length=40,default=u"高三")
    subject = models.CharField(max_length=200,default=u"英语")
    introduce = models.CharField(max_length=200)#c课程简介
    time = models.DateTimeField('2020-02-26 19:00')#开课时间
    length = models.IntegerField(default=30)#授课时长单位分钟

class StudentCourses(models.Model):#学生发布的所需课程
    student = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    grade = models.CharField(max_length=40,default=u"高三")
    subject = models.CharField(max_length=200,default=u"英语")
    introduce = models.CharField(max_length=500)

class Notices(models.Model):#新闻公告
    text = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=Ture)

class Messages(models.Model):#留言
    fromuser = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInfos)
    text = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    updatetime = models.DateTimeField(auto_now=Ture)

class BookCourse(models.Model):#预约课程
    fromuser = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    course = models.ForeignKey(TeacherCourse)
    coursetime = models.timeField('2020-02-26 19:00')#开课时间
    updatetime = models.TimeField(auto_now=Ture)

classk Courseflow(models.Model):#课程审批流程
    course = models.ForeignKey(TeacherCourse)
    state = models.IntegerField(default=0)#0-提交 1-通过 2-打回
    updatetime = models.DateTimeField(auto_now=Ture)#
