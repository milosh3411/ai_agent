import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

def check_run_status(thread_id, run_id, wait=False, check_interval=1):
    """
    Check the status of a run and optionally wait for it to complete
    
    Args:
        thread_id (str): The ID of the thread
        run_id (str): The ID of the run to check
        wait (bool): Whether to wait for the run to complete
        check_interval (int): How often to check the status when waiting (in seconds)
        
    Returns:
        Run: The run object with current status
    """
    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key)
        
        while True:
            # Get the run status
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            
            # If we're not waiting or the run is complete/failed, return the status
            if not wait or run.status in ["completed", "failed", "expired", "cancelled"]:
                return run
                
            # If we're waiting and the run isn't complete, wait before checking again
            time.sleep(check_interval)
            
    except Exception as e:
        print(f"Error checking run status: {str(e)}")
        raise

def get_run_status_description(status):
    """
    Get a human-readable description of a run status
    
    Args:
        status (str): The status from the run object
        
    Returns:
        str: A description of the status
    """
    status_descriptions = {
        "queued": "Run is queued for processing",
        "in_progress": "Run is currently in progress",
        "completed": "Run completed successfully",
        "requires_action": "Run requires additional actions",
        "expired": "Run expired before completing",
        "failed": "Run failed to complete",
        "cancelled": "Run was cancelled"
    }
    return status_descriptions.get(status, f"Unknown status: {status}")

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    import sys
    
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python check_run_status.py <thread_id> <run_id> [--wait]")
        sys.exit(1)
        
    thread_id = sys.argv[1]
    run_id = sys.argv[2]
    wait = sys.argv[3] == "--wait" if len(sys.argv) == 4 else False
    
    run = check_run_status(thread_id, run_id, wait)
    status_description = get_run_status_description(run.status)
    print(f"Run status: {run.status}")
    print(f"Description: {status_description}") 