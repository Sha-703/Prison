from django.urls import path
from . import views
from django.shortcuts import render
from .models import Detenu

def listDetenu(request):
    detenus = Detenu.objects.all()
    return render(request, 'Detenu/addandshow.html', {'detenus': detenus})

urlpatterns = [
    path('Ajout/', views.Ajout, name='Ajout'),
    path('liste/', views.listDetenu, name='listDetenu'),
    path('info/<int:id>', views.detenuInfo, name='detenu_info'),
    path('recherche/', views.chercheDetenu, name='chercheDetenu'),
    path('transfert/<int:detenu_id>/', views.transfert_detenu, name='transfert_detenu'),
    path('detenu/<int:id>/', views.detenuInfo, name='detenuInfo'),
    path('ajouter_dossier/<int:detenu_id>/', views.ajouter_dossier, name='ajouter_dossier'),
]