import os
import sys
import requests
from dotenv import load_dotenv
from agent_writer import write_content
from agent_reviewer import query_llm_farm


# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

if not api_key:
    print("Error: LLM_FARM_API_KEY is not set in the environment.")
    sys.exit(1)

def query_llm_farm(userPrompt: str):
    # Base configuration for Bosch LLM Farm API
    url = "https://aoai-farm.bosch-temp.com/api/openai/deployments/gpt-5-nano-2025-08-07/chat/completions?api-version=2025-04-01-preview"
    
    # Headers for openai LLM Farm API
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    # Payload for the API request
    payload = {
        "messages": [
            {"role": "system", "content": "You are a professional content writer. Write clear, engaging content based on the user's prompt. If provided with previous feedback, revise your work to address those points specifically."},
            {"role": "user", "content": userPrompt}
        ],
        "temperature": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        # If the API still fails with the 'api-key' header, print the response body to see the exact error message
        if hasattr(e, 'response') and e.response is not None:
            return f"Error contacting Bosch LLM Farm: {e}\nDetails: {e.response.text}"
        return f"Error contacting Bosch LLM Farm: {e}"
