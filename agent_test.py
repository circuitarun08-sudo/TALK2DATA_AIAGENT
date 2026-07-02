import os
import requests
from dotenv import load_load, load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

if not api_key:
    raise ValueError("LLM_FARM_API_KEY not found. Please set it in your .env file.")

def query_llm_farm(prompt: str):
    # Base configuration for Bosch LLM Farm API
    url = "https://aoai-farm.bosch-temp.com" # Replace with the exact endpoint provided in your LLM Farm registration
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Request payload targeting standard models available on the Farm (e.g., GPT-4o or Gemini 2.0 Flash)
    payload = {
        "model": "gpt-4o",  # Change to "gemini-2.0-flash" if preferred
        "messages": [
            {"role": "system", "content": "You are a helpful Bosch AI development assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error contacting Bosch LLM Farm: {e}"

if __name__ == "__main__":
    user_prompt = "Hello! Explain the core benefit of using AI agents for automation."
    print("Sending prompt to Bosch LLM Farm...")
    response_text = query_llm_farm(user_prompt)
    print("\nResponse from LLM Farm:")
    print(response_text)
