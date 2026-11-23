from django import forms
from django.contrib.auth.models import User
from .models import Candidate


class CandidateRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Candidate
        fields = ['username', 'email', 'password', 'phone', 'education', 'skills', 'resume']