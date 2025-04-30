from django.shortcuts import render

from rest_framework import viewsets
from .models import Station
from .serializers import StationSerializer

from django.views.generic.edit import FormView
from .forms import FileFieldForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.management import call_command

from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, schema
import time
import pytz, datetime
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from psycopg2 import sql


@method_decorator(login_required, name='dispatch')
class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "instrument_upload.html"  # Replace with your template.
    success_url = "instrument_upload"  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]

        for f in files:
            print(f,"is the file")
            call_command('create_instruments', p=f,s=1)
        return super().form_valid(form)

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer



def get_lastest_instrument_measurement_view(request,id=False,interval="min"):

    table ="instrument_latest"+interval+"data"
    sql = """Select a.*,data_folder from {} a 
    inner join instrument_instrument b on b.id=a.instrument_id
    """.format(table)
    if id:
        sql+="where b.id="+id

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)
        return HttpResponse(json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')

def get_data_folder_name(id):
    sql = """Select data_folder from instrument_instrument where id={};""".format(id)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)


def get_measurements_view(request, id, measurements='', interval="60"):

    #note that this is governed by deployment approvals - without one there's no substitution
    """

    :param request:
    :param node_id:
    :param fmt:

    Also accepts get params
    interval none , 60,10,5,1 -  defaults to 60 - todo - make sure all tables have same cols, or notify user when error
    start
    end
    internal_diagnostics none or 'true' to return all the diagnostic information
    quality_level: none, 1,2,3

    :return:

    """

    # keep track of script call duration
    script_start = time.time()

    # take local time and convert to utc for the search
    #todo make timezone dynamic by allowing it as a url param
    local = pytz.timezone("America/Los_Angeles")

    start_naive = datetime.datetime.strptime(request.GET.get('start'), "%Y-%m-%d %H:%M:%S")
    start_local_dt = local.localize(start_naive, is_dst=None)
    start = start_local_dt.astimezone(pytz.utc).strftime('%Y-%m-%d  %H:%M:%S')


    end_naive = datetime.datetime.strptime(request.GET.get('end'), "%Y-%m-%d %H:%M:%S")
    end_local_dt = local.localize(end_naive, is_dst=None)
    end = end_local_dt.astimezone(pytz.utc).strftime('%Y-%m-%d  %H:%M:%S')

    data_folder= get_data_folder_name(id)[0]['data_folder']


    table = data_folder+"_avg_" + interval

    sql = """Select %s ,datetime from \"%s\"
        where datetime between '%s' and '%s'
        """% (measurements,table,start,end)


    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = dictfetchall(cursor)
        return HttpResponse(json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    # Need to inject calculation for
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def get_table(interval):
    table = 'node_file_data_avg_' + interval
    if interval == str(-1):
        table = 'node_file_data'
    return table

def export_csv(ranges,file_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)
    if len(ranges) > 0:
        writer = csv.DictWriter(response, fieldnames=ranges[0].keys())
        writer.writeheader()

        for data in ranges:
            writer.writerow(data)
    return response