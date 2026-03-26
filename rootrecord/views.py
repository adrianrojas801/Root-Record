# Create your views here.
from django.utils import timezone

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *

from .forms import *
from django.urls import reverse

#----------------------Species Views----------------------#
class SpeciesListView(ListView):
    model = Species
    template_name = "rootrecord/species_list.html"
    context_object_name = "species_list"

class SpeciesDetailView(DetailView):
    model = Species
    template_name = "rootrecord/species_detail.html"
    context_object_name = "species"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # All plants of this species
        context["plants"] = Plant.objects.filter(species=self.object)

        return context
    
#----------------------Plant Views----------------------#
class PlantListView(ListView):
    model = Plant
    template_name = "rootrecord/plant_list.html"
    context_object_name = "plants"

class PlantDetailView(DetailView):
    model = Plant
    template_name = "rootrecord/plant_detail.html"
    context_object_name = "plant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tasks"] = CareTask.objects.filter(plant=self.object)
        for task in context["tasks"]:
            task.is_overdue = (not task.completed) and (task.due < timezone.now())
        return context
    
class PlantCreateView(CreateView):
    model = Plant
    fields = ["image_file", "nickname", "location", "species"]
    template_name = "rootrecord/plant_form.html"

    def get_success_url(self):
        return reverse("plant_detail", kwargs={"pk": self.object.pk})
    
class PlantDeleteView(DeleteView):
    model = Plant
    template_name = "rootrecord/plant_delete.html"

    def get_success_url(self):
        return reverse("plant_list")
    
class PlantUpdateView(UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = 'rootrecord/plant_update.html'  

    def get_success_url(self):
        return f'/rootrecord/plants/{self.object.pk}/'


#----------------------Tasks Views----------------------#
class CareTaskDetailView(DetailView):
    model = CareTask
    template_name = "rootrecord/caretask_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task = context["task"]

        task.is_overdue = (not task.completed) and (task.due < timezone.now())

        context["logs"] = CareLog.objects.filter(care_task=task)

        return context
    
class CareTaskCreateView(CreateView):
    model = CareTask
    form_class = CareTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plant"] = Plant.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        plant = Plant.objects.get(pk=self.kwargs["pk"])
        form.instance.plant = plant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("plant_detail", kwargs={"pk": self.kwargs["pk"]})
    
class CareTaskListView(ListView):
    model = CareTask
    template_name = "rootrecord/caretask_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = super().get_queryset().select_related("plant__species")
        now = timezone.now()

        status = self.request.GET.get("status", "")

        # filter by completion
        if status == "completed":
            tasks = tasks.filter(completed=True)
        elif status == "active":
            tasks = tasks.filter(completed=False, due__gte=now)
        elif status == "overdue":
            tasks = tasks.filter(completed=False, due__lt=now)

        # separate into groups
        overdue = tasks.filter(completed=False, due__lt=now).order_by("due")
        active = tasks.filter(completed=False, due__gte=now).order_by("due")
        completed = tasks.filter(completed=True).order_by("-due")

        # combine into single list
        return list(overdue) + list(active) + list(completed)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plants"] = Plant.objects.all()
        for task in context["tasks"]:
            task.is_overdue = (not task.completed) and (task.due < timezone.now())
        return context

class CareTaskUpdateView(UpdateView):
    model = CareTask
    form_class = CareTaskForm  
    template_name = "rootrecord/caretask_update.html"

    def get_success_url(self):
        return reverse("task_detail", kwargs={"pk": self.object.pk})

class CareTaskDeleteView(DeleteView):
    model = CareTask
    template_name = "rootrecord/caretask_delete.html"

    def get_success_url(self):
        return reverse("task_list")
    

#----------------------Logs Views----------------------#
class CareLogDetailView(DetailView):
    model = CareLog
    template_name = "rootrecord/carelog_detail.html"
    context_object_name = "log"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.object.care_task
        return context

class CareLogCreateView(CreateView):
    model = CareLog
    form_class = CareLogForm
    template_name = "rootrecord/carelog_form.html"

    def form_valid(self, form):
        task = CareTask.objects.get(pk=self.kwargs["pk"])
        form.instance.care_task = task

        task.completed = True
        task.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = CareTask.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        return reverse("task_detail", kwargs={"pk": self.kwargs["pk"]})


class CareLogListView(ListView):
    model = CareLog
    template_name = "rootrecord/carelog_list.html"
    context_object_name = "logs"
    paginate_by = 50 

    def get_queryset(self):
        logs = super().get_queryset().select_related("care_task__plant__species")

        # --- FILTERS ---
        plant = self.request.GET.get("plant", "")
        task_type = self.request.GET.get("task_type", "")
        species = self.request.GET.get("species", "")

        # filter by plant
        if plant:
            logs = logs.filter(care_task__plant__id=plant)

        # filter by task
        if task_type:
            logs = logs.filter(care_task__task=task_type)

        # filter by species
        if species:
            logs = logs.filter(care_task__plant__species__id=species)

        # order by newest
        logs = logs.order_by("-timestamp")

        return logs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs = context["logs"]

        # group logs by date
        grouped = {}
        for log in logs:
            date_key = log.timestamp.date()
            grouped.setdefault(date_key, []).append(log)

        context["grouped_logs"] = grouped

        # filter menus
        context["plant_options"] = Plant.objects.all().order_by("nickname")
        context["task_type_options"] = [
            ("water", "Water"),
            ("fertilize", "Fertilize"),
            ("repot", "Repot"),
            ("prune", "Prune"),
        ]
        context["species_options"] = Species.objects.all().order_by("name")

        context["filters"] = self.request.GET.urlencode()

        return context
    
class CareLogUpdateView(UpdateView):
    model = CareLog
    form_class = CareLogForm  
    template_name = "rootrecord/carelog_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log"] = CareLog.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        return reverse("log_detail", kwargs={"pk": self.object.pk})
