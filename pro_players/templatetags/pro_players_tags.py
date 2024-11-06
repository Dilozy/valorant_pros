from django import template
from ..models import Player


register = template.Library()


@register.simple_tag
def total_players():
    return Player.objects.count()


@register.simple_tag
def players_without_a_team():
    return Player.teamless.count()