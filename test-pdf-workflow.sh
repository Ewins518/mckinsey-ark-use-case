#!/bin/bash

# Test PDF Workflow
echo "🧪 Testing PDF Company Finder Workflow..."

# Create a simple test PDF content
echo "Creating test PDF content..."
cat > /tmp/test-construction-project.pdf << 'EOF'
CONSTRUCTION PROJECT SPECIFICATION

Project Title: Modern Office Building Construction
Location: Casablanca, Morocco
Budget: $2M - $3M
Timeline: 12-18 months

Project Description:
Construction of a modern 3-story office building with the following specifications:

Technical Requirements:
- Steel and glass facade construction
- Modern HVAC systems
- Electrical infrastructure
- Parking for 50 vehicles
- Landscaping and exterior work
- Interior fit-out for office spaces

Key Success Factors:
- Experience with commercial office buildings
- Modern construction techniques
- On-time delivery capability
- Budget management expertise
- Local market knowledge

Required Qualifications:
- Minimum 5 years experience in commercial construction
- Licensed construction company in Morocco
- Proven track record with office buildings
- Financial stability and bonding capacity

Please find the top 5 construction companies suitable for this project.
EOF

echo "✅ Test PDF content created"

# Apply the test query
echo "🚀 Creating test query..."
kubectl apply -f samples/queries/test-pdf-workflow.yaml

echo "⏳ Query created. You can monitor progress with:"
echo "   kubectl get query test-pdf-workflow -w"
echo ""
echo "📊 To see results when complete:"
echo "   kubectl get query test-pdf-workflow -o yaml"
echo ""
echo "🧹 To clean up:"
echo "   kubectl delete query test-pdf-workflow"
echo "   rm /tmp/test-construction-project.pdf"
