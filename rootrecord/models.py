# File: rootrecord/models.py
# Author: Adrian Rojas (rojasa@bu.edu), 11/20/2025
# Description: File that defines the models for the 'rootrecord' app.

from django.db import models

# Create your models here.
class Species(models.Model):
    name = models.TextField(blank=True)
    common_name = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    water_interval = models.IntegerField()
    light_req = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Plant(models.Model):
    image_file = models.ImageField(blank=True)
    nickname = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.TextField(blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
    
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return None
    
class CareTask(models.Model):

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    due = models.DateTimeField()
    completed = models.BooleanField(default=False)
    task = models.TextField(blank=True)

    def __str__(self):
        return self.task

class CareLog(models.Model):
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    care_task = models.ForeignKey(CareTask, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f"Log for {self.care_task}"