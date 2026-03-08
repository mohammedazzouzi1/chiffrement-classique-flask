from flask import Flask, render_template, request, jsonify
from crypto_logic import (
    cesar_chiffrement,
    cesar_dechiffrement,
    vernam_chiffrement,
    vernam_dechiffrement,
    vigenere_chiffrement,
    vigenere_dechiffrement,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    algorithm = data.get("algorithm", "")
    action = data.get("action", "")
    texte = data.get("texte", "").upper()
    cle = data.get("cle", "").upper()

    if not texte:
        return jsonify({"error": "Veuillez entrer un texte."}), 400
    if not cle:
        return jsonify({"error": "Veuillez entrer une clé."}), 400

    if not texte.isalpha():
        return jsonify(
            {"error": "Le texte doit contenir uniquement des lettres (A-Z)."}
        ), 400

    try:
        if algorithm == "cesar":
            cle_int = int(cle)
            if action == "chiffrement":
                resultat = cesar_chiffrement(texte, cle_int)
            else:
                resultat = cesar_dechiffrement(texte, cle_int)

        elif algorithm == "vernam":
            if not cle.isalpha():
                return jsonify(
                    {
                        "error": "La clé Vernam doit contenir uniquement des lettres (A-Z)."
                    }
                ), 400
            if len(cle) != len(texte):
                return jsonify(
                    {
                        "error": f"La clé Vernam doit avoir la même longueur que le texte ({len(texte)} caractères)."
                    }
                ), 400
            if action == "chiffrement":
                resultat = vernam_chiffrement(texte, cle)
            else:
                resultat = vernam_dechiffrement(texte, cle)

        elif algorithm == "vigenere":
            if not cle.isalpha():
                return jsonify(
                    {
                        "error": "La clé Vigenère doit contenir uniquement des lettres (A-Z)."
                    }
                ), 400
            if action == "chiffrement":
                resultat = vigenere_chiffrement(texte, cle)
            else:
                resultat = vigenere_dechiffrement(texte, cle)

        else:
            return jsonify({"error": "Algorithme invalide."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"resultat": resultat})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
