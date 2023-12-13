from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from movies.models import Movie, Like
from movies.permissions import MoviePermission
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


class PublicMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [MoviePermission]

    # get all movies liked by the authenticated user
    @action(detail=False, methods=['get'])
    def user_liked_movies(self, request):
        user_likes = Like.objects.filter(user_id=self.request.user)
        liked_movies = [like.movie for like in user_likes]
        serializer = PublicMovieSerializer(liked_movies, many=True)
        return Response(serializer.data)

# TODO: check and test
class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = PublicLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)