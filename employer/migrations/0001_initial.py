# Generated by Django 3.2.10 on 2022-01-31 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20220131_1615'),
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Employer Name')),
                ('industry', models.CharField(max_length=100, verbose_name='Industry')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('employee_id', models.CharField(max_length=100, verbose_name='Employee ID')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employee', to='employer.employer')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('external_url', models.URLField(blank=True, null=True, verbose_name='External URL')),
                ('job_description', models.TextField(blank=True, null=True, verbose_name='Job Description')),
                ('min_yoe_required', models.IntegerField(verbose_name='Min YOE required')),
                ('max_salary', models.BigIntegerField(verbose_name='Max Salary in USD')),
                ('location', models.CharField(max_length=255, verbose_name='Job Location')),
                ('remote', models.CharField(choices=[('FULLY_REMOTE', 'Fully Remote'), ('HYBRID', 'Hybrid'), ('NO_REMOTE', 'No Remote')], max_length=100, verbose_name='Remote?')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='employer.employer')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='employer.recruiter')),
                ('skills_required', models.ManyToManyField(to='candidate.Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
