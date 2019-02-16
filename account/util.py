import jwt
import random


def gen_password(len_from=8, len_to=24):
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=/'
	password_len = random.randrange(len_from, len_to)
	return ''.join([random.choice(alphabet) for _ in range(password_len)])


def token_is_valid(request, secret_key):
	payload = jwt.decode(request.data.get('confirmation_token'), secret_key, algorithms=['HS256'])
	return all([
		payload['nonce'] == request.session.get('{}_nonce'.format(request.user.email), None),
		payload['email'] == request.user.email,
		payload['username'] == request.user.username,
		payload['password'] == request.user.password
	])
