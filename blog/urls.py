from django.urls import path
from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting_page'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/stored/', views.StoredPostsView.as_view(), name='stored_posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/read-later/', views.ReadLaterView.as_view(), name='read_later'),
]
