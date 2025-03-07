from django.contrib import admin

# Register your models here.
from .models import Instrument, InstrumentMeasurement,Units

class InstrumentMeasurementInline(admin.StackedInline):
    model = InstrumentMeasurement
    extra = 3


class InstrumentAdmin(admin.ModelAdmin):

    inlines = [InstrumentMeasurementInline]


admin.site.register(Instrument, InstrumentAdmin)