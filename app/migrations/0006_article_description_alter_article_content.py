# Generated by Django 5.1.3 on 2024-11-25 17:57

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_edition_pdf_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]