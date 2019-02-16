from django.db.models import CharField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class Account(AbstractUser):

	username = CharField(max_length=100, primary_key=True)

	@staticmethod
	def get_by_pk(pk):
		try:
			account = Account.objects.get(pk=pk)
			return account
		except ObjectDoesNotExist:
			return None

	@staticmethod
	def create(username, email, password):
		if username is None or email is None or password is None:
			return None
		account = Account()
		account.username = username
		account.email = email
		account.set_password(password)
		return account

	def edit(self, password=None):
		if password:
			self.set_password(raw_password=password)
		return self

	@staticmethod
	def remove(pk):
		account = Account.get_by_pk(pk)
		if account:
			account.delete()
			return account
		return None
