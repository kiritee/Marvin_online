import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_algorithm(user_message=None, file_path=None):
    if file_path:
        # Handle file processing here
        with open(file_path, 'r') as file:
            file_content = file.read()
        processed_message = "Please analyze this file: " + file_content
    else:
        processed_message = "Please respond to the user query: " + user_message

    try:
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=processed_message,
        #     max_tokens=150,
        #     n=1,
        #     stop=None,
        #     temperature=0.7
        # )
        
        # response_text = response.choices[0].text.strip()
        response_text = "Done"
        return response_text
    except Exception as e:
        print(f"Error in chat_algorithm: {e}")
        return "An error occurred while processing your request."
