"""Views for the committees application."""

import logging
from django.views.generic import ListView, DetailView

from .models import Committee

logger = logging.getLogger(__name__)


class IndexView(ListView):
    """Display a list of committees."""

    template_name = "committees/index.html"
    context_object_name = "committee_list"

    def get_queryset(self):
        """Return all committees ordered by group name descending."""
        logger.debug("Fetching committee list ordered by group")
        return Committee.objects.order_by("-group")


class DetailView(DetailView):
    """Display details for a single committee."""

    model = Committee
    template_name = "committees/detail.html"

    def get_object(self, queryset=None):
        """Return the committee instance for the view."""
        committee = super().get_object(queryset)
        logger.debug("Retrieved committee detail for %s", committee)
        return committee
