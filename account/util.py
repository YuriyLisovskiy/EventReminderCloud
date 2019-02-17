import jwt
import random
from hashlib import sha256

from django.core.mail import EmailMultiAlternatives
from EventReminderCloud.settings import TESTING


def gen_password(len_from=8, len_to=24):
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=/'
	password_len = random.randrange(len_from, len_to + 1)
	return ''.join([random.choice(alphabet) for _ in range(password_len)])


def token_is_valid(account, secret_key, nonce, token):
	payload = {
		'email': account.email,
		'username': account.username,
		'password': account.password,
		'nonce': nonce
	}
	return sha256(jwt.encode(payload, secret_key, algorithm='HS256')).hexdigest() == token


def send_email(subject, html, plain, receivers, sender):
	msg = EmailMultiAlternatives(subject, plain, sender, receivers)
	msg.attach_alternative(html, 'text/html')
	return msg.send(fail_silently=TESTING)
