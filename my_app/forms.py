from django import forms
from django.contrib.auth.models import User
from .models import Person, Complaints

class login_form(forms.Form):
	username = forms.CharField()               #EmailField()
	password = forms.CharField(widget = forms.PasswordInput)


class user_registration_form(forms.ModelForm):
	password = forms.CharField(label ='Password',widget = forms.PasswordInput)
	password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError("Password don't match.")
		return cd['password2']

class user_edit_form(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class lodge_complaint_form(forms.ModelForm):
	class Meta:
		model = Complaints
		fields = ('id','complaint', 'rules_violated')

class track_complaint_form(forms.Form):
	complaint_id = forms.IntegerField()
