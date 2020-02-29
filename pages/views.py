from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q 
from django.utils import timezone

from .models import Users,TeacherInfos,StudentInfos,Notices,Messages,TeacherCourse,StudentCourses,Courseflow
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
                    teacherinfo_list = TeacherInfos.objects.all()
                    context = {'teacherinfo_list': teacherinfo_list,'notice_list': notice_list}
                    response=render(request, 'homepage.html',context)
                elif user.usertype==1:
                    print("11111111111111111111111111111111")
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
    if user.usertype==0:
        student=StudentInfos.objects.get(student=user)
        messages=Messages.objects.filter(Q(fromuser=student)&~Q(reply=''))
        content={'message_list':messages}
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
    if request.method == 'GET':#连接到信息编辑页面
        if user.usertype==0:
            student=StudentInfos.objects.get(student=user)
            context = {'student': student}
            return render(request, 'editmyinfo.html',context)
        elif user.usertype==1:
            teacher=TeacherInfos.objects.get(teacher=user)
            context = {'teacher':teacher}
            return render(request, 'editmyinfo_t.html',context)
        elif user.usertype==2:
            admin =AdminInfos.objects.get(admin =user)
            context = {'admin':admin }
            return render(request, 'editmyinfo_a.html',context)
    elif request.method == 'POST':#编辑提交
        if user.usertype==0:
            temp_name=request.POST['name']
            temp_major=request.POST['major']
            temp_grade=request.POST['grade']
            temp_class=request.POST['class']
            temp_phone=request.POST['phone']
            temp_address=request.POST['address']
            student=StudentInfos.objects.get(student=user)
            student.student_name=temp_name
            student.student_major=temp_major
            student.student_grade=temp_grade
            student.student_class=temp_class
            student.student_phone=temp_phone
            student.student_address=temp_address
            student.save()
        elif user.usertype==1:
            temp_name=request.POST['name']
            temp_major=request.POST['major']
            temp_title=request.POST['title']
            temp_phone=request.POST['phone']
            teacher=TeacherInfos.objects.get(teacher=user)
            teacher=TeacherInfos.objects.get(teacher=user)
            teacher.teacher_name=temp_name
            teacher.teacher_major=temp_major
            teacher.teacher_phone=temp_phone
            teacher.teacher_title=temp_title
            teacher.save()
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
    if user.usertype==0:
        student=StudentInfos.objects.get(student=user)
        # myneed=StudentCourses.objects.filter(student=student)
        context = {'student': student}
        return render(request, 'my.html',context)
    elif user.usertype==1:
        teacher=TeacherInfos.objects.get(teacher=user)
        mywork1=Workflow.objects.filter(Q(currentuser=user.name)&Q(nextaction=u'待老师审核'))
        mywork2=Workflow.objects.filter(Q(currentuser=user.name)&Q(state=u'老师审核通过'))
        context = {'teacher': teacher,'list1count':len(mywork1),'work_list1':mywork1,'list2count':len(mywork2),'work_list2':mywork2}
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
        design_list=Designs.objects.filter(teacher=teacher)
        context = {'design_list': design_list}
        return render(request, 'mgcourse.html',context)
    elif user.usertype==2:#管理员管理所有的课程
        course_list=TeacherCourse.objects.all().order_by('-id')
        context = {'notice_list': notice_list,'teachercourse_list': course_list}
        return render(request, 'mgcourse_a.html',context)

