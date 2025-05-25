from django.shortcuts import render
from django.http import HttpResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from DETENUS.models import Detenu, Prison  # Assurez-vous que les modèles Detenu et Prison sont importés

def telecharger_rapport(request):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []

    territoire_nom = request.user.territoire.nom  # Assurez-vous que l'utilisateur a un attribut territoire
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Territoire: {territoire_nom}", styles['Heading1']))

    prisons = Prison.objects.filter(territoire=request.user.territoire)
    for prison in prisons:
        elements.append(Paragraph(f"Prison: {prison.nom_de_la_prison}", styles['Heading2']))
        
        data = [["N°", "Nom", "Age", "Crime", "Date d'incarcération", "Durée de la peine", "Date de libération prévue", "Date de naissance", "Sexe"]]
        prisonniers = Detenu.objects.filter(prison_incarceree=prison)
        numero = 1  # Initialiser le numéro d'ordre
        for prisonnier in prisonniers:
            data.append([
                numero,
                prisonnier.nom,
                prisonnier.date_de_naissance,
                prisonnier.motif,
                prisonnier.date_entree,
                prisonnier.duree,
                prisonnier.date_sortie,
                prisonnier.date_de_naissance,
                prisonnier.sexe
            ])
            numero += 1  # Incrémenter le numéro d'ordre
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    
    doc.build(elements)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport.pdf"'
    return response

def imprimer_rapport(request):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []

    territoire_nom = request.user.territoire.nom  # Assurez-vous que l'utilisateur a un attribut territoire
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Territoire: {territoire_nom}", styles['Heading1']))

    prisons = Prison.objects.filter(territoire=request.user.territoire)
    for prison in prisons:
        elements.append(Paragraph(f"Prison: {prison.nom_de_la_prison}", styles['Heading2']))
        
        data = [["N°", "Nom", "Age", "Crime", "Date d'incarcération", "Durée de la peine", "Date de libération prévue", "Date de naissance", "Sexe"]]
        prisonniers = Detenu.objects.filter(prison_incarceree=prison)
        numero = 1  # Initialiser le numéro d'ordre
        for prisonnier in prisonniers:
            data.append([
                numero,
                prisonnier.nom,
                prisonnier.date_de_naissance,
                prisonnier.motif,
                prisonnier.date_entree,
                prisonnier.duree,
                prisonnier.date_sortie,
                prisonnier.date_de_naissance,
                prisonnier.sexe
            ])
            numero += 1  # Incrémenter le numéro d'ordre
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    
    doc.build(elements)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="rapport.pdf"'
    return response

