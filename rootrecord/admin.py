# File: rootrecord/admin.py
# Author: Adrian Rojas (rojasa@bu.edu), 11/25/2025
# Description: File that registers my models.

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Plant)
admin.site.register(Species)
admin.site.register(CareLog)
admin.site.register(CareTask)