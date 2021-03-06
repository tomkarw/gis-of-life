import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from game.constants import BLOB_SIZE, STARTING_BLOBS
from game.forms import GameCreateForm
from game.models import Game
from game.utils import create_blob
from image_processing.utils import process_image


class GameListView(LoginRequiredMixin, ListView):
    template_name = "game/game-list.html"

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)


class GameDetailView(LoginRequiredMixin, DetailView):
    template_name = "game/game-detail.html"

    def get_object(self, queryset=None):
        return Game.objects.get(token=self.kwargs["token"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["map_width"] = self.object.width * BLOB_SIZE
        context["map_height"] = self.object.height * BLOB_SIZE
        return context


class GameCreateView(LoginRequiredMixin, CreateView):
    template_name = "game/game-create.html"
    model = Game
    form = GameCreateForm
    fields = ("name", "image", "width", "height")

    def get_success_url(self):
        return reverse('game-details', kwargs={"token": self.object.token})

    def form_valid(self, form):
        game = form.save(commit=False)
        game.token = str(uuid.uuid4())
        game.user = self.request.user
        game.map = ""
        game.width //= BLOB_SIZE
        game.height //= BLOB_SIZE
        game.save()
        # TODO: this has to be done async as it takes some time
        game.map = process_image(game.image.path, game.width, game.height).dumps()
        for _ in range(STARTING_BLOBS): # TODO: use bulk_create?
            create_blob(game)
        return super().form_valid(form)


class GameDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "game/game-delete.html"
    model = Game
    success_url = reverse_lazy('game-list')

    def get_object(self, queryset=None):
        return Game.objects.get(token=self.kwargs["token"])
