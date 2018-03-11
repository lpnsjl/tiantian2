from django.shortcuts import render
from df_user import user_decorator
from django.http import HttpResponse,JsonResponse
from df_cart.models import *
from django.core.paginator import Paginator


@user_decorator.login
# 展现购物车页面
def cart(request):
    session_id = request.COOKIES.get('session_id', '')
    user = request.session.get(session_id)

    carts = CartInfo.objects.filter(user_id=user.get('uid'))
    num = len(carts)


    context = {
        'title': '购物车',
        'user': user,
        'carts':carts,
        'num':num,
    }
    return render(request,'df_cart/cart.html',context)


@user_decorator.login
# 添加商品到购物车，主要工作是向购物车表添加数据
def add_cart(request,gid,count):
    session_id = request.COOKIES.get('session_id')
    uid = request.session.get(session_id)['uid']
    count = int(count)

    carts = CartInfo.objects.filter(user_id=int(uid),goods_id=int(gid))
    # print (carts)
    # 用户未购买过该商品
    if len(carts) == 0:
        cart1 = CartInfo()
        cart1.count = count
        cart1.user_id = uid
        cart1.goods_id = gid

    # 用户已购买过该商品
    else:
        cart1 = carts[0]
        cart1.count += count
    cart1.save()
    count = CartInfo.objects.filter(user_id=uid, goods_id=gid)[0].count
    return JsonResponse({'count': count, 'cart_id': cart1.id})

# 编辑商品数量
@user_decorator.login
def edit(request, cid, count):
    # session_id = request.COOKIES.get('session_id')
    # uid = request.session.get(session_id)['uid']

    cart1 = CartInfo.objects.get(pk=int(cid))# cid购物车id
    cart1.count = int(count)
    cart1.save()
    return JsonResponse({'data':int(count)})

# 删除商品
@user_decorator.login
def delete(request, cid):
    cart1 = CartInfo.objects.get(pk=int(cid))
    cart1.delete()
    return JsonResponse({'data':0})

