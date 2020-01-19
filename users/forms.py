from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegForm(forms.Form):
	username = forms.CharField(label='Username', max_length=150, min_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='Password', max_length=150, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Repeat Password', max_length=150, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))

	def clean_email(self):
		email = self.cleaned_data['email']
		us = User.objects.filter(email=email)

		if us.exists():
			raise ValidationError('This email is already registered')
		return email

	def clean(self):
		cleaned_data = super().clean()
		p1 = self.cleaned_data.get('password1')
		p2 = self.cleaned_data.get('password2')

		if p1 and p2:
			if p1 != p2:
				raise ValidationError('Passwords do not match')