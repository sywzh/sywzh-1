#!/usr/bin/env python
#-*-coding:utf8-*-
__author__= 'wzh'

from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from demo.decorators import lrender
from django.contrib.auth import authenticate,login,logout
from django.utils import simplejson
from Alg.models import *
import xlrd
import os

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
	cmd = 'chmod 777 ' + name
	os.system(cmd)

@login_required
def uploadifyScript(request):
	file = request.FILES.get("Filedata",None)
	result,buf = profileUpload(file)
	writefile(buf,file.name)
	return HttpResponse(simplejson.dumps({'message':'ok'}))

def dropFile(name):
	cmd = 'rm -rf '+name
	os.system(cmd)

def storageFile(name,user):
	data = xlrd.open_workbook(name)
	table = data.sheets()[0]
	nrows = table.nrows
	ncols = table.ncols
	for i in range(1,nrows):
		'''
		print user.id,name
		print table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],\
		table.row_values(i)[3],table.row_values(i)[4],table.row_values(i)[5],\
		table.row_values(i)[6],table.row_values(i)[7],table.row_values(i)[8],\
		table.row_values(i)[9],len(table.row_values(i)[10])
		'''
		op = WarnNine(user_id = user.id,name = name,systemtype = table.row_values(i)[0],\
		gettime = table.row_values(i)[1],classify = table.row_values(i)[2],ipsrc = table.row_values(i)[3],\
		srcport = table.row_values(i)[4],srcname = table.row_values(i)[5],ipdst = table.row_values(i)[6],\
		dstport = table.row_values(i)[7],deviceads = table.row_values(i)[8],devicetype = \
		table.row_values(i)[9],event = table.row_values(i)[10] )
		op.save()

def handleData(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("filename")
	getvalue = request.POST.get("getvalue")
	username = request.user
	#if WarnLog.objects.filter(user_id = username.id,name = filename).count()>0:
	#	dropFile(filename)
	#	return HttpResponse(simplejson.dumps({'message':'uploaded'}))
	if getvalue == '1':
		if filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
			try:
				storageFile(filename,username)
				op = WarnLog(user_id = username.id,name = filename)
				op.save()
			except:
				dropFile(filename)
				return HttpResponse(simplejson.dumps({'message':'attrerror'}))
		else:
			return HttpResponse(simplejson.dumps({'message':'formerror'}))
		
	print filename,getvalue
	return HttpResponse(simplejson.dumps({'message':'ok'}))
