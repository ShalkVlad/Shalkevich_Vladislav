from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField()
    post_id = models.IntegerField()
