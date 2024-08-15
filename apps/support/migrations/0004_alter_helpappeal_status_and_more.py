# Generated by Django 4.2.11 on 2024-08-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_rightholderappeal_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpappeal',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], max_length=50),
        ),
        migrations.AlterField(
            model_name='helpappealhistory',
            name='event',
            field=models.CharField(choices=[('ASSIGNED', 'Тікет був пизначений'), ('UNASSIGNED', 'Тікет позбувся пизначення'), ('IN_PROGRESS', 'Тікет в процесі'), ('RESOLVED', 'Тікет був вирішений'), ('OPEN', 'Тікет відкритий'), ('COMMENT', 'Comment')], max_length=50),
        ),
        migrations.AlterField(
            model_name='helpappealhistory',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], max_length=100),
        ),
        migrations.AlterField(
            model_name='rightholderappeal',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], max_length=50),
        ),
        migrations.AlterField(
            model_name='rightholderappealhistory',
            name='event',
            field=models.CharField(choices=[('ASSIGNED', 'Тікет був пизначений'), ('UNASSIGNED', 'Тікет позбувся пизначення'), ('IN_PROGRESS', 'Тікет в процесі'), ('RESOLVED', 'Тікет був вирішений'), ('OPEN', 'Тікет відкритий'), ('COMMENT', 'Comment')], max_length=50),
        ),
        migrations.AlterField(
            model_name='rightholderappealhistory',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], max_length=100),
        ),
    ]
