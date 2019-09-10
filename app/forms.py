from django import forms
from django.contrib.auth.models import User
from app.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=5, label="用户名")
    password = forms.CharField(max_length=32, min_length=5, label="密码", widget=forms.PasswordInput())

    def clean(self):
        if not User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('用户名不存在，请检查您的用户名')
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=5, label="用户名")
    password = forms.CharField(max_length=32, min_length=5, label="密码", widget=forms.PasswordInput())
    email = forms.EmailField(label="邮箱")

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('用户名已存在')
        return self.cleaned_data

class FileForm(forms.Form):
    file = forms.FileField(label='图片文件', widget=forms.FileInput(attrs={'accept':'image/*'}))

class FilePathForm(forms.Form):
    file_path = forms.CharField(max_length=256, label='图片地址')