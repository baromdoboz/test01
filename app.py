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
                {"role": "system", "content": "Te egy segítőkész asszisztens vagy."},
                {"role": "user", "content": "Mondj valami szépet, maximum öt szóban! Ékezetek nélkül válaszolj!"}
            ],
            max_tokens=50
        )
        message = response.choices[0].message.content.strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_remaining_tokens():
    try:
        # Fetch usage details
        usage = client.usage.retrieve()

        # Example quota limit (replace with your actual quota)
        quota_limit = 10000  # Adjust based on your plan

        # Calculate remaining tokens
        tokens_used = usage.total_tokens
        tokens_remaining = quota_limit - tokens_used

        return tokens_remaining
    except Exception as e:
        return f"Error fetching usage: {e}"

@app.route('/remaining-tokens')
def remaining_tokens():
    tokens_remaining = get_remaining_tokens()
    return jsonify({"tokens_remaining": tokens_remaining})

if __name__ == '__main__':
    app.run(debug=True)
