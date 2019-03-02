from django.test import TestCase

from account.models import Account


class AccountTestCase(TestCase):

	def setUp(self):
		self.account = Account(**{
			'username': 'test_username',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		self.account.save()

	def test_get_by_pk_exists(self):
		self.assertIsNotNone(Account.get_by_pk('test_username'))

	def test_get_by_pk_does_not_exist(self):
		self.assertIsNone(Account.get_by_pk('test_username1'))

	def test_create(self):
		actual_account = Account.create(**{
			'username': 'test_username_1',
			'email': 'test_1@gmail.com',
			'password': 'test_password_1',
			'max_backups': 8,
		})
		actual_account.save()
		expected_account = Account.objects.get(pk='test_username_1')
		self.assertEqual(actual_account.username, expected_account.username)
		self.assertEqual(actual_account.email, expected_account.email)
		self.assertEqual(actual_account.password, expected_account.password)
		self.assertEqual(actual_account.max_backups, expected_account.max_backups)

	def test_create_failed_incorrect_username(self):
		account = Account.create(**{
			'username': None,
			'email': 'test_1@gmail.com',
			'password': 'test_password_1'
		})
		self.assertIsNone(account)
		account = Account.create(**{
			'username': '',
			'email': 'test_1@gmail.com',
			'password': 'test_password_1'
		})
		self.assertIsNone(account)

	def test_create_failed_incorrect_email(self):
		account = Account.create(**{
			'username': 'test_username_1',
			'email': None,
			'password': 'test_password_1'
		})
		self.assertIsNone(account)
		account = Account.create(**{
			'username': 'test_username_1',
			'email': '',
			'password': 'test_password_1'
		})
		self.assertIsNone(account)

	def test_create_failed_incorrect_password(self):
		account = Account.create(**{
			'username': 'test_username_1',
			'email': 'test_1@gmail.com',
			'password': None
		})
		self.assertIsNone(account)
		account = Account.create(**{
			'username': 'test_username_1',
			'email': 'test_1@gmail.com',
			'password': ''
		})
		self.assertIsNone(account)

	def test_edit(self):
		self.account.edit(**{
			'password': 'new_password',
			'max_backups': 3
		})
		self.account.save()
		actual = Account.objects.get(pk='test_username')
		self.assertEqual(self.account.password, actual.password)
		self.assertEqual(self.account.max_backups, actual.max_backups)

	def test_remove_exists(self):
		self.assertIsNotNone(Account.remove('test_username'))

	def test_remove_does_not_exist(self):
		self.assertIsNone(Account.remove('test_username1'))
