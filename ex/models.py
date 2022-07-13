from django.db import models
from django.contrib import auth
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.forms import Form

class Post(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.CharField(max_length=256, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, parent_link=True, null=True, blank=True)

    def children(self):
        return Comment.objects.filter(parent=self)

class UserDescrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    description = models.TextField()
    picture = models.ImageField(upload_to='images')

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='username')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'], None,
            self.cleaned_data['password1']  
        )
        return user