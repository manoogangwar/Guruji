from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Ads
from django.utils.timezone import now


class AdsListView(ListView):
    model = Ads
    template_name = "ads/ads_list.html"
    context_object_name = "ads"
    paginate_by = 10  

    def get_queryset(self):
        return Ads.objects.filter(
            is_active=True,
            is_approved=True
        ).order_by("-created_at")


class AdsDetailView(DetailView):
    model = Ads
    template_name = "ads/ads_details.html"
    context_object_name = "ad"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Ads.objects.filter(
            is_active=True,
            is_approved=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_ads"] = (
            Ads.objects.filter(
                is_active=True,
                is_approved=True,
                ad_type=self.object.ad_type
            )
            .exclude(id=self.object.id)
            .order_by("-created_at")[:4]
        )

        return context


class AdsApiView(View):
    def get(self, request):
        ads = (
            Ads.objects
            .filter(is_listed=True)
            .order_by("-date_published")[:4]
        )

        ads_data = [
            {
                "id": ad.id,
                "type": ad.type,
                "location": ad.location,
                "contact": ad.contact_details,
                "description": ad.description,
                "slug": ad.slug,
                "date": ad.date_published.strftime("%Y-%m-%d")
                if ad.date_published else None, 
            }
            for ad in ads
        ]

        return JsonResponse(
            {
                "status": "success",
                "count": len(ads_data),
                "data": ads_data,
            },
            status=200,
        )


Ads.objects.filter(
    is_active=True,
    is_approved=True,
    start_date__lte=now().date(),
    end_date__gte=now().date()
)
