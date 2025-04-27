from django.views.generic import ListView, DetailView, dates

from .models import Post

class IndexView(ListView):
    template_name = 'news/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.order_by('-created_at')[:5]
    
class DetailView(DetailView):
    model = Post
    template_name = 'news/detail.html'

class YearArchiveView(dates.YearArchiveView):
    queryset = Post.objects.all()
    date_field = 'created_at'
    make_object_list = True
    allow_future = False
    template_name = 'news/archive_year.html'

class MonthArchiveView(dates.MonthArchiveView):
    queryset = Post.objects.all()
    date_field = 'created_at'
    allow_future = False
    template_name = 'news/archive_month.html'
