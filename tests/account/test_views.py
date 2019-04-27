import re

from django.core import mail
from django.test import TestCase

from account.models import Account


class SendTokenAPIViewTestCase(TestCase):

	def setUp(self):
		Account.objects.create(**{
			'username': 'test_user',
			'email': 'test.user@gmail.com',
			'password': 'test_password'
		})

	def test_post_201_created(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

	def test_post_404_not_found(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user1@gmail.com'
		})
		self.assertEqual(response.status_code, 404)
		self.assertTrue('detail' in response.json())

	def test_post_400_bad(self):
		response = self.client.post('/api/v1/accounts/send/verification/code')
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())


class AccountDeleteAPIViewTestCase(TestCase):

	def setUp(self):
		Account.create(**{
			'username': 'test_user',
			'email': 'test.user@gmail.com',
			'password': 'test_password'
		}).save()

	def test_post_201_created(self):
		response = self.client.post('/api/v1/login', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		response = self.client.post('/api/v1/accounts/delete', **{
			'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

	def test_post_401_unauthorized(self):
		response = self.client.post('/api/v1/accounts/delete')
		self.assertEqual(response.status_code, 401)
		self.assertTrue('detail' in response.json())


class AccountCreateAPIViewTestCase(TestCase):

	def test_post_201_created(self):
		response = self.client.post('/api/v1/accounts/create', {
			'username': 'test_user',
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

	def test_post_400_bad_username_is_not_provided(self):
		response = self.client.post('/api/v1/accounts/create', {
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('non_field_errors' in response.json())

	def test_post_400_bad_email_is_not_provided(self):
		response = self.client.post('/api/v1/accounts/create', {
			'username': 'test_user'
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('non_field_errors' in response.json())


class ResetPasswordAPIViewTestCase(TestCase):

	def setUp(self):
		Account.objects.create(**{
			'username': 'test_user',
			'email': 'test.user@gmail.com',
			'password': 'test_password'
		})

	def test_post_201_created(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

		self.assertEqual(len(mail.outbox), 1)

		verification_code = re.search(r'code:\s*([0-9]{6})', str(mail.outbox[0].body)).group(1)

		response = self.client.post('/api/v1/accounts/password/reset', data={
			'email': 'test.user@gmail.com',
			'new_password': 'new_test_password',
			'new_password_confirm': 'new_test_password',
			'verification_code': verification_code
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

	def test_post_400_username_is_not_provided(self):
		response = self.client.post('/api/v1/accounts/password/reset')
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())

	def test_post_404_account_is_not_found(self):
		response = self.client.post('/api/v1/accounts/password/reset', data={
			'email': 'some.user@gmail.com'
		})
		self.assertEqual(response.status_code, 404)
		self.assertTrue('detail' in response.json())

	def test_post_400_missing_confirmation_token(self):
		response = self.client.post('/api/v1/accounts/password/reset', data={
			'username': 'test_user'
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())

	def test_post_400_token_token_is_incorrect(self):
		response = self.client.post('/api/v1/accounts/password/reset', data={
			'username': 'test_user',
			'confirmation_token': 'some1token'
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())

	def test_post_400_missing_new_password(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

		self.assertEqual(len(mail.outbox), 1)

		verification_code = re.search(r'code:\s*([0-9]{6})', str(mail.outbox[0].body)).group(1)

		response = self.client.post('/api/v1/accounts/password/reset', data={
			'email': 'test.user@gmail.com',
			'new_password_confirm': 'new_test_password',
			'verification_code': verification_code
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())

	def test_post_400_missing_password_confirm(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

		self.assertEqual(len(mail.outbox), 1)

		token = re.search(r'code:\s*([0-9]{6})', str(mail.outbox[0].body)).group(1)

		response = self.client.post('/api/v1/accounts/password/reset', data={
			'email': 'test.user@gmail.com',
			'new_password': 'new_test_password',
			'confirmation_token': token
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())

	def test_post_400_password_confirmation_failed(self):
		response = self.client.post('/api/v1/accounts/send/verification/code', data={
			'email': 'test.user@gmail.com'
		})
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())

		self.assertEqual(len(mail.outbox), 1)

		token = re.search(r'code:\s*([0-9]{6})', str(mail.outbox[0].body)).group(1)

		response = self.client.post('/api/v1/accounts/password/reset', data={
			'email': 'test.user@gmail.com',
			'new_password': 'new_test_password',
			'new_password_confirm': 'new_test_password_another',
			'confirmation_token': token
		})
		self.assertEqual(response.status_code, 400)
		self.assertTrue('detail' in response.json())


class AccountEditAPIViewTestCase(TestCase):

	def setUp(self):
		Account.create(**{
			'username': 'test_user',
			'email': 'test.user@gmail.com',
			'password': 'test_password'
		}).save()
		response = self.client.post('/api/v1/login', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))}

	def test_post_201_created(self):
		account = Account.get_by_pk('test_user')
		self.assertEqual(account.max_backups, 5)
		response = self.client.post('/api/v1/accounts/edit', data={
			'max_backups': 7,
		}, **self.header)
		self.assertEqual(response.status_code, 201)
		self.assertTrue('detail' in response.json())
		account = Account.get_by_pk('test_user')
		self.assertEqual(account.max_backups, 7)

	def test_post_400_max_backups_is_non_number(self):
		account = Account.get_by_pk('test_user')
		self.assertEqual(account.max_backups, 5)
		response = self.client.post('/api/v1/accounts/edit', data={
			'max_backups': 'f',
		}, **self.header)
		self.assertEqual(response.status_code, 400)


class AccountDetailsAPIViewTestCase(TestCase):

	def setUp(self):
		self.account = Account.create(**{
			'username': 'test_user',
			'email': 'test.user@gmail.com',
			'password': 'test_password'
		})
		self.account.save()
		response = self.client.post('/api/v1/login', data={
			'username': 'test_user',
			'password': 'test_password'
		})
		self.header = {'HTTP_AUTHORIZATION': 'Token {}'.format(response.json().get('key'))}

	def test_get_200_ok(self):
		response = self.client.get('/api/v1/accounts/user', **self.header)
		self.assertEqual(response.status_code, 200)
		content = response.json()
		self.assertEqual(self.account.username, content['username'])
		self.assertEqual(self.account.email, content['email'])
		self.assertEqual(self.account.max_backups, content['max_backups'])

	def test_get_401_unauthorized(self):
		response = self.client.get('/api/v1/accounts/user')
		self.assertEqual(response.status_code, 401)


class AccountActivateViaLoginViewTestCase(TestCase):

	def setUp(self):
		Account.create(**{
			'username': 'test_u_name',
			'email': 'test@gmail.com',
			'password': 'test_password'
		}).save()

	def test_activate_via_login(self):
		self.assertFalse(Account.get_by_pk('test_u_name').is_activated)
		response = self.client.post('/api/v1/login', {
			'email': 'test@gmail.com',
			'password': 'test_password'
		})
		self.assertEqual(response.status_code, 200)
		self.assertTrue(Account.get_by_pk('test_u_name').is_activated)
