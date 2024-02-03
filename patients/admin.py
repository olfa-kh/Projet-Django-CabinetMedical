from django.contrib import admin
from .models import Patient, MedicalRecord

# Register your models here.

admin.site.register(Patient)# Enregistrez le modèle dans l'interface d'administration
admin.site.register(MedicalRecord)