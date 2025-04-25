from django.views import generic

from .models import Activity

class IndexView(generic.ListView):
    template_name = 'activities/index.html'
    context_object_name = 'upcoming_activity_list'

    def get_queryset(self):
        return Activity.objects.order_by('-start')[:5]
    
class DetailView(generic.DetailView):
    model = Activity
    template_name = 'activities/detail.html'
