from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewView.as_view(), name='review_list'),
    path('thank_you/', views.ThankYouView.as_view(), name='thank_you'),
    path('review_list/', views.ReviewListView.as_view(), name='review_list_view'),
    path('review/favorite/', views.FavoriteReviewView.as_view(), name='favorite_review'),
    path('review/<int:pk>/', views.SingleReviewView.as_view(), name='single_review'),
]