from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

MODEL_URL = "http://localhost:11434/api/generate"

@app.route('/api/message', methods=['POST'])
def proxy_message():
    user_prompt = request.json.get('prompt', '')

    payload = {
        "model": "Cognicare",
        "prompt": f"User: {user_prompt}\nCognicare:"
    }

    try:
        response = requests.post(MODEL_URL, json=payload, stream=True)
        output = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    output += data["response"]
        return jsonify({"reply": output.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
