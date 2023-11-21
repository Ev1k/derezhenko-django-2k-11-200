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
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")

    def save(self, commit=True):
        post = super(AddPostForm, self).save(commit=False)
        if not self.instance.pk:
            post.user = self.initial["user"]
        if commit:
            post.save()
        return post


class PostFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Поиск"}))
