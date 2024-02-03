from django.contrib import admin
from .models import Appointment # Importez le modèle que vous souhaitez enregistrer


# Register your models here.
admin.site.register(Appointment)  # Enregistrez le modèle dans l'interface d'administration

