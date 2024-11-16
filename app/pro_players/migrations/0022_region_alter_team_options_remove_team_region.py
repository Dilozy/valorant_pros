# Generated by Django 5.1.2 on 2024-11-07 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_players', '0021_alter_highlight_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='Region name')),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'team', 'verbose_name_plural': 'teams'},
        ),
    ]
