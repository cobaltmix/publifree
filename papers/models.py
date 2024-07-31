from django.db import models
from django.contrib.auth.models import User


class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
