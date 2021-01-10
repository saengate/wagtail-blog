from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail_headless_preview.models import HeadlessPreviewMixin

# Create your models here.


class BlogsPage(HeadlessPreviewMixin, Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    created_at = models.DateField(default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('created_at'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]

    api_fields = [
        APIField('created_at'),
        APIField('intro'),
        APIField('body'),
    ]
