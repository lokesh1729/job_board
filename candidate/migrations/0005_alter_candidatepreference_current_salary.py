# Generated by Django 3.2.10 on 2023-01-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0004_alter_candidatepreference_profile_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatepreference',
            name='current_salary',
            field=models.IntegerField(help_text="We won't tell this to anyone.", verbose_name='Current Salary'),
        ),
    ]
