#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^login/$', views.LoginHd),
    url(r'^register/$',views.RegisterHd),
    url(r'^logout/$',views.LogoutHd),
    url(r'^changepw/$',views.ModifyPw)
)
