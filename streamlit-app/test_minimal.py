"""
Minimal test to verify Streamlit app works
"""

import streamlit as st
from ark_client import ARKClient
import time

st.title("🧪 Company Finder Test")

if st.button("Test Query"):
    client = ARKClient()
    
    project_data = {
        'query_name': f'test-{int(time.time())}',
        'region': 'Morocco',
        'description': 'Build a small office building'
    }
    
    st.write("Creating query...")
    success, message = client.create_query(project_data)
    
    if success:
        st.success(f"Query created: {message}")
        query_name = message
        
        # Wait for completion
        st.write("Waiting for completion...")
        for i in range(20):
            status_success, status = client.get_query_status(query_name)
            st.write(f"Status: {status}")
            
            if status == "done":
                st.success("Query completed!")
                
                # Get results
                success, results = client.get_query_results(query_name)
                
                if success and results:
                    st.write("Results received!")
                    companies = results.get('companies', [])
                    st.write(f"Found {len(companies)} companies:")
                    
                    for company in companies:
                        st.write(f"- {company.get('name', 'Unknown')} ({company.get('rating', 0)}/10)")
                else:
                    st.error("Failed to get results")
                
                # Clean up
                client.delete_query(query_name)
                break
            elif status == "error":
                st.error("Query failed")
                break
            
            time.sleep(2)
    else:
        st.error(f"Failed to create query: {message}")

