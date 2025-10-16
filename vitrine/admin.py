from django.contrib import admin
from .models import Sport

@admin.register(Sport)
class AdminSport(admin.ModelAdmin):
    list_display = ('titre',)
