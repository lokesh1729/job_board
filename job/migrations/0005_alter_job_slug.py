# Generated by Django 3.2.10 on 2022-10-08 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_update_slug_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
