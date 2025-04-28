from django.views.generic import ListView, DetailView

from .models import Committee

class IndexView(ListView):
    template_name = 'committees/index.html'
    context_object_name = 'committee_list'

    def get_queryset(self):
        return Committee.objects.order_by('-group')
    
class DetailView(DetailView):
    model = Committee
    template_name = 'committees/detail.html'