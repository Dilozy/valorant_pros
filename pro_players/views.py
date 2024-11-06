from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from .models import Comment, Team, Player
from .forms import (
    EmailRecommendationForm, NewPlayerForm,
    CommentForm, ExistingPlayerForm,
    AddHighlightForm
    )
from .filters import PlayersFilter
from .services import URL_to_ID


class HomePageView(generic.TemplateView):
    template_name = "base.html"


class AllPlayersList(generic.ListView):
    model = Player
    template_name = "players/all_players.html"
    paginate_by = 9
    
    def get_queryset(self) -> QuerySet[Any]:
        if self.request.GET.get("has_team") == "True":
            return Player.has_team.all()
        if self.request.GET.get("has_team") == "False":
            return Player.teamless.all()
        return Player.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All players"
        page = context["page_obj"]
        context["pages_range"] = page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        context["show_pagination"] = page.paginator.num_pages > 1
        context["filter"] = PlayersFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TeamsInRegionView(generic.ListView):
    template_name = "teams/region_teams.html"
    context_object_name = "teams"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = self.kwargs.get("region")
        return context


    def get_queryset(self):
        region = self.kwargs.get("region")
        return Team.objects.filter(region__iexact=region)


class AddTeamView(generic.CreateView):
    model = Team
    fields = ["name"]
    template_name = "teams/add_team.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = self.kwargs.get("region")
        return context


    def get_success_url(self) -> str:
        return reverse("pro_players:teams", args=[self.kwargs.get("region")])


    def form_valid(self, form):
        team = form.save(commit=False)
        region = self.kwargs.get("region")
        team.region = region
        team.save()
        return super().form_valid(form)


class TeamDetailsView(generic.ListView):
    context_object_name = "players"
    template_name = "teams/team_players.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region"] = self.kwargs.get("region")
        context["team"] = get_object_or_404(Team, slug=self.kwargs.get("team_slug"))
        context["form"] = CommentForm()
        context["comments"] = context["team"].comments.filter(active=True)
        return context


    def get_queryset(self):
        team = get_object_or_404(Team, slug=self.kwargs.get("team_slug"))
        queryset = team.players.all()
        return queryset


class PlayerDetailsView(generic.DetailView):
    model = Player
    template_name = "players/player_info.html"
    slug_url_kwarg = "player_slug"
    context_object_name = "player"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        highlights_data = Player.objects.filter(slug=self.kwargs.get("player_slug")) \
                                        .select_related("highlight") \
                                        .values("highlight__video_url",
                                                "highlight__video_title")
        
        if len(highlights_data) == 1 and highlights_data[0].get("highlight__video_url") is None:
            highlights_data = None
        context["highlights_data"] = highlights_data
        context["go_back_link"] = self.request.GET.get("next", "/")
        return context


class AddPlayerView(LoginRequiredMixin, generic.FormView):
    template_name = "players/add_player.html"
    form_class = NewPlayerForm


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["existing_player_form"] = ExistingPlayerForm()
        context["region"] = self.kwargs.get("region")
        context["team_slug"] = self.kwargs.get("team_slug")
        return context


    def post(self, request, *args, **kwargs):
        if request.POST.get("form_type") == "new_player":
            new_player_form = NewPlayerForm(request.POST)
            if new_player_form.is_valid():
                return self.form_valid(new_player_form)
        else:
            existing_player_form = ExistingPlayerForm(request.POST)
            if existing_player_form.is_valid():
                return self.form_valid(existing_player_form)
             

    def get_success_url(self) -> str:
        return reverse("pro_players:team_players", args=[self.kwargs.get("region"),
                                                         self.kwargs.get("team_slug")])


    def form_valid(self, form):
        if isinstance(form, NewPlayerForm):
            player = form.save(commit=False)
        else:
            player = form.cleaned_data["player"]

        player.team = get_object_or_404(Team, slug=self.kwargs.get("team_slug"))
        player.save()
        messages.success(self.request, f"Игрок {player.in_game_name} успешно добавлен в команду")
        return super().form_valid(form)


