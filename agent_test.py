import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

if not api_key:
    raise ValueError("LLM_FARM_API_KEY not found. Please set it in your .env file.")

def query_llm_farm(prompt: str):
    # Base configuration for Bosch LLM Farm API
    #url = "https://aoai-farm.bosch-temp.com" # Replace with the exact endpoint provided in your LLM Farm registration
    
    # Below are some example endpoints for different models available on the Bosch LLM Farm for Developer subscription. Uncomment the one you want to use.

    #OpenAI - Works
    url="https://aoai-farm.bosch-temp.com/api/openai/deployments/askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18/chat/completions?api-version=2025-04-01-preview"
    # url="https://aoai-farm.bosch-temp.com/api/openai/deployments/gpt-5-nano-2025-08-07/chat/completions?api-version=2025-04-01-preview"

    #Meta - Does not work
    # url="https://aoai-farm.bosch-temp.com/api/openai/deployments/deepseek-v4-flash-2026-04-23/chat/completions?api-version=2025-04-01-preview"

    #Gemini 
    # url="https://aoai-farm.bosch-temp.com/api/google/v1/endpoints/deepseek-r1-0528-maas/openapi/chat/completions"
    # url="https://aoai-farm.bosch-temp.com/api/openai/deployments/gemini-2.5-flash-lite/chat/completions"
    
    #Deepseek - Does not work
    # url="https://aoai-farm.bosch-temp.com/api/openai/deployments/deepseek-r1-0528-maas/chat/completions"


    #commented out the below headers as they are to be defined differently for Azure OpenAI Service. The headers below are for standard OpenAI API usage. For Azure OpenAI, Azure OpenAI endpoints usually expect the API key in a custom header called api-key instead of the standard standard Authorization: Bearer <key> header..
    # headers = {
    #     "Authorization": f"Bearer {api_key}",
    #     "Content-Type": "application/json"
    # }
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    # Request payload targeting standard models available on the Farm (e.g., GPT-4o or Gemini 2.0 Flash)
    # Commented out the below payload as "model": "gpt-4o" is not needed since its mentioned in the url directly. Azure openai models need not have
    # payload = {
    #     "model": "gpt-4o",  # Change to "gemini-2.0-flash" if preferred
    #     "messages": [
    #         {"role": "system", "content": "You are a helpful Bosch AI development assistant."},
    #         {"role": "user", "content": prompt}
    #     ],
    #     "temperature": 0.7
    # }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful Bosch AI development assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        # If the API  complains about the 'api-key' header, we can print the response body to see the exact error message
        if hasattr(e, 'response') and e.response is not None:
            return f"Error contacting Bosch LLM Farm: {e}\nDetails: {e.response.text}"
        return f"Error contacting Bosch LLM Farm: {e}"

if __name__ == "__main__":
    # user_prompt = "Hello! Explain the core benefit of using AI agents for automation."
    user_prompt = input("[User] : ") 
    print("Sending prompt to Bosch LLM Farm...")
    response_text = query_llm_farm(user_prompt)
    print("\nResponse from LLM Farm:")
    print(f"[AI] : {response_text}")
