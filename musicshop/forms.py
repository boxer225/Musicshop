from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Comments

class ContactForm(forms.Form):
    name = forms.CharField( label='Имя', max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя...'}))
    email = forms.EmailField(label='Адрес электронной почты', max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Адрес электронной почты...'}))
    content = forms.CharField(label='Сообщение', max_length=2000,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Текст...'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    fio = forms.CharField(label='ФИО', max_length=200,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ФИО'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Адрес электронной почты'}))
    number_of_phone = forms.CharField(label='Номер телефона',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'fio', 'number_of_phone', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        #fields = '__all__'
        fields = ['mark', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Отзыв...'}),
            'mark': forms.NumberInput(attrs={'class': 'form-control'})
        }