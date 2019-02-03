from backup.models import Backup

from rest_framework import serializers


class BackupSerializer(serializers.ModelSerializer):

	account = serializers.IntegerField(required=True, allow_null=False)
	hash_sum = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
	timestamp = serializers.DateTimeField(required=True, allow_null=False)
	data = serializers.CharField(required=True, allow_blank=False, allow_null=False)

	def create(self, validated_data):
		backup = Backup(**validated_data)
		backup.save()
		return backup

	class Meta:
		model = Backup
		fields = '__all__'
