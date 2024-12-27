from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/match/(?P<team_slug>[\w+\-]+)/$', consumers.MatchScoreConsumer.as_asgi()),
]