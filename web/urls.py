from django.contrib import admin
from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, add_post_view, edit_post_view

urlpatterns = [
    path('', main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("posts/add/", add_post_view, name="posts_add"),
    path("posts/<int:id>/", edit_post_view, name="posts_edit")
]
