from django.db import models
from django.conf import settings


CATEGORY_CHOICES = [
    ('Medical', 'Medical'),
    ('Transport', 'Transport'),
    ('Food', 'Food'),
    ('Blood', 'Blood'),
    ('Accommodation', 'Accommodation'),
    ('Education', 'Education'),
    ('Other', 'Other'),
]


URGENCY_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
]


STATUS_CHOICES = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
]

class NeedRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Medium')
    image = models.ImageField(upload_to='need_images/', blank=True, null=True)
    attachment = models.FileField(upload_to='need_attachments/', blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='needs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"



class HelpAssignment(models.Model):
    need = models.OneToOneField(NeedRequest, on_delete=models.CASCADE, related_name="assignment")
    helper = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_assignments")
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.helper} helping {self.need.title}"





