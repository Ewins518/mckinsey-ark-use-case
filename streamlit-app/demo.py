"""
Demo script showing how the Company Finder app works
"""

import time
from ark_client import ARKClient

def demo_company_finder():
    """Demonstrate the company finder functionality"""
    print("🎯 Company Finder Demo")
    print("=====================")
    
    client = ARKClient()
    
    # Demo project data - much simpler now!
    project_description = """I need to build a modern office complex project. The project includes:

- 3 office buildings (each 20,000 sq ft)
- Modern glass facade and steel structure
- HVAC systems and electrical infrastructure
- Parking garage for 200 vehicles
- Landscaping and exterior work
- Interior fit-out for office spaces

The project timeline is 12-18 months with a budget of $500K-$1M. We need a construction company that has experience with commercial office buildings, modern construction techniques, and can deliver on time and within budget.

Please find the top 5 companies that would be best suited for this project."""

    project_data = {
        'query_name': f'demo-query-{int(time.time())}',
        'region': 'Morocco',
        'description': project_description
    }
    
    print(f"📝 Project Description:")
    print(project_description[:200] + "...")
    print(f"🌍 Region: {project_data['region']}")
    print()
    
    # Create query
    print("🚀 Creating query...")
    print(f"Project data: {project_data}")
    success, message = client.create_query(project_data)
    print(f"Result: success={success}, message='{message}'")
    
    if success:
        print(f"✅ Query created: {message}")
        
        # Wait for completion
        print("⏳ Waiting for results...")
        completed, result = client.wait_for_completion(project_data['query_name'])
        
        if completed:
            print("✅ Search completed!")
            
            # Get results
            success, results = client.get_query_results(project_data['query_name'])
            
            if success and results:
                print("\n🏆 Top Companies Found:")
                print("=" * 50)
                
                companies = results.get('companies', [])
                for company in companies:
                    print(f"\n#{company.get('rank', 'N/A')} {company.get('name', 'Unknown')}")
                    print(f"   Rating: {company.get('rating', 0)}/10")
                    print(f"   Location: {company.get('location', 'N/A')}")
                    print(f"   Website: {company.get('website', 'N/A')}")
                    print(f"   Project Fit: {company.get('project_fit', 'N/A')}")
                    print(f"   Specialization: {company.get('specialization', 'N/A')[:100]}...")
                
                print(f"\n📊 Summary: Found {len(companies)} companies")
                
                # Cleanup
                client.delete_query(project_data['query_name'])
                print("🧹 Cleaned up query")
                
            else:
                print("❌ Failed to retrieve results")
        else:
            print(f"❌ Query failed: {result}")
    else:
        print(f"❌ Failed to create query: {message}")

if __name__ == "__main__":
    demo_company_finder()
