"""
Test script for the Streamlit app
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ark_client import ARKClient

def test_ark_client():
    """Test the ARK client functionality"""
    print("🧪 Testing ARK Client...")
    
    client = ARKClient()
    
    # Test kubectl connection
    print("1. Testing kubectl connection...")
    success, output = client._run_kubectl("kubectl version --client")
    if success:
        print("✅ kubectl is working")
    else:
        print("❌ kubectl not working:", output)
        return False
    
    # Test getting agents
    print("2. Testing agent retrieval...")
    agents = client.get_available_agents()
    print(f"Available agents: {agents}")
    
    # Test getting tools
    print("3. Testing tool retrieval...")
    tools = client.get_available_tools()
    print(f"Available tools: {tools}")
    
    # Test query generation
    print("4. Testing query generation...")
    project_data = {
        'query_name': 'test-query',
        'type': 'Construction',
        'region': 'Morocco',
        'budget': '$100K',
        'timeline': '6 months',
        'description': 'Build a small office building'
    }
    
    query_yaml = client._generate_query_yaml(project_data)
    print("✅ Query YAML generated successfully")
    print("Query preview:")
    print(query_yaml[:200] + "...")
    
    return True

if __name__ == "__main__":
    test_ark_client()
