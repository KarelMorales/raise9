from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class ServiceItem(Orderable):
    page = ParentalKey('ProductsPage', on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, default="🛍️")
    url = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('url'),
        FieldPanel('image'),
    ]


class FeaturedProduct(Orderable):
    page = ParentalKey('ProductsPage', on_delete=models.CASCADE, related_name='featured_products')
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('creator'),
        FieldPanel('category'),
        FieldPanel('description'),
        FieldPanel('url'),
        FieldPanel('image'),
    ]


class ProductsPage(Page):
    page_title = models.CharField(max_length=255, blank=True, default="Products & Services")
    page_subtitle = models.TextField(
        blank=True,
        default="Explore our intellectual property services, products, and technology showcases."
    )
    contact_email = models.EmailField(blank=True, default="raise@wmsu.edu.ph")

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('page_subtitle'),
        FieldPanel('contact_email'),
        InlinePanel('services', label="Services"),
        InlinePanel('featured_products', label="Featured Products"),
    ]

    class Meta:
        verbose_name = "Products Page"