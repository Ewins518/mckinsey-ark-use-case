#!/bin/bash

# Company Finder Agent Deployment Script
# This script deploys all components needed for the company finder agent

set -e

echo "🚀 Deploying Company Finder Agent"
echo "================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check cluster connectivity
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    exit 1
fi

echo "✅ Kubernetes cluster connection verified"

# Deploy web search tool
echo "📡 Deploying web search tool..."
kubectl apply -f samples/tools/web-search.yaml

# Deploy company finder agent
echo "🤖 Deploying company finder agent..."
kubectl apply -f samples/agents/company-finder.yaml

# Wait for resources to be ready
echo "⏳ Waiting for resources to be ready..."
kubectl wait --for=condition=Ready --timeout=60s tool/web-search 2>/dev/null || echo "⚠️  Tool readiness check skipped"
kubectl wait --for=condition=Ready --timeout=60s agent/company-finder 2>/dev/null || echo "⚠️  Agent readiness check skipped"

echo "✅ Company Finder Agent deployed successfully!"
echo ""
echo "📋 Available Resources:"
echo "   - Tool: web-search"
echo "   - Agent: company-finder"
echo ""
echo "🎯 Next Steps:"
echo "   1. Deploy example queries:"
echo "      kubectl apply -f samples/queries/company-finder-examples.yaml"
echo ""
echo "   2. Execute a test query:"
echo "      ark query execute company-finder-healthcare-app"
echo ""
echo "   3. Or create your own query:"
echo "      kubectl apply -f samples/queries/company-finder-template.yaml"
echo ""
echo "📚 Documentation: samples/agents/README-company-finder.md"
echo "🧪 Test Script: ./samples/agents/test-company-finder.sh"
