from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment', 'rating', 'post_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'post_id': forms.HiddenInput(),
        }
