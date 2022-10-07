# Generated by Django 3.2.10 on 2022-09-30 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220131_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('CANDIDATE', 'candidate'), ('RECRUITER', 'recruiter'), ('ADMIN', 'admin')], max_length=50, verbose_name='Role'),
        ),
    ]