from flask import Flask, jsonify, request
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
    return "éjáj"

@app.route('/generate-message')
def generate_message():
    try:
        # Generate a random message using OpenAI's GPT-3.5 Turbo
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the GPT-3.5 Turbo model
            messages=[
                #{"role": "system", "content": "Te egy segítőkész asszisztens vagy."},
                {"role": "user", "content": "Mondj valami vicceset max 10 szóban!"}
            ],
            max_tokens=50
        )
        message = response.choices[0].message.content.strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Extract user input from the POST request
        data = request.json
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "Missing message. Please provide a 'message' field in the request."}), 400

        # Call the OpenAI API with the user input
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with the actual model name
            messages=[
                {"role": "system", "content": "Egy gonosz plüssmackó vagy, aki max 10 szóban válaszol."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=50  # Limit the response to 50 tokens
        )

        # Extract and return the bot's response
        bot_response = response.choices[0].message.content.strip()
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
