import logging
from django.views.generic import ListView, DetailView, base, TemplateView

from committees.models import Committee
from .models import Post

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'home.html'


class IndexView(ListView):
    template_name = 'news/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        logger.debug("Fetching latest posts for index view")
        return Post.objects.all()[:5]


class DetailView(DetailView):
    model = Post
    template_name = 'news/detail.html'


class NewsArchiveView(base.TemplateView):
    template_name = 'news/archive.html'
    context_object_name = 'grouped_news'

    def get_queryset(self):
        # Filter posts by committee if a query parameter is provided
        queryset = Post.objects.all()
        committee_slug = self.request.GET.get('committee')
        if committee_slug:
            logger.info("Filtering posts for committee %s", committee_slug)
            queryset = queryset.filter(committee__slug=committee_slug)
        else:
            logger.debug("No committee filter applied")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Group posts by year and month
        grouped_news = {}
        for post in queryset:
            year = post.created_at.year
            month = post.created_at.strftime('%B')
            grouped_news.setdefault(year, {}).setdefault(month, []).append(post)

        # Add grouped news and committees to the context
        context['grouped_news'] = grouped_news
        context['all_committees'] = Committee.objects.all()
        committee_slug = self.request.GET.get('committee')
        if committee_slug:
            context['filtered_committee'] = Committee.objects.filter(slug=committee_slug).first()
        else:
            context['filtered_committee'] = None
        logger.debug(
            "Prepared context with %d posts",
            sum(len(month_posts) for year in grouped_news.values() for month_posts in year.values()),
        )
        return context
