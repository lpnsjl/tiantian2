from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=20)
    uemail = models.CharField(max_length=20)
    ushou = models.CharField(max_length=10, default='')
    uaddress = models.CharField(max_length=50,default='')
    uphone = models.CharField(max_length=11,default='')
    uyoubian = models.CharField(max_length=6,default='')

    class Meta(object):
        db_table = 'userinfo'


