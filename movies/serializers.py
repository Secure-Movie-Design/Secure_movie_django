from rest_framework import serializers

from movies.models import Movie, Like


class PublicMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'year', 'category', 'image_url',)
        read_only_fields = ('id',)


class PublicLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'movie', 'user_id',)
        read_only_fields = ('id', 'user_id',)
