from django.db import models
# Create your models here.

class Instance(models.Model):
    Inst = [
    ("COURS D'APPEL", "COURS D'APPEL"),
    ("TRIBUNAL DE GRANDE INSTANCE", "TRIBUNAL DE GRANDE INSTANCE"),
    ("TRIBUNAL DE PAIX", "TRIBUNAL DE PAIX"),
    ("PARUET PRE LA COUR D'APPEL", "PARUET PRE LA COUR D'APPEL"),
    ("PARQUET PRE LE TRIBUNAL DE GRANDE INSTANCE", "PARQUET PRE LE TRIBUNAL DE GRANDE INSTANCE"),
    ("PARQUE PRE LE TRIBUNAL DE PAIX", "PARQUE PRE LE TRIBUNAL DE PAIX")
]
    libelle_Instance = models.CharField(max_length=50, choices=Inst, default="COURS D'APPEL")
    def __str__(self):
        return self.libelle_Instance

class Grade(models.Model):
    gra = [
        ("PRES. DE LA COUR D'APPEL", "PRES. DE LA COUR D'APPEL"),
        ("CONS. DE LA COUR D'APPEL", "CONS. DE LA COUR D'APPEL"),
        ("JUGE DE GRANDE INSTANCE", "JUGE DE GRANDE INSTANCE"),
        ("JUGE DE PAIX", "JUGE DE PAIX"),
        ("PROC. GEN. PRE LA COUR D'APPEL", "PROC. GEN. PRE LA COUR D'APPEL"),
        ("PROC. DE LA REP. PRE LE T.G.I", "PROC. DE LA REP. PRE LE T.G.I"),
        ("PROC. DE PAIX", "PROCUREUR DE PAIX"),
        ("MAGISTRAT ADMINISTRATIF", "MAGISTRAT ADMINISTRATIF"),
    ]
    libelle_Grade = models.CharField(max_length=30, choices=gra, default="PRES. DE LA COUR D'APPEL")
    def __str__(self):
        return self.libelle_Grade

class Territoire(models.Model):
    TER = [
        ("KASANGULU", "KASANGULU"),
        ("MADIMBA", "MADIMBA"),
        ("LUKULA", "LUKULA"),
        ("MBANZA-NGUNGU", "MBANZA-NGUNGU"),
        ("SONGOLOLO", "SONGOLOLO"),
        ("LUOZI", "LUOZI"),
        ("KIMVULA", "KIMVULA"),
        ("SEKEBANZA", "SEKEBANZA"),
        ("TSHELA", "TSHELA"),
        ("MOANDA", "MOANDA"),
        ("MATADI", "MATADI"),
        ("BOMA", "BOMA"),
    ]
    nom = models.CharField(max_length=20, choices=TER)
    def __str__(self):
        return self.nom

class Agent(models.Model):
    gra = [
        ("PRES. DE LA COUR D'APPEL", "PRES. DE LA COUR D'APPEL"),
        ("CONS. DE LA COUR D'APPEL", "CONS. DE LA COUR D'APPEL"),
        ("JUGE DE GRANDE INSTANCE", "JUGE DE GRANDE INSTANCE"),
        ("JUGE DE PAIX", "JUGE DE PAIX"),
        ("PROC. GEN. PRE LA COUR D'APPEL", "PROC. GEN. PRE LA COUR D'APPEL"),
        ("PROC. DE LA REP. PRE LE T.G.I", "PROC. DE LA REP. PRE LE T.G.I"),
        ("PROC. DE PAIX", "PROCUREUR DE PAIX"),
        ("MAGISTRAT ADMINISTRATIF", "MAGISTRAT ADMINISTRATIF"),
    ]
     
    nom_Agent = models.CharField(max_length=15)
    postnom_Agent = models.CharField(max_length=15)
    prenom_Agent = models.CharField(max_length=15)
    localite = models.ForeignKey(Territoire, on_delete=models.CASCADE, default=1)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=1)
    grade = models.CharField(max_length=50, choices=gra)
    def __str__(self):
        return f'{self.nom_Agent} {self.postnom_Agent} {self.prenom_Agent}'
    

    
class Prison(models.Model):
    
    nom_de_la_prison = models.CharField(max_length=15)
    capacite = models.IntegerField()    
    territoire = models.ForeignKey(Territoire, on_delete=models.CASCADE)
    directeur = models.CharField(max_length=15)
    
# fonction qui compte le nombre de prisonniers
    @property
    def nombre_prisonniers(self):
        return self.detenu_set.count()

    #retour de la valeur nom dans l'affichage de la prison dans le menu de l'admnistrateur
    def __str__(self):
        return self.nom_de_la_prison

