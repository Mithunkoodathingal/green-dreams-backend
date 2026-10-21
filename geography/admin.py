
from django.contrib import admin

from .models import Panchayath, Ward


class WardInline(admin.TabularInline):
    model = Ward
    extra = 1
    fields = ("number", "location_name", "is_active")


@admin.register(Panchayath)
class PanchayathAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "district", "is_active")
    search_fields = ("name", "code", "district")
    list_filter = ("is_active", "district")
    prepopulated_fields = {"code": ("name",)}
    inlines = [WardInline]


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "location_name",
        "panchayath",
        "is_active",
    )
    search_fields = (
        "location_name",
        "panchayath__name",
    )
    list_filter = ("panchayath", "is_active")
