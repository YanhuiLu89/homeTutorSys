# Generated by Django 2.2.3 on 2020-03-07 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_auto_20200307_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherinfos',
            name='education',
            field=models.CharField(default='本科', max_length=40),
        ),
    ]
