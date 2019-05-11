from backup.models import Backup

from rest_framework import serializers


class BackupSerializer(serializers.ModelSerializer):

	digest = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
	timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=True, allow_null=False)
	backup = serializers.CharField(required=True, allow_blank=False, allow_null=False)
	backup_size = serializers.CharField(required=True, allow_null=False, allow_blank=False)
	events_count = serializers.IntegerField(required=True, allow_null=False)
	contains_settings = serializers.BooleanField(required=True, allow_null=False)

	def validate(self, data):
		digest = data.get('digest')
		if Backup.get_by_pk(digest) is not None:
			raise serializers.ValidationError('backup {} already exists'.format(digest))
		return data

	def create(self, validated_data):
		backup = Backup(account=self.context['request'].user, **validated_data)
		backup.save()
		return backup

	class Meta:
		model = Backup
		fields = ('digest', 'timestamp', 'backup')


class BackupListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Backup
		fields = ('digest', 'timestamp', 'backup_size', 'events_amount', 'contains_settings')
