from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .forms import SurveyForm
from .models import UserProfile, SurveyQuestion, SurveyAnswer
from .utils import calculate_category_and_priority, calculate_final_rank


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'survey/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user
        )

        context['show_popup'] = not profile.survey_completed
        context['form'] = SurveyForm()

        return context


class SurveyFormView(LoginRequiredMixin, FormView):
    form_class = SurveyForm
    template_name = 'survey/dashboard.html'
    success_url = '/search/'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.survey_completed:
            return redirect('search')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        total_score = 0

        questions = SurveyQuestion.objects.filter(is_active=True)
        total_questions = questions.count()

        filters = {}

        for question in questions:
            answer_text = form.cleaned_data.get(f'question_{question.id}')
            if answer_text:
                SurveyAnswer.objects.create(
                    user=user,
                    question=question,
                    answer_text=answer_text
                )

                total_score += question.weight

                # search filters
                if question.id == 1:
                    filters['country'] = answer_text
                elif question.id == 2:
                    filters['city'] = answer_text
                elif question.id == 3:
                    filters['occupation'] = answer_text

        profile, _ = UserProfile.objects.get_or_create(user=user)

        # category & priority
        category, priority = calculate_category_and_priority(
            total_score,
            total_questions
        )

        profile.category = category
        profile.priority = priority
        profile.score = total_score
        profile.final_rank = calculate_final_rank(total_score)

        profile.survey_completed = True
        profile.save()

        self.request.session['search_filters'] = filters
        self.request.session.modified = True

        return super().form_valid(form)
