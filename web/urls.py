from django.urls import path

from web.views import (
    main_view,
    registration_view,
    auth_view,
    logout_view,
    add_post_view,
    edit_post_view,
    my_page_view,
    analytics_view,
)

urlpatterns = [
    path("", main_view, name="main"),
    path("analytics/", analytics_view, name="analytics"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("posts/add/", add_post_view, name="posts_add"),
    path("posts/<int:id>/", edit_post_view, name="posts_edit"),
    path("my_page/", my_page_view, name="my_page"),
]
