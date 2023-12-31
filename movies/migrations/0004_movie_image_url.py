# Generated by Django 5.0 on 2023-12-12 09:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image_url',
            field=models.CharField(default=2020, max_length=200, validators=[django.core.validators.RegexValidator('https://image\\.tmdb\\.org/t/p/w500/[a-zA-Z\\d]{27}\\.jpg')]),
            preserve_default=False,
        ),
    ]
