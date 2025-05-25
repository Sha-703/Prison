from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importer les vues d'authentification de Django

urlpatterns = [
    path('', views.utilisateur, name='utilisateur'),
    path('accueil/', views.accueil, name='accueil'),
    path('logout/', views.deconnexion, name='logout'),  # Utiliser la vue de déconnexion personnalisée
    path('imprimer_rapport/', views.imprimer_rapport, name='imprimer_rapport'),  # Ajouter l'URL pour imprimer le rapport
]