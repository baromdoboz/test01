from flask import Flask, jsonify, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

@app.route('/')
def home():
    return "éjáj!"


@app.route('/public-ip')
def get_public_ip():
    public_ip = requests.get('https://api64.ipify.org?format=text').text
    return f"Publikus IP-cím: {public_ip}"


@app.route('/test2')
def test2():
    return os.getenv("TEMPLATE_NAME")

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
                {"role": "system", "content": "Te egy rendkívül gonosz, mogorva, vulgáris plüssmackó vagy, aki max 10 szóban válaszol!"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=50  # Limit the response to 50 tokens
        )

        # Extract and return the bot's response
        bot_response = response.choices[0].message.content.strip()
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/aibear', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Get the user input from the form
        user_input = request.form.get("message")

        if not user_input:
            return render_template("test2.html", error="írjad neki mitakarsz")

        # Call the OpenAI API directly (no need for test_client)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Te egy rendkívül gonosz, mogorva, vulgáris plüssmackó vagy, aki max 10 szóban válaszol!"},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50
            )
            bot_response = response.choices[0].message.content.strip()
            return render_template("test2.html", user_input=user_input, bot_response=bot_response)
        except Exception as e:
            return render_template("test2.html", error=str(e))

    # Render the test page for GET requests
    return render_template("test2.html")

if __name__ == '__main__':
    app.run(debug=True)
