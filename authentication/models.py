from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class AccountManager(BaseUserManager):

	def create_user(self, email, password=None, **kwargs):
		if not email:
			raise ValueError('Users must have a valid email address.')

		if not kwargs.get('username'):
			raise ValueError('Users must have a valid username')

		account = self.model(
			email=self.normalize_email(email), username=kwargs.get('username')
		)

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)

		account.is_admin=True
		account.save()

		return account


class Account(AbstractBaseUser):
	#making sure the email submitted is a unique email address
	email = models.EmailField(unique=True)
	#making sure the username field has a name <= the max length and is a unique username
	username = models.CharField(max_length=40, unique=True)

	#implementing the first, last, and tagline fields which dont have to be filled out
	#this is indicated by "blank=True"
	first_name = models.CharField(max_length=40, blank=True)
	last_name = models.CharField(max_length=40, blank=True)
	tagline = models.CharField(max_length=150, blank=True)

	#implementing the time stamps for when the account is created using auto_now_add and when the account is updated using auto_now
	#auto_now_add is used as a one time time-stamp where auto_now is used for whenever the account is updated email, password, etc
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	#adding an admin(super user) check for the account, we set it to false as default
	is_admin = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELD = ['username']


	#this method returns the users email such as:
	#<Account: user@userdomain.io>
	def __unicode__(self):
		return self.email
	#this method returns the users full name
	def get_full_name(self):
		' '.join([self.first_name, self.last_name])
	#this method returns the users first name
	def get_short_name(self):
		return self.first_name
