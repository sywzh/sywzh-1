#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__='wzh'

from django.conf.urls import patterns, include, url
import User
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'User.views.logoHd'),
    url(r'^user/',include('User.urls')),
    url(r'^index/$','demo.index.IndexHd'),
    url(r'^alg/$','Alg.views.warnLog'),
    url(r'^uploadifyscript/$','Alg.views.uploadifyScript'),
    url(r'^handledata/$','Alg.views.handleData'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^xadmin/', include(xadmin.site.urls)),
)
