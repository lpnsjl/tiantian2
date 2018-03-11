from django.shortcuts import *
from df_goods.models import *
from django.http import Http404
from django.core.paginator import Paginator
import datetime


def index(request):
    session_id = request.COOKIES.get('session_id','')
    user = request.session.get(session_id)

    type0 = TypeInfo.objects.get(title='新鲜水果')
    goods00 = type0.goodsinfo_set.order_by('-id')[0:4]
    goods01 = type0.goodsinfo_set.order_by('-gclick')[0:4]

    type1 = TypeInfo.objects.get(title='海鲜水产')
    goods10 = type1.goodsinfo_set.order_by('-id')[0:4]
    goods11 = type1.goodsinfo_set.order_by('-gclick')[0:4]

    type2 = TypeInfo.objects.get(title='猪牛羊肉')
    goods20 = type2.goodsinfo_set.order_by('-id')[0:4]
    goods21 = type2.goodsinfo_set.order_by('-gclick')[0:4]

    type3 = TypeInfo.objects.get(title='禽类蛋品')
    goods30 = type3.goodsinfo_set.order_by('-id')[0:4]
    goods31 = type3.goodsinfo_set.order_by('-gclick')[0:4]

    type4 = TypeInfo.objects.get(title='新鲜蔬菜')
    goods40 = type4.goodsinfo_set.order_by('-id')[0:4]
    goods41 = type4.goodsinfo_set.order_by('-gclick')[0:4]

    type5 = TypeInfo.objects.get(title='速冻食品')
    goods50 = type5.goodsinfo_set.order_by('-id')[0:4]
    goods51 = type5.goodsinfo_set.order_by('-gclick')[0:4]

    #types = {type0:[goods00,goods01],type0:[goods00,goods01],type0:[goods00,goods01],}
    context = {
        'goods00': goods00, 'goods01': goods01,
        'goods10': goods10, 'goods11': goods11,
        'goods20': goods20, 'goods21': goods21,
        'goods30': goods30, 'goods31': goods31,
        'goods40': goods40, 'goods41': goods41,
        'goods50': goods50, 'goods51': goods51,
        'title':'首页',
        'session_id': session_id,
        'user':user,
    }
    return render(request, 'df_goods/index.html',context)
############################################################################
# def test(request):
#     a = 'abccca'
#     context = {
#         'a':a,
#         'list':['a','<h1>mm</h1>'],
#         'html':'<h1>html转义</h1>',
#
#     }
#     return render(request,'test.html',context)
############################################################################

def detail(request,id):
    # try:
    session_id = request.COOKIES.get('session_id', '')
    user = request.session.get(session_id)
    news = GoodsInfo.objects.order_by('-id')[0:2]
    goods = GoodsInfo.objects.get(id=id)
    type_id = goods.gtype_id
    # print (type_id)
    type_name = TypeInfo.objects.get(id=goods.gtype_id)
    context = {
        'title':'详情页',
        'goods':goods,
        'news':news,
        'type_id':type_id,
        'type_name':type_name,
        'session_id':session_id,
        'user':user

    }
    # 修改点击量
    goods.gclick += 1
    goods.save()

    response = render(request, 'df_goods/detail.html', context)
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids == '':
        # 用户第一次登录第一次浏览商品
        goods_ids = str(goods.id)
    else:
        goods_id_list = goods_ids.split(',')
        if goods_id_list.count(str(goods.id)) >= 1:
            goods_id_list.remove(str(goods.id))
        goods_id_list.insert(0, str(goods.id))
        if len(goods_id_list) > 5:
            goods_id_list.pop()
        goods_ids = ','.join(goods_id_list)
    # print(goods_ids)
    response.set_cookie('goods_ids', goods_ids)
    return response
    # except:
    #     # 定义404页面
    #     raise Http404('<h1>页面未找到</h1>')

def list(request,id,pindex,sort):
    # try:
    session_id = request.COOKIES.get('session_id', '')
    user = request.session.get(session_id)
    type_name = TypeInfo.objects.get(id=id).title
    goods_list = TypeInfo.objects.get(id=int(id)).goodsinfo_set.all()
    if sort == '0':
        # 默认排序
        paginator = Paginator(goods_list, 3)
        page = paginator.page(int(pindex))

    if sort == '1':
        # 价格排序
        goods_list = goods_list.order_by('-gprice')
        paginator = Paginator(goods_list, 3)
        page = paginator.page(int(pindex))

    if sort == '2':
        goods_list = goods_list.order_by('-gclick')
        paginator = Paginator(goods_list, 3)
        page = paginator.page(int(pindex))

    context = {
        'title':'列表页',
        'page':page,
        'paginator':paginator,
        'pindex':pindex,
        'id':id,
        'sort':sort,
        'type_name':type_name,
        'session_id':session_id,
        'user':user
    }
    return render(request,'df_goods/list.html',context)
    # except:
    #     raise Http404('<h1>页面未找到</h1>')
