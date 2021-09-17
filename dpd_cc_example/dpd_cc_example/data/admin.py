from django.contrib import admin
from .models import Team, PlayerResults


@admin.register(PlayerResults)
class PlayerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "name",
            "team",
            "value",
            "total_points",
        )}),
    )
    list_display = ["name", "team", "value", "gw", "total_points"]
    search_fields = ["name", "team", "gw"]
    ordering = ('gw', 'name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "code",
            "draw",
            "form",
            "id",
            "loss",
            "name",
            "played",
            "points",
            "position",
            "pulse_id",
            "short_name",
        )}),
    )
    list_display = ["name", "id", "code", "points"]
    search_fields = ["name", "id"]
    ordering = ('name',)