def mgcost(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    if user.usertype==1:#老师只管理自己的课程
        teacher=TeacherInfos.objects.get(teacher=user)
        design_list=Designs.objects.filter(teacher=teacher)
        context = {'design_list': design_list}
        return render(request, 'mgcost.html',context)
    elif user.usertype==2:#管理员管理所有的课程
        teacher_list=TeacherInfos.objects.all()
        design_list=Designs.objects.all()
        context = {'design_list': design_list,'teacher_list':teacher_list}
        print('好困好困:',len(teacher_list))
        return render(request, 'mgcost_a.html',context)

def mgrecruit(request):#
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    recruit_list=Recruit.objects.all()
    context = {'recruit_list': recruit_list}
    return render(request, 'mgrecruit.html',context)
    
def addcourse(request):#添加课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    if  request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_type = request.POST['type']
        temp_introduce= request.POST['introduce']
        if Designs.objects.filter(subject=temp_subject).exists():
            messages.add_message(request,messages.ERROR,'该课题已经存在')
            return render(request, 'addcourse.html')
        else:
            #自动计算编号
            list=Designs.objects.filter(type=temp_type)
            print('count:',list.count())
            temp_idnum=temp_type+str(list.count()+101)
            print('temp_idnum:',temp_idnum)
            teacher=TeacherInfos.objects.get(teacher=user)
            desig = Designs(teacher=teacher,idno=temp_idnum,type=temp_type,subject=temp_subject,introduce=temp_introduce)
            desig.save()
            return HttpResponseRedirect(reverse('mgdcourse'))#重定向到选题管理页面
    notice_list = Notices.objects.all().order_by('-time')
    context = {'notice_list': notice_list}
    return render(request, 'addcourse.html',context)

def reviewdesign(request):#
    cook = request.COOKIES.get("username")#审核课题
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    user = Users.objects.get(name = cook)
    if user.usertype==1:#老师审核选题和自拟题
        works1=Workflow.objects.filter(Q(currentuser=user.name)&Q(nextaction=u'待老师审核')&Q(isselfdesign=False))
        works2=Workflow.objects.filter(Q(currentuser=user.name)&Q(nextaction=u'待老师审核')&Q(isselfdesign=True))
        context = {'work_list1':works1,'work_list2':works2}
        return render(request, 'reviewdesign.html',context)
    elif user.usertype==2:#老师审核自拟题目
        works=Workflow.objects.filter(Q(nextaction=u'待管理员审核')&Q(isselfdesign=True))
        context = {'work_list':works}
        return render(request, 'reviewdesign_a.html',context)

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
    return HttpResponseRedirect(reverse('reviewdesign'))
    
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
    return HttpResponseRedirect(reverse('reviewdesign'))

def editcourse(request,design_idno):#点击编辑链接跳转到编辑页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid=design_idno
    design=Designs.objects.get(idno=tempid)
    if request.method == 'POST':
        temp_subject = request.POST['subject']
        temp_type = request.POST['type']
        temp_introduce= request.POST['introduce']
        if temp_type!=design.type:#类型变了重新计算编号
            list=Designs.objects.filter(type=temp_type)
            temp_idnum=temp_type+str(list.count()+101)
            design.idno=temp_idnum
            design.type=temp_type
        design.subject=temp_subject
        design.introduce=temp_introduce
        design.save()
        return HttpResponseRedirect(reverse('mgdesign'))#重定向到选题管理页面
    context = {'curdesign': design}
    return render(request, 'editdesign.html', context)

def delcourse(request,design_idno):#删除课题
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    tempid = design_idno
    design=Designs.objects.get(idno=tempid)
    Workflow.objects.filter(subject=design.subject).delete()#课题被删除时对应的任务页删除
    Designs.objects.filter(idno=design_idno).delete()
    return HttpResponseRedirect(reverse('mgdesign'))#重定向到选题管理页面

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
    teacher_list = TeacherInfos.objects.all()
    context = {'teacher_list': teacher_list}
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
    Users.objects.filter(name=tempid).delete()
    return HttpResponseRedirect(reverse('mgteacher'))#重定向到老师管理页面

def mgmessage(request):#留言管理
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    messages1=Messages.objects.filter(reply='')
    messages2=Messages.objects.filter(~Q(reply=''))
    context = {'message_list1':messages1,'message_list2':messages2}
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

def leavmessage(request):#留言
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    if request.method == 'POST':
        temp_message=request.POST.get('message')
        user = Users.objects.get(name = cook)
        student=StudentInfos.objects.get(student=user)
        message=Messages(fromuser=student,text=temp_message,reply='',updatetime=timezone.now())
        message.save()
        messages.add_message(request,messages.INFO,'留言成功，可在 消息 中查看留言回复')
    return HttpResponseRedirect(reverse('home'))

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

def checkcost(request):#选题页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    design_list=Designs.objects.all()
    teacher_list=TeacherInfos.objects.all()
    context = {'design_list': design_list,'teacher_list':teacher_list}

def publicneed(request):#选题页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    design_list=Designs.objects.all()
    teacher_list=TeacherInfos.objects.all()
    context = {'design_list': design_list,'teacher_list':teacher_list}

def bookteacher(request,teacher_id):#选题页面
    cook = request.COOKIES.get("username")
    print('cook:', cook)
    if cook == None:
        return  render(request, 'index.html')
    design_list=Designs.objects.all()
    teacher_list=TeacherInfos.objects.all()
    context = {'design_list': design_list,'teacher_list':teacher_list}

    