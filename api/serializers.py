from rest_framework import serializers
from pro_players.models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "full_name",
            "in_game_name",
            "in_game_role",
            "team",
            "twitter_link",
            "twitch_link",
            ]


class ExistingPlayerSerializer(serializers.ModelSerializer):
    in_game_name = serializers.ChoiceField(choices=[])

    class Meta:
        model = Player
        fields = [
            "full_name",
            "in_game_name",
            "in_game_role",
            "team",
            "twitter_link",
            "twitch_link",
            ]

        read_only_fields = [
            "full_name",
            "in_game_role",
            "team",
            "twitter_link",
            "twitch_link",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически заполняем choices из базы данных
        self.fields['in_game_name'].choices = [(player.in_game_name, player.in_game_name) for player in Player.objects.all()]


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            "name", "region", "players"
        ]
