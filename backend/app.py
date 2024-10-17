from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Inizializza Firebase Admin
cred = credentials.Certificate('config/firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print("Dati ricevuti per la registrazione:", data)

    try:
        # Crea l'utente in Firebase Authentication
        user = auth.create_user(
            email=data['email'],
            password=data['password'],
            display_name=data.get('username'),  # Username
            disabled=False
        )
        print(f"Utente creato con successo: {user.uid}")

        # Salva i dati dell'utente nel database Firestore
        user_data = {
            "uid": user.uid,
            "nome": data['nome'],
            "cognome": data['cognome'],
            "sesso": data['gender'],
            "via": data['address'],
            "cap": data['cap_code'],
            "codice_fiscale": data['tax_code'],
            "cellulare": data['telefono'],
        }

        # Salva i dati nella collezione 'utenti'
        db.collection('osteoarthritiis-db').document(user.uid).set(user_data)
        print("Dati utente salvati nel database:", user_data)

        return jsonify({"message": "User registered successfully.", "user_id": user.uid}), 200

    except Exception as e:
        print("Errore nella registrazione:", str(e))
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = auth.get_user_by_email(data['email'])
        return jsonify({"message": "Login successful", "user_id": user.uid}), 200
    except Exception as e:
        print("Errore nel login:", str(e))
        return jsonify({"error": str(e)}), 400

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080') 
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
