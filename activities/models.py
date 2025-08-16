"""Database models for the activities application."""

from django.db import models
from django.utils import timezone
from django.urls import reverse
from committees.models import Committee
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.upload_paths import hashed_upload_path
from utils.slug import generate_unique_slug


def start_date_not_in_past(date):
    """Ensure the provided date is not in the past."""
    if date < timezone.now():
        raise ValidationError(
            _("Start date: %(date)s cannot be in the past") % {"date": date},
            code="invalid",
        )


class Activity(models.Model):
    """Model representing an activity organised by a committee."""

    class Meta:
        """Metadata for the :class:`Activity` model."""

        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ["start"]

    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(_("content"))
    start = models.DateTimeField(_("start date"), validators=[start_date_not_in_past])
    end = models.DateTimeField(_("end date"))
    location = models.CharField(_("location"), max_length=200)
    poster = models.ImageField(
        upload_to=hashed_upload_path("activities/posters"), blank=True, null=True
    )
    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name=_("committee"),
    )
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def save(self, *args, **kwargs):
        """Generate a unique slug from the title on first save."""
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate that the end date is not before the start date."""
        super().clean()
        if self.end and self.start and self.end < self.start:
            raise ValidationError(
                _("End date %(end)s cannot be before the start date %(start)s")
                % {"end": self.end, "start": self.start},
                code="invalid",
            )

    def get_absolute_url(self):
        """Return the URL for the activity detail page."""
        return reverse("activities:detail", args=[self.slug])

    def __str__(self):
        """Return the string representation of the activity."""
        return self.title
