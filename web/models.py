from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateTimeField()
    likes = models.ManyToManyField(User)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()


class New(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField()


# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
