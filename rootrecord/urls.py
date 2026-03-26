# File: rootrecord/urls.py
# Author: Adrian Rojas (rojasa@bu.edu), 11/20/2025
# Description: File that defines URL patterns for the 'rootrecord' app.

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", SpeciesListView.as_view(), name="species_list"),
    path("species/", SpeciesListView.as_view(), name="species_list"),
    path("species/<int:pk>/", SpeciesDetailView.as_view(), name="species_detail"),

    path("plants/", PlantListView.as_view(), name="plant_list"),
    path("plants/<int:pk>/", PlantDetailView.as_view(), name="plant_detail"),
    path("plants/create/", PlantCreateView.as_view(), name="plant_create"),
    path("plants/<int:pk>/update/", PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:pk>/delete/", PlantDeleteView.as_view(), name="plant_delete"),

    path("tasks/", CareTaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", CareTaskDetailView.as_view(), name="task_detail"),
    path("plants/<int:pk>/tasks/create/", CareTaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", CareTaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", CareTaskUpdateView.as_view(), name="task_update"),

    path("logs/", CareLogListView.as_view(), name="log_list"),
    path("logs/<int:pk>/", CareLogDetailView.as_view(), name="log_detail"),
    path("tasks/<int:pk>/logs/create/", CareLogCreateView.as_view(), name="log_create"),
    path("logs/<int:pk>/update/", CareLogUpdateView.as_view(), name="log_update"),

]
