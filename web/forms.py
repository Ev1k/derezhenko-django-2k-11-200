from django import forms
from django.contrib.auth import get_user_model

from web.models import Post

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AddPostForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()

    class Meta:
        model = Post
        fields = ('title', 'text')

    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super.save(commit)


