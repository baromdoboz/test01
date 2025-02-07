# app.py
from flask import Flask, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Welcome to the Random Message Generator!"

@app.route('/generate-message')
def generate_message():
    try:
        # Generate a random message using OpenAI's GPT-3
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the GPT-3.5 model
            prompt="Generate a random inspirational message:",
            max_tokens=50
        )
        message = response.choices[0].text.strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
