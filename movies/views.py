from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from movies.models import Movie, Like
from movies.permissions import MoviePermission
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


class PublicMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [MoviePermission]

    # TODO: check and test
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_liked_movies(self):
        return self.queryset.filter(likes__user_id=self.request.user, likes__liked=True)


# TODO: check and test
class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = PublicLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
