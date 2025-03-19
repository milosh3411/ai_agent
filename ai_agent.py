import requests
import json
import time
import os
from typing import Dict, Any, List, Optional, Callable



class AIAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        # Create a default assistant if none is provided
        self.assistant_id = self._create_assistant()

    def _create_assistant(self) -> str:
        """Create an assistant with function calling capability for Terraform"""
        response = requests.post(
            f"{self.base_url}/assistants",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v1"
            },
            json={
                "name": "Terraform Code Generator",
                "instructions": "You are a helpful assistant that generates Terraform code based on user requests.",
                "model": "gpt-4-turbo",
                "tools": [{
                    "type": "function",
                    "function": {
                        "name": "execute_terraform_code",
                        "description": "Executes and validates Terraform code",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The Terraform code to execute or validate"
                                },
                                "action": {
                                    "type": "string",
                                    "enum": ["validate", "plan", "apply"],
                                    "description": "The Terraform action to perform"
                                }
                            },
                            "required": ["code", "action"]
                        }
                    }
                }]
            }
        )
        response.raise_for_status()
        return response.json()["id"]

    def execute_terraform_code(self, code: str, action: str) -> Dict[str, Any]:
        """
        Custom Terraform code execution function.
        This is where you would implement your own Terraform interpreter logic.
        """
        # Placeholder implementation - replace with your actual Terraform execution code
        if action == "validate":
            # Simulate validation
            return {
                "valid": True,
                "message": "Terraform code is syntactically valid."
            }
        elif action == "plan":
            # Simulate plan
            return {
                "changes": 3,
                "additions": 2,
                "modifications": 1,
                "deletions": 0,
                "plan_output": "Plan: 2 to add, 1 to change, 0 to destroy."
            }
        elif action == "apply":
            # Simulate apply
            return {
                "applied": True,
                "resources_created": 2,
                "resources_modified": 1,
                "resources_destroyed": 0,
                "apply_output": "Apply complete! Resources: 2 added, 1 changed, 0 destroyed."
            }
        else:
            return {"error": f"Unsupported action: {action}"}

    def generate_code(self, prompt: str) -> str:
        # Step 1: Create a thread
        thread_response = requests.post(
            f"{self.base_url}/threads",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v1"
            },
            json={}
        )
        thread_response.raise_for_status()
        thread_id = thread_response.json()["id"]
        
        # Step 2: Add a message to the thread
        message_response = requests.post(
            f"{self.base_url}/threads/{thread_id}/messages",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v1"
            },
            json={
                "role": "user",
                "content": prompt
            }
        )
        message_response.raise_for_status()
        
        # Step 3: Run the assistant
        run_response = requests.post(
            f"{self.base_url}/threads/{thread_id}/runs",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v1"
            },
            json={
                "assistant_id": self.assistant_id
            }
        )
        run_response.raise_for_status()
        run_id = run_response.json()["id"]
        
        # Step 4: Wait for completion or function calls
        while True:
            run_status_response = requests.get(
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "OpenAI-Beta": "assistants=v1"
                }
            )
            run_status_response.raise_for_status()
            run_status = run_status_response.json()
            status = run_status["status"]
            
            if status == "requires_action":
                # Handle function calls
                tool_calls = run_status["required_action"]["submit_tool_outputs"]["tool_calls"]
                tool_outputs = []
                
                for tool_call in tool_calls:
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])
                    
                    if function_name == "execute_terraform_code":
                        # Call our custom Terraform execution function
                        result = self.execute_terraform_code(
                            function_args["code"], 
                            function_args["action"]
                        )
                        tool_outputs.append({
                            "tool_call_id": tool_call["id"],
                            "output": json.dumps(result)
                        })
                
                # Submit the outputs back to the assistant
                submit_response = requests.post(
                    f"{self.base_url}/threads/{thread_id}/runs/{run_id}/submit_tool_outputs",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "OpenAI-Beta": "assistants=v1"
                    },
                    json={
                        "tool_outputs": tool_outputs
                    }
                )
                submit_response.raise_for_status()
                
            elif status == "completed":
                break
            elif status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Run failed with status: {status}")
            
            time.sleep(1)  # Poll every second
        
        # Step 5: Retrieve messages
        messages_response = requests.get(
            f"{self.base_url}/threads/{thread_id}/messages",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "OpenAI-Beta": "assistants=v1"
            }
        )
        messages_response.raise_for_status()
        
        # Get the last assistant message
        messages = messages_response.json()["data"]
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        if not assistant_messages:
            return "No response generated"
        
        return assistant_messages[0]["content"][0]["text"]["value"]

    def deploy_code(self, code: str) -> Dict[str, Any]:
        # Custom deployment function (placeholder)
        try:
            # Simulating deployment process
            # In a real scenario, this would interact with your deployment system
            success = True
            error_message = None
        except Exception as e:
            success = False
            error_message = str(e)

        return {
            "status": "success" if success else "failure",
            "error_message": error_message
        }

    def process_request(self, prompt: str) -> Dict[str, Any]:
        generated_code = self.generate_code(prompt)
        deployment_result = self.deploy_code(generated_code)
        return {
            "generated_code": generated_code,
            "deployment_result": deployment_result
        }

# Example usage
if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    agent = AIAgent(api_key)
    result = agent.process_request("Create Terraform code to deploy an AWS S3 bucket with versioning enabled")
    print(json.dumps(result, indent=2))
