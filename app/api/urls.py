from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include, re_path
from . import views


app_name = "api"


teams_patterns = [
    path("<str:pk>/new-player/",
         views.AddNewPlayerAPI.as_view(),
         name="add_new_player"),
    path("<str:pk>/existing-player/",
         views.AddExistingPlayerToTeamAPI.as_view(),
         name="add-existing-player"),
    path("<str:pk>/comments/",
         views.CommentListCreateAPI.as_view(),
         name="comments_list"),
    path("<str:team_pk>/", views.TeamDetailsAPI.as_view()),
    path("", views.RegionTeamsAPI.as_view()),
]

players_patterns = [
    path("<int:pk>/eradicate/", views.EradicatePlayerAPI.as_view()),
    path("<int:pk>/highlights/",
         views.HighlightsListCreateAPI.as_view(),
         name="list_highlights"),
    path("teamless/",
         views.ListTeamlessPlayersAPI.as_view(),
         name="list_teamless_players"),
    path("<int:pk>/", views.PlayerDetailsAPI.as_view()),
    path("", views.PlayersListAPI.as_view()),
]


regions_patterns = [
    path("", views.ListRegionsAPI.as_view(), name="list_region"),
    path("<int:pk>/teams/", include(teams_patterns)),
]


urlpatterns = [
    path("drf-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("comments/<int:pk>/details/", views.CommentDetailsAPI.as_view()),
    path("schema/visualize/",
         SpectacularSwaggerView.as_view(url_name="api:schema"),
         name="swagger"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("all-teams/", views.AllTeamsListAPI.as_view()),
    path("players/", include(players_patterns)),
    path("regions/", include(regions_patterns)),
]
