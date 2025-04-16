from django.core.management.base import BaseCommand, CommandError
from instrument.models import Instrument,InstrumentMeasurement
import yaml

class Command(BaseCommand):
    help = "Add an instrument"

    def add_arguments(self, parser):
        parser.add_argument("-p", nargs="+", type=str)

    def handle(self, *args, **options):
        instrument_path = options['p'][0]
        with open(instrument_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
            instrument = Instrument(
                name=yaml_data.get('instrument_name'),
                data_folder=yaml_data.get('data_folder'),
                configuration_file=instrument_path,
                #instrument.alias = yaml_data['instrument_name'],
                #instrument.start_date = yaml_data['instrument_name'],
                #instrument.end_date = yaml_data['instrument_name'],
            )
            instrument.save()
            print(repr(instrument))
            ## create the measures
            cols=yaml_data.get('header').split(",")
            print(cols)
            for c in cols:
                im = InstrumentMeasurement(
                    instrument=instrument,
                    name=c,
                )
                im.save()

