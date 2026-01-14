
from django.contrib import admin
from .models import SurveyQuestion, SurveyAnswer, UserProfile


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_active', 'weight', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('question_text',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_completed', 'category', 'score')
    list_filter = ('survey_completed', 'category')
    search_fields = ('user__username',)


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'submitted_at')
    search_fields = ('user__username', 'question__question_text')
