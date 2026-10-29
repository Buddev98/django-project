from statistics import mode

from django.conf.locale import el
from django.shortcuts import redirect, render
from django.views import View
from .forms import ReviewForm
from .models import Review
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, FormView



class FavoriteReviewView(View):
    def post(self, request, *args, **kwargs):
        review_id = request.POST.get('review_id')
        review = Review.objects.get(id=review_id)
        request.session['favorite_review_id'] = review_id
        return redirect('single_review', pk=review_id)

# class ReviewView(View):
# class ReviewView(FormView):
class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/reviews.html'
    success_url = '/reviews/thank_you/'

    # form_class = ReviewForm
    # template_name = 'reviews/reviews.html'
    # success_url = '/thank-you/'

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    
    # def get(self, request):
    #     form = ReviewForm()
    #     return render(request, 'reviews/reviews.html', {'form': form})

    # def post(self, request):
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('thank_you')
    #     return render(request, 'reviews/reviews.html', {'form': form})

# Create your views here.
# def review_list(request):
#     if request.method == "POST":
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             # Review.objects.create(
#             #     username=form.cleaned_data['username'],
#             #     review=form.cleaned_data['review'],
#             #     rating=form.cleaned_data['rating']
#             # )
#             # Here you can save the review to the database if needed
#             form.save()
#             return redirect('thank_you')
#     else:
#         form = ReviewForm()
#     return render(request, 'reviews/reviews.html', {'form': form})

# def thank_you(request):
#     return render(request, 'reviews/thank_you.html')

class ThankYouView(TemplateView):
    template_name = 'reviews/thank_you.html'



class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    # def get_queryset(self):
    #     base_queryset = super().get_queryset()
    #     data = base_queryset.filter(rating__gte=5)
    #     return data


class SingleReviewView(DetailView):
    template_name = 'reviews/single_review.html'
    model = Review
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_review_id'] = self.request.session.get('favorite_review_id') == str(self.object.id)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['review'] = Review.objects.get(pk=self.kwargs['pk'])
    #     return context