class DeleteTeamView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    slug_url_kwarg = "team_slug"
    success_message = "The team has been deleted successfully"


    def get_success_url(self) -> str:
        messages.success(self.request, self.success_message)
        return reverse("pro_players:teams", args=[self.kwargs.get("region")])


class DeletePlayerView(LoginRequiredMixin, generic.DeleteView):
    model = Player
    slug_url_kwarg = "player_slug"
    success_message = "The player has been deleted successfully"


    def get_success_url(self) -> str:
        messages.success(self.request, self.success_message)
        return reverse("pro_players:team_players", args=[self.kwargs.get("region"),
                                                         self.kwargs.get("team_slug")])


    def delete(self, request, *args, **kwargs):
        Player.objects.filter(slug=self.kwargs.get("player_slug")).update(team=None)


class EditPlayerView(LoginRequiredMixin, generic.UpdateView):
    model = Player
    fields = ["full_name", "in_game_name", "in_game_role", "twitter_link", "twitch_link", "team"]
    template_name = "players/edit_player.html"
    slug_url_kwarg = "player_slug"
    success_message = "The player has been edited successfully"


    def get_success_url(self) -> str:
        messages.success(self.request, self.success_message)
        return reverse("pro_players:player_info", args=[self.kwargs.get("player_slug")])


@method_decorator(require_POST, name="dispatch")
class PostTeamCommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ["body"]
    template_name = "utils/comment_form.html"


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["team"] = get_object_or_404(Team,
                                            slug=self.kwargs.get("team_slug"))
        context["region"] = self.kwargs.get("region")
        context["comment"] = None
        return context


    def get_success_url(self) -> str:
        messages.success(self.request, "Your comment has been added")
        return reverse("pro_players:team_players", args=[self.kwargs.get("region"),
                                                         self.kwargs.get("team_slug")])


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        comment = form.save(commit=False)
        comment.team = self.get_context_data()["team"]
        comment.name = self.request.user.username
        comment.save()
        return super().form_valid(form)


class SendEmailRecommendationView(LoginRequiredMixin, generic.FormView):
    template_name = "utils/send_recommendation.html"
    form_class = EmailRecommendationForm
    extra_context = {"sent": False}

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["player"] = get_object_or_404(Player, slug=self.kwargs.get("player_slug"))
        return context


    def get_success_url(self) -> str:
        return reverse("pro_players:send_email_recommendation", args=[self.kwargs.get("player_slug")])


    def form_valid(self, form):
        player = self.get_context_data()["player"]
        sender_name = self.request.user.username
        sender_email = self.request.user.email
        
        cd = form.cleaned_data
        player_url = self.request.build_absolute_uri(player.get_absolute_url())
        subject = f"{sender_name} recommends player {player.in_game_name}" \
                    " for your team."
        message = f"I recommend {player.in_game_name} for your team on role {player.in_game_role}" \
                    f"\nYou can check their profile out on {player_url}\n\n" \
                    f"{sender_name}\'s comment: {cd['recomendation_text']}"
        send_mail(subject, message, sender_email,
                        [cd["to"]])
        self.extra_context["sent"] = True
        return super().form_valid(form)


class AddHighlightView(generic.FormView):
    form_class = AddHighlightForm
    template_name = "players/add_highlight.html"


    def get_success_url(self) -> str:
        return reverse("pro_players:player_info",
                       args=[self.kwargs.get("player_slug")])


    def form_valid(self, form: Any) -> HttpResponse:
        highlight = form.save(commit=False)
        highlight.video_url = URL_to_ID(highlight.video_url)
        highlight.player = Player.objects.get(slug=self.kwargs.get("player_slug"))
        highlight.save()
        return super().form_valid(form)