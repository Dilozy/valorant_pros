# Generated by Django 5.1.1 on 2024-09-28 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0003_alter_player_twitch_link_alter_player_twitter_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]
