from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField, PositiveIntegerField, BooleanField, EmailField


class Account(AbstractUser):
	MIN_BACKUPS_VAL = 1
	MAX_BACKUPS_VAL = 10

	username = CharField(max_length=100, primary_key=True)
	email = EmailField(blank=False, unique=True)
	lang = CharField(max_length=2, default='en')
	max_backups = PositiveIntegerField(default=5, validators=[
		MinValueValidator(MIN_BACKUPS_VAL), MaxValueValidator(MAX_BACKUPS_VAL)
	])
	is_activated = BooleanField(default=False)

	@staticmethod
	def get_by_pk(pk):
		try:
			account = Account.objects.get(pk=pk)
			return account
		except ObjectDoesNotExist:
			return None

	@staticmethod
	def create(username, email, password, lang=None, max_backups=None):
		if username is None or username == '' or email is None or email == '' or password is None or password == '':
			return None
		account = Account()
		account.username = username
		account.email = email
		account.set_password(password)
		if lang is not None:
			account.lang = lang
		if max_backups is not None:
			if Account.MIN_BACKUPS_VAL <= max_backups <= Account.MAX_BACKUPS_VAL:
				account.max_backups = max_backups
		return account

	def edit(self, password=None, lang=None, max_backups=None, is_activated=None):
		if password is not None:
			self.set_password(raw_password=password)
		if lang is not None:
			self.lang = lang
		if max_backups is not None:
			if self.MIN_BACKUPS_VAL <= max_backups <= self.MAX_BACKUPS_VAL:
				self.max_backups = max_backups
		if is_activated is not None:
			self.is_activated = is_activated
		return self

	@staticmethod
	def remove(pk):
		account = Account.get_by_pk(pk)
		if account:
			account.delete()
			return account
		return None
