from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "region",
            "user",
            "price",
            "photo",
            "kcal",
            "carbs",
            "protein",
            "fat",
        ]
