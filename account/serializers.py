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
		account = Account.create(**validated_data)
		account.save()
		return account

	def update(self, instance, validated_data):
		instance = instance.edit(password=validated_data.get('password', None))
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('username', 'email', 'password')
