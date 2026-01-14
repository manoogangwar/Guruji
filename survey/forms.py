from django import forms
from .models import SurveyQuestion

class SurveyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        questions = SurveyQuestion.objects.filter(is_active=True)

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.question_text,
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Your answer (optional)'
                })
            )