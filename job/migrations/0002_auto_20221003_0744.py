# Generated by Django 3.2.10 on 2022-10-03 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0001_initial'),
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(help_text='The details of the company such as about, size, industry etc... will be populated on the job page. If no company is shown, create a new company from the dashboard', on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='recruiter.company'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_description',
            field=models.TextField(default='NA', verbose_name='Job Description'),
            preserve_default=False,
        ),
    ]
