"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SimpleTest(TestCase):

	def setUp(self):
		u = User.objects.create(username = 'test',email = 'test@test.com')
		u.set_password('123456')
		u.save()

	def test_login(self):
		response = self.client.get('/user/login')
		self.failUnlessEqual('',response.content)

	def test_register(self):
		response = self.client.get('/user/register')
		self.failUnlessEqual('',response.content)

	def test_login_post(self):
		u = authenticate(username = 'test',password = '123456')
		self.assertEqual(u.username, 'test')

	def test_logout(self):
		response = self.client.get('/user/logout')
		self.failUnlessEqual('',response.content)

	def test_changepw(self):
		response = self.client.get('/user/changepw')
		self.failUnlessEqual('',response.content)

	def test_changepw_post(self):
		u = authenticate(username = 'test',password = '123456')
		print u
		if u:
			u.set_password("123456")
			u.save()
			self.assertEqual(u.username, 'test')
	
