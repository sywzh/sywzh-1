#!/usr/bin/env python
#-*-coding:utf8-*-

event_messages = {u"PROTOCOL-ICMP L3retriever Ping":1,
                  u"PROTOCOL-ICMP PING":2,
                  u"PROTOCOL-ICMP PING Oracle Solaris":3,
                  u"PROTOCOL-ICMP Echo Reply":4,
                  u"PROTOCOL-FTP no password":5,
                  u"PROTOCOL-FTP Bad login":6,
                  u"POLICY-OTHER FTP anonymous login attempt":7,
                  u"PROTOCOL-ICMP PING BSDtype":8,
                  u"PROTOCOL-ICMP PING *NIX":9,
                  u"SNMP AgentX/tcp request":10,
                  u"SNMP request tcp":11,
                  u"PROTOCOL-FTP format string attempt":12,
                  u"PROTOCOL-FTP wu-ftp bad file completion attempt":13,
                  u"PROTOCOL-FTP CWD overflow attempt":14,
                  u"PROTOCOL-FTP LIST buffer overflow attempt":15,
                  u"PROTOCOL-FTP MKD overflow attempt":16,
                  u"PROTOCOL-FTP USER overflow attempt":17,
                  u"PROTOCOL-FTP PASS format string attempt":18,
                  u"PROTOCOL-FTP PASS overflow attempt":19,
                  u"PROTOCOL-FTP MDTM overflow attempt":20,
                  u"PROTOCOL-FTP invalid MDTM command attempt":21,
                  u"PROTOCOL-FTP USER format string attempt":22,
                  u"INDICATOR-COMPROMISE 403 Forbidden":23,
                  u"SERVER-WEBAPP weblogic/tomcat .jsp view source a":24,
                  u"SERVER-WEBAPP Mambo upload.php access":25,
                  u"SERVER-IIS cmd.exe access":26,
                  u"SERVER-IIS pbserver access":27,
                  u"SERVER-WEBAPP webadmin.dll access":28,
                  u"SERVER-OTHER Microsoft Frontpage /_vti_bin/ acce":29,
                  u"SERVER-OTHER Microsoft Frontpage rad fp30reg.dll":30,
                  u"SERVER-WEBAPP test.php access":31,
                  u"SERVER-WEBAPP Setup.php access":32,
                  u"OS-WINDOWS DCERPC NCACN-IP-TCP IActivation remot":33,
                  u"NETBIOS SMB repeated logon failure":34,
                  u"INDICATOR-SHELLCODE x86 inc ebx NOOP":35,
                  u"SERVER-WEBAPP awstats access":36,
                  u"OS-WINDOWS DCERPC NCACN-IP-TCP lsass DsRolerUpgr":37,
                  u"INDICATOR-SHELLCODE x86 inc ecx NOOP":38,
                  u"SERVER-WEBAPP WebDAV search access":39,
                  u"SERVER-IIS ISAPI .idq attempt":40,
                  u"SERVER-IIS ISAPI .idq access":41,
                  u"NETBIOS DCERPC NCACN-IP-TCP spoolss EnumPrinters":42,
                  u"PROTOCOL-FTP MKD format string attempt":43,
                  u"SERVER-WEBAPP Cisco /%% DOS attempt":44,
                  u"SERVER-WEBAPP streaming server parse_xml.cgi acc":45,
                  u"SERVER-WEBAPP parse_xml.cgi access":46,
                  u"SERVER-IIS ISAPI .printer access":47,
                  u"FILE-IDENTIFY .htr access file download request":48,
                  u"SERVER-WEBAPP guestbook.pl access":49,
                  u"NETBIOS SMB-DS repeated logon failure":50,
                  u"PROTOCOL-ICMP Destination Unreachable Host Unrea":51,
                  u"SNMP public access udp":52,
                  u"SNMP request udp":53,
                  u"PROTOCOL-ICMP Destination Unreachable Port Unrea":54,
                  u"DOS UPnP malformed advertisement":55
                  }

from xml.dom import minidom,Node
import json
import xlrd
from dateutil.parser import parse
import datetime
import time as times

data = []

class XMLscanner:
	def __init__(self,doc):
		for child in doc.childNodes:
			if child.nodeType == Node.ELEMENT_NODE and child.tagName == "RECORD":
				self.handle_xml(child)

	def handle_xml(self,node):
		element = []
		for child in node.childNodes:
			if child.nodeType == Node.ELEMENT_NODE:
				if child.tagName == "id":
					element.append(self.getText(child.firstChild))
				if child.tagName == "event_id":
					element.append(self.getText(child.firstChild))
				if child.tagName == "start_time":
					element.append(self.getText(child.firstChild))
				if child.tagName == "end_time":
					element.append(self.getText(child.firstChild))
				if child.tagName == "alarm_count":
					element.append(self.getText(child.firstChild))
				if child.tagName == "protocol_id":
					element.append(self.getText(child.firstChild))
				if child.tagName == "src_ip":
					element.append(self.getText(child.firstChild))
				if child.tagName == "dst_ip":
					element.append(self.getText(child.firstChild))
				if child.tagName == "dst_port":
					element.append(self.getText(child.firstChild))
				if child.tagName == "sig":
					element.append(self.getText(child.firstChild))
				if child.tagName == "args":
					element.append(self.getText(child.firstChild))
		print element
		data.append(element)


	def getText(self,node):
		if node.nodeType == Node.TEXT_NODE:
			return node.nodeValue
		else:
			return ""

