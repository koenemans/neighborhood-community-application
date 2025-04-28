from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    committee = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='news')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title