from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel, \
    MultiFieldPanel, InlinePanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey


class LinkFields(models.Model):
    link_external = models.URLField("External Link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )
    link_text = models.CharField(max_length=255)

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_text'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = RichTextField()
    active = models.BooleanField(default=True)

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('image'),
        MultiFieldPanel(LinkFields.panels, "Link"),
        FieldPanel('active'),
    ]

    class Meta:
        abstract = True


# Home Page


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('home.HomePage', related_name='carousel_items')


class HomePage(Page):

    content_panels = [
        FieldPanel('title', classname="full title"),
        InlinePanel('carousel_items', label="Carousel Items"),
    ]

    class Meta:
        verbose_name = "Homepage"
