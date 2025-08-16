"""Views for the committees application."""

import logging
from django.views.generic import ListView, DetailView
from django.core.cache import cache

from .models import Committee

logger = logging.getLogger(__name__)


class IndexView(ListView):
    """Display a list of committees."""

    template_name = "committees/index.html"
    context_object_name = "committee_list"

    def get_queryset(self):
        """Return all committees ordered by group name descending."""
        logger.debug("Fetching committee list ordered by group")
        return cache.get_or_set(
            "committee_index_list",
            lambda: list(Committee.objects.order_by("-group")),
            60 * 60,
        )


class DetailView(DetailView):
    """Display details for a single committee."""

    model = Committee
    template_name = "committees/detail.html"

    def get_object(self, queryset=None):
        """Return the committee instance for the view."""
        slug = self.kwargs.get("slug")
        cache_key = f"committee_{slug}"
        committee = cache.get(cache_key)
        if committee is None:
            committee = super().get_object(queryset)
            cache.set(cache_key, committee, 60 * 60)
        logger.debug("Retrieved committee detail for %s", committee)
        return committee
