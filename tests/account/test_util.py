from django.core import mail
from django.test import TestCase

from account.util import gen_password, send_email


class UtilTestCase(TestCase):

	def setUp(self):
		self.user = self.FakeUser(
			'test@mail.com',
			'test',
			'secure_password'
		)

	def test_gen_password(self):
		pwd = gen_password(10, 10)
		self.assertEqual(len(pwd), 10)

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
