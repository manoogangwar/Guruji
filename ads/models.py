from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError


class Ads(models.Model):

    AD_TYPE_CHOICES = [
        ('donation', 'Donation'),
        ('event', 'Event'),
        ('awareness', 'Awareness'),
        ('promotion', 'Promotion'),
        ('social', 'Social'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    ad_type = models.CharField(max_length=50, choices=AD_TYPE_CHOICES)

    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    location = models.CharField(max_length=100)

    contact_details = models.CharField(max_length=100)
    cta_text = models.CharField(max_length=50)
    redirect_url = models.URLField(blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads_created')

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ads_approved'
    )

    views_count = models.PositiveIntegerField(default=0)
    clicks_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ad"
        verbose_name_plural = "Ads"
    
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1

            while Ads.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)
