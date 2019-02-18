import re

from account.models import Account

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

	password = serializers.CharField(required=False, allow_null=False, allow_blank=False)
	username = serializers.CharField(required=False, allow_null=False, allow_blank=False)

	def validate(self, data):
		if self.instance is None:
			if 'email' not in data:
				raise serializers.ValidationError('email is not provided')
			if Account.objects.filter(email=data.get('email')).exists():
				raise serializers.ValidationError('user already exists')
			if 'username' not in data:
				raise serializers.ValidationError('username is not provided')
			if Account.objects.filter(username=data.get('username')).exists():
				raise serializers.ValidationError('user already exists')
		max_backups = data.get('max_backups', None)
		if max_backups is not None:
			try:
				data['max_backups'] = int(max_backups)
			except Exception:
				raise serializers.ValidationError('max backups must be an integer value')
		username = data.get('username', None)
		if username is not None:
			if not re.match(r'^[\w]+$', username):
				raise serializers.ValidationError('password must contain lower and upper-case letters and number')
		return data

	def create(self, validated_data):
		account = Account.create(**validated_data)
		account.save()
		return account

	def update(self, instance, validated_data):
		instance = instance.edit(**{
			'password': validated_data.get('password', None),
			'lang': validated_data.get('lang', None),
			'max_backups': validated_data.get('max_backups', None)
		})
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('username', 'email', 'password', 'lang', 'max_backups')
