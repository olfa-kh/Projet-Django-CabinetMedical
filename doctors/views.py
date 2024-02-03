from django.shortcuts import render
from .models import Doctor, Schedule

# Create your views here.
def doctor_schedules(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    schedules = Schedule.objects.filter(doctor=doctor)
    return render(request, 'doctors/doctor_schedules.html', {'doctor': doctor, 'schedules': schedules})