from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        # groups
        moderator_group, _ = Group.objects.get_or_create(name="Модератор")
        user_group, _ = Group.objects.get_or_create(name="Потребител")

        # Нулиране на старите права
        moderator_group.permissions.clear()
        user_group.permissions.clear()

        # models
        from cities.models import Cities
        from events.models import Event
        from participants.models import Participant
        from events.models import Location
        from events.models import Role
        from participants.models import ParticipantEventRole

        MODELS = [Cities, Event, Participant, Location, Role, ParticipantEventRole]

        # view permission for all models

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
            moderator_group.permissions.add(
                view_perm,
            )

            # Потребител
            user_group.permissions.add(
                view_perm,
            )

            if model.__name__ == "Event":
                moderator_group.permissions.add(change_perm, delete_perm, add_perm,)

            if model.__name__ == "Cities":
                moderator_group.permissions.add(change_perm, delete_perm, add_perm,)
                user_group.permissions.add(add_perm,)

            if model.__name__ == "Location":
                moderator_group.permissions.add(change_perm, delete_perm, add_perm, )
                user_group.permissions.add(add_perm, change_perm, delete_perm, )

            if model.__name__ == "Participant":
                moderator_group.permissions.add(change_perm, delete_perm, add_perm, )
                user_group.permissions.add(add_perm, change_perm, delete_perm, )

            if model.__name__ == "ParticipantEventRole":
                moderator_group.permissions.add(change_perm, delete_perm, add_perm, )
                user_group.permissions.add(add_perm, change_perm, delete_perm, )
