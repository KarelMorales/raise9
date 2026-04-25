from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class ResourceItem(Orderable):
    page = ParentalKey('ResourcesPage', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    image = models.ForeignKey(          # ← add this
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('url'),
        FieldPanel('image'),            # ← add this
    ]


class ResourcesPage(Page):
    page_subtitle = models.TextField(
        blank=True,
        default="Access curated knowledge resources for agriculture, aquatic and natural resources."
    )
    page_description = models.TextField(
        blank=True,
        default=""
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_subtitle'),
        FieldPanel('page_description'),
        InlinePanel('resources', label="Resources"),
    ]

    class Meta:
        verbose_name = "Resources Page"