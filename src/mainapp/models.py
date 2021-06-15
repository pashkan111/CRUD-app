from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
