from django.utils.timezone import now

from django.test import TestCase

from backup.models import Backup
from account.models import Account


class BackupSerializerTestCase(TestCase):

	timestamp = now()

	def setUp(self):
		self.account = Account(**{
			'username': 'test_username',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		self.account.save()
		self.expected_backup = Backup(**{
			'digest': 'super_hash',
			'timestamp': self.timestamp,
			'backup': 'backup content',
			'account': self.account
		})
		self.expected_backup.save()

	def test_get_by_pk_exists(self):
		actual_backup = Backup.get_by_pk('super_hash')
		self.assertIsNotNone(actual_backup)
		self.assertEqual(self.expected_backup.account, actual_backup.account)
		self.assertEqual(self.expected_backup.digest, actual_backup.digest)
		self.assertEqual(self.expected_backup.timestamp, actual_backup.timestamp)
		self.assertEqual(self.expected_backup.backup, actual_backup.backup)

	def test_get_by_pk_does_not_exist(self):
		self.assertIsNone(Backup.get_by_pk('super_hash1'))

	def test_remove_exists(self):
		backup = Backup.remove('super_hash')
		self.assertIsNotNone(backup)

	def test_remove_does_not_exist(self):
		backup = Backup.remove('super_hash1')
		self.assertIsNone(backup)
