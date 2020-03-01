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
    path('designdetail/<subject>', views.designdetail, name='designdetail'),
    path('editmyinfo/', views.editmyinfo, name='editmyinfo'),

    path('reviewdesign/', views.reviewdesign, name='reviewdesign'),
    path('reviewclick/<workflow_id>', views.reviewclick, name='reviewclick'),
    path('mgcourse/', views.mgcourse, name='mgcourse'),
    path('mgcost/', views.mgcost, name='mgcost'),
    path('mgrecruit/', views.mgrecruit, name='mgrecruit'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('delcourse/<course_id>', views.delcourse, name='delcourse'),
    path('editcourse/<course_id>', views.editcourse, name='editcourse'),
    #path('submitdesign/', views.submitdesign, name='submitdesign'),
    path('definedesign/', views.definedesign, name='definedesign'),

    path('mgstudent/', views.mgstudent, name='mgstudent'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('delstudent/<user_id>', views.delstudent, name='delstudent'),
    path('mgteacher/', views.mgteacher, name='mgteacher'),
    path('addteacher', views.addteacher, name='addteacher'),
    path('delteacher/<user_id>', views.delteacher, name='delteacher'),
    path('addnotice/', views.addnotice, name='addnotice'),

    path('selectdesign/', views.selectdesign, name='selectdesign'),
    path('definedesign/', views.definedesign, name='definedesign'),
    path('searchdesign/', views.searchdesign, name='searchdesign'),
    path('selecteddesign/<design_idno>', views.selecteddesign, name='selecteddesign'),
    path('leavmessage/', views.leavmessage, name='leavmessage'),

    path('mgmessage/', views.mgmessage, name='mgmessage'),
    path('processmsg/<message_id>', views.processmsg, name='processmsg'),
    path('replymsg/<message_id>', views.replymsg, name='replymsg'),

    path('checkcost/', views.checkcost, name='checkcost'),
    path('publicneed/', views.publicneed, name='publicneed'),
    path('bookteacher/<teacher_id>', views.bookteacher, name='bookteacher'),
    path('studentcoursedetail/<stcourse_id>', views.studentcoursedetail, name='studentcoursedetail'),

]
