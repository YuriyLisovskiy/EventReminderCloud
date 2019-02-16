import random

from account.models import Account

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

	def validate(self, data):
		if self.instance is None:
			if Account.objects.filter(email=data.get('email')).exists():
				raise serializers.ValidationError('user already exists')
			if Account.objects.filter(username=data.get('username')).exists():
				raise serializers.ValidationError('user already exists')
		return data

	def create(self, validated_data):
		password = _rand_password()
		validated_data['password'] = password
		account = Account.create(**validated_data)
		account.save()

		print('\nUSERNAME: {}\nPASSWORD: {}\n\n'.format(account.username, password))

		return account

	def update(self, instance, validated_data):
		instance = instance.edit(password=validated_data.get('password', None))
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('username', 'email', 'password')


def _rand_password():
	chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	password = random.choice(chars)
	password_len = random.randrange(8, 13)
	for _ in range(password_len - 1):
		password += random.choice(chars)
	return password
