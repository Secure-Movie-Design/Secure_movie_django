import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer

from movies.models import MovieCategory
from datetime import datetime


@pytest.fixture()
def movie(db):
    yield mixer.blend('movies.Movie', title='A title', description='A description', year=2022,
                      category=MovieCategory.ACTION)


@pytest.mark.parametrize('title', [
    'A' * 51,
    ''
])
def test_invalid_title_raises_exception(db, title):
    movie = mixer.blend('movies.Movie', title=title)
    with pytest.raises(ValidationError):
        movie.full_clean()


def test_null_title_raises_exception(db):
    with pytest.raises(IntegrityError):
        mixer.blend('movies.Movie', title=None)


@pytest.mark.parametrize('description', [
    'A' * 201,
    ''
])
def test_description_of_length_201_raises_exception(db, description):
    movie = mixer.blend('movies.Movie', description=description)
    with pytest.raises(ValidationError):
        movie.full_clean()


def test_null_description_raises_exception(db):
    with pytest.raises(IntegrityError):
        mixer.blend('movies.Movie', description=None)


def test_year_prior_to_1900_raises_exception(db):
    movie = mixer.blend('movies.Movie', year=1899)
    with pytest.raises(ValidationError):
        movie.full_clean()


def test_year_after_current_year_raises_exception(db):
    next_year = datetime.now().year + 1
    movie = mixer.blend('movies.Movie', year=next_year)
    with pytest.raises(ValidationError):
        movie.full_clean()


def test_null_year_raises_exception(db):
    with pytest.raises(IntegrityError):
        mixer.blend('movies.Movie', year=None)


@pytest.mark.parametrize('category', [
    'A' * 257,
    '',
    'NONEXISTENT'
])
def test_invalid_category_raises_exception(db, category):
    movie = mixer.blend('movies.Movie', category='A' * 257)
    with pytest.raises(ValidationError):
        movie.full_clean()


def test_null_category_raises_exception(db):
    with pytest.raises(IntegrityError):
        mixer.blend('movies.Movie', category=None)


def test_valid_movie_does_not_raise_exception(db):
    movie = mixer.blend('movies.Movie', title='A title', description='A description', year=2022,
                        category=MovieCategory.ACTION)
    movie.full_clean()


def test_valid_like_does_not_raise_exception(db, movie):
    like = mixer.blend('movies.Like', movie=movie)
    like.full_clean()


def test_movie_to_string_returns_title(db):
    movie = mixer.blend('movies.Movie', title='A title')
    assert str(
        movie) == f'Title: {movie.title}, Description: {movie.description}, Year: {movie.year}, Category: {movie.category}'


def test_null_movie_id_raises_exception(db):
    with pytest.raises(IntegrityError):
        mixer.blend('movies.Like', movie_id=None)


def test_invalid_movie_id_raises_exception(db):
    with pytest.raises(ValueError):
        mixer.blend('movies.Like', movie_id='a')


def test_like_to_string_returns_movie_title(db, movie):
    like = mixer.blend('movies.Like', movie=movie)
    assert str(like) == f'Movie: {movie.title}, User: {like.user_id}'
