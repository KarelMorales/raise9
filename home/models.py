from django.db import models
from wagtail.models import Page, Orderable  # Added Orderable here
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel  # Added InlinePanel here
from modelcluster.fields import ParentalKey  # Added ParentalKey for model linking

# Import your related models
from projects.models import ProjectPage
from events.models import EventPage 


class MapLocation(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='map_locations')
    name = models.CharField(max_length=255, help_text="e.g., WMSU (Main Hub)")
    latitude = models.FloatField(help_text="e.g., 6.9186")
    longitude = models.FloatField(help_text="e.g., 122.0620")
    address = models.CharField(max_length=255, blank=True)
    google_maps_url = models.URLField(blank=True, verbose_name="Google Maps Link")
    pop_offset_x = models.IntegerField(default=0, help_text="Use -30 or 30 to shift popup if pins overlap close together.")
    pop_offset_y = models.IntegerField(default=-24, help_text="Default is -24 (places popup right over pin tip).")

    panels = [
        FieldPanel('name'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        FieldPanel('address'),
        FieldPanel('google_maps_url'),
        FieldPanel('pop_offset_x'),
        FieldPanel('pop_offset_y'),
    ]


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

        # Map Locations admin management portal row
        InlinePanel('map_locations', label="Map Locations"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        # 1. Fetch the 3 most recent LIVE event pages
        context['recent_events'] = EventPage.objects.live().public().order_by('-event_date')[:3]

        # 2. Flagship Projects - Links the cards to your project dashboards
        context['flagship_projects'] = {
            'regional_iptbm': ProjectPage.objects.live().filter(abbreviation__icontains="Regional IPTBM").first(),
            'atbi': ProjectPage.objects.live().filter(abbreviation__icontains="ATBI").first(),
            'abh': ProjectPage.objects.live().filter(abbreviation__icontains="ABH").first(),
            'raise_km': ProjectPage.objects.live().filter(abbreviation__icontains="KM").first(),
        }
        return context

    class Meta:
        verbose_name = "Home Page"