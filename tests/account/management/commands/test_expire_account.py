from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.core.management import call_command

from account.models import Account


class CommandsTestCase(TestCase):

	def setUp(self):
		Account.objects.create(**{
			'username': 'test_user_1',
			'email': 'test.user.1@gmail.com',
			'password': 'test_user_1_password',
			'date_joined': now() - timedelta(1)
		})
		Account.objects.create(**{
			'username': 'test_user_2',
			'email': 'test.user.2@gmail.com',
			'password': 'test_user_2_password'
		})

	def test_expire_account(self):
		self.assertIsNotNone(Account.get_by_pk('test_user_1'))
		self.assertIsNotNone(Account.get_by_pk('test_user_2'))

		call_command('expire_account')

		self.assertIsNone(Account.get_by_pk('test_user_1'))
		self.assertIsNotNone(Account.get_by_pk('test_user_2'))
