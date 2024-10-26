import openai
import dotenv
import os

dotenv.load_dotenv(override=True)

# Initialize OpenAI client with Helicone integration
openai_client = openai.OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
  base_url="https://oai.helicone.ai/v1",
  default_headers={
    "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}",
  },
)

def get_embedding(text, model="text-embedding-3-small"):
    return openai_client.embeddings.create(input=text, model=model).data[0].embedding
