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
    # Initialize the variables for the iterative process
    max_iterations = 3
    current_iteration = 1
    feedback_history = []  # To keep track of feedback from each iteration

    while(current_iteration <= max_iterations):

        # Step 1: Generate content based on the user's prompt and optional feedback
        print(f"Generating content for prompt: {user_prompt}...")
        generated_content = write_content(user_prompt, feedback, api_key)

        print("Content generation in-progress...")
        print(f"Iteration {current_iteration} completed.")

        if "Error contacting Bosch LLM Farm" in generated_content:
            print(generated_content)
            return

        print(f"Generated Content after Iteration {current_iteration}:")
        print(generated_content)

        # Step 2: Review the generated content
        print("Reviewing the generated content...")
        raw_json_response_content, review_score, review_feedback = review_content(generated_content, user_prompt, api_key)

        if review_score is None:
            print(review_feedback)  # This will contain the error message
            return

        print(f"Review Results after Iteration {current_iteration}:")
        print(f"Score: {review_score}")
        print(f"Feedback: {review_feedback}")

        # Step 3: If the score is less than 4, use the feedback to improve the content in the next iteration
        if review_score >= 4:
            print("Content quality is satisfactory. Ending the process.")
            break
        else:
            print("Content quality is unsatisfactory. Continuing to the next iteration.")
            feedback = review_feedback  # Use the feedback for the next iteration
            feedback_history.append({
                "iteration": current_iteration,
                "feedback": review_feedback
            })  # Keep track of feedback from each iteration
            print(f"Feedback for Iteration {current_iteration} stored for next iteration.")
            print(f"Feedback History after Iteration {current_iteration}: {feedback_history}")

        current_iteration += 1

if __name__ == "__main__":
    # Get input from the user for the topic they want to create content about
    user_prompt = input("What topic would you like me to create content about? ")
    #feedback = input("If you have any feedback from a previous review, please provide it here (or press Enter to skip): ")

    # Orchestrate the content creation and review process
    orchestrate_content_creation(user_prompt)