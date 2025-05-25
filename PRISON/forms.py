from django.core import validators
from django import forms
from .models import *

class Enregistrement_Prison(forms.ModelForm):
    class Meta:
        model = Prison
        fields = ['nom_de_la_prison', 'capacite', 'territoire', 'directeur']

        #GESTION D'ENTREES (CHAUQE TYPE DE DONNEE DANS LEUR PLACE D'ENTRER) ET METTRE UN STYLE CSS PARTICULIER
        widgets = {
        'nom_de_la_prison': forms.TextInput(attrs={'class': 'form-control'}),
        'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
        'territoire' : forms.Select(attrs={'class': 'form-control'}),      
        'directeur': forms.TextInput(attrs={'class': 'form-control'}),
        'nom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
        'postnom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
        'prenom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
        'libelle_Grade' : forms.Select(attrs={'class': 'form-control'}),
            }
       

class Enregistement_Agent(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['id', 'nom_Agent', 'postnom_Agent', 'prenom_Agent', 'localite', 'instance', 'grade']

        widgets = {
            'nom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
            'postnom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom_Agent': forms.TextInput(attrs={'class': 'form-control'}),
            'localite': forms.Select(attrs={'class': 'form-control'}),
            'instance': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            }
    
# class Enregistement_Grade(forms.ModelForm):
#     class Meta:
#         model = Grade
#         fields = ['id','libelle_Grade']

#         widgets = {
#             'libelle_Grade' : forms.Select(attrs={'class': 'form-control'}),
#             }

class Enregistement_Instance(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['id','libelle_Instance'] 

