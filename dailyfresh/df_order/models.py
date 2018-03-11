from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=30)
    oaddress = models.CharField(max_length=100)
    oIspay = models.BooleanField(default=False)
    odate = models.DateTimeField(auto_now=True)
    ototal = models.DecimalField(max_digits=7,decimal_places=2)
    user = models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)

    class Meta(object):
        db_table = 'orderinfo'

class OrderDetail(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    order = models.ForeignKey('OrderInfo',on_delete=models.CASCADE)
    count = models.IntegerField()
    subtotal = models.DecimalField(max_digits=7,decimal_places=2)

    class Meta(object):
        db_table = 'orderdetail'


