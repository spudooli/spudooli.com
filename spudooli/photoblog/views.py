from django.views import generic
from .models import Post

class PostIndex(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-datetime')[0:1]
    template_name = 'index.html'

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-datetime')
    template_name = 'postlist.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'