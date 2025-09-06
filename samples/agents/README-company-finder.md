# Company Finder Agent

The Company Finder Agent is a specialized ARK agent that helps users find the best companies to execute their projects by conducting web research and analyzing company capabilities.

## Features

- **Web Research**: Uses DuckDuckGo API to search for companies in relevant industries
- **Capability Analysis**: Evaluates companies based on expertise, experience, and track record
- **Structured Output**: Returns top 5 companies with detailed rankings and reasoning
- **Project-Specific**: Tailors search and analysis to specific project requirements

## Usage

### 1. Deploy the Required Components

First, ensure the web search tool is available:

```bash
# Deploy the web search tool
kubectl apply -f samples/tools/web-search.yaml

# Deploy the company finder agent
kubectl apply -f samples/agents/company-finder.yaml
```

### 2. Create a Query

Create a query with your project description:

```bash
# Use the template and customize it
kubectl apply -f samples/queries/company-finder-template.yaml

# Or use the healthcare app example
kubectl apply -f samples/queries/company-finder-query.yaml
```

### 3. Execute the Query

```bash
# Run the query using ark-cli
ark query execute company-finder-test

# Or use kubectl to check the query status
kubectl get queries
kubectl describe query company-finder-test
```

## Project Description Format

When creating queries, provide detailed project information:

```
I need to [project type] for [company/industry]. The project should include:

- [Requirement 1]
- [Requirement 2] 
- [Requirement 3]
- [Any specific technical requirements]
- [Compliance or regulatory requirements]
- [Timeline and budget constraints]

Please find the top 5 companies that would be best suited for this project.
```

## Output Format

The agent returns structured JSON with:

- **Project Summary**: Brief description of requirements
- **Companies**: Top 5 companies with:
  - Ranking (1-5)
  - Company name and website
  - Specialization areas
  - Suitability reasoning
  - Notable experience
  - Project fit assessment (High/Medium/Low)
  - Overall rating (1-10)
- **Research Sources**: Search queries and sources used

## Example Use Cases

1. **Software Development**: Find companies for custom software, mobile apps, web applications
2. **Consulting Services**: Identify firms for strategy, operations, or technology consulting
3. **Infrastructure Projects**: Locate companies for cloud migration, DevOps, or system integration
4. **Specialized Services**: Find experts in AI/ML, cybersecurity, data analytics, etc.

## Customization

You can modify the agent's prompt in `company-finder.yaml` to:
- Focus on specific industries or company types
- Adjust ranking criteria
- Change output format
- Add additional research requirements

## Dependencies

- Web Search Tool (`samples/tools/web-search.yaml`)
- Internet connectivity from the cluster
- DuckDuckGo API access (no authentication required)

## Troubleshooting

- Ensure the web search tool is deployed before the agent
- Check that the cluster has internet access
- Verify query timeout settings for complex research tasks
- Monitor query logs for any API rate limiting issues
