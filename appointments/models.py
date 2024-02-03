from django.db import models
from doctors.models import Doctor
from patients.models import Patient

# créer un gestionnaire personnalisé pour filtrer les rendez-vous ayant un statut "Confirmé"
class ConfirmedAppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Confirmé')
    
class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRME = 'Confirmé'
        ANNULE = 'Annulé'
        EN_ATTENTE = 'En attente'
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'appointment_set')
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EN_ATTENTE)

    def __str__(self):
            return f"Appointment for {self.patient} with Dr. {self.doctor}"
    objects = models.Manager()  # Le gestionnaire par défaut
    confirmed_appointments = ConfirmedAppointmentManager()  # Gestionnaire personnalisé pour les rendez-vous confirmés


# Modèle d'Appointment : stocke les rendez-vous associant un médecin et un patient avec leur date, raison et statut.
# doctor: clé étrangère reliant l'Appointment à un Doctor.
# patient: clé étrangère reliant l'Appointment à un Patient.
# date: date et heure du rendez-vous.
# reason: motif du rendez-vous.
# status: statut du rendez-vous (ex: confirmé, annulé, en attente).