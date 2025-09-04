#!/usr/bin/env python3
"""
Backend Flask pour l'intégration OAuth TikTok
Gère l'authentification et la publication de vidéos
"""

from flask import Flask, request, jsonify, redirect, session, render_template_string
from flask_cors import CORS
import requests
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Clé secrète pour les sessions
CORS(app)

# Configuration TikTok
CLIENT_KEY = "sbaw9sck9i4u94jbyw"
CLIENT_SECRET = "Iwl5nMhrxo3S5xUfixLam6Ha74DR19am"
REDIRECT_URI = "https://iliaskalalou.github.io/Pianorama_publish/"
SCOPES = "user.info.basic,video.publish"

# Pour le développement local
LOCAL_REDIRECT_URI = "http://localhost:5000/callback"

@app.route('/')
def index():
    """Page d'accueil avec bouton de connexion TikTok"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pianorama Publish - Backend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
            }
            .btn {
                display: inline-block;
                padding: 1rem 2rem;
                background: #000;
                color: white;
                text-decoration: none;
                border-radius: 50px;
                margin: 1rem;
            }
            .btn:hover {
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 Pianorama Publish Backend</h1>
            <p>Test de l'intégration OAuth TikTok</p>
            <a href="/auth" class="btn">Se connecter avec TikTok</a>
            <br>
            <small>Backend en développement local</small>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/auth')
def auth():
    """Redirige vers TikTok pour l'authentification"""
    # Générer un state pour la sécurité
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Construire l'URL d'autorisation
    auth_url = "https://www.tiktok.com/v2/auth/authorize/"
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": LOCAL_REDIRECT_URI,  # Pour le test local
        "state": state
    }
    
    # Construire l'URL complète
    auth_url_full = f"{auth_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    return redirect(auth_url_full)

@app.route('/callback')
def callback():
    """Callback OAuth - reçoit le code d'autorisation"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return f"Erreur OAuth: {error}", 400
    
    if not code:
        return "Code d'autorisation manquant", 400
    
    # Vérifier le state
    if state != session.get('oauth_state'):
        return "State invalide - possible attaque CSRF", 400
    
    # Échanger le code contre un token
    token_url = "https://open-api.tiktok.com/oauth/access_token/"
    
    token_data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": LOCAL_REDIRECT_URI
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        token_result = response.json()
        
        if response.status_code == 200 and "data" in token_result:
            access_token = token_result["data"].get("access_token")
            if access_token:
                # Sauvegarder le token en session
                session['access_token'] = access_token
                session['token_data'] = token_result["data"]
                
                # Récupérer les infos utilisateur
                user_info = get_user_info(access_token)
                
                return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Connexion réussie</title>
                    <style>
                        body {{
                            font-family: Arial;
                            background: linear-gradient(135deg, #667eea, #764ba2);
                            color: white;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }}
                        .success {{
                            background: rgba(255,255,255,0.1);
                            padding: 2rem;
                            border-radius: 20px;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="success">
                        <h1>✅ Connexion réussie!</h1>
                        <p>Token obtenu avec succès</p>
                        <p>Utilisateur: {user_info.get('display_name', 'Inconnu')}</p>
                        <p>Username: {user_info.get('username', 'Inconnu')}</p>
                        <a href="/test-publish" style="color: white;">Tester la publication</a>
                    </div>
                </body>
                </html>
                """
        
        return f"Erreur lors de l'obtention du token: {token_result}", 400
        
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/api/user-info')
def api_user_info():
    """API pour récupérer les infos utilisateur"""
    token = session.get('access_token')
    if not token:
        return jsonify({"error": "Non authentifié"}), 401
    
    user_info = get_user_info(token)
    return jsonify(user_info)

def get_user_info(access_token):
    """Récupère les informations de l'utilisateur TikTok"""
    url = "https://open.tiktokapis.com/v2/user/info/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                return result.get("data", {}).get("user", {})
    except:
        pass
    
    return {}

@app.route('/api/publish', methods=['POST'])
def publish_video():
    """API pour publier une vidéo sur TikTok"""
    token = session.get('access_token')
    if not token:
        return jsonify({"error": "Non authentifié"}), 401
    
    # Récupérer le fichier vidéo
    if 'video' not in request.files:
        return jsonify({"error": "Aucune vidéo fournie"}), 400
    
    video = request.files['video']
    title = request.form.get('title', 'Test Video')
    privacy = request.form.get('privacy', 'SELF_ONLY')
    
    # Ici, implémenter la logique de publication TikTok
    # Pour le moment, on simule
    
    return jsonify({
        "success": True,
        "message": f"Vidéo '{title}' publiée avec succès en mode {privacy}"
    })

@app.route('/test-publish')
def test_publish():
    """Page de test pour publier une vidéo"""
    token = session.get('access_token')
    if not token:
        return redirect('/auth')
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Publication</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 2rem;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 20px;
            }
            input, button {
                display: block;
                width: 100%;
                margin: 1rem 0;
                padding: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📹 Test de publication TikTok</h1>
            <form action="/api/publish" method="POST" enctype="multipart/form-data">
                <input type="text" name="title" placeholder="Titre de la vidéo" required>
                <select name="privacy">
                    <option value="SELF_ONLY">Privé</option>
                    <option value="MUTUAL_FOLLOW_FRIENDS">Amis</option>
                    <option value="PUBLIC_TO_EVERYONE">Public</option>
                </select>
                <input type="file" name="video" accept="video/*" required>
                <button type="submit">Publier sur TikTok</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Serveur Flask démarré sur http://localhost:5000")
    print("📌 Pour tester:")
    print("   1. Allez sur http://localhost:5000")
    print("   2. Cliquez sur 'Se connecter avec TikTok'")
    print("   3. Autorisez l'application")
    print("\n⚠️  Note: Pour la production, utilisez HTTPS et le vrai REDIRECT_URI")
    
    app.run(debug=True, port=5000)
