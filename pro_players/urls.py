from django.urls import path, include
from . import views


app_name = "pro_players"


region_patterns = [
    path("", views.TeamsInRegionView.as_view(), name="teams"),
    path("add-team/", views.AddTeamView.as_view(), name="add_team"),
    path("<slug:team_slug>/", views.TeamDetailsView.as_view(), name="team_players"),
    path("<slug:team_slug>/add_player/",
         views.AddPlayerView.as_view(), name="add_player_forms"),
    path("delete/<slug:team_slug>/",
         views.DeleteTeamView.as_view(), name="delete_team"),
    path("<slug:team_slug>/delete/<slug:player_slug>/",
         views.DeletePlayerView.as_view(), name="delete_player"),
    path("<slug:team_slug>/comment/",
         views.PostTeamCommentView.as_view(), name="post_team_comment"),
]


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("all-players/", views.AllPlayersList.as_view(), name="all-players"),
    path("player/<slug:player_slug>/", views.PlayerDetailsView.as_view(), name="player_info"),
    path("player/<slug:player_slug>/add-highlight/", views.AddHighlightView.as_view(), name="add_highlight"),
    path("player/<slug:player_slug>/edit/", views.EditPlayerView.as_view(), name="edit_player"),
    path("player/<slug:player_slug>/send_recomendation/",
         views.SendEmailRecommendationView.as_view(), name="send_email_recommendation"),
    path("<str:region>/", include(region_patterns)),
]
