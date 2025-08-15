"""Database models for the news application."""

from django.db import models
from django.utils import timezone
from django.urls import reverse
from committees.models import Committee
from django.utils.translation import gettext_lazy as _
from utils.upload_paths import hashed_upload_path
from utils.slug import generate_unique_slug


class Post(models.Model):
    """Model representing a news post."""

    class Meta:
        """Metadata for the :class:`Post` model."""

        verbose_name = _("Post")
        verbose_name_plural = _("News")
        ordering = ["-created_at"]

    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(_("content"))
    poster = models.ImageField(
        upload_to=hashed_upload_path("news/posters"), blank=True, null=True
    )
    attachment = models.FileField(
        _("attachment"),
        upload_to=hashed_upload_path("news/attachments"),
        blank=True,
        null=True,
    )
    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name=_("committee"),
    )
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def save(self, *args, **kwargs):
        """Generate a unique slug from the title on first save."""
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for the post detail page."""
        return reverse("news:detail", args=[self.slug])

    def __str__(self):
        """Return the string representation of the post."""
        return self.title
