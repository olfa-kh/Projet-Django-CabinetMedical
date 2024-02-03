from django.urls import path
from . import views
from appointments.views import AppointmentDeleteView,AppointmentUpdateView

urlpatterns = [
   
    # path('patient/<int:patient_id>/add_appointment/', views.add_appointment, name='add_appointment'),
    path('add/', views.AppointmentCreateView.as_view(), name='add_appointment'),
    path('', views.appointments_home, name='appointments_home'),
    path('list/', views.list_appointments, name='list_appointments'),
    path('<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('search/', views.search_appointments, name='search_appointments'),
    path('update/<int:pk>/',AppointmentUpdateView.as_view(), name="update-appointment"),
    path('delete/<int:pk>/',AppointmentDeleteView.as_view(), name="delete-appointment"),
]

 