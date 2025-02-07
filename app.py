from flask import Flask, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

@app.route('/')
def home():
    return "Welcome to the Random Message Generator!"

@app.route('/generate-message')
def generate_message():
    try:
        # Generate a random message using OpenAI's GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Generate a random inspirational message:"}
            ],
            max_tokens=50
        )
        message = response.choices[0].message['content'].strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
