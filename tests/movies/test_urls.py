import json

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
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
        'category': 'ACTION',
        'image_url': 'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
        'director': 'New Director'
    }


@pytest.fixture()
def movies(admin_user):
    return [
        mixer.blend('movies.Movie', id=1, title='First movie', description='First description', year=2021,
                    category='ACTION', image_url='https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                    director='A Director'),
        mixer.blend('movies.Movie', id=2, title='Second movie', description='Second description', year=2022,
                    category='ADVENTURE', image_url='https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                    director='A Director'),
        mixer.blend('movies.Movie', id=3, title='Third movie', description='Third description', year=2023,
                    category='COMEDY', image_url='https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                    director='A Director'),
        mixer.blend('movies.Movie', id=4, title='Fourth movie', description='Fourth description', year=2023,
                    category='COMEDY', image_url='https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                    director='A Director'),
    ]


@pytest.fixture()
def likes(admin_user, user, movies):
    return [
        mixer.blend('movies.Like', id=4, movie=movies[0], user_id=user),
        mixer.blend('movies.Like', id=5, movie=movies[1], user_id=admin_user),
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

    def test_anonymous_user_can_retrieve_movies(self, movies):
        path = reverse('movies-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert len(obj) == len(movies)

    def test_anonymous_user_cannot_retrieve_liked_movies(self, likes):
        path = reverse('movies-user-liked-movies')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_user_can_retrieve_liked_movies(self, likes, user):
        path = reverse('movies-user-liked-movies')
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert len(obj) == 1
        assert obj[0]['id'] == likes[0].movie.id

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
        assert obj['image_url'] == movie_content['image_url']

    def test_admin_can_update_movies(self, movie_content, admin_user):
        path = reverse('movies-list')
        client = get_client(admin_user)
        response = client.post(path, data=movie_content)
        path = reverse('movies-detail', kwargs={'pk': response.data['id']})
        movie_content['title'] = 'Updated movie'
        response = client.put(path, data=movie_content)
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'Updated movie'

    def test_admin_can_delete_movies(self, movies, admin_user):
        client = get_client(admin_user)
        path = reverse('movies-detail', kwargs={'pk': movies[0].id})
        response = client.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_anonymous_user_can_sort_movies_by_title(self, movies):
        path = reverse('movies-sort-title')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert obj[0]['title'] == 'First movie'
        assert obj[1]['title'] == 'Fourth movie'
        assert obj[2]['title'] == 'Second movie'
        assert obj[3]['title'] == 'Third movie'

    def test_anonymous_user_can_filter_movies_by_director(self, movies):
        path = reverse('movies-filter-director', kwargs={'director': 'A Director'})
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert len(obj) == len(movies)

    def test_user_type(self, user):
        path = reverse('movies-user-type')
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert obj['user-type'] == 'user'


@pytest.mark.django_db
class TestLikeList:

    def test_anonymous_user_cannot_add_like(self):
        path = reverse('likes-list')
        client = get_client()
        response = client.post(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_update_like(self):
        path = reverse('likes-list')
        client = get_client()
        response = client.put(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_remove_like(self):
        path = reverse('likes-list')
        client = get_client()
        response = client.delete(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_retrieve_likes(self, likes):
        path = reverse('likes-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_user_can_add_like(self, user, movies):
        path = reverse('likes-list')
        client = get_client(user)
        response = client.post(path, data={'movie': movies[0].id})
        assert response.status_code == HTTP_201_CREATED
        obj = parse_response(response)
        assert obj['movie'] == movies[0].id
        assert obj['user_id'] == user.id

    def test_user_can_update_like(self, user, likes, movies):
        client = get_client(user)
        path = reverse('likes-detail', kwargs={'pk': likes[0].id})
        response = client.put(path, data={'movie': movies[1].id})
        assert response.status_code == HTTP_200_OK
        obj = parse_response(response)
        assert obj['movie'] == movies[1].id

    def test_user_can_remove_like(self, user, likes):
        path = reverse('likes-detail', kwargs={'pk': likes[0].id})
        client = get_client(user)
        response = client.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_user_can_add_like_unique(self, user, movies):
        mixer.blend('movies.Like', id=1, user_id=user, movie=movies[0])
        path = reverse('likes-list')
        client = get_client(user)
        response = client.post(path, data={'movie': movies[0].id})
        assert response.status_code == HTTP_400_BAD_REQUEST
        obj = parse_response(response)

    def test_user_can_remove_like_by_movie(self, likes, user):
        path = reverse('likes-by-movie', kwargs={'movie': likes[0].movie.id})
        client = get_client(user)
        response = client.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT
