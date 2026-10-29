from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/all-posts.html'
    context_object_name = 'posts'
    ordering = ['-date']

class StartingPageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # return Post.objects.all().order_by('-date')[:3]
        return super().get_queryset()[:3]

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get_comments(self):
        return self.object.comments.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()
        context['comments'] = self.get_comments()
        context['stored_posts'] = self.request.session.get('stored_posts', [])
        if self.object.pk in context['stored_posts']:
            context['is_stored'] = True
        else:
            context['is_stored'] = False
        if 'form' not in context:
            context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect('post_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))


class ReadLaterView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        stored_posts = request.session.get('stored_posts', [])
        if post.pk not in stored_posts:
            stored_posts.append(post.pk)
        else:
            stored_posts.remove(post.pk)
        request.session['stored_posts'] = stored_posts
        return redirect('stored_posts')

class StoredPostsView(ListView):
    model = Post
    template_name = 'blog/stored-post.html'
    context_object_name = 'stored_posts'

    def get_queryset(self):
        stored_posts_ids = self.request.session.get('stored_posts', [])
        return Post.objects.filter(id__in=stored_posts_ids)

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, 'blog/index.html', {
#         'posts': latest_posts
#     })

# def post_list(request):
#     sorted_posts = Post.objects.all().order_by('-date')
#     return render(request, 'blog/all-posts.html', {
#         'posts': sorted_posts
#     })

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         'post': identified_post,
#         'tags': identified_post.tags.all()
#     })