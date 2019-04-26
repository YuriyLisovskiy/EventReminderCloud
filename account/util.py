import random

from django.core.mail import EmailMultiAlternatives
from EventReminderCloud.settings import TESTING


def gen_password(len_from=6, len_to=24):
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=/'
	password_len = random.randrange(len_from, len_to + 1)
	return ''.join([random.choice(alphabet) for _ in range(password_len)])


def send_email(subject, html, plain, receivers, sender):
	msg = EmailMultiAlternatives(subject, plain, sender, receivers)
	msg.attach_alternative(html, 'text/html')
	return msg.send(fail_silently=TESTING)


def get_verification_code(n_digits=6, code_cast_func=str):
	return code_cast_func(random.randrange(10 ** (n_digits - 1), 10 ** n_digits))
