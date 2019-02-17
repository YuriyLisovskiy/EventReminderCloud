from django.test import TestCase

from rest_framework import serializers

from account.models import Account
from account.serializers import AccountSerializer


class AccountSerializerTestCase(TestCase):

	def setUp(self):
		self.account_data = {
			'username': 'test_username',
			'email': 'test@gmail.com',
			'password': 'test_password'
		}
		self.account = Account(**self.account_data)
		self.account.save()
		self.serializer = AccountSerializer(data=self.account_data)

	def test_validate(self):
		data = {
			'username': 'test_username1',
			'email': 'test1@gmail.com',
			'password': 'test_password1'
		}
		self.assertDictEqual(data, self.serializer.validate(data))

	def test_validate_raises_email(self):
		data = {
			'username': 'test_username1',
			'email': 'test@gmail.com',
			'password': 'test_password1'
		}
		self.assertRaises(serializers.ValidationError, self.serializer.validate, data=data)

	def test_validate_raises_username(self):
		data = {
			'username': 'test_username',
			'email': 'test1@gmail.com',
			'password': 'test_password1'
		}
		self.assertRaises(serializers.ValidationError, self.serializer.validate, data=data)

	def test_validate_raises_max_backups_is_non_number(self):
		data = {
			'username': 'test_username1',
			'email': 'test1@gmail.com',
			'password': 'test_password1',
			'max_backups': '7'
		}
		serializer = AccountSerializer(data=data)
		self.assertRaises(serializers.ValidationError, serializer.validate, *(data,))

	def test_create(self):
		data = {
			'username': 'test_username1',
			'email': 'test1@gmail.com',
			'password': 'test_password1',
			'max_backups': 7
		}
		serializer = AccountSerializer(data=data)
		serializer.create(data)
		account = Account.objects.get(pk='test_username1')
		self.assertEqual(account.email, data['email'])
		self.assertEqual(account.username, data['username'])
		self.assertEqual(account.max_backups, data['max_backups'])
		self.assertTrue(account.check_password('test_password1'))

	def test_update(self):
		data = {
			'password': 'new_super_password'
		}
		serializer = AccountSerializer(instance=self.account, data=data)
		serializer.update(self.account, data)
		account = Account.objects.get(pk='test_username')
		self.assertTrue(account.check_password('new_super_password'))
