# Generated by Django 4.2.11 on 2024-08-12 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0032_delete_parseanimelog'),
        ('user', '0005_useranime_date_alter_useranime_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEpisodeViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddConstraint(
            model_name='useranime',
            constraint=models.UniqueConstraint(fields=('user', 'action', 'anime'), name='unique_user_useranime_user_anime_action'),
        ),
        migrations.AddField(
            model_name='userepisodeviewed',
            name='episode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.episode'),
        ),
        migrations.AddField(
            model_name='userepisodeviewed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_episode', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='userepisodeviewed',
            constraint=models.UniqueConstraint(fields=('user', 'episode'), name='unique_user_userepisodeviewed_user_episode'),
        ),
    ]
