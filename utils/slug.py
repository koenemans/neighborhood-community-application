"""Utility helpers for slug generation."""

from django.utils.text import slugify


def generate_unique_slug(instance, value, slug_field_name="slug"):
    """Generate a slug for *value* unique among ``instance``'s model."""
    slug = slugify(value)
    ModelClass = instance.__class__
    unique_slug = slug
    counter = 1
    queryset = ModelClass.objects
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    while queryset.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug
