from django.contrib import admin
from .models import *
# Register your models here.
# @admin.register(Pers)
# class Pers(admin.ModelAdmin):
#     list_display = ('id','nom_personne', 'postnom_personne', 'prenom_personne', 'sexe', 'identifiant')

@admin.register(Utilisateur)    
class Util(admin.ModelAdmin):
    list_display = ('id','nom_utilisateur', 'mdp', 'territoire')