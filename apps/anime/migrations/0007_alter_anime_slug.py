# Generated by Django 4.2.11 on 2024-04-23 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_alter_anime_slug_alter_studio_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
