from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q 
from django.utils import timezone

from .models import Users,TeacherInfos,StudentInfos,Notices,Messages,TeacherCourse,StudentCourses,Courseflow,BookCourseflow,Charge,Recruit
# Create your views here.
###############################公共view##################################################
def index(request):#入口页
    if request.method == 'POST':  
        temp_name = request.POST['username']
        temp_psw = request.POST['password']
        temp_mail = request.POST['mail']
        temp_usertype = int(request.POST['usertype'])
        print( temp_name+","+temp_psw+","+temp_mail)
        if Users.objects.filter(name=temp_name).exists():
            messages.add_message(request,messages.ERROR,'该用户名已经存在')
            return render(request,'index.html')
        if Users.objects.filter(email=temp_mail).exists():
            messages.add_message(request,messages.ERROR,'该邮箱已经注册过')
            return render(request,'index.html')
        user = Users(usertype=temp_usertype,name=temp_name, password=temp_psw, email=temp_mail)
        user.save()
        if user.usertype==0:
            studentinfo=StudentInfos(student=user)
            studentinfo.save()
        elif user.usertype==1:
            teacherinfo=TeacherInfos(teacher=user)
            teacherinfo.save()
        return render(request,'login.html')
    return render(request,'index.html')

def login(request):#入口页
    if request.method == 'POST':
        name = request.POST['username']
        password =  request.POST['password']
        usertype=int((request.POST['usertype']))
        # 查询用户是否在数据库中
        print("%s,%s,%d"%(name,password,usertype))
        if Users.objects.filter(name=name).exists():
            user=Users.objects.get(name=name)
            print("%s,%s,%d" % (user.name,user.password,user.usertype))
            print(user.password+",%d" % user.usertype)
            if user.password==password and user.usertype==usertype:
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                #记录cooki
                request.session['is_login'] = 'true'
                request.session["username"] = user.name
                notice_list = Notices.objects.all().order_by('-time')
                if user.usertype==0:
                    teacherinfo_list = TeacherInfos.objects.all().order_by('-mark')
                    context = {'teacherinfo_list': teacherinfo_list,'notice_list': notice_list}
                    response=render(request, 'homepage.html',context)
                elif user.usertype==1:
                    studentinfo_list = StudentInfos.objects.all().order_by('-id')
                    context = {'studentinfo_list': studentinfo_list,'notice_list': notice_list}
                    response=render(request, 'homepage_t.html',context)
                elif user.usertype==2:
                    print("222222222222222222222222222222222222")
                    context = {'notice_list': notice_list}
                    response=render(request, 'homepage_a.html',context)
                response.set_cookie("username", name)
                return response
            else:
                print("3333333333333333333333333333333333333333333")
                messages.add_message(request,messages.ERROR,'密码或身份类型错误')
                return render(request, 'login.html')
        else:
            messages.add_message(request,messages.ERROR,'用户不存在')
            return render(request, 'login.html')
    return render(request, 'login.html')
    
def home(request):#主页
    print("home in")
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    if user.usertype == 0:
        teacherinfo_list = TeacherInfos.objects.all()
        context = {'teacherinfo_list': teacherinfo_list,'notice_list': notice_list}
        response=render(request, 'homepage.html',context)
    elif user.usertype == 1:
        studentinfo_list=StudentInfos.objects.all()
        context = {'studentinfo_list': studentinfo_list,'notice_list': notice_list}
        return render(request, 'homepage_t.html',context)
    elif user.usertype == 2:
        context = {'notice_list': notice_list}
        response=render(request, 'homepage_a.html',context)
    return response

def logout(request):#退出登录
    request.session.delete()
    request.session.flush() 
    response=render(request, 'index.html')
    response.delete_cookie("username")
    return response

def designdetail(request,subject):
    print("sad sad sad sad sad")
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html',context)
    temp_subject=subject
    work=Workflow.objects.get(subject=temp_subject)
    if work.isselfdesign==True:
        selfdesign=SelfDefineDesigns.objects.get(subject=temp_subject)
        context = {'design': selfdesign}
    else:
        design=Designs.objects.get(subject=temp_subject)
        context = {'design': design}
    user=Users.objects.get(name=cook)
    if user.usertype==0:
        return render(request, 'designdetail.html',context)
    elif user.usertype==1:
        return render(request, 'designdetail_t.html',context)
    elif user.usertype==1:
        return render(request, 'designdetail_a.html',context)

