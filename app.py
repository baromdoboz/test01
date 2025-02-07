from flask import Flask, jsonify, request, render_template
from openai import OpenAI
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
    return "Welcome to the GPT-4o Mini Chat API!"

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
                {"role": "system", "content": "Egy gonosz plüssmackó vagy, aki max 10 szóban válaszol. Minden mondat végén legyen hangulatjel!"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=50  # Limit the response to 50 tokens
        )

        # Extract and return the bot's response
        bot_response = response.choices[0].message.content.strip()
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Get the user input from the form
        user_input = request.form.get("message")

        if not user_input:
            return render_template("test.html", error="írjad neki mitakarsz")

        # Call the OpenAI API directly (no need for test_client)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Egy gonosz plüssmackó vagy, aki max 10 szóban válaszol."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=50
            )
            bot_response = response.choices[0].message.content.strip()
            return render_template("test.html", user_input=user_input, bot_response=bot_response)
        except Exception as e:
            return render_template("test.html", error=str(e))

    # Render the test page for GET requests
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)
