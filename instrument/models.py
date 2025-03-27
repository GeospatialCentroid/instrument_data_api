from django.db import models


# Create your models here.
class Instrument(models.Model):
    name = models.CharField(max_length=200)
    data_folder = models.CharField(max_length=200)
    configuration_file = models.CharField(max_length=400, blank=True, null=True)
    alias = models.CharField(max_length=200)
    start_date = models.DateTimeField("Start Data", null=True)
    end_date = models.DateTimeField("End Data", null=True)
    description = models.TextField(max_length=600, null=True)

    def __repr__(self):
        return f"Instrument(name='{self.name}', data_folder={self.data_folder}, configuration_file={self.configuration_file}, alias={self.alias}), start_date={self.start_date}. end_date={self.end_date})"


class Units(models.Model):
    name = models.CharField(max_length=100)


class InstrumentMeasurement(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    units = models.ForeignKey(Units, on_delete=models.CASCADE)
    min = models.FloatField(default=0)
    max = models.FloatField(default=0, null=True)
    description = models.TextField(max_length=600, null=True)


class MeasurementCalibration(models.Model):
    instrument_measurement = models.ForeignKey(InstrumentMeasurement, on_delete=models.CASCADE)
    slope = models.FloatField(max_length=200,default=1)
    offset = models.FloatField(max_length=200,default=0)
    start_date = models.DateTimeField("Start Data")


class InstrumentFile(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    row_count = models.IntegerField(default=0)

    status_type = (
        ('i','in progress'),
        ('c', 'complete'),
        ('e','error'),
        ('n', 'not started')
    )
    status = models.CharField(max_length=2, choices=status_type, default='n')

