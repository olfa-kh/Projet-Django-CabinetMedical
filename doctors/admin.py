from django.contrib import admin
from .models import Doctor, Schedule

# Register your models here.
admin.site.register(Doctor) # Enregistrez le modèle dans l'interface d'administration
admin.site.register(Schedule) # Enregistrez le modèle dans l'interface d'administration


