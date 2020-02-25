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
    student_name = models.CharField(max_length=40,default="")
    student_phone = models.CharField(max_length=40)
    student_grade = models.CharField(max_length=40)
    student_address = models.CharField(max_length=200)
    student_class = models.CharField(max_length=40)
    student_major = models.CharField(max_length=100)

class TeacherInfos(models.Model):#老师信息，与user一对一关系
    teacher = models.OneToOneField(Users, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=40,default="")
    teacher_phone = models.CharField(max_length=40)
    teacher_title = models.CharField(max_length=200)
    teacher_major = models.CharField(max_length=100)

class AdminInfos(models.Model):#管理员信息，与user一对一关系
    admin = models.OneToOneField(Users, on_delete=models.CASCADE)
    admin_name = models.CharField(max_length=40,default="")
    admin_phone = models.CharField(max_length=40)

class Designs(models.Model):#毕业设计课题
    teacher = models.ForeignKey(TeacherInfos,on_delete=models.CASCADE)
    idno=models.CharField(max_length=10,default="XG101")
    type=models.CharField(max_length=100,default="XG")
    subject = models.CharField(max_length=200,default="")
    introduce = models.CharField(max_length=500)

class SelfDefineDesigns(models.Model):#自拟题目
    student = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInfos,on_delete=models.SET(None))
    type=models.CharField(max_length=100,default="XG")
    subject = models.CharField(max_length=200,default="")
    introduce = models.CharField(max_length=500)
    state = models.IntegerField(default=3)#0-提交，1-待老师审批，2-待管理员审批，3审批通过,4打回

class Notices(models.Model):
    text = models.CharField(max_length=500)
    time = models.DateTimeField('date published')

class Messages(models.Model):
    fromuser = models.ForeignKey(StudentInfos, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    updatetime = models.DateTimeField('date published')

class Workflow(models.Model):#工作流，选课审批
    fromuser = models.ForeignKey(StudentInfos,on_delete=models.CASCADE)#任务发起者
    currentuser = models.IntegerField(default=0)#当前任务处理者userid
    subject=models.CharField(max_length=200, default='')#对应的课题题目
    state = models.CharField(max_length=100)#任务状态
    nextaction=models.CharField(max_length=100)#下一步动作
    isselfdesign=models.BooleanField(default=False)#标记是不是自拟题目
    updatetime = models.DateTimeField('date published')#
