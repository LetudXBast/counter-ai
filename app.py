from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Route 1 : Bonjour
@app.route('/api/hello', methods=['POST'])
def hello():
    data = request.get_json()
    name = data.get('name', 'inconnu')
    return jsonify({'message': f'Bonjour {name} depuis Flask !'})

# Route 2 : Compter les lettres
@app.route('/api/count', methods=['POST'])
def count_letters():
    data = request.get_json()
    texte = data.get('texte', '')
    nb_lettres = sum(1 for c in texte if c.isalpha())
    return jsonify({'nb_lettres': nb_lettres})

# ✅ Route 3 : Résumé avec Mistral AI
@app.route('/api/llm-summary', methods=['POST'])
def llm_summary():
    data = request.get_json()
    texte = data.get('texte', '').strip()

    if not texte:
        return jsonify({'resume': ''})

    try:
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            return jsonify({'error': 'Clé API Mistral non configurée'}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "user", "content": f"Résume ce texte en 3 phrases claires et concises : {texte}"}
            ],
            "temperature": 0.7
        }

        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        resultat = response.json()

        resume = resultat['choices'][0]['message']['content']
        return jsonify({'resume': resume})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Port pour Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