def getEvents(datas,num):
	events_id = []
	for events in datas:
		events_id.append(event_messages[events[num]])
	return events_id

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
			timeStamp = int(times.mktime(times.strptime(str(data[i+1][0]),"%Y-%m-%d %H:%M:%S")))-int(times.mktime(times.strptime(str(data[i][0]),"%Y-%m-%d %H:%M:%S")))
			if T >= timeStamp:
				n = n + 1
				sumTime = sumTime + timeStamp
				events.append(data[i+1][1])
				timeArray.append(timeStamp)
				T = timeSet(sumTime,n,timeArray)
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
	for timess in timeArray:
		sumInTime = sumInTime + (timess-avgTime)**2
	varTime = (sumInTime/(n-1))**0.5
	stdTime = varTime/avgTime
	Time = avgTime + avgTime*stdTime
	return Time

def loadDataSet():
	return [[11,13,14],[13,12,15],[11,13,12,15],[12,15],[11,13,12,15],[11,13,12,15]]

def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])

	C1.sort()
	return C1

def isSubset(can,tid):
	strcan = []
	#can = json.loads(can)
	lencan = len(can)
	print 'lencan:',can,tid
	i = 0
	for j in range(len(tid)):
		if i < lencan:
			if can[i] == tid[j]:
				strcan.append(can[i])
				print strcan
				i = i + 1
		else:
			return True,json.dumps(strcan)
	if i==lencan:
		return True,json.dumps(strcan)
	return False,json.dumps(strcan)

def scanD(D,Ck,minSupport):
	ssCnt = {}
	D = json.loads(D)
	Ck = json.loads(Ck)
	for tid in D:
		for can in Ck:
			iscan,can = isSubset(can,tid)
			print 'can:',can,iscan
			if iscan == True:
				if not ssCnt.has_key(can):
					print 'haskey:',can
					ssCnt[can] = 1
				else:
					ssCnt[can] += 1
	print 'ssCnt:',ssCnt

	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >= minSupport:
			retList.insert(0,json.loads(key))
		supportData[key] = support
	return retList,supportData

def aprioriGen(Lk,k): #creates Ck
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(0,lenLk):
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			list1 = list(Lk[i])
			list2 = list(Lk[j])
			if L1 == L2:
				if list1 == list2:
					del list1
				else:
					list1.append(list2[-1])
					print list1
					retList.append(list1)
	return retList

def aprioriall(dataSet,minSupport = 0.5):
	C1 = createC1(dataSet)
	C1 = json.dumps(C1)
	D = json.dumps(dataSet)
	L1,supportData = scanD(D,C1,minSupport)
	print 'L1:',L1,'supportData:',supportData
	L = [L1]
	print L
	k = 2
	while (len(L[k-2]) > 0):
		Ck = aprioriGen(L[k-2],k)
		print 'Ck:',Ck
		Ck = json.dumps(Ck)
		Lk,supK = scanD(D,Ck,minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L,supportData

def getData(name):
	data = []
	wb = xlrd.open_workbook(name)
	table = wb.sheets()[0]
	col_data = table.col_values(6)
	len_data = len(col_data)
	for i in range(1,len_data):
		event = []
		event.append(table.cell_value(i,6))
		event.append(table.cell_value(i,2))
		data.append(event)
	return data

def setTimeWindow(data,time,step):
	len_data = len(data)
	events = []
	for i in range(0,len_data,step):
		event = []
		k = i
		end = data[i][0] + datetime.timedelta(seconds = time)
		while end >= data[k][0]:
			if k >= len_data-1:
				break
			print k,len_data
			event.append(int(data[k][1]))
			k = k + 1
		events.append(event)
	return events

if __name__ == '__main__':
	start = times.time()
	'''
	dataSet = loadDataSet()
	C1 = createC1(dataSet)
	print 'C1:',C1
	#D = map(set,dataSet)
	D = json.dumps(dataSet)
	print 'D:',D
	#retList,supportData = scanD(D,C1,0.5)
	#print 'retList:',retList,'supportData:',supportData
	L,suppData = aprioriall(dataSet)
	print L
	print 'L[0]:',L[0]
	print 'L[1]:',L[1]
	print 'L[2]:',L[2]
	print suppData
	'''
	'''
	doc = minidom.parse('ids003#snort0408.xml')
	for child in doc.childNodes:
		if child.nodeType == Node.COMMENT_NODE:
			print "Comment:",child.nodeValue
		if child.nodeType == Node.ELEMENT_NODE:
			XMLscanner(child)
	print data
	events_id = getEvents(data,1)
	print events_id
	len_data = len(events_id)
	frequency = 10
	step = 1
	dataSets = timeWindow(frequency,step,events_id,len_data)
	'''

	getdata = getData('4.xls')
	print 'getdata:',getdata

	#setdata = setTimeWindow(getdata,3,1)
	setdata = setData(getdata)

	fp = open('seqtime.txt','wb')
	for i in setdata:
		fp.writelines(str(i)+'\n')
	fp.close()

	L,suppData = aprioriall(setdata,0.3)
	print 'L:',L,'suppData:',suppData
	fp = open('result.txt','wb')
	for i in L:
		fp.writelines(str(i)+'\n')
	fp.close()
	stop = times.time()
	print str(stop-start)+"秒"
	
