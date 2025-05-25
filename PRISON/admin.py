from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Agent)
class prison(admin.ModelAdmin):
    list_display=('id', 'nom_Agent', 'postnom_Agent', 'prenom_Agent', 'localite', 'instance', 'grade')

# @admin.register(Grade)
# class prison(admin.ModelAdmin):
#     list_display=('id','libelle_Grade')

@admin.register(Prison)
class prison(admin.ModelAdmin):
    list_display=('id','nom_de_la_prison', 'capacite', 'territoire', 'directeur', 'nombre_prisonniers')

@admin.register(Instance)
class prison(admin.ModelAdmin):
    list_display=('id','libelle_Instance' )

@admin.register(Territoire)
class prison(admin.ModelAdmin):
    list_display=('id','nom' )
