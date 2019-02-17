import jwt
import ssl
import random
import smtplib
from hashlib import sha256

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from EventReminderCloud.settings import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_USER, EMAIL_PORT


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


def compose_email(receiver, subject, html, plain):
	message = MIMEMultipart('alternative')

	message['Subject'] = subject
	message['From'] = EMAIL_USER
	message['To'] = receiver

	plain_part = MIMEText(plain, 'plain')
	html_part = MIMEText(html, 'html')

	message.attach(plain_part)
	message.attach(html_part)

	return message


def send_html_email(receiver, message):
	with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(EMAIL_USER, EMAIL_PASSWORD)
		server.sendmail(
			EMAIL_USER, receiver, message.as_string()
		)
		server.quit()
