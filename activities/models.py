from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from committees.models import Committee
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.upload_paths import hashed_upload_path

def start_date_not_in_past(date):
    if date < timezone.now():
        raise ValidationError(
             _("Start date: %(date)s cannot be in the past") % {'date': date},
             code='invalid',
        )

class Activity(models.Model):
    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['start']
        
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(_('content'))
    start = models.DateTimeField(_('start date'), validators=[start_date_not_in_past])
    end = models.DateTimeField(_('end date'))
    location = models.CharField(_('location'), max_length=200)
    poster = models.ImageField(upload_to=hashed_upload_path('activities/posters'), blank=True, null=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='activities', verbose_name=_('committee'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('activities:detail', args=[self.slug])

    def __str__(self):
        return self.title