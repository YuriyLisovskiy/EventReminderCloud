from django.test import TestCase
from django.utils.timezone import now

from backup.models import Backup
from account.models import Account


class BackupListViewTestCase(TestCase):
	timestamp = now()

	def setUp(self):
		account = Account.create(**{
			'username': 'test_user',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		account.save()
		response = self.client.post('/api/v1/auth/login/', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.auth_token_header = {
			'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))
		}
		account_1 = Account.create(**{
			'username': 'test_user1',
			'email': 'test1@gmail.com',
			'password': 'test_password1'
		})
		account_1.save()
		backup = Backup(**{
			'account': account,
			'digest': 'somedigest',
			'timestamp': self.timestamp,
			'backup': 'encoded backup data'
		})
		backup.save()
		backup_1 = Backup(**{
			'account': account,
			'digest': 'somedigest_1',
			'timestamp': self.timestamp,
			'backup': 'encoded backup data 1'
		})
		backup_1.save()
		Backup(**{
			'account': account_1,
			'digest': 'somedigest_2',
			'timestamp': self.timestamp,
			'backup': 'encoded backup data 2'
		}).save()
		self.expected_list = [
			{'digest': backup_1.digest, 'timestamp': backup_1.timestamp},
			{'digest': backup.digest, 'timestamp': backup.timestamp}
		]

	def test_get_list_exists(self):
		response = self.client.get('/api/v1/backups/', **self.auth_token_header)
		self.assertEqual(response.status_code, 200)
		actual_list = response.json()
		for i in range(len(actual_list)):
			self.assertEqual(actual_list[i]['digest'], self.expected_list[i]['digest'])
			self.assertEqual(actual_list[i]['timestamp'],
			                 self.expected_list[i]['timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))


class BackupDetailsViewTestCase(TestCase):
	timestamp = now()

	def setUp(self):
		account = Account.create(**{
			'username': 'test_user',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		account.save()
		response = self.client.post('/api/v1/auth/login/', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.auth_token_header = {
			'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))
		}
		self.backup = Backup(**{
			'account': account,
			'digest': 'somedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestmedigest',
			'timestamp': self.timestamp,
			'backup': 'encoded backup data'
		})
		self.backup.save()

	def test_get_200_ok(self):
		response = self.client.get('/api/v1/backups/details/{}'.format(self.backup.digest), **self.auth_token_header)
		self.assertEqual(response.status_code, 200)
		content = response.json()
		self.assertEqual(content['digest'], self.backup.digest)
		self.assertEqual(content['backup'], self.backup.backup)
		self.assertEqual(content['timestamp'], self.backup.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

	def test_get_404_not_found(self):
		response = self.client.get('/api/v1/backups/details/{}'.format('f' + self.backup.digest[1:]), **self.auth_token_header)
		self.assertEqual(response.status_code, 404)


class BackupDeleteViewTestCase(TestCase):
	timestamp = now()

	def setUp(self):
		account = Account.create(**{
			'username': 'test_user',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		account.save()
		response = self.client.post('/api/v1/auth/login/', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.auth_token_header = {
			'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))
		}
		self.backup = Backup(**{
			'account': account,
			'digest': 'somedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestsomedigestmedigest',
			'timestamp': self.timestamp,
			'backup': 'encoded backup data'
		})
		self.backup.save()

	def test_get_200_ok(self):
		response = self.client.post('/api/v1/backups/delete/{}'.format(self.backup.digest), **self.auth_token_header)
		self.assertEqual(response.status_code, 201)

	def test_get_404_not_found(self):
		response = self.client.post('/api/v1/backups/delete/{}'.format('f' + self.backup.digest[1:]), **self.auth_token_header)
		self.assertEqual(response.status_code, 404)


class BackupCreateViewTestCase(TestCase):

	def setUp(self):
		self.account = Account.create(**{
			'username': 'test_user',
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		self.account.save()
		response = self.client.post('/api/v1/auth/login/', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.auth_token_header = {
			'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))
		}
		for i in range(4):
			Backup(**{
				'account': self.account,
				'digest': 'some_digest_{}'.format(i),
				'timestamp': now(),
				'backup': 'encoded backup data {}'.format(i)
			}).save()

	def test_post_201_created(self):
		response = self.client.post('/api/v1/backups/create', data={
			'account': self.account,
			'digest': 'some_digest_4',
			'timestamp': now(),
			'backup': 'encoded backup data 4'
		}, **self.auth_token_header)
		self.assertEqual(response.status_code, 201)

	def test_post_201_created_max_backups_reached(self):
		Backup(**{
			'account': self.account,
			'digest': 'some_digest_4',
			'timestamp': now(),
			'backup': 'encoded backup data 4'
		}).save()
		self.assertIsNotNone(Backup.get_by_pk('some_digest_0'))
		response = self.client.post('/api/v1/backups/create', data={
			'account': self.account,
			'digest': 'some_digest',
			'timestamp': now(),
			'backup': 'encoded backup data'
		}, **self.auth_token_header)
		self.assertEqual(response.status_code, 201)
		self.assertIsNone(Backup.get_by_pk('some_digest_0'))

	def test_post_400_(self):
		response = self.client.post('/api/v1/backups/create', data={
			'account': self.account,
			'digest': 'some_digest_0',
			'timestamp': now(),
			'backup': 'encoded backup data'
		}, **self.auth_token_header)
		self.assertEqual(response.status_code, 400)
