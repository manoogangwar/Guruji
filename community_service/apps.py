from django.apps import AppConfig


class CommunityServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "community_service"

    def ready(self):
        import community_service.signals
