#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__='wzh'
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from demo.decorators import lrender
from django.contrib.auth import authenticate,login,logout
from django.utils import simplejson
from Log import log
from django.core.urlresolvers import reverse

@lrender('login.html')
def logoHd(request):
	return {}

def LoginHd(request):
	if not request.is_ajax() or request.method != "POST":
		return HttpResponseRedirect(reverse('User.views.logoHd'))
	username = request.POST.get("username")
	password = request.POST.get("password")
	user = authenticate(username = username,password = password)
	if user:
		login(request,user)
		log(request.user.id,'1',user.username)
		return HttpResponse(simplejson.dumps({'message':'ok'}))
	return HttpResponse(simplejson.dumps({'message':'error'}))

def RegisterHd(request):
	if not request.is_ajax() or request.method != "POST":
		return HttpResponseRedirect(reverse('User.views.logoHd'))
	username = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	try:
		op = User(username = username,email = email)
		op.set_password(password)
		op.save()
		return HttpResponse(simplejson.dumps({'message':'ok'}))
	except:
		return HttpResponse(simplejson.dumps({'message':'error'}))

def LogoutHd(request):
	logout(request)
	return HttpResponseRedirect(reverse('User.views.logoHd'))

def ModifyPw(request):
	if not request.is_ajax() or request.method != 'POST':
		return HttpResponseRedirect(reverse('User.views.logoHd'))
	username = request.user
	old_password = request.POST.get("old_password")
	user = authenticate(username = username,password = old_password)
	if user is not None:
		new_password = request.POST.get("new_password")
		user.set_password(new_password)
		user.save()
		return HttpResponse(simplejson.dumps({'message':'ok'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'error'}))