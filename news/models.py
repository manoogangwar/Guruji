from django.db import models
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    date_published = models.DateField(auto_now_add=True)
    is_listed = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_published']
        verbose_name = "News"
        verbose_name_plural = "News"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
