# Generated by Django 5.0 on 2023-12-16 11:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movie_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator("^[a-zA-Z]+(\\s[a-zA-Z]+\\'?[a-zA-Z]*)*$")]),
        ),
    ]
