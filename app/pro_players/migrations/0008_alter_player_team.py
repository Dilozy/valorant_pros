# Generated by Django 5.1.1 on 2024-10-09 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0007_alter_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='pro_players.team'),
        ),
    ]
