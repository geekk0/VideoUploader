from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не зарегистрирован')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Неверный пароль')

        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'password']


class ResetPassword(forms.ModelForm):

    old_password = forms.CharField(label='Введите старый пароль', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Введите новый пароль', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Введите старый пароль'
        self.fields['new_password'].label = 'Введите новый пароль'

    def clean(self):

        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']

        confirm_new_password = self.cleaned_data['confirm_new_password']

        if new_password == old_password:
            raise forms.ValidationError(f'Новый пароль не отличается от старого')

        if new_password != confirm_new_password:
            raise forms.ValidationError(f'Введенные пароли не совпадают')

        username = self.cleaned_data['username']
        user = User.objects.get(username=username)

        if not user.check_password(old_password):
            raise forms.ValidationError(f'Неверный пароль')

        validate_password(new_password, user=user, password_validators=None)

        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'old_password', 'new_password', 'confirm_new_password']
