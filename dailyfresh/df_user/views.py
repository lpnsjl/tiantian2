from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from df_user.models import *
from hashlib import sha1
from django.core.cache import cache
from datetime import datetime
from df_user.verify_code import get_verify_code
from dailyfresh import settings
import os


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
        s = sha1()
        s.update(pwd.encode('utf-8'))
        new_pwd = s.hexdigest()
        userinfo.upwd = new_pwd

        userinfo.save()
        return redirect('/user/login/')
    # 假如用户注册失败，则重定向到注册页面
    else:
        return redirect('/user/register/')

# 登录页面
def login(request):
    verify_code_path = os.path.join(settings.BASE_DIR, 'static')
    now = datetime.now()
    t = now.timestamp()
    filename = ''.join(str(t).split('.'))
    verify_code = get_verify_code(verify_code_path,filename)
    # 将验证码存入缓存中
    cache.set(filename,verify_code,30)
    context = {
        'filename':filename,
    }
    return render(request,'df_user/login.html',context)

def login_handle(request):
    return