from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from django.contrib.auth.models import User


class ForumReply(Orderable):
    page = ParentalKey('ForumTopicPage', on_delete=models.CASCADE, related_name='replies_list')
    author_name = models.CharField(max_length=255, blank=True)
    content = RichTextField(blank=True)
    is_solution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel('author_name'),
        FieldPanel('content'),
        FieldPanel('is_solution'),
    ]


class ForumIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['topics'] = ForumTopicPage.objects.child_of(self).live().order_by('-first_published_at')
        return context

    class Meta:
        verbose_name = "Forum Index Page"


class ForumTopicPage(Page):
    author_name = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    commodities = models.CharField(max_length=255, blank=True, help_text="Comma separated commodities")
    views_count = models.IntegerField(default=0)

    content_panels = Page.content_panels + [
        FieldPanel('author_name'),
        FieldPanel('description'),
        FieldPanel('commodities'),
        InlinePanel('replies_list', label="Replies"),
    ]

    def get_commodity_list(self):
        if self.commodities:
            return [c.strip() for c in self.commodities.split(',')]
        return []

    @property
    def replies_count(self):
        return self.replies_list.count()

    @property
    def latest_post_date(self):
        return self.last_published_at or self.first_published_at

    def get_context(self, request):
        context = super().get_context(request)
        context['replies'] = self.replies_list.all()
        context['replies_count'] = self.replies_count
        # Increment view count
        self.views_count += 1
        self.save(update_fields=['views_count'])
        return context

    class Meta:
        verbose_name = "Forum Topic Page"