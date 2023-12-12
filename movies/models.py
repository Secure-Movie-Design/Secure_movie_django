from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, RegexValidator, \
    MinLengthValidator
from django.db import models
from datetime import datetime


class MovieCategory(models.TextChoices):
    ROMANCE = "ROMANCE",
    ACTION = "ACTION",
    ADVENTURE = "ADVENTURE",
    COMEDY = "COMEDY"
    CRIME = "CRIME"
    DRAMA = "DRAMA"
    FANTASY = "FANTASY"
    HISTORICAL = "HISTORICAL"
    HORROR = "HORROR"
    MYSTERY = "MYSTERY"
    PSYCHOLOGICAL = "PSYCHOLOGICAL"
    SCIENCE_FICTION = "SCIENCE_FICTION"
    THRILLER = "THRILLER"
    WESTERN = "WESTERN"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Movie(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
    )
    title = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        null=False,
    )
    description = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1)],
        null=False,
    )
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        null=False,
    )
    category = models.CharField(
        max_length=256,
        validators=[MinLengthValidator(1)],
        null=False,
        choices=MovieCategory.choices,
    )
    '''image_url = models.URLField(
        max_length=2000,
        validators=[URLValidator(RegexValidator(regex=r'https://%28www.%29/?[-a-zA-Z0-9@:%.+~#=]{1,256}.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%+.~#?&//=]*)'))],
        null=False,
    )'''

    def __str__(self):
        return f'Title: {self.title}, Description: {self.description}, Year: {self.year}, Category: {self.category}'


class Like(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        null=False,
    )
    user_id = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Movie: {self.movie.title}, User: {self.user_id}'

    class Meta:
        unique_together = ('movie', 'user_id',)
