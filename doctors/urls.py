from django.urls import path
from . import views

urlpatterns = [
    path('doctor/<int:doctor_id>/schedules/', views.doctor_schedules, name='doctor_schedules'),
  
]