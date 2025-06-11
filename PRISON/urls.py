from django.urls import path
from . import views


urlpatterns = [
    path('prison', views.Ajout_Prison, name='Ajout_Prison'),
    path('grade/', views.Ajout_Grade, name='Ajout_Grade'),
    path('agent', views.ajout_agent, name='ajout_agent'),
    path('recherche/', views.cherchePrison, name='cherchePrison'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('liste-prisons/', views.list_prisons, name='list_prisons'),  # Nouvelle route pour la liste des prisons
]
