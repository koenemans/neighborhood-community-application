from django.views.generic import ListView, DetailView

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
