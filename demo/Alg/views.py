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
from trans import manageData,minSupportTest
import json

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
	if WarnLog.objects.filter(user_id = request.user.id,name = file.name).count()>0:
		pass
	else:
		result,buf = profileUpload(file)
		print 'result:',result
		writefile(buf,file.name)
	return HttpResponse(simplejson.dumps({'message':'ok'}))

def dropFile(name):
	cmd = 'rm -rf '+name
	os.system(cmd)

def storageFile(name,user):
	data = xlrd.open_workbook(name)
	table = data.sheets()[0]
	nrows = table.nrows
	for i in range(1,nrows):
		op = WarnNine(user_id = user.id,name = name,systemtype = table.row_values(i)[0],\
		gettime = table.row_values(i)[1],classify = table.row_values(i)[2],ipsrc = table.row_values(i)[3],\
		srcport = table.row_values(i)[4],srcname = table.row_values(i)[5],ipdst = table.row_values(i)[6],\
		dstport = table.row_values(i)[7],deviceads = table.row_values(i)[8],devicetype = \
		table.row_values(i)[9],event = table.row_values(i)[10] )
		op.save()

def storageFiles(name,username):
	data = xlrd.open_workbook(name)
	table = data.sheets()[0]
	nrows = table.nrows
	attrs = table.row_values(0)
	print attrs

def handleFile(filename,username,getvalue):
	if getvalue == '1':
		if filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
			try:
				storageFile(filename,username)
			except:
				dropFile(filename)
				return '1'
		else:
			return '2'
	if getvalue == '0':
		if filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
			try:

				storageFiles(filename,username)
			except:
				#dropFile(filename)
				return "1"
		elif filename[-3:] == 'xml':
			try:
				storageXML(filename,username)
			except:
				dropFile(filename)
				return "1"
		else:
			return "2"
	op = WarnLog(user_id = username.id,name = filename)
	op.save()
	return 0

def handleData(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("filename")
	getvalue = request.POST.get("getvalue")
	username = request.user
	#if WarnLog.objects.filter(user_id = username.id,name = filename).count()>0:
	#	return HttpResponse(simplejson.dumps({'message':'uploaded'}))
	flag = handleFile(filename,username,getvalue)
	if flag == "1":
		return HttpResponse(simplejson.dumps({'message':'attrerror'}))
	elif flag == "2":
		return HttpResponse(simplejson.dumps({'message':'formerror'}))		
	return HttpResponse(simplejson.dumps({'message':'ok'}))


@login_required
@lrender('alg/connect.html')
def connectHd(request):
	return {}

@login_required
def dataAnalysis(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	name = request.POST.get("name")
	minSupport = request.POST.get("minSupport")
	#minConf = request.POST.get("minConf")
	try:
		key,value,results = manageData(name,minSupport)
		key = json.dumps(key)
		value = json.dumps(value)
		results = json.dumps(results)
		return HttpResponse(simplejson.dumps({'message':'ok','key':key,'value':value,"results":results}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

def traversal(attrs,name):
	attrs = [[u"FW-NAT",u"dos攻击"],[u"dos攻击",u"FW-NAT"]]
	connect = []
	result = []
	data = xlrd.open_workbook('event1.xls')
	table = data.sheets()[0]
	for attr in attrs:
		for i in range(table.nrows):
			flag = 0
			for j in range(len(attr)):
				if(attr[j] in table.row_values(i+flag)):
					flag = flag + 1
				if (flag == len(attr)):
					for k in range(i,i+flag):
						connect.append(table.row_values(k))
				else:
					continue
		result.append(connect)
	return result

@login_required
def getAttr(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	attrs = [[u"FW-NAT",u"dos攻击"],[u"dos攻击",u"FW-NAT"]]
	name = "event1.xls"
	print 'test:',name
	result = traversal(attrs,name)
	print result
	return HttpResponse(simplejson.dumps({'message':result}))

@login_required
def getTest(request):
	choice = {
	'0.3':'0.1-0.4',
	'0.5':'0.4-0.7',
	'0.8':'0.7-1.0'
	}
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	name = request.POST.get("name")
	try:
		result = minSupportTest(name)
		return HttpResponse(simplejson.dumps({'message':choice[result]}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

@login_required
@lrender('alg/safemanage.html')
def safeManager(request):
	return {}