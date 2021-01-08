from django.forms import ModelForm

from game.models import Game


class GameCreateForm(ModelForm):
    class Meta:
        model = Game
        fields = ("name", "image", "width", "height")
