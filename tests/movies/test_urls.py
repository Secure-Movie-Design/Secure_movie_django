import json

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient


@pytest.fixture()
def admin_user():
    admin = mixer.blend(get_user_model())
    group = mixer.blend(Group, name='admin')
    admin.groups.add(group)
    admin.save()
    return admin


@pytest.fixture()
def user():
    user = mixer.blend(get_user_model())
    return user


@pytest.fixture()
def movie_content():
    return {
        'title': 'New movie',
        'description': 'New description',
        'year': 2021,
        'category': 'ACTION'
    }


@pytest.fixture()
def only_movies(admin_user):
    return [
        mixer.blend('movies.Movie', title='First movie', description='First description', year=2021,
                    category='ACTION', user=admin_user),
        mixer.blend('movies.Movie', title='Second movie', description='Second description', year=2022,
                    category='ADVENTURE', user=admin_user),
        mixer.blend('movies.Movie', title='Third movie', description='Third description', year=2023,
                    category='COMEDY', user=admin_user),
    ]


@pytest.fixture()
def movies_and_likes(admin_user, user):
    movies = [
        mixer.blend('movies.Movie', title='First movie', description='First description', year=2021,
                    category='ACTION', user=admin_user),
        mixer.blend('movies.Movie', title='Second movie', description='Second description', year=2022,
                    category='ADVENTURE', user=user),
        mixer.blend('movies.Movie', title='Third movie', description='Third description', year=2023,
                    category='COMEDY', user=user),
    ]
    return [
        mixer.blend('movies.Like', movie=movies[0], liked=True, user=user),
        mixer.blend('movies.Like', movie=movies[1], liked=True, user=admin_user),
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
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_update_movies(self):
        path = reverse('movies-list')
        client = get_client()
        response = client.put(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_delete_movies(self):
        path = reverse('movies-list')
        client = get_client()
        response = client.delete(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_can_retrieve_movies(self, only_movies):
        path = reverse('movies-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert len(obj) == len(only_movies)

    def test_admin_can_create_movies(self, movie_content, admin_user):
        path = reverse('movies-list')
        client = get_client(admin_user)
        response = client.post(path, data=movie_content)
        assert response.status_code == HTTP_201_CREATED
        obj = parse_response(response)
        assert obj['title'] == movie_content['title']
        assert obj['description'] == movie_content['description']
        assert obj['year'] == movie_content['year']
        assert obj['category'] == movie_content['category']

    def test_admin_can_update_movies(self, movie_content, admin_user):
        path = reverse('movies-list')
        client = get_client(admin_user)
        response = client.post(path, data=movie_content)
        path = reverse('movies-detail', kwargs={'pk': response.data['id']})
        movie_content['title'] = 'Updated movie'
        response = client.put(path, data=movie_content)
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'Updated movie'

    def test_admin_can_delete_movies(self, movie_content, admin_user):
        path = reverse('movies-list')
        client = get_client(admin_user)
        response = client.post(path, data=movie_content)
        path = reverse('movies-detail', kwargs={'pk': response.data['id']})
        response = client.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT
