from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from movies.models import Movie, Like
from movies.permissions import LikePermission, MoviePermission
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


class PublicMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [MoviePermission]

    # get all movies liked by the authenticated user
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_liked_movies(self, request):
        user_likes = Like.objects.filter(user_id=self.request.user)
        liked_movies = [like.movie for like in user_likes]
        serializer = PublicMovieSerializer(liked_movies, many=True)
        return Response(serializer.data)


class LikesViewSet(viewsets.ModelViewSet):
    serializer_class = PublicLikeSerializer
    permission_classes = [IsAuthenticated,LikePermission]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
    
    def get_queryset(self):
        return Like.objects.filter(user_id=self.request.user)
    
    @action(detail=False, methods=['delete'], url_path=r'by_movie/(?P<movie>[^/.]+)')
    def remove_by_movie(self, request,movie = None):
        instance = get_object_or_404(Like,user_id=request.user,movie=movie)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
