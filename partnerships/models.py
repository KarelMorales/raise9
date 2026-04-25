from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class AdvisoryCouncilMember(Orderable):
    page = ParentalKey('PartnershipsPage', on_delete=models.CASCADE, related_name='advisory_members')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=10, blank=True, default="🏛️")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('institution'),
        FieldPanel('icon'),
        FieldPanel('image'),
    ]


class CollaboratingAgency(Orderable):
    page = ParentalKey('PartnershipsPage', on_delete=models.CASCADE, related_name='agencies')
    name = models.CharField(max_length=255)
    abbr = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, default="🏢")
    website = models.URLField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('abbr'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('website'),
    ]


class PartnershipActivity(Orderable):
    page = ParentalKey('PartnershipsPage', on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('location'),
        FieldPanel('summary'),
        FieldPanel('url'),
        FieldPanel('image'),
    ]


class PartnershipsPage(Page):
    page_subtitle = models.TextField(
        blank=True,
        default="Building strong relationships to advance AANR development in Western Mindanao."
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_subtitle'),
        InlinePanel('advisory_members', label="Advisory Council Members"),
        InlinePanel('agencies', label="Collaborating Agencies"),
        InlinePanel('activities', label="Partnership Activities"),
    ]

    class Meta:
        verbose_name = "Partnerships Page"