# Generated by Django 3.2.10 on 2023-02-05 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('job', '0003_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='cities_light.city'),
        ),
    ]