from django.shortcuts import render

from rest_framework import viewsets
from .models import Station
from .serializers import StationSerializer

from django.views.generic.edit import FormView
from .forms import FileFieldForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.management import call_command

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


