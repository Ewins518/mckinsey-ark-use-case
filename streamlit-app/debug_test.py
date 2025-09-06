"""
Debug test for the ARK client
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ark_client import ARKClient

def debug_test():
    """Debug the ARK client"""
    print("🔍 Debug Test")
    print("=============")
    
    client = ARKClient()
    
    # Test simple project data
    project_data = {
        'query_name': 'debug-test-query',
        'region': 'Morocco',
        'description': 'Build a small office building'
    }
    
    print("1. Generating query YAML...")
    query_yaml = client._generate_query_yaml(project_data)
    print("Generated YAML:")
    print(query_yaml)
    print()
    
    print("2. Testing kubectl apply...")
    # Write to temp file
    temp_file = "/tmp/debug_query.yaml"
    with open(temp_file, 'w') as f:
        f.write(query_yaml)
    
    print(f"Written to: {temp_file}")
    
    # Test kubectl apply
    success, output = client._run_kubectl(f"kubectl apply -f {temp_file}")
    print(f"Success: {success}")
    print(f"Output: {output}")
    
    if success:
        print("3. Checking query status...")
        success, status = client.get_query_status('debug-test-query')
        print(f"Status: {status}")
        
        # Clean up
        client.delete_query('debug-test-query')
        print("Cleaned up query")
    
    # Clean up temp file
    try:
        os.remove(temp_file)
        print("Cleaned up temp file")
    except:
        pass

if __name__ == "__main__":
    debug_test()
