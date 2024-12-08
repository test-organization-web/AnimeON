# Generated by Django 4.2.11 on 2024-12-08 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anime', '0008_remove_voiceover_file_voiceover_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date and time')),
                ('message', models.CharField(blank=True, max_length=255)),
                ('event', models.CharField(choices=[('SET_TOP', 'Додано в ТОП'), ('RESET_TOP', 'Видалено з ТОП')], max_length=50)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anime_history', to='anime.anime')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Anime history',
                'verbose_name_plural': 'Anime history',
            },
        ),
    ]
