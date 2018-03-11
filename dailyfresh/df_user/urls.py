# -*- coding: UTF-8 -*-
from django.conf.urls import url
from df_user import views


urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    # url(r'^re_name(.*)/$', views.re_name),
    url(r'^login/$',views.login),
    url(r'^login_handle/$',views.login_handle),
    url(r'^info/$',views.info),
    url(r'^logout/$',views.logout),
    url(r'^order(\d*)/$',views.order),
    url(r'^site/$', views.site),

]