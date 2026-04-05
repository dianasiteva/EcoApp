from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from cities.models import Cities
from events.models import Event, Location, Role
from participants.models import Participant, ParticipantEventRole


User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        group, _ = Group.objects.get_or_create(name="Потребител")
        instance.groups.add(group)




@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # Създаване на групи
    moderator_group, _ = Group.objects.get_or_create(name="Модератор")
    user_group, _ = Group.objects.get_or_create(name="Потребител")

    # Нулиране на старите права
    moderator_group.permissions.clear()
    user_group.permissions.clear()

    MODELS = [Cities, Event, Participant, Location, Role, ParticipantEventRole]

    # custom permission
    try:
        edit_report_perm = Permission.objects.get(codename="edit_report")
    except Permission.DoesNotExist:
        edit_report_perm = None

    for model in MODELS:
        ct = ContentType.objects.get_for_model(model)

        view_perm = Permission.objects.get(
            codename=f"view_{model._meta.model_name}",
            content_type=ct
        )
        add_perm = Permission.objects.get(
            codename=f"add_{model._meta.model_name}",
            content_type=ct
        )
        change_perm = Permission.objects.get(
            codename=f"change_{model._meta.model_name}",
            content_type=ct
        )
        delete_perm = Permission.objects.get(
            codename=f"delete_{model._meta.model_name}",
            content_type=ct
        )

        # Модератор
        moderator_group.permissions.add(view_perm)

        # Потребител
        user_group.permissions.add(view_perm)

        if model.__name__ == "Event":
            moderator_group.permissions.add(change_perm, delete_perm, add_perm)
            if edit_report_perm:
                moderator_group.permissions.add(edit_report_perm)

        if model.__name__ == "Cities":
            moderator_group.permissions.add(change_perm, delete_perm, add_perm)
            user_group.permissions.add(add_perm)

        if model.__name__ == "Location":
            moderator_group.permissions.add(change_perm, delete_perm, add_perm)
            user_group.permissions.add(add_perm, change_perm, delete_perm)

        if model.__name__ == "Participant":
            moderator_group.permissions.add(change_perm, delete_perm, add_perm)
            user_group.permissions.add(add_perm, change_perm, delete_perm)

        if model.__name__ == "ParticipantEventRole":
            moderator_group.permissions.add(change_perm, delete_perm, add_perm)
            user_group.permissions.add(add_perm, change_perm, delete_perm)
