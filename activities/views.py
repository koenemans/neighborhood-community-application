import logging
from django.views.generic import ListView, DetailView, base

from committees.models import Committee
from .models import Activity

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'activities/index.html'
    context_object_name = 'upcoming_activity_list'

    def get_queryset(self):
        logger.debug("Fetching upcoming activities for index view")
        return Activity.objects.all()[:5]


class DetailView(DetailView):
    model = Activity
    template_name = 'activities/detail.html'


class ActivitiesArchiveView(base.TemplateView):
    template_name = 'activities/archive.html'
    context_object_name = 'grouped_activities'

    def get_queryset(self):
        # Filter activities by committee if a query parameter is provided
        queryset = Activity.objects.all()
        committee_slug = self.request.GET.get('committee')
        if committee_slug:
            logger.info("Filtering activities for committee %s", committee_slug)
            queryset = queryset.filter(committee__slug=committee_slug)
        else:
            logger.debug("No committee filter applied")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Group activities by year and month
        grouped_activities = {}
        for activity in queryset:
            year = activity.created_at.year
            month = activity.created_at.strftime('%B')
            grouped_activities.setdefault(year, {}).setdefault(month, []).append(activity)

        # Add grouped activities and committees to the context
        context['grouped_activities'] = grouped_activities
        context['all_committees'] = Committee.objects.all()
        committee_slug = self.request.GET.get('committee')
        if committee_slug:
            context['filtered_committee'] = Committee.objects.filter(slug=committee_slug).first()
        else:
            context['filtered_committee'] = None
        logger.debug(
            "Prepared context with %d activities",
            sum(
                len(month_activities)
                for year in grouped_activities.values()
                for month_activities in year.values()
            ),
        )
        return context
