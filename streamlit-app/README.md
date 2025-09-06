# Company Finder Streamlit App

A Streamlit web application that integrates with ARK Company Finder Agent to help users find the best companies for their projects.

## Features

- 🏢 **Project Input Form** - Easy-to-use interface for project details
- 🌍 **Multi-Region Support** - Search in Morocco, Global, or other regions
- 🤖 **AI-Powered Search** - Uses ARK Company Finder Agent
- 📊 **Beautiful Results** - Company cards with ratings and details
- 📤 **Export Functionality** - Download results as CSV or JSON
- ⚡ **Real-time Updates** - Progress tracking and status updates

## Quick Start

### 1. Install Dependencies
```bash
cd streamlit-app
pip install -r requirements.txt
```

### 2. Ensure ARK is Running
Make sure your ARK cluster is running and accessible:
```bash
kubectl get agents
kubectl get tools
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Fill out the project form** in the sidebar:
   - Select project type (Construction, Software, etc.)
   - Choose region (Morocco, Global, etc.)
   - Add budget and timeline (optional)
   - Describe your project requirements

2. **Click "Find Companies"** to start the search

3. **Wait for results** - The AI agent will search the web and analyze companies

4. **Review results** - See top 5 companies with ratings and details

5. **Export results** - Download as CSV or JSON if needed

## Architecture

```
User Input → Streamlit UI → ARK Client → kubectl → ARK Cluster → Company Finder Agent → Web Search → Results → Streamlit Display
```

## Files

- `app.py` - Main Streamlit application
- `ark_client.py` - ARK cluster integration via kubectl
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Requirements

- Python 3.8+
- kubectl configured and accessible
- ARK cluster running with Company Finder Agent
- Internet connection for web searches

## Troubleshooting

### kubectl not found
```bash
# Install kubectl or ensure it's in PATH
which kubectl
```

### ARK cluster not accessible
```bash
# Check cluster connection
kubectl cluster-info
kubectl get agents
```

### Agent not found
```bash
# Deploy the company finder agent
kubectl apply -f ../samples/agents/company-finder-morocco.yaml
kubectl apply -f ../samples/tools/web-search.yaml
```

## Demo

The app provides a simple interface for:
- Project description input
- Region and type selection
- Real-time search progress
- Beautiful company result cards
- Export functionality

Perfect for demonstrating the ARK Company Finder Agent capabilities!
