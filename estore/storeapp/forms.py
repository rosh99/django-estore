from django.contrib.auth.models import User
from django import forms
from .models import UserInfo

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','email')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password didn't match!")
        return cd['password2']

class UserInfoForm(forms.ModelForm):
    city = forms.CharField(label='City',widget=forms.TextInput(attrs={'class':'form-control'}))
    house = forms.CharField(label='House No.',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = UserInfo
        fields = ('city','house')
        widgets = {
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'house':forms.TextInput(attrs={'class':'form-control'}),

        }
