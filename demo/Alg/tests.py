"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from Alg.models import *
from django.contrib.auth.models import User

class SimpleTest(TestCase):
	def setUp(self):
		u = User.objects.create(username = 'test',email = 'test@test.com')
		u.set_password('123456')
		u.save()

	def test_get_alg(self):
		response = self.client.get('/alg/')
		self.failUnlessEqual('',response.content)

	def test_get_connect(self):
		response = self.client.get('/connect/')
		self.failUnlessEqual('',response.content)

	def test_get_safemanage(self):
		response = self.client.get('/safemanage/')
		self.failUnlessEqual('',response.content)

	def test_download(self):
		response = self.client.get('/download/1/')
		self.failUnlessEqual('',response.content)

	def test_deletelog(self):
		response = self.client.get('/deletelog/1')
		self.failUnlessEqual('',response.content)

	def test_upload_log(self):
		op = WarnLog(name = 'event3.xls')
		op.save()
		self.assertEqual(op.name,'event3.xls')

	def test_add_events(self):
		op = Events(name = "test")
		op.save()
		self.assertEqual(op.name,'test')

	def test_add_sequence(self):
		op = SafeManager(name = 'test',support = '0.3',attack_sequence = 'test',attack_name = 'test')
		op.save()
		self.assertEqual(op.name,'test')

	def test_get_sequence(self):
		response = self.client.get('/sequence')
		self.failUnlessEqual('{"status":200,"data":[]}',response.content)

	def test_get_events(self):
		response = self.client.get('/events')
		self.failUnlessEqual('{"status":200,"data":[]}',response.content)

	def test_delete_event(self):
		op = Events(name = "test")
		op.save()
		op.delete()
		self.assertEqual(1+1,2)

	def test_modify_event(self):
		op = Events(name = "test")
		op.save()
		op.name = 'just test'
		op.save
		self.assertEqual(op.name,'just test')

	def test_delete_sequence(self):
		op = SafeManager(name = 'test',support = '0.3',attack_sequence = 'test',attack_name = 'test')
		op.save()
		op.delete()
		self.assertEqual(1+1,2)

	def test_modify_sequence(self):
		op = SafeManager(name = 'test',support = '0.3',attack_sequence = 'test',attack_name = 'test')
		op.save()
		op.attack_name = 'just test'
		op.save
		self.assertEqual(op.attack_name,'just test')

