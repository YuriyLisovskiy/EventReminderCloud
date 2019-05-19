from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account


class Backup(models.Model):

	account = models.ForeignKey(Account, on_delete=models.CASCADE, editable=False)
	digest = models.CharField(max_length=128, primary_key=True, editable=False)
	timestamp = models.DateTimeField(auto_now=True, editable=False)
	backup = models.TextField(blank=False, null=False, editable=False)
	events_count = models.IntegerField(default=0, blank=False, editable=False)
	backup_size = models.CharField(max_length=100, default='0 bytes', blank=False, editable=False)
	contains_settings = models.BooleanField(default=False, blank=False, editable=False)

	@staticmethod
	def get_by_pk(pk):
		try:
			return Backup.objects.get(pk=pk)
		except ObjectDoesNotExist:
			return None

	@staticmethod
	def remove(pk):
		backup = Backup.get_by_pk(pk)
		if backup:
			backup.delete()
			return backup
		return None
