# Generated by Django 5.1.2 on 2024-11-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0025_team_idd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='idd',
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Team name'),
        ),
    ]