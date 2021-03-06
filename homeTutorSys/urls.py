"""homeTutorSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),

    path('msgcenter/', views.msgcenter, name='msgcenter'),
    path('my/', views.my, name='my'),
    path('logout/', views.logout, name='logout'),
    path('editmyinfo/', views.editmyinfo, name='editmyinfo'),

    path('reviewcourse/', views.reviewcourse, name='reviewcourse'),
    path('processcourseflow/<courseflow_id><state>', views.processcourseflow, name='processcourseflow'),
    path('mgcourse/', views.mgcourse, name='mgcourse'),
    path('mgcharge/', views.mgcharge, name='mgcharge'),
    path('mgrecruit/', views.mgrecruit, name='mgrecruit'),
    path('recruitinfo/', views.recruitinfo, name='recruitinfo'),
    path('addrecruit/', views.addrecruit, name='addrecruit'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('delcourse/<course_id>', views.delcourse, name='delcourse'),
    path('editcourse/<course_id>', views.editcourse, name='editcourse'),
    path('addteacher2course/<course_id>', views.addteacher2course, name='addteacher2course'),
    path('rvteacherfromcourse/<course_id>', views.rvteacherfromcourse, name='rvteacherfromcourse'),
    path('teachercoursedetail/<course_id>', views.teachercoursedetail, name='teachercoursedetail'),
    path('mgstudent/', views.mgstudent, name='mgstudent'),
    path('delstudent/<user_id>', views.delstudent, name='delstudent'),
    path('mgteacher/', views.mgteacher, name='mgteacher'),
    path('delteacher/<user_id>', views.delteacher, name='delteacher'),
    path('addnotice/', views.addnotice, name='addnotice'),
    path('leavmessage/<teacher_id>', views.leavmessage, name='leavmessage'),
    path('delmsg/<message_id>', views.delmsg, name='delmsg'),
    path('replymsg/<message_id>', views.replymsg, name='replymsg'),
    path('checkcharge/', views.checkcharge, name='checkcharge'),
    path('publicneed/', views.publicneed, name='publicneed'),
    path('bookteacher/<teacher_id>', views.bookteacher, name='bookteacher'),
    path('processbook/<bookflow_id><state>', views.processbook, name='processbook'),
    path('markteacher/<bookflow_id>', views.markteacher, name='markteacher'),
    path('studentcoursedetail/<stcourse_id>', views.studentcoursedetail, name='studentcoursedetail'),
    path('editcharge/<charge_id>', views.editcharge, name='editcharge'),
    path('delcharge/<charge_id>', views.delcharge, name='delcharge'),
    path('teacherdetail/<teacher_id>', views.teacherdetail, name='teacherdetail'),
    path('studentdetail/<student_id>', views.studentdetail, name='studentdetail'),
    path('addcharge', views.addcharge, name='addcharge'),
]
