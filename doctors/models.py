from django.db import models

# Create your models here.
class Doctor(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
  



class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule')
    dayOfWeek = models.IntegerField()
    startTime = models.TimeField()
    endTime = models.TimeField()
  
    def __str__(self):
        return f"Schedule for Dr. {self.doctor}"
