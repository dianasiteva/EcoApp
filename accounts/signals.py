from django.db.models.signals import post_save, post_migrate
from django.contrib.auth import get_user_model
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

        # Опитваме да вземем permissions безопасно
        perms = {}
        for action in ["view", "add", "change", "delete"]:
            codename = f"{action}_{model._meta.model_name}"
            try:
                perms[action] = Permission.objects.get(codename=codename, content_type=ct)
            except Permission.DoesNotExist:
                # Permissions още не са създадени → пропускаме този модел
                return

        # Права за всички
        moderator_group.permissions.add(perms["view"])
        user_group.permissions.add(perms["view"])

        # Специални правила
        name = model.__name__

        if name == "Event":
            moderator_group.permissions.add(perms["add"], perms["change"], perms["delete"])
            if edit_report_perm:
                moderator_group.permissions.add(edit_report_perm)

        if name == "Cities":
            moderator_group.permissions.add(perms["add"], perms["change"], perms["delete"])
            user_group.permissions.add(perms["add"])

        if name == "Location":
            moderator_group.permissions.add(perms["add"], perms["change"], perms["delete"])
            user_group.permissions.add(perms["add"], perms["change"], perms["delete"])

        if name == "Participant":
            moderator_group.permissions.add(perms["add"], perms["change"], perms["delete"])
            user_group.permissions.add(perms["add"], perms["change"], perms["delete"])

        if name == "ParticipantEventRole":
            moderator_group.permissions.add(perms["add"], perms["change"], perms["delete"])
            user_group.permissions.add(perms["add"], perms["change"], perms["delete"])
