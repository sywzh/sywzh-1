#!/usr/bin/env python
#-*-coding:utf8-*-

from Alg.models import SafeManager,Events
from rest_framework import serializers

class SafeManagerSerializer(serializers.ModelSerializer):
	class Meta:
		model = SafeManager
		fields = ('id','name','support','attack_sequence','attack_name','time')

class EventsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Events
		fields = ('id','name')
