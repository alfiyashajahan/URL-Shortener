from django import forms
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['title', 'original_url']