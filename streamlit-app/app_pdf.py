"""
PDF Company Finder Streamlit App
Analyzes PDF documents and finds suitable companies using AI agents
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ark_client import ARKClient
import time
import json
import base64
import tempfile
import os
import PyPDF2
import io


def main():
    st.set_page_config(
        page_title="PDF Company Finder",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF Company Finder")
    st.markdown("Upload a PDF document (tender, RFP, project specification) and find the best companies using AI-powered analysis")
    
    # Initialize ARK client
    if 'ark_client' not in st.session_state:
        st.session_state.ark_client = ARKClient()
    
    # Main input area
    st.header("📄 Upload Your Document")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document containing project requirements, tender specifications, or RFP details"
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
    if submit_button and uploaded_file is not None:
        # Generate unique query name
        query_name = f"pdf-query-{int(time.time())}"
        
        try:
            # Debug information
            st.info(f"🔍 Processing file: {uploaded_file.name} ({len(uploaded_file.getvalue())} bytes)")
            
            # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
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
                pdf_text = f"PDF Document: {uploaded_file.name}\nSize: {len(uploaded_file.getvalue())} bytes\n\nThis PDF document contains project specifications but text extraction was not successful. Please analyze it based on the filename and provide recommendations for suitable companies."
            else:
                pdf_text = f"PDF Document: {uploaded_file.name}\n\nExtracted Content:\n{pdf_text}"
            
            st.success(f"✅ Text extracted: {len(pdf_text)} characters")
            
            # Prepare project data
            project_data = {
                'query_name': query_name,
                'region': region,
                'pdf_content': pdf_text,
                'file_name': uploaded_file.name
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
                        display_pdf_results(results, uploaded_file.name)
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
            
            # Afficher plus de détails pour l'erreur 403
            if "403" in str(e) or "Forbidden" in str(e):
                st.error("🚫 Erreur 403 - Accès interdit")
                st.info("""
                **Solutions possibles:**
                1. Vérifiez que le fichier PDF n'est pas corrompu
                2. Essayez avec un fichier PDF plus petit
                3. Vérifiez les permissions du fichier
                4. Redémarrez l'application Streamlit
                """)
            
            # Afficher la trace complète en mode debug
            import traceback
            with st.expander("🔍 Détails de l'erreur (Debug)"):
                st.code(traceback.format_exc())
    
    elif submit_button and uploaded_file is None:
        st.warning("⚠️ Please upload a PDF file")
    
    # Show example
    with st.expander("📋 Example Documents", expanded=False):
        st.markdown("""
        **Supported PDF Types:**
        - 📋 Tender documents (Appels d'offres)
        - 📄 Request for Proposals (RFP)
        - 🏗️ Project specifications
        - 📊 Technical requirements
        - 💼 Business proposals
        
        **What the AI will extract:**
        - Project type and scope
        - Technical requirements
        - Budget and timeline information
        - Location and regional requirements
        - Key success factors
        - Required qualifications
        """)


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
