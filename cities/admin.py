from django.contrib import admin
from participants.models import Cities

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    search_fields = ('name',)
    list_filter = ('district',)
