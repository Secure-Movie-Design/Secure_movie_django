import re

from django.db import IntegrityError
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movies.models import Movie, Like
from movies.permissions import LikePermission, MoviePermission, isAdminUser
from movies.serializers import PublicMovieSerializer, PublicLikeSerializer


def sort_by(sort_value: str, objects, serializer):
    queryset = objects.order_by(Lower(sort_value))
    serializer = serializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class PublicMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = PublicMovieSerializer
    permission_classes = [MoviePermission]

    @action(detail=False, methods=['get'], url_path=r'user-type', url_name='user-type')
    def user_type(self, request):
        return Response({'user-type': 'admin' if isAdminUser(request) else 'user'}, status=status.HTTP_200_OK)

    # get all movies liked by the authenticated user
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_liked_movies(self, request):
        user_likes = Like.objects.filter(user_id=self.request.user)
        liked_movies = [like.movie for like in user_likes]
        serializer = PublicMovieSerializer(liked_movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='sort-by-title', url_name='sort-title')
    def sort_movie_by_title(self, request):
        return sort_by('title', self.queryset, self.get_serializer_class())

    @action(detail=False, methods=['GET'], url_path=r'filter-by-director/(?P<director>[^/.]+)', url_name='filter-director')
    def filter_movie_by_director(self, request, director=None):
        queryset = Movie.objects.filter(director__icontains=director)
        serializer = PublicMovieSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LikesViewSet(viewsets.ModelViewSet):
    serializer_class = PublicLikeSerializer
    permission_classes = [IsAuthenticated, LikePermission]

    def perform_create(self, serializer):
        try:
            serializer.save(user_id=self.request.user)
        except IntegrityError:
            raise exceptions.ValidationError("Like already set")

    def get_queryset(self):
        return Like.objects.filter(user_id=self.request.user)

    @action(detail=False, methods=['delete'], url_path=r'by_movie/(?P<movie>[^/.]+)', url_name='by-movie')
    def remove_by_movie(self, request, movie=None):
        instance = get_object_or_404(Like, user_id=request.user, movie=movie)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
