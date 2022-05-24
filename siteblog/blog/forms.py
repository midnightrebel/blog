from django import forms
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Blog # для создания выпадающего списка категории
from django.core.exceptions import ValidationError
from .models import Post

class UserLoginForm(AuthenticationForm):
    password = forms.CharField(label = 'Пароль',widget= forms.PasswordInput(attrs={'class': 'form-control'}))

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__' не рекомендуется
        fields = [
            'title',
            'сontent',
            'isPublished',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d',title):
            raise ValidationError("Название не должно начинаться с цифры.")
        return title

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label = 'Имя пользователя', widget =  forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label = 'Пароль',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label= 'E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')
