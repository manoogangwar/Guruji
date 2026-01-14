from django.db import models
from django.conf import settings


# Create your models here.

class SurveyQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    weight = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    

class UserProfile(models.Model):
    CATEGORY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    final_rank = models.IntegerField(default=0)
    survey_completed = models.BooleanField(default=False)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='beginner'
    )

    score = models.PositiveIntegerField(default=0)
    priority = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"


class SurveyAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.id}"