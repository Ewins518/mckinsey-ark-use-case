"""
Version ultra-simple pour tester l'upload de fichier
"""

import streamlit as st

def main():
    st.title("📄 Test Upload Simple")
    
    # Test d'upload basique
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file is not None:
        st.write("✅ Fichier uploadé avec succès!")
        st.write(f"Nom: {uploaded_file.name}")
        st.write(f"Taille: {len(uploaded_file.getvalue())} bytes")
        
        # Test de lecture du contenu
        try:
            content = uploaded_file.getvalue()
            st.write(f"✅ Contenu lu: {len(content)} bytes")
            
            # Test d'écriture dans un fichier temporaire
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(content)
                st.write(f"✅ Fichier temporaire créé: {tmp.name}")
            
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    # Test de bouton simple
    if st.button("Test Bouton"):
        st.write("✅ Bouton fonctionne!")

if __name__ == "__main__":
    main()

