import random

from account.models import Account

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

	username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
	email = serializers.EmailField(required=True, allow_blank=False)

	def validate(self, data):
		if Account.objects.filter(email=data.get('email')).exists():
			raise serializers.ValidationError('user already exists')
		if Account.objects.filter(username=data.get('username')).exists():
			raise serializers.ValidationError('user already exists')
		return data

	def create(self, validated_data):
		account = Account(**validated_data)
		random_password = self.rand_password()

		print('\nUSERNAME: {}\nPASSWORD: {}\n\n'.format(validated_data['username'], random_password))

		account.set_password(random_password)
		account.save()
		return account

	@staticmethod
	def rand_password():
		chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		password = random.choice(chars)
		password_len = random.randrange(8, 13)
		for _ in range(password_len - 1):
			password += random.choice(chars)
		return password

	class Meta:
		model = Account
		fields = ('username', 'email')


class AccountEditSerializer(serializers.ModelSerializer):

	pk = serializers.IntegerField(read_only=True)
	password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

	def update(self, instance, validated_data):
		instance.set_password(validated_data.get('password', instance.password))
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('email',)
