from datetime import datetime

from django.test import TestCase

from account.models import Account
from backup.serializers import BackupSerializer


class BackupSerializerTestCase(TestCase):

	timestamp = datetime.now()

	def setUp(self):
		self.user = Account(**{
			'username': 'test_username',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		self.backup_attributes = {
			'digest': 'super_hash',
			'timestamp': self.timestamp,
			'backup': 'backup content'
		}
		self.serializer = BackupSerializer(data=self.backup_attributes, context={'request': self.FakeRequest(self.user)})
		self.serializer.is_valid()

	def test_is_valid(self):
		self.assertTrue(self.serializer.is_valid())

	def test_digest(self):
		self.assertEqual(self.backup_attributes.get('digest'), self.serializer.data.get('digest'))

	def test_timestamp(self):
		self.assertEqual(
			self.backup_attributes.get('timestamp').strftime('%Y-%m-%d %H:%M:%S'),
			self.serializer.data.get('timestamp')
		)

	def test_backup(self):
		self.assertEqual(self.backup_attributes.get('backup'), self.serializer.data.get('backup'))

	def test_already_exists(self):
		self.serializer.save()
		serializer = BackupSerializer(data=self.backup_attributes, context={'request': self.FakeRequest(self.user)})
		self.assertFalse(serializer.is_valid())

	class FakeRequest:

		def __init__(self, user):
			self.user = user
