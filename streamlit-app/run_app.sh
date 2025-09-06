#!/bin/bash

# Company Finder Streamlit App Launcher

echo "🚀 Starting Company Finder Streamlit App..."
echo "============================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run from streamlit-app directory."
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check kubectl connection
echo "🔍 Checking ARK cluster connection..."
if kubectl cluster-info &> /dev/null; then
    echo "✅ ARK cluster is accessible"
else
    echo "❌ Warning: ARK cluster not accessible. Make sure kubectl is configured."
fi

# Check if agents are available
echo "🤖 Checking available agents..."
agents=$(kubectl get agents -o jsonpath='{.items[*].metadata.name}' 2>/dev/null)
if [[ $agents == *"company-finder"* ]]; then
    echo "✅ Company Finder agents are available"
else
    echo "⚠️  Warning: Company Finder agents not found. Deploy them first:"
    echo "   kubectl apply -f ../samples/agents/company-finder-morocco.yaml"
    echo "   kubectl apply -f ../samples/tools/web-search.yaml"
fi

echo ""
echo "🌐 Starting Streamlit app..."
echo "The app will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

# Start the app
streamlit run app.py --server.port 8501 --server.address localhost
