#!/usr/bin/env python3
"""
Script de debug pour tester l'upload PDF dans Streamlit
"""

import PyPDF2
import io
import sys

def test_pdf_upload():
    """Test l'upload et l'extraction du PDF"""
    
    pdf_path = "pdf_test.pdf"
    
    try:
        print(f"📄 Test d'ouverture du PDF: {pdf_path}")
        
        # Ouvrir le PDF
        with open(pdf_path, 'rb') as file:
            pdf_content = file.read()
        
        print(f"✅ PDF ouvert avec succès - Taille: {len(pdf_content)} bytes")
        
        # Extraire le texte
        print("📝 Extraction du texte...")
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        print(f"📊 Nombre de pages: {len(pdf_reader.pages)}")
        
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            pdf_text += page_text + "\n"
            print(f"Page {page_num + 1}: {len(page_text)} caractères")
        
        print(f"✅ Texte extrait total: {len(pdf_text)} caractères")
        
        if pdf_text.strip():
            print("\n📋 Aperçu du contenu:")
            print("=" * 50)
            print(pdf_text[:300] + "..." if len(pdf_text) > 300 else pdf_text)
            print("=" * 50)
        else:
            print("⚠️  Aucun texte extrait du PDF")
        
        return True, pdf_text
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        print(f"Type d'erreur: {type(e).__name__}")
        return False, str(e)

if __name__ == "__main__":
    success, result = test_pdf_upload()
    if success:
        print("✅ Test réussi!")
    else:
        print("❌ Test échoué!")
        sys.exit(1)

