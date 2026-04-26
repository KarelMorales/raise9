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
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('url'),
        FieldPanel('image'),
    ]


class CommodityItem(Orderable):
    page = ParentalKey('ResourcesPage', on_delete=models.CASCADE, related_name='commodities')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    scientific_name = models.CharField(max_length=255, blank=True)
    short_description = models.TextField(blank=True)
    overview = RichTextField(blank=True)
    benefits = RichTextField(blank=True)
    cultivation = RichTextField(blank=True)
    market_info = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
        FieldPanel('scientific_name'),
        FieldPanel('short_description'),
        FieldPanel('image'),
        FieldPanel('overview'),
        FieldPanel('benefits'),
        FieldPanel('cultivation'),
        FieldPanel('market_info'),
    ]


class ResourcesPage(Page):
    page_subtitle = models.TextField(
        blank=True,
        default="Access curated knowledge resources for agriculture, aquatic and natural resources."
    )
    page_description = models.TextField(blank=True, default="")

    content_panels = Page.content_panels + [
        FieldPanel('page_subtitle'),
        FieldPanel('page_description'),
        InlinePanel('resources', label="External Resources"),
        InlinePanel('commodities', label="Commodities"),
    ]

    class Meta:
        verbose_name = "Resources Page"