from django.contrib import admin
from .models import Highlight, Team, Player


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
    list_filter = ["region"]
    search_fields = ["name", "region"]
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["in_game_name", "in_game_role", "team"]
    list_filter = ["team", "in_game_role"]
    search_fields = ["team", "in_game_name", "in_game_role"]
    prepopulated_fields = {"slug": ("in_game_name", )}

@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ["video_title", "player"]
    list_filter = ["player"]