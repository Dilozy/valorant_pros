from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from pro_players.models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer, ExistingPlayerSerializer
from .permissions import IsAdminOrReadOnly


class PlayersListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class TeamAPIList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["region"]


class TeamAPIDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrReadOnly, )

            
class PlayersAPIList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = PlayersListPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["team"]
    search_fields = ["in_game_name", "full_name"]
    permission_classes = (IsAdminOrReadOnly, )


class PlayerAPIDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def destroy(self, request, *args, **kwargs):
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
        try:
            return Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            return None


    def post(self, request, *args, **kwargs):
        team = self.get_team()

        if team is None:
            return Response({"error": "The team is not found"}, status=404)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(team=team)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AddExistingPlayerAPI(mixins.ListModelMixin,
                           generics.UpdateAPIView):
    serializer_class = ExistingPlayerSerializer
    permission_classes = (IsAdminUser, )
    
    def get_queryset(self):
        return Player.objects.exclude(team=self.get_team())


    def get(self, request, *args, **kwargs):
        existing_players = self.get_queryset()
        serializer = self.get_serializer(existing_players, many=True)

        return Response(serializer.data, status=200)


    def get_team(self):
        team_name = self.kwargs.get("pk")
        try:
            return Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            return None


    def put(self, request, *args, **kwargs):
        team = self.get_team()
        
        if team is None:
            return Response({"error": "The team is not found"}, status=404)
        
        player_name = request.data.get("in_game_name")
        if player_name is None:
            return Response({"error": "Player ID is required"})

        instance = Player.objects.get(in_game_name=player_name)
        instance.team = team
        instance.save()

        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
