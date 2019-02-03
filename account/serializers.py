from account.models import Account

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

	password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
	username = serializers.CharField(required=True)
	email = serializers.EmailField(required=True, allow_blank=False)

	def create(self, validated_data):
		account = Account(**validated_data)
		account.set_password(validated_data.get('password'))
		account.save()
		return account

	class Meta:
		model = Account
		fields = ('username', 'email')


class AccountEditSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only=True)
	password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

	def update(self, instance, validated_data):
		instance.set_password(validated_data.get('password', instance.password))
		instance.save()
		return instance

	class Meta:
		model = Account
		fields = ('username', 'email')
