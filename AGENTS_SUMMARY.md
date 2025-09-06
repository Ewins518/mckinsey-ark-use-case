# 🤖 Résumé des Agents ARK - Système Company Finder

## 📋 Vue d'ensemble

Le système ARK Company Finder utilise **3 agents spécialisés** qui travaillent en équipe pour analyser des documents PDF (appels d'offres) et trouver les meilleures entreprises pour exécuter les projets.

---

## 🎯 Agents Principaux

### 1. 📄 **PDF Analyzer** (`pdf-analyzer`)
**Rôle :** Analyseur de documents PDF
**Catégorie :** Document Analysis
**Outils :** `mcp-filesys-read-file`

**Fonctionnalités :**
- ✅ Lit et analyse les documents PDF (appels d'offres, spécifications)
- ✅ Extrait les informations clés du projet
- ✅ Identifie les exigences techniques et le budget
- ✅ Structure les données pour les autres agents

**Sortie :**
```json
{
  "project_type": "construction",
  "project_title": "Bâtiment de bureaux",
  "location": "Casablanca, Maroc",
  "budget_range": "2M-3M MAD",
  "technical_requirements": ["..."],
  "key_success_factors": ["..."],
  "project_description": "..."
}
```

### 2. 🎯 **Project Coordinator** (`project-coordinator`)
**Rôle :** Coordinateur de workflow
**Catégorie :** Coordination
**Outils :** Aucun (orchestrateur)

**Fonctionnalités :**
- ✅ Coordonne le flux d'informations entre les agents
- ✅ Intègre les résultats de l'analyse PDF
- ✅ Prépare les données pour la recherche d'entreprises
- ✅ Assure la qualité et la cohérence des résultats

**Sortie :**
```json
{
  "project_summary": "...",
  "project_requirements": ["..."],
  "recommended_companies": [...],
  "analysis_methodology": "..."
}
```

### 3. 🏢 **Company Finder** (`company-finder` / `company-finder-morocco`)
**Rôle :** Rechercheur d'entreprises
**Catégorie :** Business Research
**Outils :** `web-search`

**Fonctionnalités :**
- ✅ Recherche des entreprises spécialisées
- ✅ Évalue les capacités et l'expérience
- ✅ Classe les entreprises par pertinence
- ✅ Fournit des recommandations détaillées

**Sortie :**
```json
{
  "companies": [
    {
      "rank": 1,
      "name": "TGCC",
      "rating": 9.5,
      "location": "Casablanca, Morocco",
      "specialization": "...",
      "suitability_reason": "...",
      "project_fit": "High"
    }
  ]
}
```

---

## 👥 Teams (Équipes)

### **PDF Company Finder Team** (`pdf-company-finder-team`)
**Stratégie :** Sequential (Séquentielle)
**Membres :**
1. `pdf-analyzer` → Analyse le PDF
2. `project-coordinator` → Coordonne les résultats
3. `company-finder` → Trouve les entreprises

### **PDF Company Finder Team Morocco** (`pdf-company-finder-team-morocco`)
**Stratégie :** Sequential (Séquentielle)
**Membres :**
1. `pdf-analyzer` → Analyse le PDF
2. `project-coordinator` → Coordonne les résultats
3. `company-finder-morocco` → Trouve les entreprises marocaines

---

## 🔧 Outils Utilisés

### **MCP Filesystem Server**
- **`mcp-filesys-read-file`** : Lit les fichiers PDF
- **`mcp-filesys-write-file`** : Écrit des fichiers
- **`mcp-filesys-list-directory`** : Liste les répertoires
- **+ 11 autres outils** de gestion de fichiers

### **Web Search Tool**
- **`web-search`** : Recherche d'informations sur le web
- Utilise DuckDuckGo API
- Retourne des résultats avec titres, snippets et URLs

---

## 🚀 Workflow Complet

### **Étape 1 : Upload PDF**
- L'utilisateur upload un PDF via l'interface Streamlit
- Le PDF est traité localement (extraction de texte avec PyPDF2)

### **Étape 2 : Analyse PDF**
- **PDF Analyzer** lit le contenu du PDF
- Extrait les informations clés du projet
- Structure les données pour la suite

### **Étape 3 : Coordination**
- **Project Coordinator** reçoit les résultats de l'analyse
- Valide et enrichit les informations
- Prépare la description du projet pour la recherche

### **Étape 4 : Recherche d'Entreprises**
- **Company Finder** utilise les informations du projet
- Recherche sur le web les entreprises appropriées
- Évalue et classe les entreprises trouvées

### **Étape 5 : Présentation des Résultats**
- Les résultats sont affichés dans l'interface Streamlit
- Cartes d'entreprises avec ratings et détails
- Possibilité d'export CSV/JSON

---

## 📊 Exemple de Résultats

**Input :** PDF d'appel d'offres pour habillement et textile brandé

**Output :** 5 entreprises marocaines spécialisées
1. **SICOPA** (9.5/10) - Casablanca
2. **Tectis Maroc** (9.2/10) - Casablanca
3. **Uniformes Maroc** (9.0/10) - Casablanca
4. **+ 2 autres entreprises**

---

## 🛠️ Technologies Utilisées

- **ARK Platform** : Orchestration des agents
- **Kubernetes** : Déploiement et gestion
- **Streamlit** : Interface utilisateur
- **PyPDF2** : Extraction de texte PDF
- **MCP Protocol** : Communication entre agents
- **DuckDuckGo API** : Recherche web
- **GPT-4.1** : Modèle d'IA principal

---

## 🎯 Avantages du Système

- ✅ **Automatisation complète** : De l'analyse PDF à la recherche d'entreprises
- ✅ **Workflow coordonné** : Les agents travaillent ensemble de manière séquentielle
- ✅ **Interface intuitive** : Upload simple et résultats visuels
- ✅ **Extensible** : Facile d'ajouter de nouveaux agents ou fonctionnalités
- ✅ **Régional** : Support pour différentes régions (Maroc, Global, etc.)
- ✅ **Résultats structurés** : JSON standardisé pour l'intégration

