from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account


class Backup(models.Model):

	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	digest = models.CharField(max_length=128, primary_key=True)
	timestamp = models.DateTimeField(auto_now=True)
	backup = models.TextField(blank=False, null=False)

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
