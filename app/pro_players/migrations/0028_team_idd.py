# Generated by Django 5.1.2 on 2024-11-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0027_remove_team_idd_alter_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='idd',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
