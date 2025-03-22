import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key:
    raise ValueError("API_KEY environment variable is not set")

def create_thread(assistant_id, initial_message=None):
    """
    Create a new thread for the specified OpenAI assistant
    
    Args:
        assistant_id (str): The ID of the assistant to create a thread for
        initial_message (str, optional): Initial message to add to the thread
        
    Returns:
        Thread: The created thread object
    """
    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Create a new thread
        if initial_message:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": initial_message
                    }
                ]
            )
        else:
            thread = client.beta.threads.create()
        
        return thread
        
    except Exception as e:
        print(f"Error creating thread: {str(e)}")
        raise

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    # You would need to provide a valid assistant ID as an argument
    import sys
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python create_thread.py <assistant_id> [initial_message]")
        sys.exit(1)
        
    assistant_id = sys.argv[1]
    initial_message = sys.argv[2] if len(sys.argv) == 3 else None
    thread = create_thread(assistant_id, initial_message)
    print(f"Thread created successfully. Thread object: {thread}") 