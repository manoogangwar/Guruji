from django.contrib import admin
from .models import NeedRequest, HelpAssignment
# Register your models here.


@admin.register(NeedRequest)
class NeedRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)

admin.site.register(HelpAssignment)