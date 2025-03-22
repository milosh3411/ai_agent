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

def create_message(thread_id, message_content):
    """
    Create a new message in the specified thread
    
    Args:
        thread_id (str): The ID of the thread to add the message to
        message_content (str): The content of the message to add
        
    Returns:
        Message: The created message object
    """
    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Create a new message in the thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content
        )
        
        return message
        
    except Exception as e:
        print(f"Error creating message: {str(e)}")
        raise

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python create_message.py <thread_id> <message_content>")
        sys.exit(1)
        
    thread_id = sys.argv[1]
    message_content = sys.argv[2]
    message = create_message(thread_id, message_content)
    print(f"Message created successfully. Message object: {message}") 