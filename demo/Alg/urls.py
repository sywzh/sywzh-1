#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__='wzh'

from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^warnlog/$', views.warnLog),
)
