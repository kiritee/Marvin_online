from flask import Flask, request, render_template, jsonify
from chat_algorithm import chat_algorithm
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    try:
        response_text = chat_algorithm(user_message)
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
