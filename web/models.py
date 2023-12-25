from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager as DjangoUserManager,
)
from django.db import models
from django.contrib.auth import get_user_model


# User = get_user_model()


class Role(models.TextChoices):
    USER = "user", "User"
    ADMIN = "admin", "Admin"


class UserManager(DjangoUserManager):
    def _create_user(self, username, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField("email", blank=True)
    name = models.CharField("name", blank=False, unique=True)
    role = models.CharField("Role", choices=Role.choices)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "name"

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @classmethod
    def delete_like(cls, user_id, post_id):
        try:
            like_to_delete = cls.objects.get(user_id=user_id, post_id=post_id)
            like_to_delete.delete()
            return True
        except cls.DoesNotExist:
            return False


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class New(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    photo = models.ImageField(upload_to="news_photo/", null=True, blank=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
