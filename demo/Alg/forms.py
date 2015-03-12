#!/usr/bin/env python
#-*-coding:utf8-*-
__author__='wzh'

from django import forms

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()