#!/usr/bin/env python
#-*-coding:utf8-*-

from decorators import lrender
from django.contrib.auth.decorators import login_required

@login_required
@lrender('home.html')
def IndexHd(request):
	return {}