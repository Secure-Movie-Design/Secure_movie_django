import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mixer.backend.django import mixer

from movies.models import MovieCategory
from datetime import datetime


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
