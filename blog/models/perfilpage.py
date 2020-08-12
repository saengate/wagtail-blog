from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.images.models import Image  # NOQA
from wagtail.images.edit_handlers import ImageChooserPanel


class PerfilPage(Page):
    description = RichTextField(blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('photo'),
        FieldPanel('created_at'),
        FieldPanel('updated_at'),
    ]

    api_fields = [
        APIField('description'),
        APIField('photo'),
        APIField('created_at'),
        APIField('updated_at'),
    ]
