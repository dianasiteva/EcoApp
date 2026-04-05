from django.apps import AppConfig


class RolesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self):
        from events.models import Role

        DEFAULT_ROLES = [
            ("Организатор", "организира събитие - комуникира с всички включили се, следи за средствата, логистиката"),
            ("Спонсор", "осигурява средства - парични, материални, логистични"),
            ("Логистик", "организира логистика на хора, средства, събраните отпадъци"),
            ("Доброволец", "участва с труд и други"),
        ]

        for name, desc in DEFAULT_ROLES:
            Role.objects.get_or_create(name=name, defaults={"description": desc})


