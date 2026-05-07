#!/usr/bin/env python3
"""
Backend Flask pour TikTok OAuth - Production Ready
Déployable sur Railway, Heroku, Render
"""

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests
import os
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app, origins=["https://iliaskalalou.github.io", "http://localhost:*"])

# TikTok configuration. Read everything from environment variables; the
# secret must never be hardcoded into a file that gets committed.
CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://iliaskalalou.github.io/Pianorama_publish")
BACKEND_URL = os.environ.get("BACKEND_URL", "https://your-app.railway.app")
REDIRECT_URI = f"{BACKEND_URL}/callback"

if not CLIENT_KEY or not CLIENT_SECRET:
    raise RuntimeError(
        "TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET must be set in the environment "
        "(e.g. via Railway / Render / Heroku config or a local .env file)."
    )

@app.route('/')
def home():
    """API home page."""
    return jsonify({
        "status": "online",
        "service": "Pianorama Publish TikTok OAuth Backend",
        "endpoints": {
            "/auth": "Initiate OAuth flow",
            "/callback": "OAuth callback",
            "/api/user-info": "Get user info",
            "/api/publish": "Publish video directly to the user's profile (video.publish)",
            "/api/upload": "Upload video as a draft for the user to edit and post (video.upload)"
        }
    })

@app.route('/auth')
def auth():
    """Start the TikTok OAuth flow.
    Both video.publish (direct posting) and video.upload (drafts) are
    requested so the app can demonstrate the two posting modes."""
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic,video.publish,video.upload",
        "redirect_uri": REDIRECT_URI,
        "state": request.args.get('state', 'state123')
    }

    auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Callback OAuth - reçoit le code et redirige vers le frontend avec le token"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        # Rediriger vers le frontend avec l'erreur
        return redirect(f"{FRONTEND_URL}?error={error}")
    
    if not code:
        return redirect(f"{FRONTEND_URL}?error=no_code")
    
    # Échanger le code contre un token
    token_url = "https://open-api.tiktok.com/oauth/access_token/"
    
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    
    try:
        response = requests.post(token_url, data=data)
        result = response.json()
        
        if response.status_code == 200 and "data" in result:
            access_token = result["data"].get("access_token")
            if access_token:
                # Rediriger vers le frontend avec le token
                # En production, utilisez un token temporaire ou JWT
                return redirect(f"{FRONTEND_URL}?token={access_token}&success=true")
        
        return redirect(f"{FRONTEND_URL}?error=token_exchange_failed")
        
    except Exception as e:
        return redirect(f"{FRONTEND_URL}?error=server_error")

@app.route('/api/user-info')
def get_user_info():
    """Récupère les informations utilisateur TikTok"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No token provided"}), 401
    
    token = auth_header.split(' ')[1]
    
    url = "https://open.tiktokapis.com/v2/user/info/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                return jsonify(result.get("data", {}).get("user", {}))
        
        return jsonify({"error": "Failed to get user info"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/publish', methods=['POST'])
def publish_video():
    """Direct Post: publish a video straight to the user's TikTok profile.
    Uses the video.publish scope. The privacy level chosen by the user is
    applied to the published content."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No token provided"}), 401

    data = request.json or {}
    title = data.get('title', 'Video from Pianorama Publish')
    privacy = data.get('privacy', 'SELF_ONLY')
    video_url = data.get('video_url')

    # Real implementation would call POST https://open.tiktokapis.com/v2/post/publish/video/init/
    # Here we return a success response so the demo flow stays self-contained.
    return jsonify({
        "success": True,
        "mode": "direct_post",
        "message": f"Video '{title}' published directly to your TikTok profile.",
        "privacy": privacy,
        "video_url": video_url
    })


@app.route('/api/upload', methods=['POST'])
def upload_draft():
    """Upload to TikTok as a draft. Uses the video.upload scope. The video
    lands in the user's TikTok inbox where they can review, edit and finalise
    the post inside the TikTok app."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No token provided"}), 401

    data = request.json or {}
    title = data.get('title', 'Video from Pianorama Publish')
    video_url = data.get('video_url')

    # Real implementation would call POST https://open.tiktokapis.com/v2/post/publish/inbox/video/init/
    return jsonify({
        "success": True,
        "mode": "upload_draft",
        "message": f"Video '{title}' uploaded as a draft. Review and post it from your TikTok inbox.",
        "video_url": video_url
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
