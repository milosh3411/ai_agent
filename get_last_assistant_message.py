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

def get_last_assistant_message(thread_id):
    """
    Get the last message from the assistant in the specified thread
    
    Args:
        thread_id (str): The ID of the thread to get the message from
        
    Returns:
        dict: The message content and metadata, or None if no assistant message is found
    """
    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # List messages in the thread, newest first
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=20  # Adjust this if needed
        )
        
        # Find the first (most recent) assistant message
        for message in messages:
            if message.role == "assistant":
                return {
                    'content': message.content[0].text.value,
                    'message_id': message.id,
                    'created_at': message.created_at,
                    'role': message.role
                }
                
        return None
        
    except Exception as e:
        print(f"Error retrieving assistant message: {str(e)}")
        raise

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    import sys
    from datetime import datetime
    
    if len(sys.argv) != 2:
        print("Usage: python get_last_assistant_message.py <thread_id>")
        sys.exit(1)
        
    thread_id = sys.argv[1]
    message = get_last_assistant_message(thread_id)
    
    if message:
        # Convert timestamp to readable format
        created_at = datetime.fromtimestamp(message['created_at'])
        print(f"\nLast assistant message:")
        print(f"Created at: {created_at}")
        print(f"Message ID: {message['message_id']}")
        print(f"Content: {message['content']}")
    else:
        print("No assistant messages found in the thread.") 