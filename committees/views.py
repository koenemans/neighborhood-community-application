import logging
from django.views.generic import ListView, DetailView

from .models import Committee

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = "committees/index.html"
    context_object_name = "committee_list"

    def get_queryset(self):
        logger.debug("Fetching committee list ordered by group")
        return Committee.objects.order_by("-group")


class DetailView(DetailView):
    model = Committee
    template_name = "committees/detail.html"

    def get_object(self, queryset=None):
        committee = super().get_object(queryset)
        logger.debug("Retrieved committee detail for %s", committee)
        return committee
