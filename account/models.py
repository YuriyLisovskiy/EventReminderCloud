from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class Account(AbstractUser):

	@staticmethod
	def get_by_id(pk):
		try:
			account = Account.objects.get(pk=pk)
			return account
		except ObjectDoesNotExist:
			return None

	@classmethod
	def filter_by(cls, username=None, email=None, **kwargs):
		query = {}
		if username:
			query['username'] = username
		if email:
			query['email'] = email
		query.update(**kwargs)
		return cls.objects.filter(**query)

	@staticmethod
	def create(username, email, password, save=True):
		if username is None or email is None or password is None:
			return None
		account = Account()
		account.username = username
		account.email = email
		account.set_password(password)
		if save:
			account.save()
		return account

	def edit(self, username=None, password=None, save=True):
		if username:
			self.username = username
		if password:
			self.set_password(raw_password=password)
		if save:
			self.save()

	@staticmethod
	def remove(pk):
		account = Account.get_by_id(pk)
		if account:
			account.delete()
			return account
		return None
