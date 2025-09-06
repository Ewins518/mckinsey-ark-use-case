# 🔄 Workflow Simple - PDF Company Finder

## Architecture Visuelle

```
┌─────────────────────────────────────────────────────────────────┐
│                    🤖 ARK PDF COMPANY FINDER                    │
└─────────────────────────────────────────────────────────────────┘

👤 UTILISATEUR
    │
    ▼
┌─────────────────┐
│ 📱 Streamlit    │
│ Interface       │
└─────────────────┘
    │
    ▼ (Upload PDF)
┌─────────────────┐
│ 📄 PyPDF2       │
│ Extraction      │
└─────────────────┘
    │
    ▼ (PDF Content)
┌─────────────────────────────────────────────────────────────────┐
│                    👥 PDF COMPANY FINDER TEAM                   │
│                        (Sequential Strategy)                    │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 📄 PDF Analyzer │───▶│ 🎯 Coordinator  │───▶│ 🏢 Company      │
│                 │    │                 │    │    Finder       │
│ • Lit PDF       │    │ • Coordonne     │    │ • Recherche     │
│ • Extrait info  │    │ • Valide data   │    │ • Évalue        │
│ • Structure     │    │ • Prépare       │    │ • Classe        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
    │                         │                         │
    ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 📁 MCP          │    │ 🤖 GPT-4.1      │    │ 🌐 Web Search   │
│ Filesystem      │    │ AI Model        │    │ DuckDuckGo      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        📊 RÉSULTATS                            │
│                                                                 │
│ 🏢 Top 5 Entreprises avec Ratings                              │
│ • SICOPA (9.5/10) - Casablanca                                 │
│ • Tectis Maroc (9.2/10) - Casablanca                           │
│ • Uniformes Maroc (9.0/10) - Casablanca                        │
│ • + 2 autres entreprises                                       │
│                                                                 │
│ 📤 Export CSV/JSON disponible                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Step-by-Step

```
1. 📄 UPLOAD PDF
   └── Utilisateur upload un PDF d'appel d'offres
       └── Streamlit traite le fichier avec PyPDF2

2. 🔍 EXTRACTION
   └── Texte extrait du PDF
       └── Contenu structuré pour l'analyse

3. 🤖 ANALYSE PDF (PDF Analyzer)
   └── Lit le contenu via MCP Filesystem
       └── Extrait: type projet, budget, exigences, localisation
           └── Structure les données JSON

4. 🎯 COORDINATION (Project Coordinator)
   └── Reçoit les données du PDF Analyzer
       └── Valide et enrichit les informations
           └── Prépare la description pour la recherche

5. 🏢 RECHERCHE ENTREPRISES (Company Finder)
   └── Utilise Web Search (DuckDuckGo)
       └── Trouve les entreprises appropriées
           └── Évalue et classe par pertinence

6. 📊 PRÉSENTATION
   └── Résultats affichés dans Streamlit
       └── Cartes d'entreprises avec ratings
           └── Export CSV/JSON disponible
```

## Agents et leurs Rôles

```
┌─────────────────────────────────────────────────────────────────┐
│                        🎯 LES 3 AGENTS                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 📄 PDF ANALYZER │  │ 🎯 COORDINATOR  │  │ 🏢 COMPANY      │
│                 │  │                 │  │    FINDER       │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ Rôle:           │  │ Rôle:           │  │ Rôle:           │
│ • Lit PDF       │  │ • Orchestre     │  │ • Recherche     │
│ • Extrait info  │  │ • Valide data   │  │ • Évalue        │
│ • Structure     │  │ • Prépare       │  │ • Classe        │
│                 │  │                 │  │                 │
│ Outils:         │  │ Outils:         │  │ Outils:         │
│ • MCP Filesys   │  │ • Aucun         │  │ • Web Search    │
│                 │  │                 │  │                 │
│ Sortie:         │  │ Sortie:         │  │ Sortie:         │
│ • Project info  │  │ • Coordinated   │  │ • Top 5         │
│ • Requirements  │  │   description   │  │   companies     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Technologies Utilisées

