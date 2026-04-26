from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class TimelineActivity(Orderable):
    page = ParentalKey('ProjectPage', on_delete=models.CASCADE, related_name='timeline_activities')
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('description'),
    ]


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['projects'] = ProjectPage.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name = "Project Index Page"


class ProjectPage(Page):
    abbreviation = models.CharField(max_length=50, blank=True)
    implementing_agency = models.CharField(max_length=255, blank=True)
    short_description = models.TextField(blank=True)
    duration_text = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('upcoming', 'Upcoming'),
        ],
        default='active'
    )
    is_featured = models.BooleanField(default=False)
    categories = models.CharField(max_length=255, blank=True, help_text="Comma separated categories")
    general_objective = RichTextField(blank=True)
    specific_objectives = RichTextField(blank=True)
    overview = RichTextField(blank=True)
    team_members = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    demo_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('abbreviation'),
        FieldPanel('implementing_agency'),
        FieldPanel('short_description'),
        FieldPanel('duration_text'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('status'),
        FieldPanel('is_featured'),
        FieldPanel('categories'),
        FieldPanel('hero_image'),
        FieldPanel('overview'),
        FieldPanel('general_objective'),
        FieldPanel('specific_objectives'),
        FieldPanel('team_members'),
        FieldPanel('demo_url'),
        FieldPanel('source_url'),
        InlinePanel('timeline_activities', label="Timeline Activities"),
    ]

    def get_status_display(self):
        return dict(self._meta.get_field('status').choices).get(self.status, self.status)

    def get_status_badge_color(self):
        colors = {
            'active': 'bg-green-500/20 text-green-300',
            'completed': 'bg-blue-500/20 text-blue-300',
            'upcoming': 'bg-yellow-500/20 text-yellow-300',
        }
        return colors.get(self.status, 'bg-gray-500/20 text-gray-300')

    def get_category_list(self):
        if self.categories:
            return [c.strip() for c in self.categories.split(',')]
        return []

    def get_specific_objectives_list(self):
        if self.specific_objectives:
            import re
            from django.utils.html import strip_tags
            text = strip_tags(self.specific_objectives)
            items = re.split(r'\n|;', text)
            return [item.strip() for item in items if item.strip()]
        return []

    def get_team_member_list(self):
        if self.team_members:
            import re
            from django.utils.html import strip_tags
            text = strip_tags(self.team_members)
            items = re.split(r'\n', text)
            return [item.strip() for item in items if item.strip()]
        return []

    @property
    def activities_count(self):
        return self.timeline_activities.count()

    class Meta:
        verbose_name = "Project Page"