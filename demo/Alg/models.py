from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class WarnLog(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 60)

class Warn(models.Model):
	user = models.ForeignKey(User)
	name = models.ForeignKey(WarnLog)
	attack_name = models.CharField(max_length = 60)
	attack_type = models.CharField(max_length = 60)
	ipsrc = models.CharField(max_length = 16)
	ipdst = models.CharField(max_length = 16)
	srcport = models.IntegerField()
	dstport = models.IntegerField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

class WarnNine(models.Model):
	user = models.ForeignKey(User)
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

class Correlation(models.Model):
	name = models.ForeignKey(WarnLog)
	algorithm = models.CharField(max_length = 20)
	support = models.FloatField()
	time = models.FloatField()

class SafeManager(models.Model):
	user = models.ForeignKey(User)
	name = models.ForeignKey(WarnLog)
	attack_sequence = models.CharField(max_length = 100)
	attack_name = models.CharField(max_length = 60)

	

