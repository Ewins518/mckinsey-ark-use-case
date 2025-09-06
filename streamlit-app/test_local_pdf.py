#!/usr/bin/env python3
"""
Test du workflow avec le PDF local
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ark_client import ARKClient
import PyPDF2
import io
import time

def test_local_pdf_workflow():
    """Test le workflow avec le PDF local"""
    
    print("🧪 Test du workflow avec PDF local...")
    
    # Vérifier que le PDF existe
    pdf_file = "pdf_test.pdf"
    if not os.path.exists(pdf_file):
        print(f"❌ Fichier PDF non trouvé: {pdf_file}")
        return False
    
    print(f"✅ PDF trouvé: {pdf_file}")
    
    # Lire et extraire le texte
    print("📄 Extraction du texte...")
    with open(pdf_file, 'rb') as file:
        pdf_content = file.read()
    
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    pdf_text = ""
    
    # Limiter aux 5 premières pages pour le test
    max_pages = min(5, len(pdf_reader.pages))
    for page_num in range(max_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        pdf_text += page_text + "\n"
    
    print(f"✅ Texte extrait: {len(pdf_text)} caractères")
    
    # Créer la query
    client = ARKClient()
    query_name = f"test-local-{int(time.time())}"
    
    project_data = {
        'query_name': query_name,
        'region': 'Morocco',
        'pdf_content': f"PDF Document: {pdf_file}\n\nExtracted Content:\n{pdf_text}",
        'file_name': pdf_file
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
                print(f"Clés disponibles: {list(results.keys())}")
                
                # Vérifier les deux formats possibles
                companies = None
                if 'recommended_companies' in results and results['recommended_companies']:
                    companies = results['recommended_companies']
                    print(f"📊 Nombre d'entreprises trouvées (recommended_companies): {len(companies)}")
                elif 'companies' in results and results['companies']:
                    companies = results['companies']
                    print(f"📊 Nombre d'entreprises trouvées (companies): {len(companies)}")
                
                if companies:
                    for i, company in enumerate(companies[:3]):  # Afficher les 3 premières
                        print(f"\n{i+1}. {company.get('name', 'N/A')} - {company.get('rating', 0)}/10")
                        print(f"   📍 {company.get('location', 'N/A')}")
                        print(f"   🎯 Fit: {company.get('project_fit', 'N/A')}")
                else:
                    print("❌ Aucune entreprise trouvée dans les résultats")
                    # Afficher un aperçu des résultats
                    for key, value in results.items():
                        if isinstance(value, list):
                            print(f"  {key}: {len(value)} éléments")
                        else:
                            print(f"  {key}: {str(value)[:100]}...")
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
    
    return True

if __name__ == "__main__":
    test_local_pdf_workflow()
