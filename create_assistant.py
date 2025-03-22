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

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key, base_url=base_url)

assistant = client.beta.assistants.create(
  name="Terraform Engineer",
  instructions="You are an experienced Terraform engineer. You are able to generate Terraform code based on user requests.",
  #tools=[{"type": "function"}],
  model="gpt-4o-mini",
)

print(assistant)
