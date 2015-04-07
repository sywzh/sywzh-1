#!/ust/bin/env python
#-*-coding:utf8-*-

import xlrd
import xlwt
from dateutil.parser import parse
import datetime
import time
import apriori

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
     "frozenset([1, 2])":u"FW-NAT dos攻击"
}

def getExcel(name):
	wb = xlrd.open_workbook(name)
	table = wb.sheets()[0]
	col_data = table.col_values(9)
	eventMsg = []
	len_data = len(col_data)
	for i in range(1,len_data):
		events = []
		if col_data[i] != u"/服务器/Windows":
			event = table.cell_value(i,10)
			try:
				events.append(table.cell_value(i,1))
				events.append(event_messages[event])
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


'''
len_events = len(events)
#print 'events:',events

def timeWindow(time,step,events,len_data):
	data = []
	for i in range(0,len_data,step):
		sets = []
		numbers = time + i
		if numbers > len_data:
			return data
		for j in range(i,numbers):
			sets.append(events[j])
		data.append(sets)
	return data

dataSet = timeWindow(5,1,events,len_events)
#print 'data:',timeWindow(10,1,events,len_data)

fp = open('test.txt','wb')
fp.write(str(dataSet))
fp.close()
'''


'''
C1 = apriori.createC1(dataSet)
#print 'C1:',C1

D = map(set,dataSet)
#print D

L1,suppData0 = apriori.scanD(D,C1,0.001)
#print 'L1:',L1

L,suppData = apriori.apriori(dataSet)
print 'L:',L
#print 'L[0]:',L[0]
#print 'L[1]:',L[1]
#print 'L[2]:',L[2]
print 'suppData:',suppData

#answer = apriori.aprioriGen(L[0],2)
#print answer

L,suppData = apriori.apriori(dataSet,minSupport = 0.7)
#print L
#print suppData
'''
'''
eventMsg = getAllExcel()
SetData = setData(eventMsg)
print SetData

L,suppData = apriori.apriori(SetData,minSupport = 0.3)
rules = apriori.generateRules(L,suppData,minConf = 0.1)
print 'rules:',rules

#rules = apriori.generateRules(L,suppData,minConf = 0.5)
#print '0.5 rules:',rules
'''
def manageData(name,minSupport = 0.3,minConf = 0.1):
	eventMsg = getExcel(name)
	SetData = setData(eventMsg)
	key = []
	value = []
	results = []
	L,suppData = apriori.apriori(SetData,minSupport)
	for (k,v) in suppData.items():
		try:
			key.append(events_id[str(k)])
			value.append(v)
		except:
			pass
	rules = apriori.generateRules(L,suppData,minConf)
	for rule in rules:
		events = []
		for event in rule[0:-1]:
			events.append(events_id[str(event)])
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
	


