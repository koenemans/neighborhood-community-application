from django.views.generic import ListView, DetailView, base

from .models import Activity

class IndexView(ListView):
    template_name = 'activities/index.html'
    context_object_name = 'upcoming_activity_list'

    def get_queryset(self):
        return Activity.objects.order_by('-start')[:5]
    
class DetailView(DetailView):
    model = Activity
    template_name = 'activities/detail.html'

class ActivitiesArchiveView(base.TemplateView):
    template_name = 'activities/archive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_activities = Activity.objects.all().order_by('-start')

        # Group posts by year, then by month, then by committee
        grouped_activities = {}
        for activity in all_activities:
            year = activity.start.year
            month = activity.start.strftime('%B')  # Get month name
            committee = activity.committee if activity.committee else "No Committee"

            grouped_activities.setdefault(year, {}).setdefault(month, {}).setdefault(committee, []).append(activity)

        context['grouped_activities'] = grouped_activities
        return context