from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class AboutPage(Page):

    # Hero
    hero_subtitle = models.TextField(blank=True)

    # Program Rationale
    program_rationale = RichTextField(blank=True)

    # Objectives
    program_objectives_general = RichTextField(blank=True)
    program_objectives_specific = RichTextField(blank=True)

    # Org Structure
    org_structure_title = models.CharField(max_length=255, blank=True, default="Our Organizational Structure")
    org_structure_description = models.TextField(blank=True)
    org_structure_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Mission Vision
    mission = RichTextField(blank=True)
    vision = RichTextField(blank=True)
    objectives = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_subtitle'),
        FieldPanel('program_rationale'),
        FieldPanel('program_objectives_general'),
        FieldPanel('program_objectives_specific'),
        FieldPanel('org_structure_title'),
        FieldPanel('org_structure_description'),
        FieldPanel('org_structure_image'),
        FieldPanel('mission'),
        FieldPanel('vision'),
        FieldPanel('objectives'),
    ]

    class Meta:
        verbose_name = "About Page"