from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Patient, MedicalRecord
from appointments.models import Appointment
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# , UpdateView, DeleteView

# Create your views here.
def patient_appointments(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    appointments = Appointment.confirmed_appointments.filter(patient=patient)
    return render(request, 'patients/liste.html', context={'patient': patient, 'appointments': appointments})

class ListPatientView(ListView):
    model = Patient
    paginate_by = 100
    queryset = Patient.objects.filter(appointment_set__status='Confirmé')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class PatientCreateView(CreateView):
    model = Patient
    fields = ["firstName","lastName","birth_date","contact_info","phone","email","adress"]    
    success_url = reverse_lazy("patient-list-view") 
    template_name = "patients/form.html"

class PatientUpdateView(UpdateView):
    model = Patient
    fields = ["firstName","lastName","birth_date","contact_info","phone","email","adress"]
    template_name="patients/form.htmlvenv" 
    success_url = reverse_lazy("patient-list-view") 

class PatientDeleteView(DeleteView):
    model = Patient
    template_name_suffix ="_delete_form"
    success_url = reverse_lazy("patient-list-view")

def HomeView(request):
    if request.user.is_authenticated:
      return render(request,'patients/index.html', )
    else:
        return redirect (reverse_lazy("login"))
 
