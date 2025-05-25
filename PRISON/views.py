from django.shortcuts import render, redirect
from .forms import *
from .models import *
from DETENUS.models import Detenu  # Assurez-vous que le modèle Detenu est importé correctement
import logging
from django.db.models import Count, Q

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
    error_message = None
    search_error_message = None
    if request.method == 'POST':
        EP = Enregistrement_Prison(request.POST)
        territoire_id = request.session.get('territoire_id')
        if EP.is_valid():
            prison = EP.save(commit=False)
            if prison.territoire.id != territoire_id:
                error_message = "Vous ne pouvez qu'enregistrer une prison dans votre site"
            else:
                prison.save()
                return redirect('Ajout_Prison')
    else:
        EP = Enregistrement_Prison()
    territoire_id = request.session.get('territoire_id')
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
    query = request.GET.get('query')
    if not query:
        raise Http404("Aucune requête de recherche fournie.")
    
    pri = Prison.objects.filter(nom_de_la_prison__icontains=query)
    if not pri.exists():
        raise Http404("Le nom saisi n'existe pas.")
    
    return render(request, 'Detenu/recherchePrison.html', {'pri': pri})

def statistiques(request):
    territoire_id = request.session.get('territoire_id')
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
        
        logger.debug('Prison: %s', prison.nom_de_la_prison)
        logger.debug('Total prisonniers: %s', prison.total_prisonniers)
        logger.debug('Prisonniers incarcérés: %s', prison.prisonniers_incarceres)
        logger.debug('Prisonniers libres: %s', prison.prisonniers_libres)
        logger.debug('Hommes: %s', hommes)
        logger.debug('Femmes: %s', femmes)
        logger.debug('Peine à mort: %s', peine_a_mort)
        logger.debug('Peine capitale: %s', peine_capitale)
        logger.debug('Travaux forcés: %s', travaux_forces)
        
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
    
    return render(request, 'Detenu/statitistique.html', {
        'prisons': prisons_stats
    })