# Generated by Django 5.1.1 on 2024-09-25 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='team_name')),
                ('region', models.CharField(max_length=10, verbose_name='region')),
            ],
            options={
                'db_table': 'team',
                'ordering': ['-region'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('in_game_name', models.CharField(max_length=50)),
                ('in_game_role', models.CharField(max_length=15, verbose_name='role')),
                ('twitter_link', models.URLField(verbose_name='twitter')),
                ('twitch_link', models.URLField(verbose_name='twitch')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro_players.team')),
            ],
            options={
                'db_table': 'player',
                'ordering': ['-team'],
            },
        ),
    ]
