from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date = models.DateTimeField()


class New(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    photo = models.ImageField(upload_to='news_photo/', null=True, blank=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField()