```
┌─────────────────────────────────────────────────────────────────┐
│                      🛠️ STACK TECHNOLOGIQUE                    │
└─────────────────────────────────────────────────────────────────┘

🏗️ Infrastructure:
├── ☸️ Kubernetes (Orchestration)
├── 🤖 ARK Platform (Agent Management)
└── 🔐 Kubernetes Secrets (API Keys)

🤖 AI & Models:
├── 🧠 GPT-4.1 (Azure OpenAI)
├── 🔌 MCP Protocol (Communication)
└── 🌐 DuckDuckGo API (Web Search)

📁 Data & Storage:
├── 💾 Persistent Volume (File Storage)
├── 📄 PyPDF2 (PDF Processing)
└── 📊 JSON (Structured Output)

📱 User Interface:
├── 📱 Streamlit (Web Interface)
├── 🎨 Plotly (Visualizations)
└── 📤 CSV/JSON Export
```

## Exemple de Résultats

```
┌─────────────────────────────────────────────────────────────────┐
│                    📊 EXEMPLE DE RÉSULTATS                     │
└─────────────────────────────────────────────────────────────────┘

📄 Document analysé: Appel d'offres habillement et textile brandé
🌍 Région: Maroc
⏱️ Temps de traitement: ~30 secondes

🏢 TOP 5 ENTREPRISES TROUVÉES:

1. 🥇 SICOPA (9.5/10) ⭐⭐⭐⭐⭐
   📍 Casablanca, Maroc
   🎯 Project Fit: High
   🔍 Spécialisation: Habillement professionnel, textile brandé
   💡 Pourquoi: Leader marocain, expérience avec les aéroports

2. 🥈 Tectis Maroc (9.2/10) ⭐⭐⭐⭐⭐
   📍 Casablanca, Maroc
   🎯 Project Fit: High
   🔍 Spécialisation: Uniformes, équipements professionnels
   💡 Pourquoi: Expertise textile, qualité reconnue

3. 🥉 Uniformes Maroc (9.0/10) ⭐⭐⭐⭐⭐
   📍 Casablanca, Maroc
   🎯 Project Fit: High
   🔍 Spécialisation: Uniformes corporatifs, textile technique
   💡 Pourquoi: Spécialiste uniformes, marché local

4. 🏅 [Entreprise 4] (8.5/10) ⭐⭐⭐⭐
5. 🏅 [Entreprise 5] (8.0/10) ⭐⭐⭐⭐

📊 STATISTIQUES:
• Note moyenne: 8.8/10
• Entreprises High Fit: 5/5
• Total entreprises: 5
• Temps de recherche: 25s
```

## Avantages du Système

```
┌─────────────────────────────────────────────────────────────────┐
│                      ✨ AVANTAGES CLÉS                         │
└─────────────────────────────────────────────────────────────────┘

🚀 AUTOMATISATION:
├── ✅ Analyse PDF automatique
├── ✅ Recherche d'entreprises intelligente
├── ✅ Évaluation et classement automatique
└── ✅ Génération de rapports structurés

🎯 PRÉCISION:
├── ✅ Extraction précise des exigences
├── ✅ Recherche ciblée par région
├── ✅ Évaluation basée sur l'expérience
└── ✅ Justifications détaillées

⚡ EFFICACITÉ:
├── ✅ Traitement en ~30 secondes
├── ✅ Interface utilisateur simple
├── ✅ Export des résultats
└── ✅ Workflow entièrement automatisé

🔧 EXTENSIBILITÉ:
├── ✅ Facile d'ajouter de nouveaux agents
├── ✅ Support multi-régions
├── ✅ Intégration avec d'autres systèmes
└── ✅ Personnalisation des critères
```

