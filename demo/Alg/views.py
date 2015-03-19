#!/usr/bin/env python
#-*-coding:utf8-*-
__author__= 'wzh'

from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from demo.decorators import lrender
from django.contrib.auth import authenticate,login,logout
from django.utils import simplejson

@lrender('alg/warnlog.html')
@login_required
def warnLog(request):
	return {}

def profileUpload(file):
	if file:
		buf = ''
		for content in file.chunks():
			buf = buf + content
		return True,buf
	return False,buf

def writefile(buf,name):
	fp = open(name,'wb')
	fp.write(buf)
	fp.close()

@login_required
def uploadifyScript(request):
	file = request.FILES.get("Filedata",None)
	test = request.POST.get("someKey")
	print 'test:',test
	result,buf = profileUpload(file)
	writefile(buf,file.name);
	print dir(file)
	print 'result:',result
	return HttpResponse(simplejson.dumps({'message':'ok'}))