# Generated by Django 5.0 on 2023-12-07 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1)])),
                ('description', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(1)])),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2023)])),
                ('category', models.CharField(choices=[('ROMANCE', 'Romance'), ('ACTION', 'Action'), ('ADVENTURE', 'Adventure'), ('COMEDY', 'Comedy'), ('CRIME', 'Crime'), ('DRAMA', 'Drama'), ('FANTASY', 'Fantasy'), ('HISTORICAL', 'Historical'), ('HORROR', 'Horror'), ('MYSTERY', 'Mystery'), ('PSYCHOLOGICAL', 'Psychological'), ('SCIENCE_FICTION', 'Science Fiction'), ('THRILLER', 'Thriller'), ('WESTERN', 'Western')], max_length=256, validators=[django.core.validators.MinLengthValidator(1)])),
                ('image_url', models.URLField(max_length=2000, validators=[django.core.validators.URLValidator(django.core.validators.RegexValidator(regex='https://%28www.%29/?[-a-zA-Z0-9@:%.+~#=]{1,256}.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%+.~#?&//=]*)'))])),
            ],
        ),
    ]