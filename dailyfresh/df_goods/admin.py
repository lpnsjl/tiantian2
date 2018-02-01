from django.contrib import admin
from df_goods.models import *


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','title','is_delete']
    list_filter = ['title']
    search_fields = ['title']
    list_per_page = 3


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'gname', 'gprice','gunit','gkucun','gclick','gtype']
    list_filter = ['gname']
    search_fields = ['gname']
    list_per_page = 10


admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)