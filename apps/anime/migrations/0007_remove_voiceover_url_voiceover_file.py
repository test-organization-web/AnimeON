# Generated by Django 4.2.11 on 2024-09-24 18:22

import apps.anime.s3_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_reaction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voiceover',
            name='url',
        ),
        migrations.AddField(
            model_name='voiceover',
            name='file',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
