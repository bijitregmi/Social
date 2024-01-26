from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(null=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked')

    def __str__(self):
        return f"{self.poster} posted {self.content}"

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="following")
    followed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="followed_by")

    def __str__(self):
        return f'{self.following} followed by {self.followed_by}'