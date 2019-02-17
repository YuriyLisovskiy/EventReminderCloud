from account.models import Account

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

	def validate(self, data):
		if self.instance is None:
			if 'email' not in data:
				raise serializers.ValidationError('email is not provided')
			if Account.objects.filter(email=data.get('email')).exists():
				raise serializers.ValidationError('user already exists')
			if Account.objects.filter(username=data.get('username')).exists():
				raise serializers.ValidationError('user already exists')
		max_backups = data.get('max_backups', None)
		if max_backups is not None:
			if not isinstance(max_backups, int):
				raise serializers.ValidationError('max backups must be an integer value')
		return data

	def create(self, validated_data):
		account = Account.create(**validated_data)
		account.save()
		return account

	def update(self, instance, validated_data):
		instance = instance.edit(password=validated_data.get('password', None))
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('username', 'email', 'password', 'lang', 'max_backups')
