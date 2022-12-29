# Generated by Django 3.2.10 on 2022-12-29 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schools', related_query_name='school', to='cities_light.country'),
        ),
    ]