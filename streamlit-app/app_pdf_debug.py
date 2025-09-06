"""
Version de debug de l'app PDF pour diagnostiquer l'erreur 403
"""

import streamlit as st
import PyPDF2
import io
import traceback

def main():
    st.set_page_config(
        page_title="PDF Debug",
        page_icon="🐛",
        layout="wide"
    )
    
    st.title("🐛 PDF Upload Debug")
    st.markdown("Version de debug pour diagnostiquer l'erreur 403")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to test"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Fichier uploadé: {uploaded_file.name}")
        st.info(f"📊 Taille: {len(uploaded_file.getvalue())} bytes")
        
        # Test d'extraction
        try:
            st.write("🔍 Test d'extraction du texte...")
            
            # Lire le contenu
            pdf_content = uploaded_file.getvalue()
            st.write(f"✅ Contenu lu: {len(pdf_content)} bytes")
            
            # Extraire le texte
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            st.write(f"✅ PDF Reader créé - Pages: {len(pdf_reader.pages)}")
            
            pdf_text = ""
            for page_num in range(min(3, len(pdf_reader.pages))):  # Seulement les 3 premières pages
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                pdf_text += page_text + "\n"
            
            st.write(f"✅ Texte extrait: {len(pdf_text)} caractères")
            
            # Afficher un aperçu
            st.subheader("📋 Aperçu du contenu")
            st.text_area("Contenu extrait", pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text, height=200)
            
            # Test de création de données
            st.write("🔍 Test de création des données de projet...")
            project_data = {
                'query_name': 'debug-test',
                'region': 'Morocco',
                'pdf_content': f"PDF: {uploaded_file.name}\n\n{pdf_text[:500]}...",
                'file_name': uploaded_file.name
            }
            
            st.write("✅ Données de projet créées")
            st.json(project_data)
            
            st.success("🎉 Tous les tests sont passés ! Le problème ne vient pas de l'extraction PDF.")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'extraction: {str(e)}")
            st.code(traceback.format_exc())
    
    # Test de l'ARK client
    st.subheader("🔍 Test de l'ARK Client")
    
    if st.button("Test ARK Client"):
        try:
            from ark_client import ARKClient
            client = ARKClient()
            st.write("✅ ARK Client importé avec succès")
            
            # Test simple
            success, agents = client.get_available_agents()
            if success:
                st.write(f"✅ Agents disponibles: {len(agents)}")
                st.write(agents[:5])  # Afficher les 5 premiers
            else:
                st.write(f"❌ Erreur agents: {agents}")
                
        except Exception as e:
            st.error(f"❌ Erreur ARK Client: {str(e)}")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()

