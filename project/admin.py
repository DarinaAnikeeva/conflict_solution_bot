from django.contrib import admin
from .models import Situation, Advice, Feedback

@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    pass

@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
