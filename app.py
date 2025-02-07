from flask import Flask, jsonify
from openai import OpenAI  # Import the new OpenAI client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

@app.route('/')
def home():
    return "Welcome to the Random Message Generator!"

@app.route('/generate-message')
def generate_message():
    try:
        # Generate a random message using OpenAI's GPT-3.5 Turbo
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the GPT-3.5 Turbo model
            messages=[
                #{"role": "system", "content": "Te egy segítőkész asszisztens vagy."},
                {"role": "user", "content": "Kedves max 10 szó ékezetek nélkül!"}
            ],
            max_tokens=50
        )
        message = response.choices[0].message.content.strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
