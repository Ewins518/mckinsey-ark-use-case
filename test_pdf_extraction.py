#!/usr/bin/env python3
"""
Test script pour valider l'extraction de texte PDF
"""

import PyPDF2
import io

def test_pdf_extraction():
    """Test l'extraction de texte du PDF de test"""
    
    # Lire le PDF de test
    with open('/tmp/test-construction-project.pdf', 'rb') as file:
        pdf_content = file.read()
    
    # Extraire le texte
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    pdf_text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text() + "\n"
    
    print("✅ Extraction PDF réussie!")
    print(f"📄 Nombre de pages: {len(pdf_reader.pages)}")
    print(f"📝 Longueur du texte extrait: {len(pdf_text)} caractères")
    print("\n📋 Contenu extrait:")
    print("=" * 50)
    print(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
    print("=" * 50)
    
    return pdf_text

if __name__ == "__main__":
    test_pdf_extraction()
