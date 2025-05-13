from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from committees.models import Committee
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('News')
        ordering = ['-created_at']

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(_('content'))
    poster = models.ImageField(upload_to='news/posters/%Y/%m/%d/', blank=True, null=True)
    attachment = models.FileField(_('attachment'), upload_to='news/attachments/%Y/%m/%d/', blank=True, null=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='news', verbose_name=_('committee'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])

    def __str__(self):
        return self.title