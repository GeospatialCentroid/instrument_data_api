from django.contrib import admin

# Register your models here.
from .models import Instrument, InstrumentMeasurement,Units,Station



class StationAdmin(admin.ModelAdmin):
    model = Station

admin.site.register(Station, StationAdmin)


class InstrumentMeasurementInline(admin.StackedInline):
    model = InstrumentMeasurement
    extra = 3


class InstrumentAdmin(admin.ModelAdmin):

    inlines = [InstrumentMeasurementInline]


admin.site.register(Instrument, InstrumentAdmin)

# Hide units from main admin page
class UnitsAdmin(admin.ModelAdmin):
  def has_module_permission(self, request):
    return False

admin.site.register(Units,UnitsAdmin)