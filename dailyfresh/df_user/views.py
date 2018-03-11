from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from df_user.models import *
from hashlib import sha1
from django.core.cache import cache
from df_user.verify_code import cache_verify_code,encrypte,get_seesion_id
from df_user import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import *


# 注册页面
def register(request):
    context = {
        're_name': True,
    }
    return render(request, 'df_user/register.html', context)
# 注册用户名已存在
# def re_name(request,user_name):
#     user_list = UserInfo.objects.filter(uname=user_name)
#     data = 0
#     if len(user_list)>0:
#         data = 1
#     return JsonResponse({'data':data})


# 注册信息处理
def register_handle(request):
    # 读取注册信息
    post = request.POST
    user_name = post['user_name']
    pwd = post['pwd']
    email = post['email']
    user_list = UserInfo.objects.filter(uname=user_name)
    # 注册成功，转向登录页
    if user_name!='' and len(user_list)==0:
        userinfo = UserInfo()
        userinfo.uname = user_name
        userinfo.uemail = email

        # 对密码加密进行存储
        new_pwd = encrypte(pwd)
        userinfo.upwd = new_pwd

        userinfo.save()
        return redirect('/user/login/')
    # 假如用户注册失败，则重定向到注册页面
    else:
        return redirect('/user/register/')

# 登录页面
def login(request):
    filename = cache_verify_code()
    context = {
        'filename':filename,'user_error': 0, 'pwd_error':0,'code_error':0
    }
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    jizhu = post.get('jizhu')
    verify_code = post.get('verify_code')
    verify_code_key = post.get('verify_code_key')

    user = UserInfo.objects.filter(uname=uname)
    if len(user)!=0:
        # 密码加密，方便对比
        new_pwd = encrypte(pwd)
        # print (new_pwd)

        if user[0].upwd == new_pwd:
            if cache.get(verify_code_key) == verify_code:
                url = request.COOKIES.get('url','')
                if url == '':
                    url = '/index/'
                red = redirect(url)


                # print ('登录成功')
                if jizhu == 1:
                    red.set_cookie('jizhu',uname)
                else:
                    # 让cookie立马失效
                    red.set_cookie('jizhu','',max_age=0)
                  # 将用户信息存到服务器，以便用户验证
                # session_id向浏览器发送一份，服务器保存一份做对比
                session_id = get_seesion_id()
                red.set_cookie('session_id',session_id)
                request.session[session_id] = {'uid': user[0].id, 'uname': uname}
                return red
            else:
                # 验证码错误
                filename = cache_verify_code()
                context = {
                    'filename': filename, 'user_error': 0, 'pwd_error': 0, 'code_error': 1
                }
                return render(request, 'df_user/login.html', context)

        else:
            # 密码错误
            filename = cache_verify_code()
            context = {
                'filename': filename, 'user_error': 0, 'pwd_error': 1, 'code_error': 0
            }
            return render(request, 'df_user/login.html', context)


    else:
        # 用户名错误
        filename = cache_verify_code()
        context = {
            'filename': filename, 'user_error': 1, 'pwd_error': 0, 'code_error': 0
        }
        return render(request,'df_user/login.html',context)

def logout(request):
    session_id = request.COOKIES['session_id']
    if session_id in request.session:
        del request.session[session_id]

    red = redirect('/index/')
    red.delete_cookie('session_id')
    red.set_cookie('goods_ids','',max_age=0)

    # print (request.session[session_id])
    #print (request.COOKIES['session_id'])
    #print (request.COOKIES[ 'sessionid'])
    #del request.COOKIES[ 'sessionid']
    return red

@user_decorator.login
def info(request):
    session_id = request.COOKIES['session_id']
    try:
        uid = request.session.get(session_id).get('uid')
        user = UserInfo.objects.get(id=uid)

        goods_ids = request.COOKIES.get('goods_ids', '')
        if goods_ids == '':
            context = {
                'title': '个人信息',
                'user': user,
                'goods_ids':goods_ids,
            }
        else:
            # print(goods_ids)
            zuijin = goods_ids.split(',')
            goods_list = []
            for id in zuijin:
                goods_list.append(GoodsInfo.objects.filter(id=int(id))[0])
            context = {
                'title': '个人信息',
                'user': user,
                'goods_ids': goods_ids,
                'goods_list':goods_list,
            }



        return render(request, 'df_user/user_center_info.html',context)
    except:
        return redirect('/index/')

@user_decorator.login
def order(request,pindex):
    session_id = request.COOKIES['session_id']
    # try:
    uid = request.session.get(session_id).get('uid')
    user = UserInfo.objects.get(id=uid)
    order = OrderInfo.objects.filter(user_id=uid).order_by('-oid')
    paginator = Paginator(order, 2)
    if pindex == '':
        pindex = 1
    page = paginator.page(int(pindex))
    context = {
        'title': '全部订单',
        'user': user,
        'page':page,
    }
    return render(request, 'df_user/user_center_order.html', context)
    # except:
    #     return redirect('/index/')

@user_decorator.login
def site(request):
    try:
        session_id = request.COOKIES['session_id']
        uid = request.session.get(session_id).get('uid')

        user = UserInfo.objects.get(id=uid)
        if request.method == 'POST':
            post = request.POST
            user.ushou = post['ushou']
            print (user.ushou)
            user.uaddress = post['address']
            user.uyoubian = post['youbian']
            user.uphone = post['phone']
            user.save()

        context = {
            'title': '收货地址',
            'user': user,

        }
        return render(request, 'df_user/user_center_site.html', context)
    except:
        return redirect('/index/')