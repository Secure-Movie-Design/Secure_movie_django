from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from movies.models import Movie, Like
from movies.permissions import MoviePermission
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


class PublicMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [MoviePermission]


