from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import ParkingType, Parking, ParkingInOut


class ParkingTypeAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]

    list_display = ("name")
    search_fields = ['name']


class ParkingAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]

    list_display = ("name", "type", "capacity", "entrancePrice", "availableSpace")
    search_fields = ['name']


class ParkingInOutAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]

    list_display = ("user", "parking", "reserveType", "state", "carNumber", "dateTime", "exited")
    search_fields = ['user', 'parking', 'carNumber', 'reserveType', 'state']

    def save_model(self, request, obj, form, change):
        result = super(ParkingInOutAdmin, self).save_model(request, obj, form, change)
        if not result:
            messages.error(request, "Problem in saving, Maybe your car is not in parking or Your car is already in parking")


admin.site.register(ParkingType)
admin.site.register(Parking, ParkingAdmin)
admin.site.register(ParkingInOut, ParkingInOutAdmin)
