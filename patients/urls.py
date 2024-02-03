from django.urls import path
from . import views
from patients.views import ListPatientView, PatientCreateView, PatientUpdateView, PatientDeleteView


urlpatterns = [
    path("", ListPatientView.as_view(), name="patient-list-view"),
    path('patient/<int:patient_id>/appointments/', views.patient_appointments, name='patient_appointments'),
    path('create-patient/',PatientCreateView.as_view(), name="create-patient"),   
    path('update-patient/<int:pk>',PatientUpdateView.as_view(), name="update-patient"),
    path('delete-patient/<int:pk>',PatientDeleteView.as_view(), name="delete-patient"),
    
]