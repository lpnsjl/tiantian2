# -*- coding: UTF-8 -*-
from django.shortcuts import redirect

def login(fun):
    def wrapper(request,*kw,**kwargs):
        if 'session_id' in request.COOKIES:
            return fun(request,*kw,**kwargs)
        else:
            full_url = request.get_full_path()
            red = redirect('/user/login/')
            red.set_cookie('url',full_url)
            return red
    return wrapper

