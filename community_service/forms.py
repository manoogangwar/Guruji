from django import forms
from .models import NeedRequest

class NeedCreateForm(forms.ModelForm):
    class Meta:
        model = NeedRequest
        fields = ['title', 'description', 'location','category', 'urgency', 'image', 'attachment',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter short title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your need'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional location'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
