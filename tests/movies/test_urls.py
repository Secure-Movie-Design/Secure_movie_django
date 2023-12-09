import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient


@pytest.fixture()
def only_movies(db):
    user = mixer.blend(get_user_model())
    admin = mixer.blend(get_user_model())
    user.is_staff = user.is_superuser = False
    admin.is_staff = admin.is_superuser = True
    admin.save()
    user.save()
    return [
        mixer.blend('movies.Movie', title='First movie', description='First description', year=2021,
                    category='ACTION', user=admin),
        mixer.blend('movies.Movie', title='Second movie', description='Second description', year=2022,
                    category='ADVENTURE', user=admin),
        mixer.blend('movies.Movie', title='Third movie', description='Third description', year=2023,
                    category='COMEDY', user=admin),
    ]


@pytest.fixture()
def movies_and_likes(db):
    user = mixer.blend(get_user_model())
    admin = mixer.blend(get_user_model())
    user.is_staff = user.is_superuser = False
    admin.is_staff = admin.is_superuser = True
    admin.save()
    user.save()
    movies = [
        mixer.blend('movies.Movie', title='First movie', description='First description', year=2021,
                    category='ACTION', user=admin),
        mixer.blend('movies.Movie', title='Second movie', description='Second description', year=2022,
                    category='ADVENTURE', user=user),
        mixer.blend('movies.Movie', title='Third movie', description='Third description', year=2023,
                    category='COMEDY', user=user),
    ]
    return [
        mixer.blend('movies.Like', movie=movies[0], liked=True, user=user),
        mixer.blend('movies.Like', movie=movies[1], liked=True, user=admin),
        mixer.blend('movies.Like', movie=movies[2], liked=False, user=user),
    ]


def get_client(user=None):
    client = APIClient()
    if user is not None:
        client.force_login(user)
    return client


def parse_response(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


@pytest.mark.django_db
class TestMovieList:

    def test_anonymous_user_cannot_create_movies(self):
        path = reverse('movies-list')
        client = get_client()
        response = client.post(path)
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_anonymous_user_cannot_update_movies(self):
        path = reverse('movies-list')
        client = get_client()
        response = client.put(path)
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_anonymous_user_cannot_delete_movies(self):
        path = reverse('movies-list')
        client = get_client()
        response = client.delete(path)
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_anonymous_user_can_retrieve_movies(self, only_movies):
        path = reverse('movies-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert len(obj) == len(only_movies)
