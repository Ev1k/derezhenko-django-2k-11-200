from django import forms
from django.contrib.auth import get_user_model

from web.models import Post, New, Comment

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(
        max_length=15, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class AddPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

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


class AddNewForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

    class Meta:
        model = New
        fields = ("title", "description", "photo")

    def save(self, commit=True):
        new = super(AddNewForm, self).save(commit=False)
        if not self.instance.pk:
            new.user = self.initial["user"]
        if commit:
            new.save()
        return new


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

    class Meta:
        model = Comment
        fields = ("text",)

    def save(self, commit=True):
        comment = super(AddCommentForm, self).save(commit=False)
        if not self.instance.pk:
            comment.user = self.initial["user"]
        if commit:
            comment.save()
        return comment
