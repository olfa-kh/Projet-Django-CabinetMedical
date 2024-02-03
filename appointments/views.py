from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor, Schedule
from .forms import AppointmentForm
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView,DeleteView


def appointment_details(request, appointment_id):
    # Logique pour afficher les détails d'un rendez-vous spécifique
    return HttpResponse(f"Détails du rendez-vous avec l'ID {appointment_id}")
def delete_appointment(request, appointment_id):
    # Logique de suppression du rendez-vous avec l'ID appointment_id
    return HttpResponse(f"Suppression du rendez-vous avec l'ID {appointment_id}")

def list_appointments(request):
    # Logique pour récupérer et afficher la liste des rendez-vous
    return HttpResponse("Liste des rendez-vous")

class AppointmentCreateView(CreateView):
    model = Appointment
    fields = "__all__"    #envoyer tout les champ de model appointements 
    success_url = reverse_lazy("patient-list-view") 
    template_name = "patients/form.html"

class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ["doctor","patient","date","reason","status"]
    template_name="patients/form.html" 
    success_url = reverse_lazy("patient-list-view") 

class AppointmentDeleteView(DeleteView):    
    model= Appointment
    template_name_suffix ="_delete_form"
    success_url = reverse_lazy("patient-list-view")

def add_appointment(request, patient_id):
    if request.method == 'POST':
        doctor_id = 1  # Remplacez 1 par l'ID de votre médecin
        date = request.POST.get('date')
        reason = request.POST.get('reason')
        status = request.POST.get('status')
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)

        if not all([date, reason, status]):
            messages.error(request, 'Veuillez remplir tous les champs.' )
            return HttpResponseRedirect(request.path_info)
        
        appointment = Appointment(doctor=doctor, patient=patient, date=date, reason=reason, status=status)
        appointment.save()
        
        messages.success(request, 'Rendez-vous ajouté avec succès !')
        
        return redirect('patient_appointments', patient_id=patient_id)
    else:
        return render(request, 'appointments/add_appointment.html', {'patient_id': patient_id})
    
# Vue pour ajouter un rendez-vous : récupère les données postées pour créer un nouvel Appointment liant un patient et un médecin.
# Si la méthode HTTP est POST, les données sont extraites du formulaire pour créer un nouvel Appointment.
# Sinon, renvoie la page d'ajout de rendez-vous avec la liste des médecins.

def appointments_home(request):
    # Récupérer les rendez-vous à afficher sur la page d'accueil des rendez-vous
    appointments = Appointment.objects.all()  # Remplacez cela par votre logique de récupération des rendez-vous
    return render(request, 'appointments/appointments_home.html', {'appointments': appointments})    


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments_home')  # Rediriger vers la liste des rendez-vous
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/edit_appointment.html', {'form': form})
 
#Ajouter des fonctionnalités de recherche et de filtrage des rendez-vous
def search_appointments(request):
    if request.method == 'GET':
        search_query = request.GET.get('q')
        appointments = Appointment.objects.filter(
            Q(patient__first_name__icontains=search_query) | 
            Q(patient__last_name__icontains=search_query) | 
            Q(reason__icontains=search_query) |
            Q(status__icontains=search_query)
        )
        return render(request, 'appointments/search.html', {'appointments': appointments})
    return render(request, 'appointments/search.html', {})

def find_available_slots(doctor, date):
    # Récupérer les plannings du médecin pour le jour spécifié
    schedules = Schedule.objects.filter(doctor=doctor, dayOfWeek=date.weekday())
    
    # Récupérer tous les rendez-vous existants pour ce médecin à cette date
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        date__year=date.year,
        date__month=date.month,
        date__day=date.day
    )
    
    # Logique pour trouver les créneaux disponibles en soustrayant les rendez-vous existants des plannings
    available_slots = []
    for schedule in schedules:
        slot_start = timezone.datetime.combine(date, schedule.startTime)
        slot_end = timezone.datetime.combine(date, schedule.endTime)
        slot_taken = False
        
        for appointment in existing_appointments:
            # Vérifier si le rendez-vous existant chevauche le créneau horaire
            if appointment.date >= slot_start and appointment.date < slot_end:
                slot_taken = True
                break
        
        if not slot_taken:
            available_slots.append((slot_start, slot_end))
    
    return available_slots

# Gestion de la disponibilité des médecins
def doctor_availability(request):
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')
        date_string = request.GET.get('date')
        date = timezone.datetime.strptime(date_string, '%Y-%m-%d').date()
        
        doctor = Doctor.objects.get(pk=doctor_id)
        
        schedules = Schedule.objects.filter(doctor_id=doctor_id, dayOfWeek=date.weekday())
        existing_appointments = Appointment.objects.filter(doctor=doctor, date__date=date)
        
        available_slots = []
        for schedule in schedules:
            slot_start = timezone.datetime.combine(date, schedule.startTime)
            slot_end = timezone.datetime.combine(date, schedule.endTime)
            slot_taken = False
            
            for appointment in existing_appointments:
                if appointment.date >= slot_start and appointment.date < slot_end:
                    slot_taken = True
                    break
            
            if not slot_taken:
                available_slots.append((slot_start, slot_end))
        
        return render(request, 'appointments/doctor_availability.html', {
            'doctor': doctor,
            'date': date,
            'available_slots': available_slots
        })
    return render(request, 'appointments/doctor_availability.html', {})
