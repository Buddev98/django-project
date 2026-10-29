from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'content']
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'content': 'Your Comment',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }