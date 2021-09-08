from django.views.generic import DetailView
from django.views.generic.list import ListView
from dpd_cc_example.example.models import Post

class BlogListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'pages/blogs.html'
    context_object_name = 'posts'
    ordering = ['-created_on']


class BlogDetailView(DetailView):
    model = Post
    template_name = 'pages/post_detail.html'
