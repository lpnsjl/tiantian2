# Generated by Django 2.0.1 on 2018-01-29 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=20)),
                ('uemail', models.CharField(max_length=20)),
                ('ushou', models.CharField(max_length=10)),
                ('uaddress', models.CharField(max_length=50)),
                ('uphone', models.CharField(max_length=11)),
                ('uyoubian', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
    ]
