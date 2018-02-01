from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    class Meta(object):
        db_table = 'goods_type'

    def __str__(self):
        return self.title


class GoodsInfo(models.Model):
    gname = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='')
    gprice = models.DecimalField(max_digits=6, decimal_places=2)
    gclick = models.IntegerField()
    gkucun = models.IntegerField()
    gjianjie = models.CharField(max_length=255)
    gcontent = HTMLField()
    gunit = models.CharField(max_length=10)
    is_delete = models.BooleanField(default=False)
    gtype = models.ForeignKey('TypeInfo', on_delete=models.CASCADE)

    def __str__(self):
        return self.gname

    class Meta(object):
        db_table = 'goodsinfo'


