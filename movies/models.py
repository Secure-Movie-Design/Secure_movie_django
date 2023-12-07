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
        print(tuple((i.name, i.value) for i in cls))
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

    def str(self):
        return self.title
