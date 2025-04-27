from django.views.generic import ListView, DetailView

from .models import Activity

class IndexView(ListView):
    template_name = 'activities/index.html'
    context_object_name = 'upcoming_activity_list'

    def get_queryset(self):
        return Activity.objects.order_by('-start')[:5]
    
class DetailView(DetailView):
    model = Activity
    template_name = 'activities/detail.html'
