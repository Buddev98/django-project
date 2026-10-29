from django import forms

from reviews.models import Review

# class ReviewForm(forms.Form):
#     username = forms.CharField(label="Your Name", max_length=100, error_messages={'required': 'Please enter your name', 'max_length': 'Name cannot exceed 100 characters'})
#     review = forms.CharField(label="Your Review", widget=forms.Textarea, max_length=500, error_messages={'required': 'Please enter your review', 'max_length': 'Review cannot exceed 500 characters'})
#     rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5, error_messages={'required': 'Please enter your rating', 'min_value': 'Rating must be at least 1', 'max_value': 'Rating cannot exceed 5'})

class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ['username', 'review', 'rating']
        labels = {
            'username': 'Your Name',
            'review': 'Your Review',
            'rating': 'Your Rating'
        }
        error_messages = {
            'username': {
                'required': 'Please enter your name',
                'max_length': 'Name cannot exceed 100 characters'
            },
            'review': {
                'required': 'Please enter your review',
                'max_length': 'Review cannot exceed 500 characters'
            },
            'rating': {
                'required': 'Please enter your rating',
                'min_value': 'Rating must be at least 1',
                'max_value': 'Rating cannot exceed 5'
            }
        }
        # fields = '__all__'
        # exclude = []