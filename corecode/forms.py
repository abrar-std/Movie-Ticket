from django import forms
from .models import *
from django.core.validators import ValidationError


class registerForm(forms.ModelForm):
    rPassword = forms.CharField(label='Re-Password', widget=forms.TextInput)

    class Meta:
        model = user
        fields = ['name', 'email', 'address', 'phone', 'password', 'rPassword', 'gender']

    # def clean(self):
    #     data = self.cleaned_data
    #     pwd = data['password'] or "2"
    #     rpwd = data['rPassword'] or "1"
    #     print(pwd + "   " + rpwd)
    #     if pwd != rpwd:
    #         raise forms.ValidationError("Password Are Not Match")