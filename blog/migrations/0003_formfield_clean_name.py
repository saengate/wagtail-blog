# Generated by Django 3.1.1 on 2020-09-08 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contactpage_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='clean_name',
            field=models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name'),
        ),
    ]
