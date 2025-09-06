#!/bin/bash

# Deploy PDF Company Finder Workflow
# This script deploys all the agents and teams needed for PDF analysis workflow

set -e

echo "🚀 Deploying PDF Company Finder Workflow..."

# Deploy the PDF analyzer agent
echo "📄 Deploying PDF Analyzer Agent..."
kubectl apply -f samples/agents/pdf-analyzer.yaml

# Deploy the project coordinator agent
echo "🎯 Deploying Project Coordinator Agent..."
kubectl apply -f samples/agents/project-coordinator.yaml

# Deploy the company finder agents (if not already deployed)
echo "🏢 Deploying Company Finder Agents..."
kubectl apply -f samples/agents/company-finder.yaml
kubectl apply -f samples/agents/company-finder-morocco.yaml

# Deploy the teams
echo "👥 Deploying Teams..."
kubectl apply -f samples/teams/pdf-company-finder-team.yaml

# Wait for resources to be ready
echo "⏳ Waiting for resources to be ready..."
kubectl wait --for=condition=ready --timeout=60s agent/pdf-analyzer
kubectl wait --for=condition=ready --timeout=60s agent/project-coordinator
kubectl wait --for=condition=ready --timeout=60s team/pdf-company-finder-team
kubectl wait --for=condition=ready --timeout=60s team/pdf-company-finder-team-morocco

# Verify deployment
echo "✅ Verifying deployment..."
echo "Agents:"
kubectl get agents -l category=document-analysis
kubectl get agents -l category=coordination
kubectl get agents -l category=business

echo "Teams:"
kubectl get teams -l workflow=pdf-analysis

echo "🎉 PDF Company Finder Workflow deployed successfully!"
echo ""
echo "📋 Available resources:"
echo "  - pdf-analyzer (PDF document analysis)"
echo "  - project-coordinator (Workflow coordination)"
echo "  - company-finder (Global company research)"
echo "  - company-finder-morocco (Moroccan company research)"
echo "  - pdf-company-finder-team (Global team)"
echo "  - pdf-company-finder-team-morocco (Morocco team)"
echo ""
echo "🚀 You can now use the Streamlit app with PDF upload functionality!"
