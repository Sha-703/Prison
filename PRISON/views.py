from django.shortcuts import render, redirect
from .forms import *
from .models import *
from DETENUS.models import Detenu  # Assurez-vous que le modèle Detenu est importé correctement
import logging
from django.db.models import Count, Q
from django.contrib.auth.models import Group
from PERS_AUTH.models import Utilisateur

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Create your views here.
logger = logging.getLogger(__name__)

def Ajout_Prison(request):
    user = request.user
    is_consultant = user.is_authenticated and user.groups.filter(name='Consultants').exists()
    error_message = None
    search_error_message = None
    territoire_id = request.session.get('territoire_id')
    if request.method == 'POST':
        EP = Enregistrement_Prison(request.POST)
        if EP.is_valid():
            prison = EP.save(commit=False)
            if not is_consultant and prison.territoire.id != territoire_id:
                error_message = "Vous ne pouvez qu'enregistrer une prison dans votre site"
            else:
                prison.save()
                return redirect('Ajout_Prison')
    else:
        EP = Enregistrement_Prison()
    if is_consultant:
        LPS = Prison.objects.all()
        prisons = Prison.objects.all()
    else:
        LPS = Prison.objects.filter(territoire_id=territoire_id)
        prisons = Prison.objects.filter(territoire_id=territoire_id)
    return render(request, 'Detenu/prison.html', {'form': EP, 'LPS': LPS, 'prisons': prisons, 'error_message': error_message, 'search_error_message': search_error_message}) 

def Ajout_Grade(request):
    if request.method == 'POST':
        EG = Enregistement_Grade(request.POST)
        #pour sauvegarder les données depuis le formulaire de la page vers la base de données
        if EG.is_valid():
            EG.save()
            return redirect('Ajout_Grade')
    else:
        EG = Enregistement_Grade(request.POST)
        LEG = Grade.objects.all()
        return render(request, 'Detenu/grade.html', {'grade':EG, 'LEG':LEG})
    
def ajout_agent(request):
    if request.method == 'POST':
        AG = Enregistement_Agent(request.POST)
        if AG.is_valid():
            AG.save()
            return redirect('ajout_agent')
    else:
        AG = Enregistement_Agent()
        LAG = Agent.objects.all()
        return render (request, 'Detenu/agent.html', {'agent': AG, 'LAG': LAG})
    
# recherche 
from django.http import Http404

def cherchePrison(request):
    user = request.user
    is_consultant = user.is_authenticated and user.groups.filter(name='Consultants').exists()
    query = request.GET.get('query')
    if not query:
        raise Http404("Aucune requête de recherche fournie.")
    if is_consultant:
        pri = Prison.objects.filter(nom_de_la_prison__icontains=query)
    else:
        territoire_id = request.session.get('territoire_id')
        pri = Prison.objects.filter(nom_de_la_prison__icontains=query, territoire_id=territoire_id)
    if not pri.exists():
        raise Http404("Le nom saisi n'existe pas.")
    return render(request, 'Detenu/recherchePrison.html', {'pri': pri})

def statistiques(request):
    # Récupérer l'utilisateur connecté depuis la session
    nom_utilisateur = request.session.get('nom_utilisateur')
    if not nom_utilisateur:
        return redirect('utilisateur')
    utilisateur = Utilisateur.objects.get(nom_utilisateur=nom_utilisateur)
    if utilisateur.is_superuser:
        prisons = Prison.objects.all().annotate(
            total_prisonniers=Count('detenu'),
            prisonniers_incarceres=Count('detenu', filter=Q(detenu__est_libere=False)),
            prisonniers_libres=Count('detenu', filter=Q(detenu__est_libere=True)),
        )
    else:
        territoire_id = utilisateur.territoire.id
        prisons = Prison.objects.filter(territoire_id=territoire_id).annotate(
            total_prisonniers=Count('detenu'),
            prisonniers_incarceres=Count('detenu', filter=Q(detenu__est_libere=False)),
            prisonniers_libres=Count('detenu', filter=Q(detenu__est_libere=True)),
        )
    prisons_stats = []
    for prison in prisons:
        hommes = Detenu.objects.filter(prison_incarceree=prison, sexe='M').count()
        femmes = Detenu.objects.filter(prison_incarceree=prison, sexe='F').count()
        peine_a_mort = Detenu.objects.filter(prison_incarceree=prison, peine='A MORT').count()
        peine_capitale = Detenu.objects.filter(prison_incarceree=prison, peine='CAPITALE').count()
        travaux_forces = Detenu.objects.filter(prison_incarceree=prison, peine='TRAVAUX FORCES').count()
        prisons_stats.append({
            'prison': prison,
            'total_prisonniers': prison.total_prisonniers,
            'prisonniers_incarceres': prison.prisonniers_incarceres,
            'prisonniers_libres': prison.prisonniers_libres,
            'hommes': hommes,
            'femmes': femmes,
            'peine_a_mort': peine_a_mort,
            'peine_capitale': peine_capitale,
            'travaux_forces': travaux_forces
        })
    return render(request, 'Detenu/statitistique.html', {'prisons': prisons_stats, 'utilisateur': utilisateur})

def list_prisons(request):
    # Récupérer l'utilisateur connecté depuis la session
    nom_utilisateur = request.session.get('nom_utilisateur')
    if not nom_utilisateur:
        return redirect('utilisateur')
    utilisateur = Utilisateur.objects.get(nom_utilisateur=nom_utilisateur)
    if utilisateur.is_superuser:
        prisons = Prison.objects.all()
    else:
        territoire_id = utilisateur.territoire.id
        prisons = Prison.objects.filter(territoire_id=territoire_id)
    return render(request, 'Detenu/listPrison.html', {'prisons': prisons, 'utilisateur': utilisateur})