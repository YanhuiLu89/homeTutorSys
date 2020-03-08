# Generated by Django 2.2.3 on 2020-03-01 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_auto_20200301_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookcourseflow',
            name='course',
        ),
        migrations.AddField(
            model_name='bookcourseflow',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='bookcourseflow',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='bookcourseflow',
            name='phone',
            field=models.CharField(default='', max_length=50),
        ),
    ]