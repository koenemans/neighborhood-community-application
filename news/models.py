from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from committees.models import Committee

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'News'
        ordering = ['-created_at']

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='news')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])

    def __str__(self):
        return self.title