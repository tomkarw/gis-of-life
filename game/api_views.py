import json
import pickle
from json import JSONEncoder

import numpy as np
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from game.models import Blob, Game
from game.utils import advance_frame


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class BlobFrameSerializer(ModelSerializer):
    class Meta:
        model = Blob
        fields = ("x", "y", "color", "age", "energy")


class GameFrameAPIView(APIView):

    def get(self, request, **kwargs):
        try:
            game = Game.objects.prefetch_related('blobs').get(token=kwargs["token"])
        except Game.DoesNotExist:
            raise NotFound(f"Game with token {kwargs['token']} not found")

        advance_frame(game)

        serialized_blobs = BlobFrameSerializer(game.blobs, many=True)
        return Response(serialized_blobs.data, status=status.HTTP_200_OK)


class GameMapAPIView(APIView):

    def get(self, request, **kwargs):
        try:
            game = Game.objects.prefetch_related('blobs').get(token=kwargs["token"])
        except Game.DoesNotExist:
            raise NotFound(f"Game with token {kwargs['token']} not found")

        serialized_map = json.dumps(pickle.loads(game.map), cls=NumpyArrayEncoder)
        return Response(serialized_map, status=status.HTTP_200_OK)

