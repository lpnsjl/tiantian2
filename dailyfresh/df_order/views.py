from django.shortcuts import *
from df_user import user_decorator
from df_cart.models import *
from df_user.models import *
from df_order.models import *
from django.db import transaction
from datetime import datetime


@user_decorator.login
def order(request):
    session_id = request.COOKIES.get('session_id')
    uid = request.session.get(session_id).get('uid')
    user = UserInfo.objects.get(id=uid)

    get = request.GET
    # 得到购物车表中所购买物品的id号
    cart_ids = get.getlist('cart_id')
    print (cart_ids)
    cart_ids1 = [int(cart_id) for cart_id in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    # print (carts[0].goods.gpic)
    count = len(carts)
    context = {
        'title':'支付页',
        'carts': carts,
        'user': user,
        'count': count,
        'cart_ids': ','.join(cart_ids),

    }
    return render(request, 'df_order/place_order.html', context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()

    session_id = request.COOKIES.get('session_id')
    # print(session_id)
    uid = request.session.get(session_id).get('uid')
    # print(uid)
    user = UserInfo.objects.get(id=uid)
    # print(user.uname)

    post = request.POST
    # print(post['address'])
    # 订单信息
    try:
        order = OrderInfo()
        now = datetime.now()
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        # print(order.oid)
        order.odate = now
        order.ototal = post['total_1']
        # print(order.ototal)
        order.user_id = uid
        # print(order.user_id)
        order.oaddress = post['address']
        order.save()
        cart_ids = post['cart_ids']

        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        # print (cart_ids1)
        carts = CartInfo.objects.filter(id__in=cart_ids1)
        # print (carts[0].goods)
        # 订单详情
        for cart in carts:
            goods = cart.goods
            # 库存足够
            if goods.gkucun > cart.count:
                goods.gkucun = goods.gkucun - cart.count
                # print(goods.gkucun)
                goods.save()
                orderdetail = OrderDetail()
                orderdetail.goods_id = goods.id
                orderdetail.subtotal = goods.gprice*cart.count
                print(orderdetail.subtotal)
                # print (orderdetail.price)
                orderdetail.order_id = order.id
                orderdetail.count = cart.count
                orderdetail.save()
                print(orderdetail.count)
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except:
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')