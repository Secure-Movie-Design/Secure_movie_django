from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from movies.models import Movie, Like
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


class PublicMovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [AllowAny]
