# Generated by Django 5.1.2 on 2024-11-07 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0022_region_alter_team_options_remove_team_region'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['-region'], 'verbose_name': 'team', 'verbose_name_plural': 'teams'},
        ),
        migrations.AlterField(
            model_name='team',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro_players.region', verbose_name='Region'),
        ),
    ]
