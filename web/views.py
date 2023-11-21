from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from web.forms import RegistrationForm, AuthForm, AddPostForm, PostFilterForm
from web.models import Post

User = get_user_model()


def main_view(request):
    posts = Post.objects.all().order_by("-date")

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
            "form": AddPostForm(),
            "filter_form": filter_form,
            "total_count": total_count,
        },
    )


def my_page_view(request):
    posts = Post.objects.filter(user=request.user).order_by("-date")
    year = datetime.now().year
    return render(request, "web/home.html", {"posts": posts, "form": AddPostForm()})


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
                username=form.cleaned_data["username"], email=form.cleaned_data["email"]
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
