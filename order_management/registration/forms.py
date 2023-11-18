# forms.py
from django import forms
from .models import CustomUser

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email")
    security_question = forms.CharField(label="Security Question")
    security_answer = forms.CharField(label="Security Answer", widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email']
