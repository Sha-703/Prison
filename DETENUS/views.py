from django.shortcuts import render, redirect, get_object_or_404
from .forms import Enregistrement_Detenu, TransfertForm, DossierForm
from .models import Detenu, Transfert, Dossier
from PRISON.models import Prison  # Importer uniquement les modèles nécessaires
import logging
from django import forms
import json  # Ajouter l'importation de json pour le débogage

class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['nouvelle_prison']


# Create your views here.
logger = logging.getLogger(__name__)
def Ajout(request):
    logger.debug('Received POST request')
    territoire_id = request.session.get('territoire_id')
    DET = Enregistrement_Detenu(request.POST, request.FILES, territoire_id=territoire_id)
    if DET.is_valid():
            DET.save()
    logger.debug('Received GET request')
    DET = Enregistrement_Detenu(territoire_id=territoire_id)
    prisons = Prison.objects.filter(territoire_id=territoire_id)
    LDET = Detenu.objects.filter(prison_incarceree__territoire_id=territoire_id)
    return render(request, 'Detenu/addandshow.html', {'detenu': DET, 'LDET': LDET, 'prisons': prisons})

#RECUPERER LES DONNES DE LA BASE DE DONNEES POUR LES AFFICHER DANS LA PAGE LISTPRISONNIER.HTML

def listDetenu(request):
    territoire_id = request.session.get('territoire_id')
    LDET = Detenu.objects.filter(prison_incarceree__territoire_id=territoire_id)
    return render(request, 'Detenu/listPrisonnier.html', {'LDET': LDET})

#   RECUPERER UNIQUEMENT LE ID DE CHAQUE DETENU POUR L'AFFICHER SUR LA PAGE INFOPRISONNIER.HTML
def detenuInfo(request, id):
    Pri = Detenu.objects.get(id=id)
    return render(request, 'Detenu/infoPrisonnier.html', {'Pri': Pri})

# RECHERCHE DETENU
def chercheDetenu(request):
    query = request.GET.get('query')
    det = Detenu.objects.filter(nom__icontains=query)
    if not det:
        error_message = "Le nom saisi n'existe pas"
        territoire_id = request.session.get('territoire_id')
        DET = Enregistrement_Detenu(territoire_id=territoire_id)
        prisons = Prison.objects.filter(territoire_id=territoire_id)
        LDET = Detenu.objects.filter(prison_incarceree__territoire_id=territoire_id)
        return render(request, 'Detenu/addandshow.html', {'detenu': DET, 'LDET': LDET, 'prisons': prisons, 'error_message': error_message})
    return render(request, 'Detenu/rechercheDetenu.html', {'det': det})

def transfert_detenu(request, detenu_id):
    detenu = Detenu.objects.get(id=detenu_id)
    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():
            transfert = form.save(commit=False)
            transfert.detenu = detenu
            transfert.ancienne_prison = detenu.prison_incarceree
            detenu.prison_incarceree = transfert.nouvelle_prison
            detenu.save()
            transfert.save()
            return redirect('detenu_info', id=detenu.id)
    else:
        form = TransfertForm()
    return render(request, 'Detenu/transfert_detenu.html', {'form': form, 'detenu': detenu})

def ajouter_dossier(request, detenu_id):
    detenu = get_object_or_404(Detenu, id=detenu_id)
    if request.method == 'POST':
        form = DossierForm(request.POST, request.FILES)
        if form.is_valid():
            dossier = form.save()
            detenu.dossiers.add(dossier)
            return redirect('detenu_info', id=detenu.id)
    else:
        form = DossierForm()
        return render(request, 'Detenu/ajouter_dossier.html', {'form': form, 'detenu': detenu})

def statistiques(request):
    territoire_id = request.session.get('territoire_id')
    prisons = Prison.objects.filter(territoire_id=territoire_id)
    prisons_stats = []
    
    for prison in prisons:
        total_prisonniers = Detenu.objects.filter(prison_incarceree=prison).count()
        prisonniers_incarceres = Detenu.objects.filter(prison_incarceree=prison, est_libere=False).count()
        prisonniers_libres = Detenu.objects.filter(prison_incarceree=prison, est_libere=True).count()
        hommes = Detenu.objects.filter(prison_incarceree=prison, sexe='M').count()
        femmes = Detenu.objects.filter(prison_incarceree=prison, sexe='F').count()
        peine_a_mort = Detenu.objects.filter(prison_incarceree=prison, peine='A MORT').count()
        peine_capitale = Detenu.objects.filter(prison_incarceree=prison, peine='CAPITALE').count()
        travaux_forces = Detenu.objects.filter(prison_incarceree=prison, peine='TRAVAUX FORCES').count()
        
        prisons_stats.append({
            'prison': prison,
            'total_prisonniers': total_prisonniers,
            'prisonniers_incarceres': prisonniers_incarceres,
            'prisonniers_libres': prisonniers_libres,
            'hommes': hommes,
            'femmes': femmes,
            'peine_a_mort': peine_a_mort,
            'peine_capitale': peine_capitale,
            'travaux_forces': travaux_forces
        })
    
    return render(request, 'Detenu/statitistique.html', {
        'prisons': prisons_stats
    })