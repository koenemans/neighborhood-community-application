"""Database models for the committees application."""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _


class Committee(models.Model):
    """Model representing a committee within the community."""

    class Meta:
        """Metadata for the :class:`Committee` model."""

        verbose_name = _("Committee")
        verbose_name_plural = _("Committees")
        ordering = ["group"]

    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, verbose_name=_("group")
    )
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(_("description"))
    contact_person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="committees",
        verbose_name=_("contact person"),
    )
    email = models.EmailField(_("email"))

    def save(self, *args, **kwargs):
        """Generate a slug from the group's name on first save."""
        if not self.slug:
            self.slug = slugify(self.group.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for the committee detail page."""
        return reverse("committees:detail", args=[self.slug])

    def __str__(self):
        """Return the string representation of the committee."""
        return self.group.name
