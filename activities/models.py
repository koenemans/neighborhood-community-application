from django.db import models
from django.utils import timezone

class Activity(models.Model):
    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
    title = models.CharField(max_length=200)
    content = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title