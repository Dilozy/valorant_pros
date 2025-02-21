# Generated by Django 5.1.1 on 2024-11-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0018_highlight_youtube_api_snippet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highlight',
            name='youtube_API_snippet',
        ),
        migrations.AddField(
            model_name='highlight',
            name='snippet',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='video_url',
            field=models.URLField(unique=True),
        ),
    ]
