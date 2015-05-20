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
from django.core import serializers
from similiarAttr import analysisData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Alg.serializers import SafeManagerSerializer,EventsSerializer
from Log import log
import xlwt
from random import Random

@lrender('alg/warnlog.html')
@login_required
def warnLog(request):
	logs = WarnLog.objects.all()
	return {'logs':logs}

def profileUpload(file):
	if file:
		buf = ''
		for content in file.chunks():
			buf = buf + content
		return True,buf
	return False,buf

def writefile(buf,name):
	name = 'demo/media/upload/' + name
	fp = open(name,'wb')
	fp.write(buf)
	fp.close()
	cmd = 'chmod 777 ' + name
	os.system(cmd)

def readfile(name):
	name = 'demo/media/upload/' + name
	fp = open(name,'rb')
	buf = fp.read()
	fp.close()
	return buf

@login_required
def uploadifyScript(request):
	file = request.FILES.get("Filedata",None)
	if WarnLog.objects.filter(user_id = request.user.id,name = file.name).count()>0:
		pass
	else:
		result,buf = profileUpload(file)
		writefile(buf,file.name)
		log(request.user.id,'2',file.name)
	return HttpResponse(simplejson.dumps({'message':'ok'}))

def wtFile(buf,name):
	fp = open(name,'wb')
	fp.write(buf)
	fp.close()
	cmd = 'chmod 777 ' + name
	os.system(cmd)

@login_required
def uploadScript(request):
	file = request.FILES.get("Filedata",None)
	result,buf = profileUpload(file)
	wtFile(buf,file.name)
	return HttpResponse(simplejson.dumps({'message':'ok'}))

def dropFile(name):
	name = 'demo/media/upload/' + name
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
'''
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
'''

def handleFile(name,user):
	try:
		obj = WarnLog(user_id = user.id,name = name)
		obj.save()
		return True
	except:
		return False

def formData(name,fileUrl = 'demo/media/upload/'):
	name = fileUrl + name
	data = xlrd.open_workbook(name)
	table = data.sheets()[0]
	nrows = table.ncols
	if nrows != 11:
		return False
	if table.row_values(0)[0] != u'系统类型':
		return False
	return True

