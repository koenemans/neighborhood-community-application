from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import Group, User

class Committee(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    contact_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='committees')
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('committees:detail', args=[self.slug])

    def __str__(self):
        return self.group.name