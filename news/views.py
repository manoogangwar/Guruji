from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from .models import News


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_item'

    def get_queryset(self):
        return News.objects.filter(is_listed=True)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_items'] = News.objects.filter(is_listed=True)
        return context


class NewsApiView(View):
    def get(self, request):
        newses = News.objects.filter(is_listed=True)[:4]

        news_data = [
            {
                "id": news.id,
                "title": news.title,
                "category": news.category,
                "content": news.content,
                "date": news.date_published.strftime('%Y-%m-%d'),
            }
            for news in newses
        ]

        return JsonResponse(news_data, safe=False)
