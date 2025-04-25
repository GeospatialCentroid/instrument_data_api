from rest_framework import serializers
from .models import Station, Instrument, Measurement


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement

        fields = ('id', 'name','alias','units','min','max','description')

class InstrumentSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Instrument
        fields = ('id', 'name','start_date','end_date','description', 'measurements')

class StationSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = Instrument.objects.filter(station_id=obj)
        serializer = InstrumentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Station

        fields = ('id', 'name','description','lat','lng','children')