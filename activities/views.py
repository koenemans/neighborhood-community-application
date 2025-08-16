"""Views for the activities application."""

import logging
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, base
from django.core.cache import cache

from committees.models import Committee
from .models import Activity

logger = logging.getLogger(__name__)


class IndexView(ListView):
    """Display a list of upcoming activities."""

    template_name = "activities/index.html"
    context_object_name = "upcoming_activity_list"

    def get_queryset(self):
        """Return the next five upcoming activities."""
        logger.debug("Fetching upcoming activities for index view")
        cache_key = "upcoming_activities"
        return cache.get_or_set(
            cache_key,
            lambda: list(
                Activity.objects.select_related("committee")
                .filter(start__gte=timezone.now())
                .order_by("start")[:5]
            ),
            60 * 15,
        )


class DetailView(DetailView):
    """Display the details of a single activity."""

    model = Activity
    template_name = "activities/detail.html"


@method_decorator(cache_page(60 * 15), name="dispatch")
class ActivitiesArchiveView(base.TemplateView):
    """Render an archive of activities grouped by date."""

    template_name = "activities/archive.html"
    context_object_name = "grouped_activities"

    def get_queryset(self):
        """Return activities optionally filtered by committee slug."""
        # Filter activities by committee if a query parameter is provided
        queryset = Activity.objects.select_related("committee").all()
        committee_slug = self.request.GET.get("committee")
        if committee_slug:
            logger.info("Filtering activities for committee %s", committee_slug)
            queryset = queryset.filter(committee__slug=committee_slug)
        else:
            logger.debug("No committee filter applied")
        return queryset

    def get_context_data(self, **kwargs):
        """Build the context with grouped activities and committees."""
        context = super().get_context_data(**kwargs)
        committee_slug = self.request.GET.get("committee")
        cache_key = f"activities_archive_{committee_slug or 'all'}"
        grouped_activities = cache.get(cache_key)
        if grouped_activities is None:
            queryset = self.get_queryset()

            grouped_activities = {}
            for activity in queryset:
                year = activity.created_at.year
                month = activity.created_at.strftime("%B")
                grouped_activities.setdefault(year, {}).setdefault(month, []).append(
                    activity
                )
            cache.set(cache_key, grouped_activities, 60 * 15)

        context["grouped_activities"] = grouped_activities
        context["all_committees"] = cache.get_or_set(
            "all_committees",
            lambda: list(Committee.objects.all()),
            60 * 60,
        )
        if committee_slug:
            context["filtered_committee"] = cache.get_or_set(
                f"committee_{committee_slug}",
                lambda: Committee.objects.filter(slug=committee_slug).first(),
                60 * 60,
            )
        else:
            context["filtered_committee"] = None
        logger.debug(
            "Prepared context with %d activities",
            sum(
                len(month_activities)
                for year in grouped_activities.values()
                for month_activities in year.values()
            ),
        )
        return context
