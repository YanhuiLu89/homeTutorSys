# Generated by Django 2.2.3 on 2020-02-25 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('time', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(default='', max_length=40)),
                ('student_phone', models.CharField(max_length=40)),
                ('student_grade', models.CharField(max_length=40)),
                ('student_address', models.CharField(max_length=200)),
                ('student_class', models.CharField(max_length=40)),
                ('student_major', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.IntegerField(default=0)),
                ('userid', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentuser', models.IntegerField(default=0)),
                ('subject', models.CharField(default='', max_length=200)),
                ('state', models.CharField(max_length=100)),
                ('nextaction', models.CharField(max_length=100)),
                ('isselfdesign', models.BooleanField(default=False)),
                ('updatetime', models.DateTimeField(verbose_name='date published')),
                ('fromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.StudentInfos')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(default='', max_length=40)),
                ('teacher_phone', models.CharField(max_length=40)),
                ('teacher_title', models.CharField(max_length=200)),
                ('teacher_major', models.CharField(max_length=100)),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.Users')),
            ],
        ),
        migrations.AddField(
            model_name='studentinfos',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.Users'),
        ),
        migrations.CreateModel(
            name='SelfDefineDesigns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='XG', max_length=100)),
                ('subject', models.CharField(default='', max_length=200)),
                ('introduce', models.CharField(max_length=500)),
                ('state', models.IntegerField(default=3)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.StudentInfos')),
                ('teacher', models.ForeignKey(on_delete=models.SET(None), to='pages.TeacherInfos')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('reply', models.CharField(max_length=500)),
                ('updatetime', models.DateTimeField(verbose_name='date published')),
                ('fromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.StudentInfos')),
            ],
        ),
        migrations.CreateModel(
            name='Designs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idno', models.CharField(default='XG101', max_length=10)),
                ('type', models.CharField(default='XG', max_length=100)),
                ('subject', models.CharField(default='', max_length=200)),
                ('introduce', models.CharField(max_length=500)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.TeacherInfos')),
            ],
        ),
        migrations.CreateModel(
            name='AdminInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(default='', max_length=40)),
                ('admin_phone', models.CharField(max_length=40)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pages.Users')),
            ],
        ),
    ]
