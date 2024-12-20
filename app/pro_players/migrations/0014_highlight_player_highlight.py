# Generated by Django 5.1.1 on 2024-11-05 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0013_remove_player_highlight_delete_highlight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='highlight',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pro_players.highlight'),
        ),
    ]
