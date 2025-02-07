import openai
import random
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Assign your OpenAI API key directly in the code (or use environment variable directly)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Read the API key from environment variable

# Example prompt list
prompts = [
    "Tell me a fun fact about space.",
    "Write a short motivational quote.",
    "Give me a random philosophical thought.",
    "Describe a futuristic city in one sentence.",
    "Say something funny about technology."
]

@app.route('/random-sentence', methods=['GET'])
def get_random_sentence():
    prompt = random.choice(prompts)

    # Use the updated OpenAI API method: chat_completions.create() for v1.0.0+
    response = openai.chat_completions.create(
        model="gpt-3.5-turbo",  # Use the desired model, e.g., "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    
    ai_sentence = response['choices'][0]['message']['content'].strip()
    return jsonify({"sentence": ai_sentence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
