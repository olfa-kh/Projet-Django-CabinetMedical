from django.db import models
from django.urls import reverse

# Create your models here.

class Patient(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    birth_date= models.DateTimeField()
    contact_info = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    adress = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
   
    


class MedicalRecord(models.Model):
    Patient =  models.ForeignKey(Patient, on_delete=models.CASCADE,related_name='medicalRecords')  
    history = models.TextField()
    allergies = models.TextField()
    current_medications = models.TextField()
    symptoms = models.TextField()
    def __str__(self):
        return f"Medical record for {self.Patient}"
