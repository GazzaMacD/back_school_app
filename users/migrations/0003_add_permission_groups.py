from django.db import migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create(
        [
            Group(name="Students"),
            Group(name="Admins"),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_customuser_full_en_name_and_more"),
    ]

    operations = [migrations.RunPython(apply_migration)]
