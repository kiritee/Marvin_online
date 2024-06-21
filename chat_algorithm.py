import openai
import os
from utils import preprocess_message, postprocess_response
from constants import OPENAI_MODEL, MAX_TOKENS, TEMPERATURE

# Ensure the OpenAI API key is set
openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_algorithm(user_message):
    custom_instruction = "Please respond to the user query: "
    processed_message = custom_instruction + preprocess_message(user_message)

    try:
        response = openai.Completion.create(
            model=OPENAI_MODEL,
            prompt=processed_message,
            max_tokens=MAX_TOKENS,
            n=1,
            stop=None,
            temperature=TEMPERATURE
        )
        
        response_text = response.choices[0].text.strip()
        return postprocess_response(response_text)
    except Exception as e:
        print(f"Error in chat_algorithm: {e}")
        return "An error occurred while processing your request."
