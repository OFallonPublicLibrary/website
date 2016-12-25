from django.db import models
from django import forms
from django.shortcuts import redirect

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, \
    CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


PAGE_SKIN_CHOICES = (
  (' ', 'Default'),
  ('kids', 'Kids'),
  ('teens', 'Teens'),
)


# Global Streamfield definition

class PullQuoteBlock(StructBlock):
    quote = TextBlock("Quote Title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('float-left', 'Wrap left'),
        ('float-right', 'Wrap right'),
        ('float-center', 'Mid width'),
        ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


class StandardStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")


# Abstract Classes which contain commonly used fields

class LinkFields(models.Model):
    link_external = models.URLField("External Link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = RichTextField()
    link_text = models.CharField(max_length=255)


    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('link_text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class Skinable(models.Model):
    page_skin = models.CharField(
        max_length=255,
        choices=PAGE_SKIN_CHOICES,
        default=PAGE_SKIN_CHOICES[0][0],
    )

    class Meta:
        abstract = True

# Home Page


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('cms.HomePage', related_name='carousel_items')


class HomePage(Page, Skinable):

    content_panels = Page.content_panels + [
        InlinePanel('carousel_items', label="Carousel Items"),
        FieldPanel('page_skin'),
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = "Homepage"


# Standard Page

class StandardPage(Page, Skinable):
    body = StreamField(StandardStreamBlock())

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('body'),
        FieldPanel('page_skin'),
    ]


# Form Page

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


# PageAlias Page (for redirecting to external URLs)

class RedirectPage(Page, LinkFields):

    def serve(self, request):
        return redirect(self.link, permanent=False)

RedirectPage.content_panels = [FieldPanel('title')] + LinkFields.panels
