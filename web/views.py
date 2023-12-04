from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from web.forms import (
    RegistrationForm,
    AuthForm,
    AddPostForm,
    PostFilterForm,
    AddNewForm,
    AddCommentForm,
)
from web.models import Post, New, Comment, Like

User = get_user_model()


def main_view(request):
    posts = Post.objects.all().order_by("-date")
    news = New.objects.all().order_by("-date")

    filter_form = PostFilterForm(request.GET)
    filter_form.is_valid()
    filters = filter_form.cleaned_data

    try:
        if filters["search"]:
            posts = posts.filter(title__icontains=filters["search"])
    except KeyError:
        print('keyError ("search")')

    posts = posts.select_related("author")
    total_count = posts.count()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, per_page=4)

    return render(
        request,
        "web/home.html",
        {
            "posts": paginator.get_page(page_number),
            "comment_form": AddCommentForm(),
            "news": news,
            "form": AddPostForm(),
            "new_form": AddNewForm(),
            "filter_form": filter_form,
            "total_count": total_count,
        },
    )


@login_required
def analytics_view(request):
    overall_stat = Post.objects.aggregate(Count("id"))

    return render(request, "web/analytics.html", {"overall_stat": overall_stat})


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                name=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            is_success = True
            print(form.cleaned_data)
    return render(
        request, "web/registration.html", {"form": form, "is_success": is_success}
    )


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


@login_required
def add_post_view(request):
    form = AddPostForm()
    if request.method == "POST":
        form = AddPostForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            post = Post(
                title=form.cleaned_data["title"],
                text=form.cleaned_data["text"],
                author_id=request.user.id,
            )
            post.save()
            print(form.cleaned_data)
            return redirect("main")
    return render(request, "web/post_form.html", {"form": form})


@login_required
def edit_post_view(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = AddPostForm(request.POST, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.user = request.user
            edited_post.save()
            return redirect("main")
    else:
        form = AddPostForm(instance=post)
    return render(request, "web/post_form.html", {"form": form})


@login_required
def add_new_view(request):
    form = AddNewForm()
    if request.method == "POST":
        form = AddNewForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            new = New(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                author_id=request.user.id,
            )
            new_photo = request.FILES["photo"]
            new.photo = new_photo
            new.save()
            print(form.cleaned_data)
            return redirect("main")
    return render(request, "web/new_form.html", {"new_form": form})


# def get_absolute_url(self):
#     return "/user/%i/" % self.id


def get_absolute_url(self):
    from django.urls import reverse

    return reverse("user.views.details", args=[str(self.id)])


def profile_view(request, id=None):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        return my_page_view(request)
    posts = Post.objects.filter(author=user).order_by("-date")
    return render(
        request,
        "web/profile.html",
        {"posts": posts, "the_user": user, "comment_form": AddCommentForm},
    )


def my_page_view(request):
    posts = Post.objects.filter(author=request.user).order_by("-date")
    change_profile_photo(request)
    return render(
        request,
        "web/my_page.html",
        {
            "form": AddPostForm(),
            "posts": posts,
            "photo": request.user.photo,
            "comment_form": AddCommentForm,
        },
    )


def change_profile_photo(request):
    if request.method == "POST":
        profile_photo = request.FILES["profile_photo"]
        user = request.user

        user.photo = profile_photo
        user.save()


def add_comment_view(request, id_post=None):
    post = get_object_or_404(Post, id=id_post)
    form = AddCommentForm()
    if request.method == "POST":
        form = AddCommentForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            comment = Comment(
                author=request.user, text=form.cleaned_data["text"], post=post
            )
            comment.save()
            print(form.cleaned_data)
            return redirect("main")
    return render(request, "web/comment_form.html", {"comment_form": form})


def add_or_remove_like(request, id_post=None):
    post = get_object_or_404(Post, id=id_post)
    user = request.user

    if not post.likes.filter(user_id=user.id).first():
        like = Like.objects.create(user=user, post=post)
        return like
    else:
        like = post.likes.filter(user_id=user.id).first()
        like.delete_like(Like, user.id, post.id)


def get_like_count(request, id_post=None):
    post = get_object_or_404(Post, id=id_post)
    if request.method == "GET":
        likeCount = post.likes.all().count()
        return render(request, likeCount)
