from django.views.generic import ListView, DetailView, base

from .models import Post

class IndexView(ListView):
    template_name = 'news/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:5]
    
class DetailView(DetailView):
    model = Post
    template_name = 'news/detail.html'

class NewsArchiveView(base.TemplateView):
    template_name = 'news/archive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_news = Post.objects.all().order_by('-created_at')

        # Group posts by year, then by month, then by committee
        grouped_news = {}
        for post in all_news:
            year = post.created_at.year
            month = post.created_at.strftime('%B')  # Get month name
            committee = post.committee.name if post.committee else "No Committee"

            grouped_news.setdefault(year, {}).setdefault(month, {}).setdefault(committee, []).append(post)

        context['grouped_news'] = grouped_news
        return context