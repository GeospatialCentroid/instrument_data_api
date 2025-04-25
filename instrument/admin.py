from django.contrib import admin
from django.core.management import call_command
from django.contrib import messages

from .models import Instrument, Measurement,Units,Station



class StationAdmin(admin.ModelAdmin):
    model = Station

admin.site.register(Station, StationAdmin)


class MeasurementInline(admin.StackedInline):
    model = Measurement
    extra = 0



class InstrumentAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


admin.site.register(Instrument, InstrumentAdmin)

# Hide units from main admin page
class UnitsAdmin(admin.ModelAdmin):
  def has_module_permission(self, request):
    return False

admin.site.register(Units,UnitsAdmin)




