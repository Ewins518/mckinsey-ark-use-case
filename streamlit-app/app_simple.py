"""
Simple Company Finder Streamlit App
Clean and professional version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ark_client import ARKClient
import time
import json


def main():
    st.set_page_config(
        page_title="Company Finder",
        page_icon="🏢",
        layout="wide"
    )
    
    st.title("🏢 Company Finder")
    st.markdown("Find the best companies for your project using AI-powered research")
    
    # Initialize ARK client
    if 'ark_client' not in st.session_state:
        st.session_state.ark_client = ARKClient()
    
    # Main input area
    st.header("📝 Describe Your Project")
    
    # Simple text input for entire project description
    project_description = st.text_area(
        "Project Description",
        height=150,
        help="Describe your project in detail. Include requirements, budget, timeline, and any specific needs."
    )
    
    # Region selection (simple)
    region = st.selectbox(
        "🌍 Search Region",
        ["Morocco", "Global", "Europe", "North America", "Asia"],
        help="Choose the region where you want to find companies"
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.button("🔍 Find Companies", type="primary", use_container_width=True)
    
    # Process the request
    if submit_button and project_description:
        # Generate unique query name
        query_name = f"query-{int(time.time())}"
        
        # Prepare project data
        project_data = {
            'query_name': query_name,
            'region': region,
            'description': project_description
        }
        
        # Create query
        with st.spinner("Creating query..."):
            success, message = st.session_state.ark_client.create_query(project_data)
        
        if success:
            st.success(f"✅ Query created: {query_name}")
            
            # Simple spinner while waiting for results
            with st.spinner("🔍 AI is searching for the best companies..."):
                # Wait for completion
                completed, result = st.session_state.ark_client.wait_for_completion(query_name)
            
            if completed:
                # Get results immediately
                success, results = st.session_state.ark_client.get_query_results(query_name)
                
                if success and results:
                    display_results(results)
                    # Clean up the query
                    st.session_state.ark_client.delete_query(query_name)
                else:
                    st.error("❌ Failed to retrieve results")
            else:
                st.error(f"❌ Query failed: {result}")
        else:
            st.error(f"❌ Failed to create query: {message}")
    
    elif submit_button and not project_description:
        st.warning("⚠️ Please provide a project description")


def display_results(results: dict):
    """Display the search results in a beautiful format"""
    
    st.header("🎯 Top Companies Found")
    
    if 'companies' in results and results['companies']:
        companies = results['companies']
        
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
        st.header("📊 Summary")
        
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
        st.header("📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to CSV"):
                df = pd.DataFrame(companies)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"companies_{int(time.time())}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Export to JSON"):
                json_data = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"companies_{int(time.time())}.json",
                    mime="application/json"
                )
    
    else:
        st.error("❌ No companies found in the results")


if __name__ == "__main__":
    main()
