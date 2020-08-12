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
from rest_framework import serializers

# Create your models here.


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class FormFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ('__all__')
        many = True
        read_only = True


class ContactPage(AbstractEmailForm):
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
        APIField('form_fields', serializer=FormFieldsSerializer()),
        APIField('thank_you'),
    ]
