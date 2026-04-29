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
    page_subtitle = models.TextField(blank=True, default="Access curated knowledge resources for agriculture, aquatic and natural resources.")
    page_description = models.TextField(blank=True, default="")

    content_panels = Page.content_panels + [
        FieldPanel('page_subtitle'),
        FieldPanel('page_description'),
        InlinePanel('resources', label="External Resources"),
        InlinePanel('commodities', label="Commodities"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # This allows the Resources page to list its sub-pages (the categories)
        context['resource_categories'] = ResourceCategoryPage.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name = "Resources Page"


class ResourceCategoryEntryItem(Orderable):
    """These are the individual list items (Events, News, etc.) inside a Category Page"""
    page = ParentalKey('ResourceCategoryPage', on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, help_text="Link for the event or resource")
    date = models.DateField(null=True, blank=True, help_text="Optional date for events or news")
    
    # Keeping the fields you had for flexibility
    file_type = models.CharField(max_length=50, blank=True, help_text="e.g. PDF, Video, Link")
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
        FieldPanel('date'),
        FieldPanel('file_type'),
        FieldPanel('image'),
    ]


class ResourceCategoryPage(Page):
    """The landing page for a specific category like 'Events' or 'Media'"""
    category_icon = models.CharField(max_length=10, blank=True, default="📁")
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=50,
        blank=True,
        default="from-primary to-accent",
        help_text="Tailwind gradient e.g. from-primary to-accent"
    )

    content_panels = Page.content_panels + [
        FieldPanel('category_icon'),
        FieldPanel('description'),
        FieldPanel('color'),
        # This InlinePanel allows you to add the list of items
        InlinePanel('entries', label="Resource Entries (List Items)"),
    ]

    class Meta:
        verbose_name = "Resource Category Page"