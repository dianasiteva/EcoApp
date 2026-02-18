from django.contrib import admin

from participants.models import Participant


# Register your models here.

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'appended_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('appended_at',)