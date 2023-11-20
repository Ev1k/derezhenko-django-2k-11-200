import requests

from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from web.forms import RegistrationForm, AuthForm, AddPostForm
from web.models import Post

User = get_user_model()


def main_view(request):
    posts = Post.objects.all()
    year = datetime.now().year
    return render(request, "web/home.html", {
        'posts': posts
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
            print(form.cleaned_data)
    return render(request, "web/registration.html", {
        "form": form,
        "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == "POST":
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


def add_post_view(request):
    form = AddPostForm()
    if request.method == 'POST':
        form = AddPostForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            post = Post(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author_id=request.user.id
            )
            post.save()
            print(form.cleaned_data)
            return redirect("main")
    return render(request, "web/post_form.html", {"form": form})


def edit_post_view(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = AddPostForm(request.POST, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.user = request.user
            edited_post.save()
            return redirect("main")
    else:
        form = AddPostForm(instance=post)
    return render(request, "web/post_form.html", {"form": form})


