from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Get JSON payload
    print("Received data:", data)  # Log to console
    return jsonify({"message": "Webhook received!"}), 200

@app.route('/webhook', methods=['GET'])
def webhook_info():
    return jsonify({"message": "Webhook server is running!", "status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
