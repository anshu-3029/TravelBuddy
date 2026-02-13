from django.contrib import admin
from .models import Package, Booking


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'package', 'travel_date', 'persons', 'booked_at')