def msgcenter(request):#消息中心
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    if user.usertype==0:
        student=StudentInfos.objects.get(student=user)
        messages=Messages.objects.filter(fromuser=student)
        content={'notice_list':notice_list,'message_list':messages}
        print("+++++++++++++++++++++++++++++++++++++++++=")
        print( messages.count())
        return render(request, 'msgcenter.html',content)
    if user.usertype==1:
        return render(request, 'msgcenter_t.html')
    if user.usertype==2:
        messages=Messages.objects.all()
        content={'message_list':messages}
        return render(request, 'msgcenter_a.html',content)

def editmyinfo(request):#我的
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    if request.method == 'GET':#连接到信息编辑页面
        if user.usertype==0:
            studentinfo=StudentInfos.objects.get(student=user)
            context = {'notice_list': notice_list,'studentinfo': studentinfo}
            return render(request, 'editmyinfo.html',context)
        elif user.usertype==1:
            teacher=TeacherInfos.objects.get(teacher=user)
            context = {'notice_list': notice_list,'teacherinfo':teacher}
            return render(request, 'editmyinfo_t.html',context)
        elif user.usertype==2:
            admin =AdminInfos.objects.get(admin =user)
            context = {'admin':admin }
            return render(request, 'editmyinfo_a.html',context)
    elif request.method == 'POST':#编辑提交
        if user.usertype==0:
            temp_name=request.POST['name']
            temp_fullname=request.POST['fullname']
            temp_grade=request.POST['grade']
            temp_gender=request.POST['gender']
            temp_phone=request.POST['phone']
            temp_address=request.POST['address']
            temp_password=request.POST['password']
            studentinfo=StudentInfos.objects.get(student=user)
            user.ame=temp_name
            user.fullname=temp_fullname
            studentinfo.grade=temp_grade
            user.gender=temp_gender
            user.phone=temp_phone
            user.address=temp_address
            userpassword=temp_password
            user.save()
            studentinfo.save()
        elif user.usertype==1:
            temp_name=request.POST['name']
            temp_fullname=request.POST['fullname']
            temp_education=request.POST['education']
            temp_gender=request.POST['gender']
            temp_phone=request.POST['phone']
            temp_address=request.POST['address']
            temp_password=request.POST['password']
            temp_title=request.POST['title']
            temp_fee=request.POST['fee']
            teacherinfo=TeacherInfos.objects.get(teacher=user)
            user.name=temp_name
            user.fullname=temp_fullname
            teacherinfo.education=temp_education
            teacherinfo.fee=temp_fee
            teacherinfo.title=temp_title
            user.gender=temp_gender
            user.phone=temp_phone
            user.address=temp_address
            userpassword=temp_password
            user.save()
            teacherinfo.save()
        elif user.usertype==2:
            admin =AdminInfos.objects.get(admin =user)
            temp_name=request.POST['name']
            temp_phone=request.POST['phone']
            admin.admin_name=temp_name
            admin.admin_phone=temp_phone
            admin.save()
        return HttpResponseRedirect(reverse('my'))

def my(request):#我的
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    if user.usertype==0:
        student=StudentInfos.objects.get(student=user)
        studentcourses_list=StudentCourses.objects.filter(student=student)
        bookcourseflow_list=BookCourseflow.objects.filter(student=student)
        context = {'notice_list': notice_list,'studentinfo': student,'studentcourses_list':studentcourses_list,'bookcourseflow_list':bookcourseflow_list}
        return render(request, 'my.html',context)
    elif user.usertype==1:
        teacher=TeacherInfos.objects.get(teacher=user)
        context = {'notice_list': notice_list,'teacherinfo': teacher}
        return render(request, 'my_t.html',context)
    elif user.usertype==2:
        admin=AdminInfos.objects.get(admin=user)
        mywork1=Workflow.objects.filter(Q(nextaction=u'待管理员审核')&Q(isselfdesign=True))
        mywork2=Workflow.objects.filter(Q(state=u'管理员审核通过')&Q(isselfdesign=True))
        context = {'admin': admin,'list1count':len(mywork1),'work_list1':mywork1,'list2count':len(mywork2),'work_list2':mywork2}
        return render(request, 'my_a.html',context)

