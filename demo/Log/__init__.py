#!/usr/bin/env python
#-*-coding:utf8-*-

from Log.models import Log
def log(userid,operate,name=''):
	print userid,operate
	log = Log(user_id = userid,operation = operate,name = name)
	log.save()