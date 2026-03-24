from django.contrib import admin
from participants.models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'appended_at')
    list_select_related = ('user',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone')
    list_filter = ('appended_at',)


    @admin.display(ordering='user__first_name', description='First name')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering='user__last_name', description='Last name')
    def last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering='user__email', description='Email')
    def email(self, obj):
        return obj.user.email

    readonly_fields = ('appended_at',)