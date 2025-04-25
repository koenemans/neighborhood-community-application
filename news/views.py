from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    latest_posts_list = Post.objects.order_by('-created_at')[:5]
    context = { "latest_posts_list": latest_posts_list }
    return render(request, 'news/index.html', context)

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/detail.html', { 'post': post })
