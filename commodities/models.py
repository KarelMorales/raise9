from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class CommodityIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['commodities'] = CommodityPage.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name = "Commodity Index Page"


class CommodityPage(Page):
    category = models.CharField(max_length=100, blank=True, default="Aquaculture")
    scientific_name = models.CharField(max_length=255, blank=True)
    short_description = models.TextField(blank=True)
    overview = RichTextField(blank=True)
    benefits = RichTextField(blank=True)
    cultivation = RichTextField(blank=True)
    market_info = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('scientific_name'),
        FieldPanel('short_description'),
        FieldPanel('hero_image'),
        FieldPanel('overview'),
        FieldPanel('benefits'),
        FieldPanel('cultivation'),
        FieldPanel('market_info'),
    ]

    class Meta:
        verbose_name = "Commodity Page"