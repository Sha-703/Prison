from django.db import models
from PRISON.models import Agent, Prison  # Importer uniquement les modèles nécessaires
from datetime import date, timedelta

class Dossier(models.Model):
    fichier = models.FileField(upload_to='dossier_detenu')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or str(self.fichier)

class Detenu(models.Model):
    SEXE = [
        ('M', 'M'),
        ('F', 'F'),
    ]

    SENT = [
        ('A MORT', 'A MORT'),
        ('CAPITALE', 'CAPITALE'),
        ('TRAVAUX FORCES', 'TRAVAUX FORCES'),
    ]

    nom = models.CharField(max_length=15)
    postnom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=15)
    profil = models.FileField(upload_to='photo_detenus')
    matricule = models.CharField(max_length=15, unique=True, default=None)
    sexe = models.CharField(max_length=15, choices=SEXE, default=None)
    date_de_naissance = models.DateField()
    lieu_de_naissance = models.CharField(max_length=100)
    motif = models.CharField(max_length=500)
    peine = models.CharField(max_length=20, choices=SENT, default=None)
    condamne_par = models.ForeignKey(Agent, on_delete=models.CASCADE, default=None)
    prison_incarceree = models.ForeignKey(Prison, on_delete=models.CASCADE, default=None)
    date_entree = models.DateField()
    date_sortie = models.DateField(null=True, blank=True)
    cellule = models.CharField(max_length=15)
    dossiers = models.ManyToManyField(Dossier, blank=True)
    est_libere = models.BooleanField(default=False)
    duree = models.CharField(max_length=50, blank=True, null=True)

    @property
    def incarceration_duration(self):
        if self.peine == 'A MORT' and not self.date_sortie:
            self.duree = 'A VIE'
        elif self.date_sortie:
            delta = self.date_sortie - self.date_entree
            years, remainder = divmod(delta.days, 365)
            months, days = divmod(remainder, 30)
            self.duree = f"{years} ans, {months} mois, {days} jours"
        else:
            self.duree = 'Non définie'
        self.save()
        return self.duree

    @property
    def est_libere_status(self):
        if self.date_sortie and self.date_sortie < date.today():
            self.est_libere = True
        else:
            self.est_libere = False
        self.save()
        return 'EST LIBRE' if self.est_libere else 'EST TOUJOUR INCARCERE'

class Transfert(models.Model):
    detenu = models.ForeignKey(Detenu, on_delete=models.CASCADE)
    ancienne_prison = models.ForeignKey(Prison, related_name='ancienne_prison', on_delete=models.CASCADE)
    nouvelle_prison = models.ForeignKey(Prison, related_name='nouvelle_prison', on_delete=models.CASCADE)
    date_transfert = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.detenu.nom} transféré de {self.ancienne_prison.nom} à {self.nouvelle_prison.nom}"