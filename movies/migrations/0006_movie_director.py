# Generated by Django 5.0 on 2023-12-16 11:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_merge_0004_movie_image_url_0004_remove_like_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.CharField(default='Mario Rossi', max_length=50, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator("^[a-zA-Z]+(\\s[a-zA-Z]+\\'?[a-zA-Z]*)*$")]),
        ),
    ]
