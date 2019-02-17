from django.core import mail
from django.test import TestCase

from account.util import token_is_valid, gen_password, send_email


class UtilTestCase(TestCase):

	def setUp(self):
		self.user = self.FakeUser(
			'test@mail.com',
			'test',
			'secure_password'
		)
		self.secret_key = 'SuPeR_SeCrEt_KeY!'
		self.nonce = '7ef198c01d5dd45dd7d2bf97089a5e41e5974dc7a8880f79c48cee9f52c66e9c'
		self.token = '01cb2b432c2568227d140307f9d621a5ab8f789af51592303d8e9b302c06e2a0'

	def test_gen_password(self):
		pwd = gen_password(10, 10)
		self.assertEqual(len(pwd), 10)

	def test_token_is_valid_true(self):
		self.assertTrue(token_is_valid(self.user, self.secret_key, self.nonce, self.token))

	def test_token_is_valid_false(self):
		token = '01cb2b432c2568227d140307f9d621a5ab8f889af51592303d8e9b302c06e2a0'
		self.assertFalse(token_is_valid(self.user, self.secret_key, self.nonce, token))

	def test_send_email(self):
		send_email('Test subject', '<p>Test body .html</p>', 'Test body .txt', ['to@gmail.com'], 'from@gmail.com')
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].subject, 'Test subject')
		self.assertEqual(mail.outbox[0].from_email, 'from@gmail.com')
		self.assertListEqual(mail.outbox[0].to, ['to@gmail.com'])
		self.assertEqual(mail.outbox[0].body, 'Test body .txt')

	class FakeUser:

		def __init__(self, email, username, password):
			self.email = email
			self.username = username
			self.password = password
