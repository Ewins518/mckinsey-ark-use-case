#!/usr/bin/env python3
"""
Test complet du workflow PDF Company Finder
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'streamlit-app'))

from ark_client import ARKClient
import PyPDF2
import io
import time

def test_complete_workflow():
    """Test le workflow complet avec le PDF de test"""
    
    print("🧪 Test du workflow PDF Company Finder complet...")
    
    # Lire et extraire le texte du PDF
    print("📄 Extraction du texte PDF...")
    with open('/tmp/test-construction-project.pdf', 'rb') as file:
        pdf_content = file.read()
    
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    pdf_text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text() + "\n"
    
    print(f"✅ Texte extrait: {len(pdf_text)} caractères")
    
    # Créer la query
    client = ARKClient()
    query_name = f"test-complete-{int(time.time())}"
    
    project_data = {
        'query_name': query_name,
        'region': 'Morocco',
        'pdf_content': f"PDF Document: test-construction-project.pdf\n\nExtracted Content:\n{pdf_text}",
        'file_name': 'test-construction-project.pdf'
    }
    
    print("🚀 Création de la query...")
    success, message = client.create_pdf_query(project_data)
    
    if success:
        print(f"✅ Query créée: {query_name}")
        
        print("⏳ Attente de la completion...")
        completed, result = client.wait_for_completion(query_name, timeout=300)
        
        if completed:
            print("✅ Query terminée!")
            
            # Récupérer les résultats
            success, results = client.get_query_results(query_name)
            
            if success and results:
                print("🎯 Résultats obtenus:")
                
                if 'recommended_companies' in results:
                    companies = results['recommended_companies']
                    print(f"📊 Nombre d'entreprises trouvées: {len(companies)}")
                    
                    for i, company in enumerate(companies[:3]):  # Afficher les 3 premières
                        print(f"\n{i+1}. {company.get('name', 'N/A')} - {company.get('rating', 0)}/10")
                        print(f"   📍 {company.get('location', 'N/A')}")
                        print(f"   🎯 Fit: {company.get('project_fit', 'N/A')}")
                else:
                    print("❌ Aucune entreprise trouvée dans les résultats")
                    print(f"Clés disponibles: {list(results.keys())}")
            else:
                print(f"❌ Échec de récupération des résultats: {results}")
        else:
            print(f"❌ Query échouée: {result}")
    else:
        print(f"❌ Échec de création de la query: {message}")
    
    # Nettoyage
    print("🧹 Nettoyage...")
    client.delete_query(query_name)
    print("✅ Test terminé!")

if __name__ == "__main__":
    test_complete_workflow()
