from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path("drf-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("players-list/list-teamless-players/",
         views.ListTeamlessPlayersAPI.as_view(),
         name="list_teamless_players"),
    path("players-list/", views.PlayersAPIList.as_view()),
    path("teams-list/", views.TeamAPIList.as_view()),
    path("team/<str:pk>/add-new-player/", views.AddNewPlayerAPI.as_view()),
    path("team/<str:pk>/add-existing-player/",
         views.AddExistingPlayerToTeamAPI.as_view(),
         name="add-existing-player"),
    path("team/<str:pk>/comments-list/",
         views.CommentListCreateAPI.as_view(),
         name="comments_list"),
    path("team/<str:pk>/", views.TeamAPIDetailsView.as_view()),
    path("player/<int:pk>/eradicate/", views.EradicatePlayerAPI.as_view()),
    path("player/<int:pk>/list-highlights/",
         views.HighlightsListCreateAPI.as_view(),
         name="list_highlights"),
    path("player/<int:pk>/", views.PlayerAPIDetailsView.as_view()),
    path("comment/<int:pk>/details/", views.CommentDetailsAPI.as_view()),
    path("schema/visualize/", 
         SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
