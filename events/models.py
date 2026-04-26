from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class EventIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['events'] = EventPage.objects.child_of(self).live().order_by('-event_date')
        return context

    class Meta:
        verbose_name = "Events Index Page"


class EventPagePhoto(Orderable):
    page = ParentalKey('EventPage', on_delete=models.CASCADE, related_name='photos')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class EventPage(Page):
    event_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('workshop', 'Workshop'),
            ('meeting', 'Meeting'),
            ('review', 'Review'),
            ('training', 'Training'),
            ('promotional', 'Promotional'),
            ('pitching', 'Pitching'),
            ('other', 'Other'),
        ],
        default='other'
    )
    intro = models.TextField(blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_duration = models.CharField(max_length=255, blank=True)
    event_location = models.CharField(max_length=255, blank=True)
    participants = models.TextField(blank=True)
    overview = RichTextField(blank=True)
    objectives = RichTextField(blank=True)
    highlights = RichTextField(blank=True)
    outcomes = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('event_type'),
        FieldPanel('intro'),
        FieldPanel('event_date'),
        FieldPanel('event_duration'),
        FieldPanel('event_location'),
        FieldPanel('participants'),
        FieldPanel('overview'),
        FieldPanel('objectives'),
        FieldPanel('highlights'),
        FieldPanel('outcomes'),
        InlinePanel('photos', label="Event Photos (up to 5)"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['related_events'] = EventPage.objects.sibling_of(self).live().exclude(pk=self.pk).order_by('-event_date')[:3]
        return context

    class Meta:
        verbose_name = "Event Page"