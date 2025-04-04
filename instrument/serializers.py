from rest_framework import serializers
from .models import Instrument, InstrumentMeasurement


class InstrumentMeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstrumentMeasurement

        fields = ('id', 'name','alias','units','min','max','description')

class InstrumentSerializer(serializers.ModelSerializer):
    measurements = InstrumentMeasurementSerializer(many=True)

    class Meta:
        model = Instrument
        fields = ('id', 'name','start_date','end_date','description', 'measurements')