from django.conf import settings
from django.db import migrations


def create_profiles(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Profile = apps.get_model("users", "Profile")

    for user in User.objects.all():
        role = "admin" if user.is_superuser else "user"
        Profile.objects.get_or_create(user=user, defaults={"role": role})


def delete_profiles(apps, schema_editor):
    Profile = apps.get_model("users", "Profile")
    Profile.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_profiles, delete_profiles),
    ]