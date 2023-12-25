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
    add_new_view,
    profile_view,
    add_comment_view,
    add_or_remove_like,
    get_like_count,
)

urlpatterns = [
    path("", main_view, name="main"),
    path("analytics/", analytics_view, name="analytics"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("posts/add/", add_post_view, name="posts_add"),
    path("posts/<int:id>/", edit_post_view, name="posts_edit"),
    path("user/<int:id>/", profile_view, name="profile"),
    path("my_profile/", my_page_view, name="my_page"),
    path("news/add/", add_new_view, name="new_add"),
    path("comment/add/<int:id_post>/", add_comment_view, name="comment_add"),
    path("like/", add_or_remove_like, name="like"),
    path("like/count/", get_like_count, name="like_count"),
]
