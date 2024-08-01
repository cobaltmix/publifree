from django.db import models
from django.contrib.auth.models import User


class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='papers/pdfs/', null=True, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    views = models.IntegerField(default=0)
    # Add fields for ratings
    total_ratings = models.IntegerField(default=0)
    rating_sum = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # Calculate the average rating
    @property
    def average_rating(self):
        if self.total_ratings > 0:
            return self.rating_sum / self.total_ratings
        return 0

    # Calculate rating count
    @property
    def rating_count(self):
        return self.total_ratings