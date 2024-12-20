# Generated by Django 5.1.3 on 2024-11-28 02:09

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_edition_editors_desk_speech'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='contributors/'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='coverimage',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='editions/'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='edition_pdfs/'),
        ),
    ]
