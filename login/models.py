from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Create your models here.
class BaseAccountModel(TimeStampedModel):
	GENDER_CHOICES = Choices(
		('male', _('Male')),
		('female', _('Female')),
	)

	user = models.OneToOneField(
		'auth.User',
		null=True,
		blank=True,
		on_delete=models.SET_NULL
	)

	first_name = models.CharField(
		max_length=255,
		verbose_name=_('first name'),
		blank=False,
	)

	last_name = models.CharField(
		max_length=255,
		verbose_name=_('last name'),
		blank=False,
	)

	gender = models.CharField(
		max_length=255,
		verbose_name=_('gender'),
		choices=GENDER_CHOICES,
		blank=True,
		null=True,
	)

	date_of_birth = models.DateField(
		blank=True,
		null=True,
	)

	address = models.TextField(
		verbose_name=_('address'),
		blank=True,
		null=True,
	)

	email = models.EmailField(
		verbose_name=_('email'),
		blank=True,
		null=True,
	)

	def full_name(self):
		return '%s %s' % (self.first_name, self.last_name)

	def is_step_one_complete(self):
		if self.first_name and self.last_name:
			return True
		return False

	def is_step_two_complete(self):
		if self.gender and self.date_of_birth:
			return True
		return False

	def is_data_complete(self):
		if self.address and self.email:
			return True
		return False
