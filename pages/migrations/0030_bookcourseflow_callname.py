# Generated by Django 2.2.3 on 2020-03-08 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_auto_20200308_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcourseflow',
            name='callname',
            field=models.CharField(default='', max_length=30),
        ),
    ]
