from django.contrib import admin
from django.utils.html import format_html
from .models import Participant
from django import forms
from .widgets import AdminImagePreviewWidget


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            "profile_picture": AdminImagePreviewWidget,
        }



@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    form = ParticipantForm

    list_display = (
        "first_name",
        "last_name",
        "contact_email",
        "city",
        "car_registration_number",
        "phone",
        "appended_at",
        "profile_picture"
    )

    list_filter = ("city", "appended_at")

    search_fields = (
        "first_name",
        "last_name",
        "contact_email",
        "car_registration_number",
        "phone",
    )


    ordering = ("-appended_at",)
    readonly_fields = ("appended_at", "profile_picture")

    def profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.profile_picture.url
            )
        return "—"

    profile_picture.short_description = "Снимка"

