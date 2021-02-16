from django import forms
from .models import BaseAccountModel
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class UserForm(forms.ModelForm):
	login_type = forms.CharField(
        label=_(''),
        required=True,
        initial='Login',
    )

	username = forms.CharField(
        label=_(''),
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username',
                'class': 'form-control input-lg',
            }
        )
    )

	password = forms.CharField(
        label=_(''),
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter password',
                'class': 'form-control input-lg',
                'type': 'password',
            }
        )
    )

	class Meta:
		model = User
		fields = (
			'username',
			'password',
		)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username):
			raise forms.ValidationError(_('Username already exists.'))
		return username


class FirstStepForm(forms.ModelForm):
	class Meta:
		model = BaseAccountModel
		fields = (
			'user',
			'first_name',
			'last_name',
		)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user') or None
		super(FirstStepForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = "First Name"
		self.fields['last_name'].label = "Last Name"
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['user'].initial = self.user
		self.fields['user'].widget = forms.HiddenInput()


class SecondStepForm(forms.ModelForm):
	class Meta:
		model = BaseAccountModel
		fields = (
			'gender',
			'date_of_birth',
		)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user') or None
		super(SecondStepForm, self).__init__(*args, **kwargs)
		self.fields['gender'].label = "Gender"
		self.fields['date_of_birth'].label = "Date of Birth"
		self.fields['gender'].required = True
		self.fields['date_of_birth'].required = True


class ThirdStepForm(forms.ModelForm):
	class Meta:
		model = BaseAccountModel
		fields = (
			'address',
			'email',
		)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user') or None
		super(ThirdStepForm, self).__init__(*args, **kwargs)
		self.fields['address'].label = "Address"
		self.fields['email'].label = "Email"
		self.fields['address'].required = True
		self.fields['email'].required = True


class BaseAccountForm(forms.ModelForm):
	class Meta:
		model = BaseAccountModel
		fields = (
			'user',
			'first_name',
			'last_name',
			'gender',
			'date_of_birth',
			'address',
			'email',
		)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user') or None
		super(BaseAccountForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['gender'].required = True
		self.fields['date_of_birth'].required = True
		self.fields['address'].required = True
		self.fields['email'].required = True
		self.fields['user'].initial = self.user
		self.fields['user'].widget = forms.HiddenInput()