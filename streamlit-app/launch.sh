#!/bin/bash

echo "🚀 Launching Company Finder Streamlit App"
echo "=========================================="

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check ARK cluster
echo "🔍 Checking ARK cluster..."
if kubectl get agents | grep -q "company-finder"; then
    echo "✅ Company Finder agents are available"
else
    echo "⚠️  Warning: Company Finder agents not found"
fi

echo ""
echo "🌐 Starting Streamlit app..."
echo "The app will open at: http://localhost:8501"
echo ""

# Launch the app
streamlit run app.py --server.port 8501 --server.address localhost
