import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

"""
if not api_key:
        raise ValueError("LLM_FARM_API_KEY not found. Please set it in your .env file.")
else:
        print("LLM_FARM_API_KEY found. Proceeding with API call.")
"""
def write_content(userPrompt: str, current_draft: str = None, feedback: list = None, api_key: str = None):
    # Base configuration for Bosch LLM Farm API
    if not api_key:
        raise ValueError("LLM_FARM_API_KEY not found. Please set it in your .env file.")
    else:
        print("LLM_FARM_API_KEY found. Proceeding with API call.")

    url="https://aoai-farm.bosch-temp.com/api/openai/deployments/gpt-5-nano-2025-08-07/chat/completions?api-version=2025-04-01-preview"
    #print(requests.utils.get_environ_proxies(url))
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
        feedback_history="\nHere are the instructions to be followed:\n"
        for entry in feedback:
            feedback_history += f"- Iteration {entry['iteration']} : {entry['feedback']}\n"
        payload["messages"].append({"role": "user", "content": f"Consider following instructions while generating content:\n{feedback_history}"})

    if feedback and current_draft:
            feedback_history="\nHere is the previous feedback to be addressed:\n"
            for entry in feedback:
                feedback_history += f"- Iteration {entry['iteration']} : {entry['feedback']}\n"
            #payload["messages"].append({"role": "user", "content": f"Current draft: {current_draft}\n{feedback_history}"})
            payload["messages"].append({"role": "user", "content": (
            f"\n\nYour previous draft was:\n---START DRAFT---\n{current_draft}\n---END DRAFT---\n"
            f"{feedback_history}\n"
            f"Please revise the draft to fully address all the feedback points listed above."
            )})
    
    print("Request to Bosch LLM Farm..")

    #for debugging purposes, print the payload being sent to Bosch LLM Farm
    #print("Payload being sent to Bosch LLM Farm:")
    #print(payload)

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
    print(f"Before sending prompt to Bosch LLM Farm for topic... {userPrompt}...")
    feedback=input("If you have any instructions to be followed, please provide it here (or press Enter to skip): ")

    print("Waiting for response from Bosch LLM Farm...")

    #Send request to Bosch LLM Farm and get the response
    response_text = write_content(userPrompt, current_draft=None, feedback=[{"iteration": 1, "feedback": feedback}] if feedback else None, api_key=api_key)
    print("Response from Bosch LLM Farm:")
    print(response_text)
    