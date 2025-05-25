from django.core import validators
from django import forms
from .models import Detenu, Transfert, Dossier
from PRISON.models import Prison

class Enregistrement_Detenu(forms.ModelForm):
    class Meta:
        model = Detenu
        fields = ['nom', 'postnom', 'prenom','sexe','lieu_de_naissance', 'date_de_naissance', 'motif','prison_incarceree','cellule','matricule', 'peine', 'condamne_par', 'date_entree', 'date_sortie','dossiers', 'profil']
 
        #GESTION D'ENTREES (CHAUQE TYPE DE DONNEE DANS LEUR PLACE D'ENTRER)
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'postnom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            # 'photo_Droit': forms.FileInput(attrs={'class': 'form-control'}),
            'profil': forms.FileInput(attrs={'class': 'form-control'}),
            # 'photo_Gauche': forms.FileInput(attrs={'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'lieu_de_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'date_de_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'peine': forms.Select(attrs={'class': 'form-control'}),
            'condamne_par': forms.Select(attrs={'class': 'form-control'}),
            'prison_incarceree': forms.Select(attrs={'class': 'form-control'}),
            'date_entree': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_sortie': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cellule': forms.TextInput(attrs={'class': 'form-control'}),
            'dossiers': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        territoire_id = kwargs.pop('territoire_id', None)
        super().__init__(*args, **kwargs)
        if territoire_id:
            self.fields['prison_incarceree'].queryset = Prison.objects.filter(territoire_id=territoire_id)

class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['nouvelle_prison']

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['description', 'fichier']