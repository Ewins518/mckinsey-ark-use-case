"""
ARK Client for Streamlit App
Handles communication with ARK cluster via kubectl
"""

import subprocess
import json
import time
import yaml
from typing import Dict, List, Optional, Tuple


class ARKClient:
    def __init__(self):
        self.namespace = "default"
    
    def _run_kubectl(self, command: str) -> Tuple[bool, str]:
        """Run kubectl command and return success status and output"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, f"stderr: {result.stderr}, stdout: {result.stdout}"
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def create_query(self, project_data: Dict) -> Tuple[bool, str]:
        """Create and submit a query to ARK cluster"""
        try:
            # Generate query YAML
            query_yaml = self._generate_query_yaml(project_data)
            
            # Write to temporary file
            temp_file = f"/tmp/query_{int(time.time())}.yaml"
            with open(temp_file, 'w') as f:
                f.write(query_yaml)
            
            # Apply to cluster
            success, output = self._run_kubectl(f"kubectl apply -f {temp_file}")
            
            if success:
                query_name = project_data.get('query_name', 'company-finder-query')
                # Clean up temp file
                import os
                try:
                    os.remove(temp_file)
                except:
                    pass
                return True, query_name
            else:
                # Clean up temp file even on failure
                import os
                try:
                    os.remove(temp_file)
                except:
                    pass
                return False, f"Failed to create query: '{output}' (success={success})"
                
        except Exception as e:
            return False, f"Error creating query: {str(e)}"
    
    def create_pdf_query(self, project_data: Dict) -> Tuple[bool, str]:
        """Create and submit a PDF analysis query to ARK cluster"""
        try:
            # Generate query YAML for PDF analysis
            query_yaml = self._generate_pdf_query_yaml(project_data)
            
            # Write to temporary file
            temp_file = f"/tmp/pdf_query_{int(time.time())}.yaml"
            with open(temp_file, 'w') as f:
                f.write(query_yaml)
            
            # Apply to cluster
            success, output = self._run_kubectl(f"kubectl apply -f {temp_file}")
            
            if success:
                query_name = project_data.get('query_name', 'pdf-company-finder-query')
                # Clean up temp file
                import os
                try:
                    os.remove(temp_file)
                except:
                    pass
                return True, query_name
            else:
                # Clean up temp file even on failure
                import os
                try:
                    os.remove(temp_file)
                except:
                    pass
                return False, f"Failed to create PDF query: '{output}' (success={success})"
                
        except Exception as e:
            return False, f"Error creating PDF query: {str(e)}"
    
    def get_query_status(self, query_name: str) -> Tuple[bool, str]:
        """Get the status of a query"""
        success, output = self._run_kubectl(f"kubectl get query {query_name} -o jsonpath='{{.status.phase}}'")
        if success:
            # Remove quotes if present
            status = output.strip().strip("'\"")
            return True, status
        return False, "Unknown"
    
    def get_query_results(self, query_name: str) -> Tuple[bool, Dict]:
        """Get the results of a completed query"""
        try:
            success, output = self._run_kubectl(
                f"kubectl get query {query_name} -o jsonpath='{{.status.responses[0].content}}'"
            )
            
            if success and output.strip():
                # Remove quotes that kubectl jsonpath might add
                cleaned_output = output.strip().strip("'\"")
                # The content is a JSON string, so we need to parse it
                results = json.loads(cleaned_output)
                return True, results
            else:
                return False, {}
                
        except json.JSONDecodeError as e:
            return False, {"error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def delete_query(self, query_name: str) -> bool:
        """Delete a query from the cluster"""
        success, _ = self._run_kubectl(f"kubectl delete query {query_name} --ignore-not-found=true")
        return success
    
    def _generate_query_yaml(self, project_data: Dict) -> str:
        """Generate query YAML from project data"""
        query_name = project_data.get('query_name', f"query-{int(time.time())}")
        project_description = project_data.get('description', '')
        region = project_data.get('region', 'global')
        
        # Select agent based on region
        agent_name = "company-finder-morocco" if region.lower() == "morocco" else "company-finder"
        
        # Use the project description directly as input (much simpler!)
        input_text = project_description
        
        # Properly format the multiline input text for YAML
        # Each line after the | should be indented with 4 spaces
        lines = input_text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():  # Non-empty lines
                formatted_lines.append(f"    {line}")
            else:  # Empty lines
                formatted_lines.append("")
        formatted_input = '\n'.join(formatted_lines)
        
        query_yaml = f"""apiVersion: ark.mckinsey.com/v1alpha1
kind: Query
metadata:
  name: {query_name}
  namespace: {self.namespace}
spec:
  input: |
{formatted_input}
  targets:
    - type: agent
      name: {agent_name}
  ttl: 5m"""
        
        return query_yaml
    
    def _generate_pdf_query_yaml(self, project_data: Dict) -> str:
        """Generate query YAML for PDF analysis workflow"""
        query_name = project_data.get('query_name', f"pdf-query-{int(time.time())}")
        pdf_content = project_data.get('pdf_content', '')
        file_name = project_data.get('file_name', 'document.pdf')
        region = project_data.get('region', 'global')
        
        # Select team based on region
        team_name = "pdf-company-finder-team-morocco" if region.lower() == "morocco" else "pdf-company-finder-team"
        
        # Create input that includes the PDF content directly
        input_text = f"""Please analyze the following PDF document and find suitable companies for the project:

Document: {file_name}
PDF Content: {pdf_content}

Please:
1. Analyze the PDF document content to extract project requirements
2. Coordinate the analysis with company research
3. Find the best companies for this project
4. Provide comprehensive recommendations

Region: {region}"""
        
        # Properly format the multiline input text for YAML
        lines = input_text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():  # Non-empty lines
                formatted_lines.append(f"    {line}")
            else:  # Empty lines
                formatted_lines.append("")
        formatted_input = '\n'.join(formatted_lines)
        
        query_yaml = f"""apiVersion: ark.mckinsey.com/v1alpha1
kind: Query
metadata:
  name: {query_name}
  namespace: {self.namespace}
spec:
  input: |
{formatted_input}
  targets:
    - type: team
      name: {team_name}
  ttl: 10m"""
        
        return query_yaml
    
    def wait_for_completion(self, query_name: str, timeout: int = 300) -> Tuple[bool, str]:
        """Wait for query to complete with timeout"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            success, status = self.get_query_status(query_name)
            
            if success:
                if status == "done":
                    return True, "completed"
                elif status == "error":
                    return False, "error"
                # Continue waiting for "running" status
            
            time.sleep(2)  # Check every 2 seconds for faster response
        
        return False, "timeout"
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        success, output = self._run_kubectl("kubectl get agents -o jsonpath='{.items[*].metadata.name}'")
        if success:
            return output.strip().split() if output.strip() else []
        return []
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        success, output = self._run_kubectl("kubectl get tools -o jsonpath='{.items[*].metadata.name}'")
        if success:
            return output.strip().split() if output.strip() else []
        return []
