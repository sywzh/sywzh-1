#!/ust/bin/env python
#-*-coding:utf8-*-

import xlrd
import xlwt
from dateutil.parser import parse
import datetime
import time
import apriori
import aprioriall
from Alg.models import Events

def setData(data):
	len_data = len(data)
	events = []
	result = []
	timeArray = []
	n = 1
	T = 999999999
	sumTime = 0.0
	events.append(data[0][1])
	for i in range(len_data):
		try:
			timeStamp = int(time.mktime(time.strptime(str(data[i+1][0]),"%Y-%m-%d %H:%M:%S")))-int(time.mktime(time.strptime(str(data[i][0]),"%Y-%m-%d %H:%M:%S")))
			if T >= timeStamp:
				n = n + 1
				sumTime = sumTime + timeStamp
				events.append(data[i+1][1])
				timeArray.append(timeStamp)
				T = timeSet(sumTime,n,timeArray)
				#print T
			else:
				result.append(events)
				events = []
				events.append(data[i+1][1])
				T = 999999999
				sumTime = 0.0
				timeArray = []
		except:
			pass
		
	return result

def timeSet(sumTime,n,timeArray):
	sumInTime = 0.0
	avgTime = sumTime/(n-1)
	if avgTime == 0:
		return 0
	for times in timeArray:
		sumInTime = sumInTime + (times-avgTime)**2
	varTime = (sumInTime/(n-1))**0.5
	stdTime = varTime/avgTime
	Time = avgTime + avgTime*stdTime
	return Time

event_messages = {u"FW-NAT":1,
                  u"dos攻击":2,
                  u"流量信息":3,
                  u"SNMP_缺省口令[public]":4,
                  u"SNMP_登录尝试":5,
                  u"SMB_登录失败":6,
                  u"ARP_IP地址欺骗":7,
                  u"SMB_IPC$默认共享连接":8,
                  u"MSRPC_连接":9}

events_id = {
	"frozenset([1])":u"FW-NAT",
     "frozenset([2])":u"dos攻击",
     "frozenset([3])":u"流量信息",
     "frozenset([4])":u"SNMP_缺省口令[public]",
     "frozenset([5])":u"SNMP_登录尝试",
     "frozenset([6])":u"SMB_登录失败",
     "frozenset([7])":u"ARP_IP地址欺骗",
     "frozenset([8])":u"SMB_IPC$默认共享连接",
     "frozenset([9])":u"MSRPC_连接",
     "frozenset([1, 2])":u"FW-NAT dos攻击",
     "frozenset([2, 1])":u"dos攻击 FW-NAT"
}

def storageEvents(event):
	events = set(event)
	for event_type in events:
		if Events.objects.filter(name = event_type).count()>0:
			pass
		else:
			op = Events(name = event_type)
			op.save()

def get_events_dict():
	events_dict = {}
	count = 0
	events = Events.objects.all()
	for event in events:
		events_dict[count] = event.name
		count = count + 1
	return events_dict

def get_dict_events():
	dict_events = {}
	count = 0
	events = Events.objects.all()
	for event in events:
		dict_events[event.name] = count
		count = count + 1
	return dict_events

def setEvents(name):
	wb = xlrd.open_workbook(name)
	table = wb.sheets()[0]
	col_data = table.col_values(9)
	eventMsg = []
	len_data = len(col_data)
	storage = []
	for i in range(1,len_data):
		events = []
		if col_data[i] == u"/安全设备/防火墙" or col_data[i] == u"/安全设备/入侵检测保护系统":
			event = table.cell_value(i,10)
			try:
				storage.append(event)
			except:
				pass
	storageEvents(storage)

def getExcel(name):
	wb = xlrd.open_workbook(name)
	table = wb.sheets()[0]
	col_data = table.col_values(9)
	eventMsg = []
	len_data = len(col_data)
	event_msgs = get_dict_events()
	for i in range(1,len_data):
		events = []
		if col_data[i] == u"/安全设备/防火墙" or col_data[i] == u"/安全设备/入侵检测保护系统":
			event = table.cell_value(i,10)
			try:
				events.append(table.cell_value(i,1))
				events.append(event_msgs[event])
				eventMsg.append(events)
			except:
				pass
	return eventMsg

def getAllExcel():
	Msg = []
	for i in range(1,17):
		print i
		if i != 7 and i != 5:
			name = 'event' + str(i) + '.xls'
			eventMsg = getExcel(name)
			Msg = Msg + eventMsg
		else:
			pass
	return Msg

def manageData(name,minSupport = 0.2,minConf = 0.1):
	eventMsg = getExcel(name)
	SetData = setData(eventMsg)
	events_dict = get_events_dict()
	L,suppData = apriori.apriori(SetData,float(minSupport))
	#aprioriall.aprioriall(SetData,float(minSupport))
	rules = apriori.generateRules(L,suppData,minConf=0.1)
	key = []
	value = []
	results = []
	for (ks,v) in suppData.items():
		try:
			event_name = ''
			for k in ks:
				event_name = event_name+events_dict[k]+' '
			key.append(event_name)
			value.append(v)
		except:
			pass
	for rule in rules:
		events = []
		for event in rule[0:-1]:
			try:
				k_name = ''
				for k in event:
					k_name = k_name + events_dict[k] + ' '
				events.append(k_name)
			except:
				pass
		events.append(rule[-1])
		results.append(events)
	return key,value,results

def getMinSupport(name,minSupport,minConf):
	eventMsg = getExcel(name)
	SetData = setData(eventMsg)
	L,suppData = apriori.apriori(SetData,minSupport)
	rules = apriori.generateRules(L,suppData,minConf)
	return len(rules)

def minSupportTest(name):
	minsupport = {}
	minsupport['0.3'] = getMinSupport(name,0.3,0.1)
	minsupport['0.5'] = getMinSupport(name,0.5,0.1)
	minsupport['0,8'] = getMinSupport(name,0.8,0.1)
	result = sorted(minsupport.iteritems(),key = lambda asd:asd[1],reverse = True)
	return result[0][0]
	


