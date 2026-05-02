from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

# Import your related models
from projects.models import ProjectPage
from events.models import EventPage 

class HomePage(Page):
    # --- HERO SECTION ---
    hero_title = models.CharField(max_length=255, blank=True, default="Raise Western Mindanao")
    hero_subtitle = models.TextField(blank=True, default="Empowering agricultural communities through innovation, sustainability, and knowledge sharing.")
    hero_description = models.TextField(blank=True, default="A multi-institutional program advancing technology transfer, business incubation, and knowledge sharing across Western Mindanao's AANR sector.")
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # --- STATS SECTION ---
    stat1_number = models.CharField(max_length=10, default="1000")
    stat1_label = models.CharField(max_length=100, default="Knowledge Resources")
    stat1_description = models.CharField(max_length=200, default="Research papers and technical docs")

    stat2_number = models.CharField(max_length=10, default="500")
    stat2_label = models.CharField(max_length=100, default="Community Members")
    stat2_description = models.CharField(max_length=200, default="Active researchers and innovators")

    stat3_number = models.CharField(max_length=10, default="50")
    stat3_label = models.CharField(max_length=100, default="Active Programs")
    stat3_description = models.CharField(max_length=200, default="Innovation and training initiatives")

    content_panels = Page.content_panels + [
        # Hero
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_description'),
        FieldPanel('hero_image'),

        # Stats
        FieldPanel('stat1_number'),
        FieldPanel('stat1_label'),
        FieldPanel('stat1_description'),
        FieldPanel('stat2_number'),
        FieldPanel('stat2_label'),
        FieldPanel('stat2_description'),
        FieldPanel('stat3_number'),
        FieldPanel('stat3_label'),
        FieldPanel('stat3_description'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # 1. Fetch the 3 most recent LIVE event pages
        # This fixes the "Read Full Article" button on the homepage
        context['recent_events'] = EventPage.objects.live().public().order_by('-event_date')[:3]

        # 2. Flagship Projects - Links the cards to your project dashboards
        # Using 'icontains' to prevent 404s caused by spacing/dash mismatches
        context['flagship_projects'] = {
            'regional_iptbm': ProjectPage.objects.live().filter(abbreviation__icontains="Regional IPTBM").first(),
            'atbi': ProjectPage.objects.live().filter(abbreviation__icontains="ATBI").first(),
            'abh': ProjectPage.objects.live().filter(abbreviation__icontains="ABH").first(),
            'raise_km': ProjectPage.objects.live().filter(abbreviation__icontains="KM").first(),
        }
        return context

    class Meta:
        verbose_name = "Home Page"