from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Post, SavedPost
from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        messages.success(self.request, "Your thought has been posted!")
        return super().form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pull the 3 most recent Discovery posts for the "Cure Watch" section
        context['discovery_posts'] = Post.objects.filter(
            post_type='DISCOVERY'
        ).order_by('-created_at')[:3]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_saved'] = SavedPost.objects.filter(
                user=self.request.user, 
                post=self.get_object()
            ).exists()
        return context

@login_required
@require_POST
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    
    if created:
        messages.success(request, f'"{post.title}" has been saved to your wall.')
    else:
        saved_post.delete()
        messages.info(request, f'"{post.title}" has been removed from your wall.')
    
    return redirect('dashboard')

class DashboardView(ListView):
    model = SavedPost
    template_name = 'posts/dashboard.html'
    context_object_name = 'saved_posts'

    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user).select_related('post')

class SearchResultsView(ListView):
    model = Post
    template_name = 'posts/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by('-created_at')
        else:
            object_list = Post.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("q")
        # Ensure Cure Watch doesn't show up on search results to keep it clean
        context['discovery_posts'] = None 
        return context
