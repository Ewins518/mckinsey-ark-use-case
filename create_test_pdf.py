#!/usr/bin/env python3
"""
Script pour créer un PDF de test pour le workflow PDF Company Finder
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_test_pdf():
    """Créer un PDF de test avec des spécifications de projet"""
    
    # Créer le document PDF
    doc = SimpleDocTemplate("/tmp/test-construction-project.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour les titres
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=1  # Centré
    )
    
    # Style pour les sous-titres
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8
    )
    
    # Contenu du PDF
    content = []
    
    # Titre principal
    content.append(Paragraph("APPEL D'OFFRES - CONSTRUCTION BÂTIMENT DE BUREAUX", title_style))
    content.append(Spacer(1, 20))
    
    # Informations du projet
    content.append(Paragraph("INFORMATIONS DU PROJET", subtitle_style))
    content.append(Paragraph("• <b>Titre du projet:</b> Construction d'un bâtiment de bureaux moderne", styles['Normal']))
    content.append(Paragraph("• <b>Localisation:</b> Casablanca, Maroc", styles['Normal']))
    content.append(Paragraph("• <b>Budget estimé:</b> 2 000 000 - 3 000 000 MAD", styles['Normal']))
    content.append(Paragraph("• <b>Durée du projet:</b> 12-18 mois", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Description du projet
    content.append(Paragraph("DESCRIPTION DU PROJET", subtitle_style))
    content.append(Paragraph("Construction d'un bâtiment de bureaux moderne de 3 étages avec les spécifications suivantes:", styles['Normal']))
    content.append(Spacer(1, 8))
    
    # Exigences techniques
    content.append(Paragraph("EXIGENCES TECHNIQUES", subtitle_style))
    content.append(Paragraph("• Construction de façade en acier et verre", styles['Normal']))
    content.append(Paragraph("• Systèmes CVC modernes", styles['Normal']))
    content.append(Paragraph("• Infrastructure électrique complète", styles['Normal']))
    content.append(Paragraph("• Parking pour 50 véhicules", styles['Normal']))
    content.append(Paragraph("• Aménagement paysager et travaux extérieurs", styles['Normal']))
    content.append(Paragraph("• Aménagement intérieur pour espaces de bureaux", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Facteurs de succès
    content.append(Paragraph("FACTEURS DE SUCCÈS CLÉS", subtitle_style))
    content.append(Paragraph("• Expérience avec les bâtiments de bureaux commerciaux", styles['Normal']))
    content.append(Paragraph("• Techniques de construction modernes", styles['Normal']))
    content.append(Paragraph("• Capacité de livraison dans les délais", styles['Normal']))
    content.append(Paragraph("• Expertise en gestion de budget", styles['Normal']))
    content.append(Paragraph("• Connaissance du marché local marocain", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Qualifications requises
    content.append(Paragraph("QUALIFICATIONS REQUISES", subtitle_style))
    content.append(Paragraph("• Minimum 5 ans d'expérience en construction commerciale", styles['Normal']))
    content.append(Paragraph("• Entreprise de construction agréée au Maroc", styles['Normal']))
    content.append(Paragraph("• Antécédents prouvés avec des bâtiments de bureaux", styles['Normal']))
    content.append(Paragraph("• Stabilité financière et capacité de cautionnement", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Instructions
    content.append(Paragraph("INSTRUCTIONS", subtitle_style))
    content.append(Paragraph("Veuillez fournir les 5 meilleures entreprises de construction adaptées à ce projet, en incluant:", styles['Normal']))
    content.append(Paragraph("• Nom de l'entreprise et site web", styles['Normal']))
    content.append(Paragraph("• Spécialisation et expertise", styles['Normal']))
    content.append(Paragraph("• Raisons de l'adéquation au projet", styles['Normal']))
    content.append(Paragraph("• Expérience notable et projets similaires", styles['Normal']))
    content.append(Paragraph("• Évaluation de l'adéquation au projet (1-10)", styles['Normal']))
    
    # Construire le PDF
    doc.build(content)
    print("✅ PDF de test créé: /tmp/test-construction-project.pdf")

if __name__ == "__main__":
    create_test_pdf()
