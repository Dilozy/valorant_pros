from rest_framework import serializers
from pro_players.models import Highlight, Player, Team, Comment


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "full_name",
            "in_game_name",
            "team",
            "in_game_role",
            "twitter_link",
            "twitch_link",
            ]

        read_only_fields = [
            "team",
        ]


class ExistingPlayerSerializer(serializers.ModelSerializer):
    in_game_name = serializers.ChoiceField(choices=[])

    class Meta:
        model = Player
        fields = [
            "id",
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
            "twitter_link",
            "twitch_link",
        ]

    def __init__(self, *args, **kwargs):
        team_name = kwargs.get("pk")
        super().__init__(*args, **kwargs)
        # Динамически заполняем choices из базы данных
        self.fields['in_game_name'].choices = [(player.in_game_name, player.in_game_name)
                                               for player in Player.objects.exclude(team__name=team_name)]


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            "name", "region", "players"
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

        read_only_fields = [
            "team",
            "name",
            "active",
        ]


class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = "__all__"

        read_only_fields = [
            "player",
        ]