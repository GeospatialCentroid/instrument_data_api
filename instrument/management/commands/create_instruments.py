from django.core.management.base import BaseCommand, CommandError
from instrument.models import Instrument,Measurement,Station
import yaml

class Command(BaseCommand):
    help = "Add an instrument. Call python manage.py create_instruments -s 1 -p /Users/kevin/projects/instrument_data_api/sample_data/thermo_42itl.yml"

    def add_arguments(self, parser):
        parser.add_argument("-p", type=str)
        parser.add_argument("-s", type=str)

    def handle(self, *args, **options):
        instrument_file = options['p']
        instrument_station = options['s']
        station = Station.objects.get(id=instrument_station)

        try:
            f = open(instrument_file, 'r')
        except Exception as e:
            f = instrument_file.read()


        yaml_data = yaml.safe_load(f)
        try:
            instrument = Instrument(
                name=yaml_data.get('instrument_name'),
                data_folder=yaml_data.get('instrument_folder'),
                configuration_file=instrument_file,
                station=station,
                #instrument.alias = yaml_data['instrument_name'],
                #instrument.start_date = yaml_data['instrument_name'],
                #instrument.end_date = yaml_data['instrument_name'],
            )
            instrument.save()
            print(repr(instrument))
            ## create the measures
            cols=yaml_data.get('header').split(",")
            exclude=['time','date','utc_datetime']
            for c in cols:
                if c not in exclude:
                    im = Measurement(
                        instrument=instrument,
                        name=c,
                    )
                    im.save()
        except Exception as e:
            print("***error", e)
