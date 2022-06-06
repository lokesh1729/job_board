# Generated by Django 3.2.10 on 2022-06-01 11:35

import candidate.constants
from django.db import migrations, models

skill_data = []


def get_candidate_skill_data(apps, _schema_editor):
    candidate_skill = apps.get_model("candidate", "candidateskill")
    global skill_data
    skill_data = list(
        candidate_skill.objects.values_list("skill", "proficiency", "yoe")
    )


def migrate_data_to_skill(apps, _schema_editor):
    candidate_skill = apps.get_model("candidate", "candidateskill")
    global skill_data
    for candidate in skill_data:
        candidate[0].proficiency = candidate[1]
        candidate[0].yoe = candidate[2]


class Migration(migrations.Migration):

    dependencies = [
        ("candidate", "0003_auto_20220322_1831"),
    ]

    operations = [
        migrations.RunPython(get_candidate_skill_data),
        migrations.RemoveField(
            model_name="candidateskill",
            name="proficiency",
        ),
        migrations.RemoveField(
            model_name="candidateskill",
            name="yoe",
        ),
        migrations.AddField(
            model_name="skill",
            name="proficiency",
            field=models.IntegerField(
                choices=[
                    (1, candidate.constants.Proficiency["ONE"]),
                    (2, candidate.constants.Proficiency["TWO"]),
                    (3, candidate.constants.Proficiency["THREE"]),
                    (4, candidate.constants.Proficiency["FOUR"]),
                    (5, candidate.constants.Proficiency["FIVE"]),
                    (6, candidate.constants.Proficiency["SIX"]),
                    (7, candidate.constants.Proficiency["SEVEN"]),
                    (8, candidate.constants.Proficiency["EIGHT"]),
                    (9, candidate.constants.Proficiency["NINE"]),
                    (10, candidate.constants.Proficiency["TEN"]),
                ],
                null=True,
                verbose_name="Proficiency",
            ),
        ),
        migrations.AddField(
            model_name="skill",
            name="yoe",
            field=models.IntegerField(null=True, verbose_name="Years of Experience"),
        ),
        migrations.RunPython(migrate_data_to_skill),
    ]
