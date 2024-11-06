from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class TeamlessManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                      .filter(team__isnull=True)


class HasTeamManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                      .filter(team__isnull=False)


class Team(models.Model):
    name = models.CharField(max_length=20, primary_key=True, verbose_name="Team name")
    region = models.CharField(max_length=10, verbose_name="region")
    slug = models.SlugField(unique=True, blank=True)


    class Meta:
        db_table = "team"
        ordering = ["-region"]
        verbose_name = "team"
        verbose_name_plural = "teams"


    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("pro_players:team_players", args=[self.region,
                                                         self.slug])


class Player(models.Model):
    full_name = models.CharField(max_length=255)
    in_game_name = models.CharField(max_length=50, verbose_name="In game name")
    in_game_role = models.CharField(max_length=15, verbose_name="role")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    twitter_link = models.URLField(verbose_name="twitter", null=True, blank=True)
    twitch_link = models.URLField(verbose_name="twitch", null=True, blank=True)
    slug = models.SlugField(unique=True)

    objects = models.Manager()
    has_team = HasTeamManager()
    teamless = TeamlessManager()


    class Meta:
        db_table = "player"
        ordering = ["-team"]
        verbose_name = "player"
        verbose_name_plural = "players"


    def __str__(self):
        return self.in_game_name


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.in_game_name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("pro_players:player_info", args=[self.slug])


class Comment(models.Model):
    team = models.ForeignKey(Team,
                             on_delete=models.CASCADE,
                             verbose_name="team",
                             related_name="comments"
                             )
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]


    def __str__(self):
        return f"Comment by {self.name} on {self.team}"


class Highlight(models.Model):
    video_title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=150, unique=True)
    player = models.ForeignKey("Player", on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"Youtube video: {self.video_title}"