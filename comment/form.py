from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'image', 'video']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
            'video': forms.ClearableFileInput(attrs={'required': False}),
        }