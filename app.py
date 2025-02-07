import openai
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = OPENAI_API_KEY

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
    prompt = random.choice(prompts)  # Pick a random prompt
    
    # Generate text using OpenAI's API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    ai_sentence = response["choices"][0]["message"]["content"].strip()

    return jsonify({"sentence": ai_sentence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
