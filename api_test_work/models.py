from django.db import models


class HackerNews(models.Model):
    title = models.TextField()
    url = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)