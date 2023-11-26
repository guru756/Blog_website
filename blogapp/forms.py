from django import forms
from .models import Blog

class LoginForm(forms.Form):
    full_name=forms.CharField(max_length=50)
    username=forms.EmailField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput())

class BlogForm(forms.Form):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        
    