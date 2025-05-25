from django.shortcuts import render, redirect
from django.contrib.auth import logout  # Importer la fonction de déconnexion
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from PRISON.models import *
from DETENUS.models import *
from django.http import HttpResponse
import io
from reportlab.lib.pagesizes import letter, landscape  # Importer le format paysage
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from datetime import datetime  # Importer la bibliothèque datetime

# Create your views here.
#RECUPERER LES DONNEES SAISIES DANS LE FORMULAIRE DE LA PAGE LOGING QUE NOU AVONS NOUS MEME CREER
def utilisateur(request):
        if request.method == 'POST':
            nom_utilisateur = request.POST.get('userame')
            mdp = request.POST.get('password')
            try: 
                utilisateur = Utilisateur.objects.get(nom_utilisateur = nom_utilisateur, mdp = mdp)
                request.session['territoire_id'] = utilisateur.territoire.id
                return redirect('accueil')
            except Utilisateur.DoesNotExist:
                messages.error(request, "Nom d'utilisateur ou mot de passe non valide")
                return render(request, 'Detenu/loging.html')
        return render(request, 'Detenu/loging.html')

def accueil(request):
    territoire_id = request.session.get('territoire_id')
    territoire = Territoire.objects.get(id=territoire_id)
    prisons = Prison.objects.filter(territoire_id=territoire_id)
    return render(request, 'Detenu/accueil.html', {'prisons': prisons, 'territoire_nom': territoire.nom})

def deconnexion(request):
    logout(request)
    return redirect('utilisateur')  # Rediriger vers la page de connexion après déconnexion

def imprimer_rapport(request):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(letter))  # Utiliser le format paysage
    elements = []

    territoire_id = request.session.get('territoire_id')
    territoire = Territoire.objects.get(id=territoire_id)
    styles = getSampleStyleSheet()
    
    # Ajouter le titre du rapport
    title_style = ParagraphStyle(name='TitleStyle', alignment=1, fontSize=18, spaceAfter=20)
    elements.append(Paragraph(f"Rapport du territoire de: {territoire.nom}", title_style))
    
    prisons = Prison.objects.filter(territoire=territoire)
    for prison in prisons:
        prison_style = ParagraphStyle(name='PrisonStyle', alignment=0, fontSize=14, spaceAfter=10)  # Alignement à gauche
        elements.append(Paragraph(f"Prison: {prison.nom_de_la_prison}", prison_style))
        
        data = [["N°", "Nom", "Crime", "Date d'incarcération", "Durée de la peine", "Date de libération", "Sexe"]]
        prisonniers = Detenu.objects.filter(prison_incarceree=prison)
        numero = 1  # Initialiser le numéro d'ordre
        for prisonnier in prisonniers:
            data.append([
                numero,
                prisonnier.nom,
                prisonnier.motif,
                prisonnier.date_entree.strftime('%d/%m/%Y'),  # Formater la date d'incarcération
                prisonnier.duree,
                prisonnier.date_sortie.strftime('%d/%m/%Y') if prisonnier.date_sortie else '',  # Formater la date de libération prévue
                prisonnier.sexe
            ])
            numero += 1  # Incrémenter le numéro d'ordre
        
        # Ajouter la ligne de synthèse pour le nombre total de prisonniers
        data.append(["", "Total Détenu.:", "", "", "", "", "",len(prisonniers)])
        
        table = Table(data, colWidths=[30, 110, 100, 110, 120, 100, 40])  # Ajuster la largeur des colonnes
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))  # Ajouter un espace entre les tableaux
    
    # Ajouter le nom de l'utilisateur connecté et la date/heure d'impression à la fin du rapport
    utilisateur_nom = "MANAGER_PRISON"
    user_style = ParagraphStyle(name='UserStyle', alignment=0, fontSize=12, spaceAfter=20)
    elements.append(Paragraph(f"Rapport généré par: {utilisateur_nom} {user_style}, Date et heure d'impression: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", user_style))
    
    doc.build(elements)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="rapport.pdf"'
    return response