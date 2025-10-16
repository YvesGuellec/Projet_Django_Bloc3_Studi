from django.contrib import admin
from .models import Profil
from django.contrib.auth.models import User

@admin.register(Profil)
class Profil(admin.ModelAdmin):
    list_display = ['id','uuid']