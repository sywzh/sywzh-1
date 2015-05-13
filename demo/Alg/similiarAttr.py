#!/usr/bin/env python
#-*-coding:utf8-*-
import xlrd
import time

def getExcel(name):
	wb = xlrd.open_workbook(name)
	table = wb.sheets()[0]
	col_data = table.col_values(9)
	eventMsg = []
	len_data = len(col_data)
	for i in range(1,len_data):
		events = []
		if col_data[i] != u"/服务器/Windows":
			try:
				events.append(table.cell_value(i,1))
				events.append(table.cell_value(i,3))
				events.append(table.cell_value(i,6))
				events.append(table.cell_value(i,4))
				events.append(table.cell_value(i,7))
				eventMsg.append(events)
			except:
				pass
	return eventMsg

def limitTime(get_time):
	if get_time >= 0 and get_time <1:
		return 10
	if get_time >=1 and get_time < 2:
		return 9
	if get_time >= 2 and get_time < 3:
		return 8
	if get_time >= 3 and get_time < 4:
		return 7
	if get_time >= 4 and get_time < 5:
		return 6
	if get_time >= 5 and get_time < 6:
		return 5
	if get_time >= 6 and get_time < 7:
		return 4
	if get_time >= 7 and get_time < 8:
		return 3
	if get_time >= 8 and get_time < 9:
		return 2
	if get_time >= 9 and get_time < 10:
		return 1
	if get_time >= 10:
		return 0

def manageTime(time1,time2):
	time1=time.strptime(time1,"%Y-%m-%d %H:%M:%S")
	time1 = time.mktime(time1)
	time2 = time.strptime(time2,"%Y-%m-%d %H:%M:%S")
	time2 = time.mktime(time2)
	get_time = time2 - time1
	return limitTime(get_time)

def ipcounts(count):
	if count == 0:
		return 0
	if count == 1:
		return 3
	if count == 2:
		return 5
	if count == 3:
		return 8
	if count == 4:
		return 10

def manageIp(ip1,ip2):
	ip1 = ip1.split('.')
	ip2 = ip2.split('.')
	count = 0
	for i in range(len(ip1)):
		if ip1[i] == ip2[i]:
			count = count + 1
		else:
			break
	if count > 4:
		count = 4
	return ipcounts(count)

def managePort(srcport1,srcport2):
	if srcport1 == srcport2:
		return 1
	else:
		return 0

def manageData(data1,data2,a,b,c,d,e):
	time = manageTime(data1[0],data2[0])
	srcip = manageIp(data1[1],data2[1])
	dstip = manageIp(data1[2],data2[2])
	srcport = managePort(data1[3],data2[3])
	dstport = managePort(data1[4],data2[4])
	return float(time)*a/10+float(srcip)*b/10+float(dstip)*c/10+float(srcport)*d+float(dstport)*e

def resultData(data_list):
	result = 0
	len_data_list = len(data_list)
	if len_data_list == 0:
		return 0
	for i in range(len_data_list):
		result = result + data_list[i]
	return result/len_data_list

def analysisData(data,a=0.3,b=0.3,c=0.3,d=0.05,e=0.05):
	len_data = len(data)
	data_list = []
	for i in range(len_data-1):
		getdata = manageData(data[i],data[i+1],a,b,c,d,e)
		data_list.append(getdata)
	return resultData(data_list)

if __name__ == '__main__':
	eventMsg = getExcel('event1.xls')
	data = analysisData(eventMsg)
	print data
	