from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    original_url = models.URLField()
    short_url = models.CharField(max_length=50)
    visit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    visited_at = models.DateTimeField(null=True, blank=True)  # Updates on access

    def __str__(self):
        return self.title
