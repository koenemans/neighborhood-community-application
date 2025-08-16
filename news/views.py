"""Views for the news application."""

import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, base, TemplateView
from django.core.cache import cache

from committees.models import Committee
from .models import Post

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    """Render the site's home page."""

    template_name = "home.html"


class IndexView(ListView):
    """Display a list of the latest news posts."""

    template_name = "news/index.html"
    context_object_name = "latest_posts_list"

    def get_queryset(self):
        """Return the five most recent posts."""
        logger.debug("Fetching latest posts for index view")
        return cache.get_or_set(
            "latest_posts",
            lambda: list(Post.objects.select_related("committee").all()[:5]),
            60 * 15,
        )


class DetailView(DetailView):
    """Display details for a single news post."""

    model = Post
    template_name = "news/detail.html"


@method_decorator(cache_page(60 * 15), name="dispatch")
class NewsArchiveView(base.TemplateView):
    """Render an archive of news posts grouped by date."""

    template_name = "news/archive.html"
    context_object_name = "grouped_news"

    def get_queryset(self):
        """Return posts optionally filtered by committee slug."""
        # Filter posts by committee if a query parameter is provided
        queryset = Post.objects.select_related("committee").all()
        committee_slug = self.request.GET.get("committee")
        if committee_slug:
            logger.info("Filtering posts for committee %s", committee_slug)
            queryset = queryset.filter(committee__slug=committee_slug)
        else:
            logger.debug("No committee filter applied")
        return queryset

    def get_context_data(self, **kwargs):
        """Build the context with grouped news and committees."""
        context = super().get_context_data(**kwargs)
        committee_slug = self.request.GET.get("committee")
        cache_key = f"news_archive_{committee_slug or 'all'}"
        grouped_news = cache.get(cache_key)
        if grouped_news is None:
            queryset = self.get_queryset()

            grouped_news = {}
            for post in queryset:
                year = post.created_at.year
                month = post.created_at.strftime("%B")
                grouped_news.setdefault(year, {}).setdefault(month, []).append(post)
            cache.set(cache_key, grouped_news, 60 * 15)

        context["grouped_news"] = grouped_news
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
            "Prepared context with %d posts",
            sum(
                len(month_posts)
                for year in grouped_news.values()
                for month_posts in year.values()
            ),
        )
        return context
