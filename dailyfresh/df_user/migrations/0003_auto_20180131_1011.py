# Generated by Django 2.0.1 on 2018-01-31 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180129_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='upwd',
            field=models.CharField(max_length=100),
        ),
    ]