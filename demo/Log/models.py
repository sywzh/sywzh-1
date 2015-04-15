#!/usr/bin/env python
#-*-coding:utf8-*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Log(models.Model):

	OP_CHANGES = (
		('',''),
		('1','登录'),
		('2','上传日志'),
		('3','下载'),
		('4','关联分析'),
		('5','量化分析')
		)

	user = models.ForeignKey(User)
	name = models.CharField(max_length = 40,null = True,blank = True)
	operation = models.CharField(max_length = 2,choices = OP_CHANGES)
	time = models.DateTimeField(default = datetime.now)

	def Status(self):
		return dict(self.OP_CHANGES)[self.operation]

	class Meta:
		ordering = ['-time']
