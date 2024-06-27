# myapp/forms.py
from django import forms
from myapp.models import Resume
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

