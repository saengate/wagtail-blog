from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
)
from wagtailcache.cache import WagtailCacheMixin, cache_page
from django.utils.decorators import method_decorator


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

    api_fields = [
        APIField('label'),
        APIField('help_text'),
        APIField('required'),
        APIField('field_type'),
        APIField('choices'),
        APIField('default_value'),
    ]


@method_decorator(cache_page, name='serve')
class ContactPage(WagtailCacheMixin, AbstractEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"

    intro = RichTextField(blank=True)
    thank_you = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel(
            'form_fields',
            label='Form Fields',
        ),
        FieldPanel('thank_you'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
    ]

    api_fields = [
        APIField('intro'),
        APIField('form_fields'),
        APIField('thank_you'),
    ]
