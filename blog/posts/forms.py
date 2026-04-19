from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'carbs_per_serving', 'fiber', 'glycemic_index']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of your thought...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Share your recipe or idea...'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'carbs_per_serving': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fiber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'glycemic_index': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Low, 15, etc.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add labels and help text if needed
        self.fields['carbs_per_serving'].label = "Carbs per Serving (for Recipes)"
        self.fields['fiber'].label = "Fiber (for Recipes)"
