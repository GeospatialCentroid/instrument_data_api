from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    description = models.TextField(max_length=600, null=True)

    def __str__(self):
        return self.name

class Instrument(models.Model):
    name = models.CharField(max_length=200, unique=True)
    data_folder = models.CharField(max_length=200)
    configuration_file = models.CharField(max_length=400, blank=True, null=True)
    alias = models.CharField(max_length=200, null=True)
    start_date = models.DateTimeField("Start Data", null=True, blank=True)
    end_date = models.DateTimeField("End Data", null=True, blank=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="instruments", null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Instrument(name='{self.name}', data_folder={self.data_folder}, configuration_file={self.configuration_file}, alias={self.alias}), start_date={self.start_date}. end_date={self.end_date})"


class Units(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name


class Measurement(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name="measurements")
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, null=True, blank=True)
    units = models.ForeignKey(Units, on_delete=models.CASCADE, null=True, blank=True)
    min = models.FloatField( null=True, blank=True)
    max = models.FloatField( null=True, blank=True)
    description = models.TextField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name


class Calibration(models.Model):
    instrument_measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    slope = models.FloatField(max_length=200,default=1)
    offset = models.FloatField(max_length=200,default=0)
    start_date = models.DateTimeField("Start Date")



class File(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500, null=True)


    start_time = models.DateTimeField("Start Date", null=True)
    end_time = models.DateTimeField("End Date", null=True)
    row_count = models.IntegerField(default=0, null=True)
    error_num = models.IntegerField(default=0, null=True)
    manual_load=models.BooleanField(default=False, null=True)
    synced = models.BooleanField(default=False, null=True)

class LatestMinData(models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE,primary_key=True)
    datetime = models.DateTimeField("DateTime", null=True)
    data = models.JSONField()

class LatestHourData(models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE,primary_key=True)
    datetime = models.DateTimeField("DateTime", null=True)
    data = models.JSONField()



