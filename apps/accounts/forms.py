from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _
from .models import MyUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Имя пользователя'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите имя пользователя')
    }))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите пароль'),
        'id': 'password',
        'name': 'password',

    }))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = MyUser.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError(_('Такого пользователя нет'))
            if not check_password(password, qs[0].password):
                raise forms.ValidationError(_('Неверный пароль'))
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('Данный пользователь не активен'))
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Имя пользователя'), widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите имя пользователя')
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'name': 'password',
            'id': 'password',
    }))
    password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Повторите пароль'),
            'name': 'password2',
            'id': 'password2',
        }))

    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return data['password2']


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Текущий пароль'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Введите текущий пароль'),
            'name': _('Текущий пароль'),
            'id': 'old_password',
        }))
    new_password1 = forms.CharField(label=_('Новый пароль'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль',
            'name': _('Новый пароль 1'),
            'id': 'new_password1',
    }))
    new_password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Повторите новый пароль'),
            'name':  _('Новый пароль 2'),
            'id': 'new_password2',
        }))

    def clean_password2(self):
        data = self.cleaned_data
        if data['new_password1'] != data['new_password2']:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return data['new_password2']
