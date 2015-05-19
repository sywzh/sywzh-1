from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class WarnLog(models.Model):
	user = models.ForeignKey(User,null = True)
	name = models.CharField(max_length = 20)
	time = models.DateTimeField(default = datetime.now())

class WarnNine(models.Model):
	user = models.ForeignKey(User,null = True)
	name = models.CharField(max_length = 60)
	systemtype = models.CharField(max_length = 15)
	gettime = models.CharField(max_length = 20)
	classify = models.CharField(max_length = 10)
	ipsrc = models.CharField(max_length = 16)
	srcport = models.CharField(max_length=5)
	srcname = models.CharField(max_length = 50)
	ipdst = models.CharField(max_length = 16)
	dstport = models.CharField(max_length = 5)
	deviceads = models.CharField(max_length = 16)
	devicetype = models.CharField(max_length = 20)
	event = models.CharField(max_length = 300)

class SafeManager(models.Model):
	user = models.ForeignKey(User,null = True)
	name = models.CharField(max_length = 40)
	support = models.FloatField()
	attack_sequence = models.CharField(max_length = 100)
	attack_name = models.CharField(max_length = 60,default = '')
	time = models.DateTimeField(default = datetime.now())

class Events(models.Model):
	name = models.CharField(max_length = 100)