from django.contrib import admin
from .models import ResearchPaper


class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    actions = ['publish_papers', 'unpublish_papers']

    def publish_papers(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish_papers(self, request, queryset):
        queryset.update(is_published=False)

    publish_papers.short_description = "Publish selected papers"
    unpublish_papers.short_description = "Unpublish selected papers"


admin.site.register(ResearchPaper, ResearchPaperAdmin)