from django.db import models
from PRISON.models import *

# Create your models here.
    
class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=15, unique=True)
    mdp = models.CharField(max_length=15)
    territoire = models.ForeignKey(Territoire, on_delete=models.CASCADE, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)  # Ajout

    def __str__(self):
        return f"{self.nom_utilisateur}"
