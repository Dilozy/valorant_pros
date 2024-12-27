from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from pro_players.models import Player, Team, Comment, Highlight, Region
from .serializers import (
    PlayerSerializer, TeamSerializer,
    ExistingPlayerSerializer, CommentSerializer,
    HighlightSerializer, RegionSerializer,
)
from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly


class PlayersListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class AllTeamsListAPI(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["region"]


class RegionTeamsAPI(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrReadOnly, )


    def dispatch(self, request, *args, **kwargs):
        self.region = get_object_or_404(Region, id=kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    
    def get_queryset(self):
        return Team.objects.filter(region=self.region)


    def perform_create(self, serializer):
        serializer.save(region=self.region)


class TeamDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrReadOnly, )


    def get_object(self):
        region = get_object_or_404(Region, id=self.kwargs.get("pk"))
        team = get_object_or_404(Team, region=region, name=self.kwargs.get("team_pk"))
        return team
            

class PlayersListAPI(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = PlayersListPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["team"]
    search_fields = ["in_game_name", "full_name"]
    permission_classes = (IsAdminOrReadOnly, )


class EradicatePlayerAPI(generics.RetrieveDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_class = (IsAdminUser, )


class PlayerDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (IsAdminOrReadOnly, )


    def destroy(self, request, *args, **kwargs):
        """Метод сбрасывает команду на значение null"""
        instance = self.get_object()
        instance.team = None
        instance.save()
        
        serializer = PlayerSerializer(instance)
        return Response(serializer.data)


class AddNewPlayerAPI(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer
    permission_classes = (IsAdminUser, )
    

    def get_queryset(self):
        return Player.objects.filter(team=self.get_team())


    def get_team(self):
        team_name = self.kwargs.get("pk")
        return get_object_or_404(Team, name=team_name)


    def perform_create(self, serializer):
        serializer.save(team=self.get_team())


class ListTeamlessPlayersAPI(generics.ListAPIView):
    serializer_class = PlayerSerializer
    queryset = Player.teamless.all()


class AddExistingPlayerToTeamAPI(generics.UpdateAPIView):
    serializer_class = ExistingPlayerSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        player_name = self.request.data.get("in_game_name")
        player = get_object_or_404(Player, in_game_name=player_name)
        return player

    def update(self, request, *args, **kwargs):
        player = self.get_object()
        team = get_object_or_404(Team, name=self.kwargs.get("pk"))

        player.team = team
        player.save()

        serializer = self.get_serializer(player, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


    def dispatch(self, request, *args, **kwargs):
        # Извлекаем команду один раз и сохраняем её как атрибут экземпляра
        team_name = self.kwargs.get("pk")
        self.team = get_object_or_404(Team, name=team_name)
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return Comment.objects.filter(team=self.team)


    def perform_create(self, serializer):
        serializer.save(team=self.team, name=self.request.user.username)


class CommentDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentSerializer


class HighlightsListCreateAPI(generics.ListCreateAPIView):
    serializer_class = HighlightSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def dispatch(self, request, *args, **kwargs):
        player = get_object_or_404(Player, id=self.kwargs.get("pk"))
        self.player = player
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return Highlight.objects.filter(player=self.player)


    def perform_create(self, serializer):
        serializer.save(player=self.player)


class ListRegionsAPI(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer