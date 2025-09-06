"""
Quick test to verify the Streamlit app components work
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ark_client import ARKClient

def test_complete_flow():
    """Test the complete flow from query creation to results"""
    print("🧪 Testing Complete Flow")
    print("========================")
    
    client = ARKClient()
    
    # Test project data
    project_data = {
        'query_name': f'test-flow-{int(time.time())}',
        'region': 'Morocco',
        'description': 'Build a small office building with 2 floors, parking, and modern design. Budget: $200K, Timeline: 6 months.'
    }
    
    print("1. Creating query...")
    success, message = client.create_query(project_data)
    print(f"   Result: {success}, {message}")
    
    if success:
        query_name = message
        print("2. Waiting for completion...")
        
        # Wait for completion
        max_attempts = 30
        for attempt in range(max_attempts):
            status_success, status = client.get_query_status(query_name)
            print(f"   Attempt {attempt+1}: {status}")
            
            if status_success and status == "done":
                print("3. Getting results...")
                success, results = client.get_query_results(query_name)
                
                if success and results:
                    companies = results.get('companies', [])
                    print(f"   Found {len(companies)} companies:")
                    for company in companies:
                        print(f"   - {company.get('name', 'Unknown')} ({company.get('rating', 0)}/10)")
                    
                    # Clean up
                    client.delete_query(query_name)
                    print("4. Cleaned up query")
                    return True
                else:
                    print("   Failed to get results")
                    break
            elif status_success and status == "error":
                print("   Query failed")
                break
            
            time.sleep(2)
        else:
            print("   Timeout waiting for completion")
    
    return False

if __name__ == "__main__":
    import time
    test_complete_flow()
