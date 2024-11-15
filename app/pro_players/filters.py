from django_filters import FilterSet, ChoiceFilter
from .models import Player


class PlayersFilter(FilterSet):
    OPTIONS = (
        (True, "Has a team"),
        (False, "Teamless"),
    )
    
    has_team = ChoiceFilter(
        field_name="Status",
        choices=OPTIONS,
        label="Status"
    )

    class Meta:
        model = Player
        fields = ["has_team"]