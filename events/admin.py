# Register your models here.
from django.contrib import admin

from .models import Event, Location, Role


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'location', 'created_at')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ('name', 'address')
    ordering = ('name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    ordering = ('name',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
