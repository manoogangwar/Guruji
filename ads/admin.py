from django.contrib import admin
from .models import Ads


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'ad_type',
        'location',
        'is_active',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'ad_type',
        'is_active',
        'is_approved',
        'created_at',
    )

    search_fields = ('title', 'description', 'location')

    ordering = ('-created_at',)

    readonly_fields = (
        'slug',
        'views_count',
        'clicks_count',
        'created_at',
    )
