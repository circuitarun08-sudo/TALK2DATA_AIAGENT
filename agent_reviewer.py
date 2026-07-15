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

def review_content(response_content: str, prompt: str):
    # Base configuration for Bosch LLM Farm API
    url="https://aoai-farm.bosch-temp.com/api/openai/deployments/gpt-5-nano-2025-08-07/chat/completions?api-version=2025-04-01-preview"
    print(requests.utils.get_environ_proxies(url))
    #headers for openai LLM Farm API
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    #Payload for the API request
    payload = {
        "messages": [
            {"role": "system", "content": "You are a critical quality controller. Review the provided text for accuracy, clarity, and depth. You must respond ONLY in a valid JSON format: {\"score\": <1 to 5>, \"feedback\": \"<detailed critique>\"}."},
            {"role": "user", "content": response_content},
            {"role": "user", "content": f"Prompt: {prompt}"}
        ],
        "temperature": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_content=response.json()['choices'][0]['message']['content']
        parsed_response_content = eval(response_content)  # Convert string representation of dict to actual dict
        return parsed_response_content['score'], parsed_response_content['feedback']
        #return response.json()['choices'][0]['message']['content']['score'], response.json()['choices'][0]['message']['content']['feedback']
        #return response.json()
    except Exception as e:
        # If the API still fails with the 'api-key' header, print the response body to see the exact error message
        if hasattr(e, 'response') and e.response is not None:
            return None, f"Error contacting Bosch LLM Farm: {e}\nDetails: {e.response.text}"
        return None, f"Error contacting Bosch LLM Farm: {e}"
    
if __name__ == "__main__":
    # Get input from the user for the content they want to review
    response_content=input("Please provide the content you would like to have reviewed:")
    prompt=input("Please provide the original prompt that was used to generate this content:")
    print(f"Sending content to Bosch LLM Farm for review...")
    
    #Send request to Bosch LLM Farm and get the response
    review_response_score, review_response_feedback = review_content(response_content,prompt)
    print("Review response from Bosch LLM Farm:")
    print('Score:', review_response_score)
    print('Feedback:', review_response_feedback)