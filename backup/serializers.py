from backup.models import Backup

from rest_framework import serializers


class BackupSerializer(serializers.ModelSerializer):

	hash_sum = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
	timestamp = serializers.DateTimeField(required=True, allow_null=False)
	data = serializers.CharField(required=True, allow_blank=False, allow_null=False)

	def create(self, validated_data):
		backup = Backup(account=self.context['request'].user, **validated_data)
		backup.save()
		return backup

	class Meta:
		model = Backup
		fields = ('hash_sum', 'timestamp', 'data')