###############################老师相关view##################################################
def mgcourse(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    if user.usertype==1:#老师只管理自己的课程
        teacher=TeacherInfos.objects.get(teacher=user)
        course_list=teacher.teachercourse_set.all()
        context = {'notice_list': notice_list,'teachercourse_list': course_list}
        return render(request, 'mgcourse_t.html',context)
    elif user.usertype==2:#管理员管理所有的课程
        course_list=TeacherCourse.objects.all().order_by('-id')
        context = {'notice_list': notice_list,'teachercourse_list': course_list}
        return render(request, 'mgcourse_a.html',context)

def teachercoursedetail(request,course_id):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    course=TeacherCourse.objects.get(id=course_id)
    context = {'course': course}
    return render(request, 'teachercoursedetail.html',context)

def mgcharge(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    chargelist=Charge.objects.all()
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list,'charge_list':chargelist}
    return render(request, 'mgcharge.html',context)

def addcharge(request):#添加资费
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list}
    if  request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_name = request.POST['name']
        temp_teachertype= request.POST['teachertype']
        temp_grade = request.POST['grade']
        temp_fee = request.POST['fee']
        if Charge.objects.filter(Q(subject=temp_subject)&Q(grade=temp_grade)&Q(name=temp_name)).exists():
            messages.add_message(request,messages.ERROR,'该资费已经存在')
            return render(request, 'addcharge.html')
        else:
            charge = Charge(name=temp_name,grade=temp_grade,subject=temp_subject,teachertype=temp_teachertype,fee=temp_fee)
            charge.save()
            return HttpResponseRedirect(reverse('mgcharge'))#重定向到选题管理页面
    return render(request, 'addcharge.html',context)

def editcharge(request,charge_id):#点击编辑链接跳转到编辑页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid=charge_id
    charge=Charge.objects.get(id=tempid)
    if request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_grade = request.POST['grade']
        temp_name = request.POST['name']
        temp_teachertype = request.POST['teachertype']
        temp_fee = request.POST['fee']
        charge.name=temp_name
        charge.grade=temp_grade
        charge.subject=temp_subject
        charge.teachertype=temp_teachertype
        charge.fee=temp_fee
        charge.save()
        return HttpResponseRedirect(reverse('mgchrge'))#重定向到选题管理页面
    notice_list = Notices.objects.all().order_by('-time')
    context = {'course': charge,'notice_list': notice_list}
    return render(request, 'editcharge.html', context)

def delcharge(request,charge_id):#删除课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid = charge_id
    Charge.objects.filter(id=tempid).delete()
    return HttpResponseRedirect(reverse('mgcharge'))#重定向到选题管理页面

