# Generated by Django 2.2.3 on 2020-03-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20200301_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookcourseflow',
            old_name='email',
            new_name='mail',
        ),
        migrations.AddField(
            model_name='bookcourseflow',
            name='callname',
            field=models.CharField(default='', max_length=20),
        ),
    ]
