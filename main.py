from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Récupérer l'App ID Wolfram Alpha depuis les variables d'environnement
WOLFRAM_APP_ID = os.getenv('WOLFRAM_APP_ID')

@app.route('/api/wolfram', methods=['GET'])
def wolfram_query():
    # Récupérer l'expression mathématique depuis les paramètres de l'URL
    expression = request.args.get('expression')
    
    if not expression:
        return jsonify({"error": "Veuillez fournir une expression mathématique."}), 400

    # Construire l'URL de la requête à Wolfram Alpha
    url = f"https://api.wolframalpha.com/v1/result?i={expression}&appid={WOLFRAM_APP_ID}"

    try:
        # Envoyer la requête à Wolfram Alpha
        response = requests.get(url)
        response.raise_for_status()

        # Retourner la réponse de Wolfram Alpha
        return jsonify({"expression": expression, "result": response.text})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur lors de la communication avec Wolfram Alpha.", "details": str(e)}), 500

if __name__ == '__main__':
    # Lancer l'application Flask sur 0.0.0.0 pour qu'elle soit accessible publiquement
    app.run(host='0.0.0.0', port=5000)
