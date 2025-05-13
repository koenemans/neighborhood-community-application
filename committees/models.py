from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

class Committee(models.Model):
    class Meta:
        verbose_name = _('Committee')
        verbose_name_plural = _('Committees')
        ordering = ['group']
    
    group = models.OneToOneField(Group, on_delete=models.CASCADE, verbose_name=_('group'))
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(_('description'))
    contact_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='committees', verbose_name=_('contact person'))
    email = models.EmailField(_('email'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('committees:detail', args=[self.slug])

    def __str__(self):
        return self.group.name