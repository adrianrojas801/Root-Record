from django import forms
from .models import *

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['nickname', 'species', 'image_file', 'location']

class CareTaskForm(forms.ModelForm):
    TASK_CHOICES = [
        ('', '--- Select a task ---'),
        ('water', 'Water'),
        ('fertilize', 'Fertilize'),
        ('prune', 'Prune'),
        ('repot', 'Repot'),
    ]
    
    task = forms.ChoiceField(
        choices=TASK_CHOICES,
        widget=forms.Select(),
        required=True
    )
    
    class Meta:
        model = CareTask
        fields = ['task', 'due']
        widgets = {
            'due': forms.DateInput(attrs={'type': 'date'}),
        }


class CareLogForm(forms.ModelForm):
    class Meta:
        model = CareLog
        fields = ['notes', 'image_file', ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }