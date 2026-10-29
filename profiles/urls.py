from django.urls import path

from . import views

urlpatterns = [
    path("", views.CreateProfileView.as_view(), name="create_profile"),
    path("list/", views.UserProfileListView.as_view(), name="user_profiles"),
]