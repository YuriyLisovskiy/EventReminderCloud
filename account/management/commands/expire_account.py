from account.models import Account

from datetime import datetime, timezone, timedelta

from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Expires account objects which are not activated in 24 hours after creation'

	def handle(self, *args, **options):
		unactivated_users = Account.objects.filter(is_activated=False)
		now = datetime.now(tz=timezone.utc)
		expire_time = timedelta(1)
		for user in unactivated_users:
			if (now - user.date_joined) >= expire_time:
				Account.remove(user.username)
