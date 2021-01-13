import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from game.forms import GameCreateForm
from game.models import Game
from image_processing.utils import process_image


class GameListView(LoginRequiredMixin, ListView):
    template_name = "game/game-list.html"

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)


class GameDetailView(LoginRequiredMixin, DetailView):
    template_name = "game/game-detail.html"

    def get_object(self, queryset=None):
        return Game.objects.get(token=self.kwargs["token"])


class GameCreateView(LoginRequiredMixin, CreateView):
    template_name = "game/game-create.html"
    model = Game
    form = GameCreateForm
    fields = ("name", "image", "width", "height")

    def get_success_url(self):
        return reverse('game-details', kwargs={"token": self.object.token})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.token = str(uuid.uuid4())
        obj.user = self.request.user
        obj.map = ""
        obj.save()
        # TODO: this has to be done async as it takes ages
        obj.map = process_image(obj.image.path).dumps()
        return super().form_valid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "game/game-delete.html"
    model = Game
    success_url = reverse_lazy('game-list')

    def get_object(self, queryset=None):
        return Game.objects.get(token=self.kwargs["token"])
