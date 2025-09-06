"""
Version alternative qui utilise le PDF local au lieu de l'upload
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ark_client import ARKClient
import time
import json
import PyPDF2
import io

def main():
    st.set_page_config(
        page_title="PDF Company Finder (Local)",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF Company Finder (Version Locale)")
    st.markdown("Version qui utilise le PDF local pour contourner les problèmes d'upload")
    
    # Initialize ARK client
    if 'ark_client' not in st.session_state:
        st.session_state.ark_client = ARKClient()
    
    # PDF Selection
    st.header("📄 Sélection du PDF")
    
    # Liste des PDFs disponibles
    import os
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if pdf_files:
        selected_pdf = st.selectbox(
            "Choisir un PDF à analyser:",
            pdf_files,
            help="Sélectionnez un fichier PDF local"
        )
        
        # Region selection
        region = st.selectbox(
            "🌍 Search Region",
            ["Morocco", "Global", "Europe", "North America", "Asia"],
            help="Choose the region where you want to find companies"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.button("🔍 Analyze PDF & Find Companies", type="primary", use_container_width=True)
        
        # Process the request
        if submit_button and selected_pdf:
            # Generate unique query name
            query_name = f"pdf-query-{int(time.time())}"
            
            try:
                # Read and extract PDF content
                st.info(f"🔍 Processing file: {selected_pdf}")
                
                with open(selected_pdf, 'rb') as file:
                    pdf_content = file.read()
                
                st.info(f"📊 File size: {len(pdf_content)} bytes")
                
                # Extract text from PDF
                with st.spinner("Extracting text from PDF..."):
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                    pdf_text = ""
                    
                    # Limit to first 10 pages for performance
                    max_pages = min(10, len(pdf_reader.pages))
                    st.info(f"📄 Processing {max_pages} pages out of {len(pdf_reader.pages)} total pages")
                    
                    for page_num in range(max_pages):
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        pdf_text += page_text + "\n"
                
                # If no text extracted, provide fallback
                if not pdf_text.strip():
                    pdf_text = f"PDF Document: {selected_pdf}\nSize: {len(pdf_content)} bytes\n\nThis PDF document contains project specifications but text extraction was not successful. Please analyze it based on the filename and provide recommendations for suitable companies."
                else:
                    pdf_text = f"PDF Document: {selected_pdf}\n\nExtracted Content:\n{pdf_text}"
                
                st.success(f"✅ Text extracted: {len(pdf_text)} characters")
                
                # Show preview
                with st.expander("📋 Aperçu du contenu extrait"):
                    st.text(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)
                
                # Prepare project data
                project_data = {
                    'query_name': query_name,
                    'region': region,
                    'pdf_content': pdf_text,
                    'file_name': selected_pdf
                }
                
                # Create query
                with st.spinner("Creating query..."):
                    success, message = st.session_state.ark_client.create_pdf_query(project_data)
                
                if success:
                    st.success(f"✅ Query created: {query_name}")
                    
                    # Show progress steps
                    progress_container = st.container()
                    with progress_container:
                        st.info("🔄 Processing workflow:")
                        st.write("1. 📄 Analyzing PDF document...")
                        st.write("2. 🔍 Extracting project requirements...")
                        st.write("3. 🏢 Researching suitable companies...")
                        st.write("4. 📊 Generating recommendations...")
                    
                    # Wait for completion
                    with st.spinner("🤖 AI agents are working on your request..."):
                        completed, result = st.session_state.ark_client.wait_for_completion(query_name)
                    
                    if completed:
                        # Get results immediately
                        success, results = st.session_state.ark_client.get_query_results(query_name)
                        
                        if success and results:
                            display_pdf_results(results, selected_pdf)
                            # Clean up the query
                            st.session_state.ark_client.delete_query(query_name)
                        else:
                            st.error("❌ Failed to retrieve results")
                    else:
                        st.error(f"❌ Query failed: {result}")
                else:
                    st.error(f"❌ Failed to create query: {message}")
            
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
                st.error(f"Error type: {type(e).__name__}")
                
                # Afficher la trace complète en mode debug
                import traceback
                with st.expander("🔍 Détails de l'erreur (Debug)"):
                    st.code(traceback.format_exc())
    
    else:
        st.warning("⚠️ Aucun fichier PDF trouvé dans le répertoire courant")
        st.info("Placez un fichier PDF dans le répertoire streamlit-app pour l'utiliser")


def display_pdf_results(results: dict, filename: str):
    """Display the PDF analysis and company search results"""
    
    st.header("🎯 Analysis Results")
    st.info(f"📄 **Document Analyzed:** {filename}")
    
    # Project Summary
    if 'project_summary' in results:
        st.subheader("📋 Project Summary")
        st.write(results['project_summary'])
    
    # Project Requirements
    if 'project_requirements' in results and results['project_requirements']:
        st.subheader("📝 Project Requirements")
        for i, requirement in enumerate(results['project_requirements'], 1):
            st.write(f"{i}. {requirement}")
    
    # Company Recommendations
    companies = None
    if 'recommended_companies' in results and results['recommended_companies']:
        companies = results['recommended_companies']
        st.subheader("🏢 Recommended Companies")
    elif 'companies' in results and results['companies']:
        companies = results['companies']
        st.subheader("🏢 Recommended Companies")
    
    if companies:
        
        # Create company cards
        for i, company in enumerate(companies):
            with st.expander(f"#{company.get('rank', i+1)} {company.get('name', 'Unknown')} - {company.get('rating', 0)}/10 ⭐", expanded=(i==0)):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**🏢 Company:** {company.get('name', 'N/A')}")
                    st.markdown(f"**🌐 Website:** [{company.get('website', 'N/A')}]({company.get('website', '#')})")
                    if 'location' in company:
                        st.markdown(f"**📍 Location:** {company.get('location', 'N/A')}")
                    st.markdown(f"**⭐ Rating:** {company.get('rating', 0)}/10")
                    st.markdown(f"**🎯 Project Fit:** {company.get('project_fit', 'N/A')}")
                
                with col2:
                    # Rating visualization
                    rating = company.get('rating', 0)
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = rating,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Rating"},
                        gauge = {
                            'axis': {'range': [None, 10]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 5], 'color': "lightgray"},
                                {'range': [5, 8], 'color': "yellow"},
                                {'range': [8, 10], 'color': "green"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 9
                            }
                        }
                    ))
                    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Company details
                st.markdown("**🔍 Specialization:**")
                st.write(company.get('specialization', 'N/A'))
                
                st.markdown("**💡 Why they're suitable:**")
                st.write(company.get('suitability_reason', 'N/A'))
                
                st.markdown("**🏆 Notable Experience:**")
                st.write(company.get('notable_experience', 'N/A'))
        
        # Summary statistics
        st.subheader("📊 Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_rating = sum(c.get('rating', 0) for c in companies) / len(companies)
            st.metric("Average Rating", f"{avg_rating:.1f}/10")
        
        with col2:
            high_fit = len([c for c in companies if c.get('project_fit') == 'High'])
            st.metric("High Fit Companies", high_fit)
        
        with col3:
            st.metric("Total Companies", len(companies))
        
        # Export functionality
        st.subheader("📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to CSV"):
                df = pd.DataFrame(companies)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"pdf_companies_{int(time.time())}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Export to JSON"):
                json_data = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"pdf_analysis_{int(time.time())}.json",
                    mime="application/json"
                )
    
    else:
        st.error("❌ No companies found in the results")
    
    # Analysis methodology
    if 'analysis_methodology' in results:
        st.subheader("🔬 Analysis Methodology")
        st.write(results['analysis_methodology'])


if __name__ == "__main__":
    main()
