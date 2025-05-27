from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Pasword'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Pasword'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords doesn't match"
            )


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={     
        'placeholder': 'Enter Password'
    }))
    class Meta:
        model = Account
        fields = ['email', 'password']


class ResetPasswordForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={     
        'placeholder': 'Enter New Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={     
        'placeholder': 'Repeat Password'
    }))

    class Meta:
        model = Account
        fields = ['password']

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords doesn't match"
            )