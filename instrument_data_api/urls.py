"""
URL configuration for instrument_data_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from instrument import views

from rest_framework import routers
from instrument.views import StationViewSet
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Serializers define the API representation.
router = routers.DefaultRouter()
router.register(r'stations', StationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path("instrument_upload", views.FileFieldFormView.as_view()),
    #
    #http://localhost:8000/measurement/5/measurements/ozone/?start=2025-04-21%2011:42:01&end=2025-04-28%2011:42:01
    re_path(r'^measurement/(?P<id>[0-9]+(,[0-9]+)*)/measurements(?:/(?P<measurements>[a-zA-Z]+(,[a-zA-Z]+)*))?/(?P<interval>[0-9]+)/$', views.get_measurements_view, name='measurements'),

    #http://localhost:8000/latest_measurement/5/hour
    re_path(r'^latest_measurement/(?P<id>[0-9]+(,[0-9]+)*)/(?P<interval>[a-zA-Z]+)/$', views.get_lastest_instrument_measurement_view,
            name='latest_measurement by id and table'),
    #http://localhost:8000/latest_measurement/5
    re_path(r'^latest_measurement/(?P<id>[0-9]+(,[0-9]+)*)?/$', views.get_lastest_instrument_measurement_view,
            name='latest_measurement by id'),
    #http://localhost:8000/latest_measurement
    path("latest_measurement", views.get_lastest_instrument_measurement_view, name='get_last_measurement'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
