from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include, re_path
from .views import (
    PlayersAPIList, PlayerAPIDetailsView,
    TeamAPIList, TeamAPIDetailsView,
    AddNewPlayerAPI, AddExistingPlayerAPI
    )


urlpatterns = [
    path("drf-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("players-list/", PlayersAPIList.as_view()),
    path("teams-list/", TeamAPIList.as_view()),
    path("team/<str:pk>/add-new-player", AddNewPlayerAPI.as_view()),
    path("team/<str:pk>/add-existing-player", AddExistingPlayerAPI.as_view()),
    path("team/<str:pk>/", TeamAPIDetailsView.as_view()),
    path("player/<int:pk>/", PlayerAPIDetailsView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/visualize", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]
