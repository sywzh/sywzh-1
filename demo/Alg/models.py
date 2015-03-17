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

	

