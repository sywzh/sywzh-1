#!/usr/bin/python
#-*-coding:utf8-*-

from django.core.management import setup_environ
import settings

setup_environ(settings)
import os
from django.db import connection
cur = connection.cursor()
dbname = settings.DATABASES['default']['NAME']
try:
	cur.execute('drop database %s;' %dbname)
except:
	pass

cur.execute('create database %s CHARACTER SET utf8;' %dbname)
cur.execute('use %s' %dbname)
cur.close()

if os.system('echo "no" | python ../manage.py syncdb'):
	exit(-1)

from django.contrib.auth.models import User
u = User(username = 'wzh',email = '821308407@qq.com')
u.set_password('123456')
u.is_staff = True
u.is_superuser = True
u.is_active = True
u.save()

