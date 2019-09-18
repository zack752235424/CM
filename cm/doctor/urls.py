from django.urls import path

from doctor.views import *

urlpatterns = [
    path('doctor/', doctor, name='doctor'),
    path('drug_socket/', drug_socket, name='drug_socket'),
    path('analysis_doctor/', analysis_doctor, name='analysis_doctor'),
    path('doctor_download/', doctor_download, name='doctor_download'),
]