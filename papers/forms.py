from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ResearchPaper


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ["title", "abstract", "pdf"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "abstract": forms.Textarea(attrs={"class": "form-control"}),
            "pdf": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ContactForm(forms.Form):
    user_email = forms.EmailField(
        label="Your Email",
        max_length=255,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    subject = forms.CharField(
        label="Subject",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    content = forms.CharField(
        label="Content", widget=forms.Textarea(attrs={"class": "form-control"})
    )
