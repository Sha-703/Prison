from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Detenu)
class Enregistrement_Detenu(admin.ModelAdmin):
    list_display = ('id', 'nom', 'postnom', 'prenom', 'sexe', 'lieu_de_naissance', 'date_de_naissance', 'motif', 'prison_incarceree', 'cellule', 'matricule', 'peine', 'condamne_par', 'date_entree', 'date_sortie', 'profil')