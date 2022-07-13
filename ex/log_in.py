from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Comment
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

class LogForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UpdateUser(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)
    picture = forms.FileField()

class PubliForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ["content"]

class ComForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ["content"]

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ["title", "content"]

    