def handleData(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("filename")
	if WarnLog.objects.filter(name = filename).count()>0:
		return HttpResponse(simplejson.dumps({'message':'uploaded'}))
	if filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
		pass
	else:
		dropFile(filename)
		return HttpResponse(simplejson.dumps({'message':'formerror'}))
	if formData(filename) == False:
		dropFile(filename)
		return HttpResponse(simplejson.dumps({'message':'attrerror'}))
	flag = handleFile(filename,request.user)
	if flag == False:
		return HttpResponse(simplejson.dumps({'message':'error'}))
	return HttpResponse(simplejson.dumps({'message':'ok'}))

@login_required
@lrender('alg/connect.html')
def connectHd(request):
	logs = WarnLog.objects.all()
	return {'logs':logs}

def storageAnalysis(user,name,results,minSupport):
	filename = name + '/'
	name = filename.split('/')[-2]
	for result in results:
		sequence = ''
		for element in result[0:-1]:
			if element != result[-2]:
				sequence = sequence + element + '->'
			else:
				sequence = sequence + element
		obj = SafeManager(user_id = user.id,name = name,support = minSupport,attack_sequence = sequence)
		obj.save()


@login_required
def dataAnalysis(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	name = request.POST.get("name")
	minSupport = request.POST.get("minSupport")
	try:
		key,value,results = manageData(name,minSupport)
		key = json.dumps(key)
		value = json.dumps(value)
		storageAnalysis(request.user,name,results,minSupport)
		results = json.dumps(results)
		log(request.user.id,'4',name.split('/')[-1])
		return HttpResponse(simplejson.dumps({'message':'ok','key':key,'value':value,"results":results}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

def similiarData(data):
	result = []
	for i in range(len(data)):
		attrs = []
		attrs.append(data[i][1])
		attrs.append(data[i][3])
		attrs.append(data[i][6])
		attrs.append(data[i][4])
		attrs.append(data[i][7])
		result.append(attrs)
	return result

def traversal(attrs,name,value = 0.94,time = 0.3,srcip=0.3,dstip=0.3,srcport=0.05,dstport=0.05):
	result = []
	result_attrs = []
	data = xlrd.open_workbook(name)
	table = data.sheets()[0]
	for attr in attrs:
		connect = []
		attr_result = []
		count = 0
		cont = 0
		for i in range(table.nrows):
			flag = 0
			for j in range(len(attr)):
				similiar = []
				try:
					table.row_values(i+flag)
				except:
					continue
				if(attr[j] in table.row_values(i+flag)):
					flag = flag + 1
				if (flag == len(attr)):
					cont = cont + 1
					for k in range(i,i+flag):
						similiar.append(table.row_values(k))
						connect.append(table.row_values(k))
					if analysisData(similiarData(similiar),time,srcip,dstip,srcport,dstport) > value:
						count = count + 1
						for k in range(i,i+flag):
							attr_result.append(table.row_values(k))
				else:
					continue
		result.append(connect)
		result_attrs.append(attr_result)
	return result,result_attrs

def random_str(randomlength=32):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str+=chars[random.randint(0, length)]
	return str

def get_name():
	name = random_str(8)
	return name + '.xls'

def set_cache(results):
	wb = xlwt.Workbook(encoding = 'utf-8')
	sheet = wb.add_sheet(u'sheet1')
	sheet.write(0,0,u'系统类型')
	sheet.write(0,1,u'接收时间')
	sheet.write(0,2,u'等级')
	sheet.write(0,3,u'源地址')
	sheet.write(0,4,u'源端口')
	sheet.write(0,5,u'源用户名称')
	sheet.write(0,6,u'目的地址')
	sheet.write(0,7,u'目的端口')
	sheet.write(0,8,u'设备地址')
	sheet.write(0,9,u'设备类型')
	sheet.write(0,10,u'事件名称')
	row = 1
	for result in results:
		for data in result:
			for i in range(11):
				sheet.write(row,i,data[i])
			row = row + 1
	name = get_name()
	wb.save(name)
	return name

@login_required
def getAttr(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("fileName")
	results = request.POST.get("results")
	attrs = []
	for attr in simplejson.loads(results):
		attrs.append(attr[0:-1])
	result,attr_result = traversal(attrs,filename)
	name = set_cache(result)
	return HttpResponse(simplejson.dumps({'message':result,'name':name}))

def quantitative(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("fileName")
	results = request.POST.get("results")
	flag = request.POST.get("flag")
	attrs = []
	for attr in simplejson.loads(results):
		attrs.append(attr[0:-1])
	log(request.user.id,'5',filename)
	if flag == '1':
		time = request.POST.get("time")
		srcip = request.POST.get("srcip")
		dstip = request.POST.get("dstip")
		srcport = request.POST.get("srcport")
		dstport = request.POST.get("dstport")
		value = request.POST.get("value")
		time = simplejson.loads(time)
		srcip = simplejson.loads(srcip)
		dstip = simplejson.loads(dstip)
		srcport = simplejson.loads(srcport)
		dstport = simplejson.loads(dstport)
		value = simplejson.loads(value)
		result,attr_result = traversal(attrs,filename,value,time,srcip,dstip,srcport,dstport)
		name = set_cache(attr_result)
		return HttpResponse(simplejson.dumps({'message':attr_result,'name':name}))
	if flag == '0':
		result,attr_result = traversal(attrs,filename)
		name = set_cache(attr_result)
		return HttpResponse(simplejson.dumps({'message':attr_result,'name':name}))

def exportLog(request,name):
	try:
		buf = readfile(name)
		cmd = 'rm -rf ' + name
		os.system(cmd)
		name = name.encode('utf8')
		response = HttpResponse(buf,mimetype = 'application/octet-stream')
		response['Content-Disposition'] = 'attachment;filename=%s' % name
		return response
	except:
		raise Http404

@login_required
def getTest(request):
	choice = {
	'0.3':'0.1-0.4',
	'0.5':'0.4-0.7',
	'0.8':'0.7-1.0'
	}
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	filename = request.POST.get("name")

	if filename[-3:] == 'xls' or filename[-4:] == 'xlsx':
		pass
	else:
		cmd = 'rm -rf ' + filename
		os.system(cmd)
		return HttpResponse(simplejson.dumps({'message':'formerror'}))
	if formData(filename,'') == False:
		cmd = 'rm -rf ' + filename
		os.system(cmd)
		return HttpResponse(simplejson.dumps({'message':'attrerror'}))
	try:
		result = minSupportTest(filename)
		return HttpResponse(simplejson.dumps({'message':choice[result]}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

@login_required
@lrender('alg/safemanage.html')
def safeManager(request):
	return {}

@login_required
def downLoad(request,sid):
	try:
		obj = WarnLog.objects.get(id = sid)
		name = obj.name
		buf = readfile(name)
		name = name.encode('utf8')
		log(request.user.id,'3',name)
		response = HttpResponse(buf,mimetype = 'application/octet-stream')
		response['Content-Disposition'] = 'attachment;filename=%s' % name
		return response
	except:
		raise Http404

@login_required
def deleteLog(request,sid):
	try:
		obj = WarnLog.objects.get(id = sid)
		name = obj.name
		cmd = 'rm -rf demo/media/upload/' + name
		os.system(cmd)
		obj.delete()
		return HttpResponseRedirect('/alg')
	except:
		raise Http404

@login_required
def importData(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	choice = {
	'0.3':'0.1-0.4',
	'0.5':'0.4-0.7',
	'0.8':'0.7-1.0'
	}
	name = request.POST.get("name")
	try:
		result = minSupportTest(name)
		return HttpResponse(simplejson.dumps({'message':choice[result]}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

class SafeManagerList(APIView):
	def get(self,request,format=None):
		sequence = SafeManager.objects.filter(user_id = request.user.id)
		serializer = SafeManagerSerializer(sequence,many = True)
		return Response({'status':200,'data':serializer.data})

class SafeManagerDetail(APIView):
	def get_object(self,pk):
		try:
			return SafeManager.objects.get(pk = pk)
		except SafeManager.DoesNotExist:
			raise Http404
	def put(self,request,pk,format = None):
		safe = self.get_object(pk)
		try:
			safe.attack_name = request.data['name']
			safe.save()
			return Response({'status':0})
		except:
			return Response({"status":400,'data':'error'})
	def delete(self,request,pk,format = None):
		safe = self.get_object(pk)
		safe.delete()
		return Response({'status':0})

class EventsList(APIView):
	def get(self,request,format = None):
		events = Events.objects.all()
		serializer = EventsSerializer(events,many = True)
		return Response({'status':200,'data':serializer.data})

	def post(self,request,format = None):
		serializer = EventsSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status':0})
		return Response({'status':400,'data':serializer.errors})

class EventDetails(APIView):
	def get_object(self,pk):
		try:
			return Events.objects.get(pk = pk)
		except Events.DoesNotExist:
			raise Http404
	def put(self,request,pk,format = None):
		event = self.get_object(pk)
		serializer = EventsSerializer(event,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status':0})
		return Response({'status':400,'data':serializer.errors})
	def delete(self,request,pk,format = None):
		event = self.get_object(pk)
		event.delete()
		return Response({'status':0})