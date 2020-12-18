from django.http import HttpResponseNotFound
from django.shortcuts import render

from game.models import Game


def main(request, *args, **kwargs):
    try:
        game = Game.objects.get(token=kwargs["token"])
    except Game.DoesNotExist:
        return HttpResponseNotFound()
    context = {
        "game": game,
        "map": game.map,
    }
    return render(request, "game/main.html", context=context)
