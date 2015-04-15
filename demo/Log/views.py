#!/usr/bin/env python
#-*-coding:utf8-*-

from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from demo.decorators import lrender
from Log.models import Log

@lrender('log/log.html')
def historyLog(request):
	logs = Log.objects.filter(user__username = request.user)
	return {'logs':logs}