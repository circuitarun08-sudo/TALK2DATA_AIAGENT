import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

if not api_key:
        raise ValueError("LLM_FARM_API_KEY not found. Please set it in your .env file.")
else:
        print("LLM_FARM_API_KEY found. Proceeding with API call.")

def write_content(userPrompt: str, feedback: str = None):
    # Base configuration for Bosch LLM Farm API
    url="https://aoai-farm.bosch-temp.com/api/openai/deployments/gpt-5-nano-2025-08-07/chat/completions?api-version=2025-04-01-preview"
    
    #headers for openai LLM Farm API
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    #Payload for the API request
    payload = {
        "messages": [
            {"role": "system", "content": "You are a professional content writer. Write clear, engaging content based on the user's prompt. If provided with previous feedback, revise your work to address those points specifically."},
            {"role": "user", "content": userPrompt}
        ],
        "temperature": 1
    }

    if feedback:
        payload["messages"].append({"role": "user", "content": f"Previous feedback: {feedback}"})
    
    print("Request to Bosch LLM Farm:")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        # If the API still fails with the 'api-key' header, print the response body to see the exact error message
        if hasattr(e, 'response') and e.response is not None:
            return f"Error contacting Bosch LLM Farm: {e}\nDetails: {e.response.text}"
        return f"Error contacting Bosch LLM Farm: {e}"
    
if __name__ == "__main__":
    # Get input from the user for the topic they want to create content about
    userPrompt=input("What topic would you like me to create content about?")
    print(f"Sending prompt to Bosch LLM Farm for topic: {userPrompt}...")
    feedback=input("If you have any feedback from a previous review, please provide it here (or press Enter to skip): ")

    #Send request to Bosch LLM Farm and get the response
    response_text = write_content(userPrompt, feedback)
    print("Response from Bosch LLM Farm:")
    print(response_text)
    