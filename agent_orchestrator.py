import os
import sys
import requests
import json
from dotenv import load_dotenv
from agent_writer import write_content
from agent_reviewer import review_content


# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("LLM_FARM_API_KEY")

if not api_key:
    print("Error: LLM_FARM_API_KEY is not set in the environment.")
    sys.exit(1)

def orchestrate_content_creation(user_prompt: str, feedback: str = None):
    max_iterations = 3
    current_iteration = 1

    # Step 1: Generate content based on the user's prompt and optional feedback
    print(f"Generating content for prompt: {user_prompt}...")
    generated_content = write_content(user_prompt, feedback)
    
    if "Error contacting Bosch LLM Farm" in generated_content:
        print(generated_content)
        return

    print("Generated Content:")
    print(generated_content)

    # Step 2: Review the generated content
    print("Reviewing the generated content...")
    review_score, review_feedback = review_content(generated_content, user_prompt)

    if review_score is None:
        print(review_feedback)  # This will contain the error message
        return

    print("Review Results:")
    print(f"Score: {review_score}")
    print(f"Feedback: {review_feedback}")

if __name__ == "__main__":
    # Get input from the user for the topic they want to create content about
    user_prompt = input("What topic would you like me to create content about? ")
    #feedback = input("If you have any feedback from a previous review, please provide it here (or press Enter to skip): ")

    # Orchestrate the content creation and review process
    orchestrate_content_creation(user_prompt)