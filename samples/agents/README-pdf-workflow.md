# PDF Company Finder Workflow

Ce système utilise trois agents qui travaillent en équipe pour analyser des documents PDF (appels d'offres, spécifications de projets) et trouver les meilleures entreprises pour exécuter ces projets.

## Architecture

### Agents

1. **PDF Analyzer** (`pdf-analyzer`)
   - **Rôle**: Analyse les documents PDF et extrait les informations clés
   - **Outils**: `mcp-filesys-read-file` pour lire les fichiers PDF
   - **Sortie**: Informations structurées sur le projet (type, exigences, budget, etc.)

2. **Project Coordinator** (`project-coordinator`)
   - **Rôle**: Coordonne le workflow entre l'analyse PDF et la recherche d'entreprises
   - **Fonction**: Intègre les résultats et prépare les données pour la recherche d'entreprises
   - **Sortie**: Description complète du projet pour la recherche d'entreprises

3. **Company Finder** (`company-finder` / `company-finder-morocco`)
   - **Rôle**: Recherche et analyse les entreprises appropriées
   - **Outils**: `web-search` pour rechercher des informations sur les entreprises
   - **Sortie**: Top 5 entreprises avec évaluations et recommandations

### Teams

- **`pdf-company-finder-team`**: Team global avec les trois agents
- **`pdf-company-finder-team-morocco`**: Team spécialisé pour le Maroc

### Workflow

```
PDF Upload → PDF Analyzer → Project Coordinator → Company Finder → Results
```

1. **Upload PDF**: L'utilisateur upload un document PDF via l'interface Streamlit
2. **Analyse PDF**: L'agent PDF Analyzer lit et analyse le document
3. **Coordination**: L'agent Project Coordinator intègre les résultats
4. **Recherche Entreprises**: L'agent Company Finder trouve les meilleures entreprises
5. **Affichage**: Les résultats sont présentés dans l'interface Streamlit

## Déploiement

### 1. Déployer le serveur MCP Filesystem

```bash
cd mcp/filesys
./build.sh
helm install filesys-mcp ./chart
```

### 2. Déployer le workflow PDF

```bash
./samples/agents/deploy-pdf-workflow.sh
```

### 3. Vérifier le déploiement

```bash
kubectl get agents -l category=document-analysis
kubectl get agents -l category=coordination
kubectl get teams -l workflow=pdf-analysis
```

## Utilisation

### Interface Streamlit

```bash
cd streamlit-app
streamlit run app_pdf.py
```

L'interface permet de:
- Uploader un fichier PDF
- Sélectionner la région de recherche
- Analyser le document et trouver des entreprises
- Exporter les résultats

### Test en ligne de commande

```bash
./test-pdf-workflow.sh
```

## Fichiers créés

### Agents
- `samples/agents/pdf-analyzer.yaml`
- `samples/agents/project-coordinator.yaml`

### Teams
- `samples/teams/pdf-company-finder-team.yaml`

### Applications
- `streamlit-app/app_pdf.py` - Interface Streamlit pour PDF
- `streamlit-app/ark_client.py` - Client ARK mis à jour

### Scripts
- `samples/agents/deploy-pdf-workflow.sh` - Script de déploiement
- `test-pdf-workflow.sh` - Script de test

## Exemple d'utilisation

1. **Upload PDF**: Uploader un appel d'offres ou une spécification de projet
2. **Sélection région**: Choisir "Morocco" ou "Global"
3. **Analyse**: Cliquer sur "Analyze PDF & Find Companies"
4. **Résultats**: Voir l'analyse du projet et les entreprises recommandées

## Avantages

- **Automatisation complète**: De l'analyse PDF à la recherche d'entreprises
- **Workflow coordonné**: Les agents travaillent ensemble de manière séquentielle
- **Interface intuitive**: Upload simple et résultats visuels
- **Extensible**: Facile d'ajouter de nouveaux agents ou fonctionnalités
- **Régional**: Support pour différentes régions (Maroc, Global, etc.)

## Prochaines étapes

- Ajouter support pour d'autres formats de documents (Word, Excel)
- Intégrer des bases de données d'entreprises
- Ajouter des critères de filtrage avancés
- Implémenter des notifications et suivi de projets
