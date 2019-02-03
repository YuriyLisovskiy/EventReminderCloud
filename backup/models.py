from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account


class Backup(models.Model):

	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	hash_sum = models.CharField(max_length=128, blank=False, null=False)
	timestamp = models.DateTimeField(default=now)
	data = models.TextField(blank=False, null=False)

	@staticmethod
	def get_by_id(pk):
		try:
			return Backup.objects.get(pk=pk)
		except ObjectDoesNotExist:
			return None

	@staticmethod
	def remove(pk):
		backup = Backup.get_by_id(pk)
		if backup:
			backup.delete()
			return backup
		return None
