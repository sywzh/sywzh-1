#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__='wzh'

from django.conf.urls import patterns, include, url
import User
import settings
from  Alg import views
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
    url(r'^connect/$','Alg.views.connectHd'),
    url(r'^analysis/$','Alg.views.dataAnalysis'),
    url(r'^getattr/$','Alg.views.getAttr'),
    url(r'^gettest/$','Alg.views.getTest'),
    url(r'^safemanage/$','Alg.views.safeManager'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^uploadscript/$','Alg.views.uploadScript'),
    url(r'^download/(\w+)/$','Alg.views.downLoad'),
    url(r'^deletelog/(\w+)$','Alg.views.deleteLog'),
    url(r'^historylog/$','Log.views.historyLog'),
    url(r'^importdata/$','Alg.views.importData'),
    url(r'^sequence$',views.SafeManagerList.as_view()),
    url(r'^events$',views.EventsList.as_view()),
    url(r'^sequence/(\w+)$',views.SafeManagerDetail.as_view()),
    url(r'^events/(\w+)$',views.EventDetails.as_view()),
    url(r'^quantitative/$','Alg.views.quantitative'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^xadmin/', include(xadmin.site.urls)),
)
