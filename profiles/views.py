from django.shortcuts import render
from django.views import View
# from django.http import HttpResponseRedirect
# from .forms import ProfileForm
from .models import UserProfile
from django.views.generic import CreateView
from django.views.generic import ListView

class CreateProfileView(CreateView):
    model = UserProfile
    # form_class = ProfileForm
    template_name = "profiles/profile.html"
    success_url = "/profiles/"
    fields = ["profile_picture"]

class UserProfileListView(ListView):
    model = UserProfile
    template_name = "profiles/user_profiles.html"
    context_object_name = "user_profiles"
# Create your views here.




# def store_file(file):
#     with open(f"profiles/static/profiles/{file.name}", "wb+") as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)


# class CreateProfileView(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, "profiles/profile.html", {"form": form})

#     def post(self, request):
#         # profile_picture = request.FILES.get("profile_picture")
#         # if profile_picture:
#         #     store_file(profile_picture)
#         # return HttpResponseRedirect("/profiles/")

#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile_picture = form.cleaned_data.get("profile_picture")
#             if profile_picture:
#                 # store_file(profile_picture)
#                 UserProfile.objects.create(profile_picture=profile_picture)
#             return HttpResponseRedirect("/profiles/")
#         return render(request, "profiles/profile.html", {"form": form})