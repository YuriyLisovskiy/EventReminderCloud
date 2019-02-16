import jwt
import random
from hashlib import sha256


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
