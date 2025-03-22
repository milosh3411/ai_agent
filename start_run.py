import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

def start_run(thread_id, assistant_id, instructions=None):
    """
    Start a new run for the specified thread and assistant
    
    Args:
        thread_id (str): The ID of the thread to start the run in
        assistant_id (str): The ID of the assistant to use for the run
        instructions (str, optional): Additional instructions for the run
        
    Returns:
        Run: The created run object
    """
    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key)
        
        # Create run parameters
        run_params = {
            "assistant_id": assistant_id,
            "thread_id": thread_id,
        }
        
        # Add instructions if provided
        if instructions:
            run_params["instructions"] = instructions
            
        # Create a new run
        run = client.beta.threads.runs.create(**run_params)
        
        return run
        
    except Exception as e:
        print(f"Error starting run: {str(e)}")
        raise

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    import sys
    
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python start_run.py <thread_id> <assistant_id> [instructions]")
        sys.exit(1)
        
    thread_id = sys.argv[1]
    assistant_id = sys.argv[2]
    instructions = sys.argv[3] if len(sys.argv) == 4 else None
    run = start_run(thread_id, assistant_id, instructions)
    print(f"Run started successfully. Run object: {run}") 