from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Log(models.Model):
	user = models.ForeignKey(User)
	operation = models.CharField(max_length = 20)
	time = models.DateTimeField(default = datetime.now)
