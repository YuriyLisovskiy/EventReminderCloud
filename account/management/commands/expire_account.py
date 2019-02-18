from django.core.management.base import BaseCommand

from account.models import Account


class Command(BaseCommand):
	help = 'Expires account objects which are not activated in 24 hours after creation'

	def handle(self, *args, **options):
		unactivated_users = Account.objects.filter(is_activated=False)
		for user in unactivated_users:
			print(user.date_joined)
