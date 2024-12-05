from django.contrib import admin
from .models import Situation

@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    pass