def mgrecruit(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    recruit_list=Recruit.objects.all().order_by('-updatetime')
    notice_list = Notices.objects.all().order_by('-time')
    context = {'recruit_list': recruit_list,'notice_list': notice_list}
    return render(request, 'mgrecruit.html',context)

def addrecruit(request):#
    print("mgrecruit in")
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        print("cook == None")
        return  render(request, 'index.html')
    if request.method == 'POST':
        print("request.method == 'POST'")
        temp_name=request.POST['name']
        temp_minage=request.POST['minage']
        temp_maxage=request.POST['maxage']
        temp_wage=request.POST['wage']
        temp_education=request.POST['education']
        temp_description=request.POST['description']
        temp_phone=request.POST['phone']
        temp_email=request.POST['email']
        recruit=Recruit(name=temp_name,minage=temp_minage,maxage=temp_maxage,wage=temp_wage,\
            education=temp_education,description=temp_description,email=temp_email,phone=temp_phone,updatetime=timezone.now())
        recruit.save()
        messages.add_message(request,messages.INFO,'招聘信息已发布')
    return HttpResponseRedirect(reverse('mgrecruit'))
    
def addcourse(request):#添加课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list}
    if  request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_name = request.POST['name']
        temp_introduce= request.POST['introduce']
        temp_grade = request.POST['grade']
        if TeacherCourse.objects.filter(Q(subject=temp_subject)&Q(grade=temp_grade)&Q(name=temp_name)).exists():
            messages.add_message(request,messages.ERROR,'该课课程已经存在')
            if user.usertype==1:
                messages.add_message(request,messages.ERROR,'请直接在已有课程中选择')
            return HttpResponseRedirect(reverse('addcourse'))
        else:
            teachercourse = TeacherCourse(name=temp_name,grade=temp_grade,subject=temp_subject,introduce=temp_introduce)
            teachercourse.save()
            if user.usertype==1:
                teacher=TeacherInfos.objects.get(teacher=user)
                teachercourse.teacher.add(teacher)
                courseflow=Courseflow(course=teachercourse,state=0,teacher=teacher,time=timezone.now())
                courseflow.save()
                messages.add_message(request,messages.INFO,'自定义课程已提交，可在我的->我的自定义课程 中查看审批状态')
            return HttpResponseRedirect(reverse('mgcourse'))#重定向到选题管理页面
    if user.usertype==1:
        teacher=TeacherInfos.objects.get(teacher=user)
        hascourse_list=teacher.teachercourse_set.all().values('id')
        teachercourse_list = TeacherCourse.objects.exclude(id__in=hascourse_list)
        context = {'teachercourse_list':teachercourse_list,'notice_list': notice_list}
        return render(request, 'addcourse_t.html',context)
    elif user.usertype==2:
        return render(request, 'addcourse_a.html',context)

def addteacher2course(request,course_id):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    course=TeacherCourse.objects.get(id=course_id)
    if user.usertype==1:
        teacher=TeacherInfos.objects.get(teacher=user)
        course.teacher.add(teacher)
        course.save()
        messages.add_message(request,messages.ERROR,'已添加，可在课程管理->我的可授课程 中查看')
    return HttpResponseRedirect(reverse('addcourse'))#重定向到选题管理页面

def rvteacherfromcourse(request,course_id):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    course=TeacherCourse.objects.get(id=course_id)
    if user.usertype==1:
        teacher=TeacherInfos.objects.get(teacher=user)
        course.teacher.remove(teacher)
        course.save()
    return HttpResponseRedirect(reverse('mgcourse'))#重定向到选题管理页面


def reviewcourse(request):#管理员审核老师提交的课程
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    notice_list = Notices.objects.all().order_by('-time')
    courseflow_list1=Courseflow.objects.filter(state=0)
    courseflow_list2=Courseflow.objects.filter(state=1)
    courseflow_list3=Courseflow.objects.filter(state=2)
    context = {'courseflow_list1':courseflow_list1,'courseflow_list2':courseflow_list2,'courseflow_list3':courseflow_list3,'notice_list': notice_list}
    return render(request, 'reviewcourse_a.html',context)

def reviewclick(request,workflow_id):
    cook = request.COOKIES.get("username")#审核课题
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    temp_id=workflow_id
    work=Workflow.objects.get(id=temp_id)
    if request.method == 'POST':
        if 'pass' in request.POST:
            work.state=u'老师审核通过'
            work.nextaction=''
            if work.isselfdesign==True and user.usertype==2:#是自拟课题并且管理员审核通过的，加到系统课题中
                work.state=u'管理员审核通过'
                selfdesign=SelfDefineDesigns.objects.get(subject=work.subject)
                list=Designs.objects.filter(type=selfdesign.type)
                temp_type=selfdesign.type
                temp_idnum=temp_type+str(list.count()+101)
                desig = Designs(teacher=selfdesign.teacher,idno=temp_idnum,type=selfdesign.type,subject=selfdesign.subject,introduce=selfdesign.introduce)
                desig.save()
        elif 'back' in request.POST:
            work.state='打回'
            work.nextaction='请重新选题'
            if work.isselfdesign==True:
                selfdesig=SelfDefineDesigns.objects.get(subject=work.subject)
                selfdesig.state=4
                selfdesig.save()

        elif 'passandsubmit' in request.POST:
            selfdesig=SelfDefineDesigns.objects.get(subject=work.subject)
            work.state='老师审核通过'
            work.nextaction='待管理员审核'
            selfdesig.state=2
            selfdesig.save()
    work.save()
    return HttpResponseRedirect(reverse('reviewcourse'))
    
def reviewselfdesign(request,selfdesign_id):
    cook = request.COOKIES.get("username")#审核课题
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    temp_id=selfdesign_id
    self
    work=Workflow.objects.get(id=temp_id)
    if request.method == 'POST':
        if 'pass' in request.POST:
            work.state='审核通过'
        elif 'back' in request.POST:
            work.state='打回'
    work.save()
    return HttpResponseRedirect(reverse('reviewcourse'))

def editcourse(request,course_id):#点击编辑链接跳转到编辑页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid=course_id
    course=TeacherCourse.objects.get(id=tempid)
    if request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_grade = request.POST['grade']
        temp_name = request.POST['name']
        temp_introduce= request.POST['introduce']
        course.name=temp_name
        course.grade=temp_grade
        course.subject=temp_subject
        course.introduce=temp_introduce
        course.save()
        return HttpResponseRedirect(reverse('mgcourse'))#重定向到选题管理页面
    notice_list = Notices.objects.all().order_by('-time')
    context = {'course': course,'notice_list': notice_list}
    return render(request, 'editcourse.html', context)

def delcourse(request,course_id):#删除课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid = course_id
    TeacherCourse.objects.filter(id=tempid).delete()
    return HttpResponseRedirect(reverse('mgcourse'))#重定向到选题管理页面

###############################管理员相关view##################################################
def mgstudent(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    studentinfo_list = StudentInfos.objects.all()
    print('studentinfo_list.count():', studentinfo_list.count())
    context = {'studentinfo_list': studentinfo_list}
    return render(request, 'mgstudent.html',context)

def addstudent(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    if request.method == 'POST':
        student_id = request.POST["username"]
        student_psw = request.POST['password']
        student_name= request.POST['name']

        if Users.objects.filter(name=student_id,usertype=0).exists():
            messages.add_message(request,messages.ERROR,'该学生已经存在')
            return render(request, 'mgstudent.html')
        else:
            user=Users(usertype=0,name=student_id,password=student_psw)
            user.save()
            student=StudentInfos(student=user,student_name=student_name)
            student.save()
            return HttpResponseRedirect(reverse('mgstudent'))
    return render(request, 'mgstudent.html')

def delstudent(request,user_id):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')#如果没有登录返回到入口页面
    tempid = user_id
    Users.objects.filter(id=tempid).delete()
    return HttpResponseRedirect(reverse('mgstudent'))#重定向到老师管理页面

#管理老师相关接口
def mgteacher(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    teacherinfo_list = TeacherInfos.objects.all()
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list,'teacherinfo_list': teacherinfo_list}
    return render(request, 'mgteacher.html',context)

def addteacher(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    if request.method == 'POST':
        teacher_id = request.POST["username"]
        teacher_psw = request.POST['password']
        teacher_name= request.POST['name']

        if Users.objects.filter(name=teacher_id,usertype=1).exists():
            messages.add_message(request,messages.ERROR,'该老师已经存在')
            return render(request, 'mgteacher.html')
        else:
            user=Users(usertype=1,name=teacher_id,password=teacher_psw)
            user.save()
            teacher=TeacherInfos(teacher=user,teacher_name=teacher_name)
            teacher.save()
            return HttpResponseRedirect(reverse('mgteacher'))
    return render(request, 'mgteacher.html')

def delteacher(request,user_id):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid = user_id
    Users.objects.filter(id=tempid).delete()
    return HttpResponseRedirect(reverse('mgteacher'))#重定向到老师管理页面

def mgmessage(request):#留言管理
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    if user.usertype==0:
        return render(request, 'studentcoursedetail.html',context)
    elif user.usertype==1:
        teacherinfo=TeacherInfos.objects.get(teacher=user)
        messages1=Messages.objects.filter(Q(reply='')&Q(teacher=teacherinfo))
        messages2=Messages.objects.filter(~Q(reply='')&Q(teacher=teacherinfo))
        notice_list = Notices.objects.all().order_by('-time')
        context = {'message_list1':messages1,'message_list2':messages2,'notice_list':notice_list}
        return render(request, 'mgmessage_t.html',context)
    elif user.usertype==2:
        return render(request, 'studentcoursedetail_a.html',context)
    return render(request, 'mgmessage.html',context)

def processmsg(request,message_id):#删除或回复留言
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    temp_id=message_id
    if request.method == 'POST':
        if 'delmsg' in request.POST:
            Messages.objects.filter(id= temp_id).delete()#删除留言
            return HttpResponseRedirect(reverse('mgmessage'))
        elif 'replymsg' in request.POST:#回复留言
            message=Messages.objects.get(id=temp_id)
            context={'message':message}
            return render(request, 'replymessage.html',context)
    return HttpResponseRedirect(reverse('mgmessage'))

def replymsg(request,message_id):#删除或回复留言
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    temp_id=message_id
    if request.method == 'POST':
        temp_reply_content=request.POST.get('replycontent')
        message=Messages.objects.get(id=temp_id)
        message.reply=temp_reply_content
        message.updatetime=timezone.now()
        message.save()
    return HttpResponseRedirect(reverse('mgmessage'))

def leavmessage(request,teacher_id):#留言
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    teacher=Users.objects.get(id=teacher_id)
    teacherinfo=TeacherInfos.objects.get(teacher=teacher)
    if request.method == 'POST':
        temp_message=request.POST.get('message')
        student=StudentInfos.objects.get(student=user)
        message=Messages(fromuser=student,text=temp_message,reply='',teacher=teacherinfo,updatetime=timezone.now())
        message.save()
        messages.add_message(request,messages.INFO,'留言成功，可在 消息 中查看留言回复')
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list,'teacher':teacher}
    return render(request, 'leavemessage.html',context)

def addnotice(request):#
    print("addnotice in")
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        print("cook == None")
        return  render(request, 'index.html')
    if request.method == 'POST':
        print("request.method == 'POST'")
        temp_title=request.POST['title']
        temp_text=request.POST['noticetext']
        notice=Notices(title=temp_title,text=temp_text,time=timezone.now())
        notice.save()
        print(notice.text)
    return HttpResponseRedirect(reverse('home'))

###############################学生相关view##################################################
def selectdesign(request):#选题页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    design_list=Designs.objects.all()
    teacher_list=TeacherInfos.objects.all()
    context = {'design_list': design_list,'teacher_list':teacher_list}
    return render(request, 'selectdesign.html',context)

def selecteddesign(request,design_idno):#确定选择某一个课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    student=StudentInfos.objects.get(student=user)
    if Workflow.objects.filter(Q(fromuser=student)&(~Q(state=u'打回'))).exists():
        messages.add_message(request,messages.ERROR,'你已经选择了课题，不能多次选择')
        design_list=Designs.objects.all()
        context = {'design_list': design_list}
        return render(request, 'selectdesign.html',context)
    tmep_idno=design_idno
    design =Designs.objects.get(idno=tmep_idno)
    design_list=Designs.objects.all()
    teacher=Users.objects.get(name=design.teacher.teacher.name)
    #建立任务流
    workflow=Workflow(fromuser=student,currentuser=teacher.name,subject=design.subject,state=u'已提交',nextaction=u'待老师审核',isselfdesign=False,updatetime=timezone.now())
    workflow.save()
    messages.add_message(request,messages.INFO,'你已经选择《'+design.subject+'》课题，可在 我的->毕业进程 中关注最新进展')
    context = {'design_list': design_list}
    return render(request, 'selectdesign.html',context)

def searchdesign(request):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    filter_count=0
    design_list=Designs.objects.all()

    print('count1',len(design_list))
    temp_keyword=request.POST['search_content']
    if temp_keyword!=None and temp_keyword!='':
        design_list=design_list.filter(Q(subject__contains=temp_keyword)|Q(introduce__contains=temp_keyword)\
            |Q(idno__contains=temp_keyword)|Q(type__contains=temp_keyword))
        filter_count+=1
        print('count2',len(design_list))
    teacher_list=TeacherInfos.objects.all()
    temp_teacher= request.POST['search_teacher']
    if temp_teacher!=None and temp_teacher!='':
        teacher=TeacherInfos.objects.get(teacher_name=temp_teacher)
        design_list=design_list.filter(teacher=teacher)
        filter_count+=1
        print('count3',len(design_list))
    temp_type= request.POST.get('type') 
    if temp_type!=None and temp_type!='':
        print('type',temp_type)
        design_list=design_list.filter(type=temp_type)
        filter_count+=1
        print('count4',len(design_list))
    if filter_count==0:
        messages.add_message(request,messages.ERROR,'至少要有一个筛选条件')
        context = {'design_list': design_list,'teacher_list':teacher_list}
        return render(request, 'selectdesign.html',context)
    if len(design_list)==0:
        messages.add_message(request,messages.INFO,'没有符合条件的搜索结果')
    else:
        messages.add_message(request,messages.INFO,'共'+str(len(design_list))+'条结果')
    context = {'design_list': design_list,'teacher_list':teacher_list}
    print('好困好困:',len(teacher_list))
    if user.usertype==2:
        return render(request, 'mgdesign_a.html',context)
    elif user.usertype==0:
        return render(request, 'selectdesign.html',context)

def definedesign(request):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    student=StudentInfos.objects.get(student=user)
    if  request.method == 'POST':
        if Workflow.objects.filter(Q(fromuser=student)&(~Q(state=u'打回'))).exists():
            messages.add_message(request,messages.ERROR,'你已经选择了课题，不能再自拟题目')
            return render(request, 'definedesign.html')
        temp_subject = request.POST['subject']
        temp_type = request.POST['type']
        temp_introduce= request.POST['introduce']
        temp_teacher=request.POST['teacher']
        print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu:',temp_teacher)
        if Designs.objects.filter(subject=temp_subject).exists():
            messages.add_message(request,messages.ERROR,'该课题已经存在')
            return render(request, 'definedesign.html')
        else:
            teacher=TeacherInfos.objects.get(teacher_name=temp_teacher)

            desig = SelfDefineDesigns(student=student,teacher=teacher,type=temp_type,subject=temp_subject,introduce=temp_introduce,state=0)
            desig.save()
            
            #建立任务流
            workflow=Workflow(fromuser=student,currentuser=teacher.teacher.name,subject=temp_subject,state=u'已提交',nextaction='待老师审核',isselfdesign=True,updatetime=timezone.now())
            workflow.save()
            messages.add_message(request,messages.INFO,'你已经自拟《'+temp_subject+'》课题，可在 我的->毕业进程 中关注最新进展')
            return render(request, 'definedesign.html')
    teacher_list=TeacherInfos.objects.all()
    content={'teacher_list':teacher_list}
    return render(request, 'definedesign.html',content)

def checkcharge(request):#资费标准
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    charge_list=Charge.objects.all()
    notice_list = Notices.objects.all().order_by('-time')
    content = {'notice_list': notice_list,'charge_list':charge_list}
    return render(request, 'checkcharge.html',content)


def publicneed(request):#选题页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    student=StudentInfos.objects.get(student=user)
    if  request.method == 'POST':
        temp_name = request.POST['name']
        temp_grade = request.POST['grade']
        temp_subject = request.POST['subject']
        temp_demand = request.POST['demand']
        temp_phone = request.POST['phone']
        temp_address = request.POST['address']
        studentcourse=StudentCourses(student=student,name=temp_name,grade=temp_grade,subject=temp_subject,demand=temp_demand,phone=temp_phone,address=temp_address)
        studentcourse.save()
        messages.add_message(request,messages.INFO,'已发布《'+temp_name+'》需求，可在 我的->我的需求 中查看')
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list}
    return render(request, 'publicneed.html',context)

def bookteacher(request,teacher_id):#预约老师
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user=Users.objects.get(name=cook)
    student=StudentInfos.objects.get(student=user)
    teacher=Users.objects.get(id=teacher_id)
    teacherinfo=TeacherInfos.objects.get(teacher=teacher)
    if  request.method == 'POST':
        temp_name = request.POST['name']
        temp_phone = request.POST['phone']
        temp_mail = request.POST['mail']
        temp_address = request.POST['address']
        temp_demand = request.POST['demand']
        bookcourseflow=BookCourseflow(student=student,callname=temp_name,teacher=teacherinfo,phone=temp_phone,mail=temp_mail,address=temp_address,demand=temp_demand)
        bookcourseflow.save()
        messages.add_message(request,messages.INFO,'预约已提交，可在 我的->我的预约 中查看')
    notice_list = Notices.objects.all().order_by('-time')
    context = {'teacher': teacher,'notice_list': notice_list}
    return render(request, 'bookteacher.html',context)

def cancelbook(request,bookflow_id):#取消预约
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user=Users.objects.get(name=cook)
    bookflow=BookCourseflow.objects.get(id=bookflow_id)
    bookflow.state=4
    bookflow.save()
    return HttpResponseRedirect(reverse('my'))

def processbook(request,bookflow_id,state):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user=Users.objects.get(name=cook)
    bookflow=BookCourseflow.objects.get(id=bookflow_id)
    bookflow.state=state
    bookflow.save()
    if state==0:
        messages.add_message(request,messages.INFO,'已提交预约')
    elif state==1:
        messages.add_message(request,messages.INFO,'已接受预约')
    elif state==2:
        messages.add_message(request,messages.INFO,'已完成')
    elif state==3:
        messages.add_message(request,messages.INFO,'已拒绝预约')
    elif state==4:
        messages.add_message(request,messages.INFO,'已取消预约')
    return HttpResponseRedirect(reverse('my'))


def markteacher(request,bookflow_id):#根据预约上课情况给老师打分
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user=Users.objects.get(name=cook)
    bookcourseflow=BookCourseflow.objects.get(id=bookflow_id)
    if  request.method == 'POST':
        temp_mark = request.POST['mark']
        bookcourseflow.teacher.mark=(bookcourseflow.teacher.mark*bookcourseflow.teacher.marknum+int(temp_mark))/(bookcourseflow.teacher.marknum+1)
        bookcourseflow.teacher.save()
        bookcourseflow.teacher.marknum+=1
        messages.add_message(request,messages.INFO,'评价成功')
        return HttpResponseRedirect(reverse('my'))
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list,'bookcourseflow':bookcourseflow}
    return render(request, 'mark.html',context)
    
def studentcoursedetail(request,stcourse_id):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html',context)
    user=Users.objects.get(name=cook)
    temp_stcourse_id=stcourse_id
    studentcourse=StudentCourses.objects.get(id=temp_stcourse_id)
    notice_list = Notices.objects.all().order_by('-time')
    context = {'studentcourse': studentcourse,'notice_list': notice_list}
    if user.usertype==0:
        return render(request, 'studentcoursedetail.html',context)
    elif user.usertype==1:
        return render(request, 'studentcoursedetail_t.html',context)
    elif user.usertype==2:
        return render(request, 'studentcoursedetail_a.html',context)

def teacherdetail(request,teacher_id):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html',context)
    user=Users.objects.get(name=cook)
    temp_id=teacher_id
    teacherinfo=TeacherInfos.objects.get(id=temp_id)
    course_list=  teacherinfo.teachercourse_set.all()
    context = {'teacherinfo': teacherinfo,'course_list': course_list}
    return render(request, 'teacherdetail.html',context)

def studentdetail(request,student_id):
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html',context)
    user=Users.objects.get(name=cook)
    temp_id=student_id
    studentinfo=StudentInfos.objects.get(id=temp_id)
    context = {'studentinfo': studentinfo}
    return render(request, 'studentdetail.html',context)