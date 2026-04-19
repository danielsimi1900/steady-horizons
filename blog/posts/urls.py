from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import PostListView, PostDetailView, SearchResultsView, save_post, DashboardView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', login_required(PostCreateView.as_view()), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/save/', save_post, name='save_post'),
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
