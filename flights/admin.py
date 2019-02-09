from django.contrib import admin

from .models import Airport, Flight, Passenger

# .through - refers to intermediary table
class PassengerInline(admin.StackedInline):
  model = Passenger.flights.through # pylint: disable=no-member
  extra = 1

class FlightAdmin(admin.ModelAdmin):
  inlines = [PassengerInline]

class PassengerAdmin(admin.ModelAdmin):
  filter_horizontal = ('flights',)

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)