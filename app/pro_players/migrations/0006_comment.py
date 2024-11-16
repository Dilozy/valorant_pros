# Generated by Django 5.1.1 on 2024-10-03 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0005_alter_player_slug_alter_team_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='pro_players.team', verbose_name='team')),
            ],
            options={
                'ordering': ['created'],
                'indexes': [models.Index(fields=['created'], name='pro_players_created_fca343_idx')],
            },
        ),
    ]
