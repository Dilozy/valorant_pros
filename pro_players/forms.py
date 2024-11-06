from django import forms
from .models import Highlight, Team, Player, Comment


class TeamForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label="New team name")


    class Meta:
        model = Team
        fields = ["name"]


class NewPlayerForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("Duelist", "Duelist"),
        ("Smoker", "Smoker"),
        ("Sentinel", "Sentinel"),
        ("Initiator", "Initiator"),
        ("Flex", "Flex"),
        ("IGL", "IGL")
    ]

    full_name = forms.CharField(max_length=60, label="Full name")
    in_game_name = forms.CharField(max_length=30, label="In game name")
    in_game_role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    twitter_link = forms.URLField(label="Twitter link", required=False)
    twitch_link = forms.URLField(label="Twitch link", required=False)

    class Meta:
        model = Player
        fields = ["in_game_name", "in_game_role", "full_name", "twitter_link", "twitch_link"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": "Your comment",
        }


class EmailRecommendationForm(forms.Form):
    to = forms.EmailField()
    recomendation_text = forms.CharField(widget=forms.Textarea)


class ExistingPlayerForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Player.teamless.all(),
                                    label="Choose a player",
                                    empty_label="None")


class AddHighlightForm(forms.ModelForm):
    class Meta:
        model = Highlight
        fields = ["video_title", "video_url"]