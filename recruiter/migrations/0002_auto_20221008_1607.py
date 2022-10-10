# Generated by Django 3.2.10 on 2022-10-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruiter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="logo",
            field=models.ImageField(
                default="company_logo.png",
                help_text="Logo of the company",
                upload_to="",
                verbose_name="Logo of the company",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="company",
            name="url",
            field=models.URLField(
                null=True,
                help_text="URL of the company website",
                verbose_name="Website URL",
            ),
            preserve_default=False,
        ),
    ]
