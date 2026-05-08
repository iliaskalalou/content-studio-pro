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
# Render's free tier accepts up to ~100 MB request bodies; cap to 100 MB.
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
CORS(app, origins=["https://iliaskalalou.github.io", "http://localhost:*"])

# TikTok configuration. Read everything from environment variables; the
# secret must never be hardcoded into a file that gets committed.
CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://iliaskalalou.github.io/content-studio-pro")
BACKEND_URL = os.environ.get("BACKEND_URL", "https://content-studio-pro.onrender.com")
REDIRECT_URI = f"{BACKEND_URL}/callback"

if not CLIENT_KEY or not CLIENT_SECRET:
    raise RuntimeError(
        "TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET must be set in the environment "
        "(e.g. via Railway / Render / Heroku config or a local .env file)."
    )

VERSION = "v2.1-2026-05-07-real-publish"


@app.route('/')
def home():
    """API home page."""
    return jsonify({
        "status": "online",
        "version": VERSION,
        "service": "Content Studio Pro Backend",
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
    """OAuth callback. Receives the auth code, exchanges it for an access
    token via TikTok's V2 token endpoint, then redirects back to the
    frontend with the token in the URL."""
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return redirect(f"{FRONTEND_URL}?error={error}")
    if not code:
        return redirect(f"{FRONTEND_URL}?error=no_code")

    # V2 OAuth token endpoint. Must match the V2 auth URL used in /auth.
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    try:
        response = requests.post(token_url, data=data, headers=headers, timeout=10)
        result = response.json()
    except Exception as e:
        app.logger.error(f"Token exchange request failed: {e}")
        return redirect(f"{FRONTEND_URL}?error=server_error")

    # V2 response: access_token is at the top level, not under "data".
    access_token = result.get("access_token")
    if response.status_code == 200 and access_token:
        return redirect(f"{FRONTEND_URL}?token={access_token}&success=true")

    # Log the actual TikTok error to make future debugging possible.
    app.logger.error(
        f"Token exchange failed (status {response.status_code}): {result}"
    )
    err_code = result.get("error", "token_exchange_failed")
    return redirect(f"{FRONTEND_URL}?error={err_code}")

@app.route('/api/user-info')
def get_user_info():
    """Fetch TikTok user info via the V2 endpoint. The fields parameter is
    mandatory in V2 — without it the API returns an error."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No token provided"}), 401

    token = auth_header.split(' ')[1]

    url = "https://open.tiktokapis.com/v2/user/info/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"fields": "open_id,union_id,avatar_url,display_name"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                return jsonify(result.get("data", {}).get("user", {}))
            app.logger.error(f"User info API error: {result}")
            return jsonify({"error": result.get("error", {})}), 400
        app.logger.error(f"User info HTTP {response.status_code}: {response.text}")
        return jsonify({"error": "Failed to get user info"}), 400
    except Exception as e:
        app.logger.error(f"User info request failed: {e}")
        return jsonify({"error": str(e)}), 500

def _read_token():
    """Extract the OAuth bearer token from the request headers."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ', 1)[1]


def _read_video_file():
    """Return (filename, bytes) for the uploaded video, or None.
    The frontend can either send the file as multipart/form-data under the
    'video' key, or fall back to a JSON body during the demo."""
    if 'video' in request.files:
        f = request.files['video']
        return f.filename, f.read()
    return None, None


def _post_to_tiktok(init_url, init_body, file_bytes, token):
    """Run the TikTok V2 publish flow:
    1. POST to init_url to obtain an upload_url and publish_id.
    2. PUT the video bytes to that upload_url.
    Returns (status_code, response_payload).
    """
    init_resp = requests.post(
        init_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json=init_body,
        timeout=15,
    )
    init_data = init_resp.json()
    if init_resp.status_code != 200 or init_data.get("error", {}).get("code") not in ("ok", None):
        app.logger.error(f"TikTok init failed (HTTP {init_resp.status_code}): {init_data}")
        return init_resp.status_code, init_data

    upload_url = init_data.get("data", {}).get("upload_url")
    publish_id = init_data.get("data", {}).get("publish_id")
    if not upload_url:
        app.logger.error(f"No upload_url returned by TikTok: {init_data}")
        return 500, {"error": {"code": "no_upload_url", "message": "TikTok did not return an upload URL"}}

    file_size = len(file_bytes)
    put_resp = requests.put(
        upload_url,
        data=file_bytes,
        headers={
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
        },
        timeout=60,
    )
    if put_resp.status_code not in (200, 201):
        app.logger.error(f"TikTok upload PUT failed (HTTP {put_resp.status_code}): {put_resp.text}")
        return put_resp.status_code, {"error": {"code": "upload_failed", "message": put_resp.text[:500]}}

    return 200, {"publish_id": publish_id}


@app.route('/api/publish', methods=['POST'])
def publish_video():
    """Direct Post: publish a video straight to the user's TikTok profile.
    Uses the video.publish scope. The privacy level chosen by the user is
    applied to the published content."""
    token = _read_token()
    if not token:
        return jsonify({"error": "No token provided"}), 401

    title = request.form.get('title', 'Video from Pianorama Publish')
    privacy = request.form.get('privacy', 'SELF_ONLY')
    filename, file_bytes = _read_video_file()
    if not file_bytes:
        return jsonify({"success": False, "message": "No video file provided"}), 400

    init_body = {
        "post_info": {
            "title": title,
            "privacy_level": privacy,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 0,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": len(file_bytes),
            "chunk_size": len(file_bytes),
            "total_chunk_count": 1,
        },
    }

    status, payload = _post_to_tiktok(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        init_body, file_bytes, token,
    )

    if status == 200:
        return jsonify({
            "success": True,
            "mode": "direct_post",
            "publish_id": payload.get("publish_id"),
            "filename": filename,
            "privacy": privacy,
            "message": f"Video '{title}' was sent to TikTok. In Sandbox the post is private to the connected creator.",
        })

    return jsonify({
        "success": False,
        "mode": "direct_post",
        "error": payload.get("error", {}),
        "message": payload.get("error", {}).get("message", "Direct post failed."),
    }), status if status != 200 else 500


@app.route('/api/upload', methods=['POST'])
def upload_draft():
    """Upload to TikTok as a draft. Uses the video.upload scope. The video
    lands in the user's TikTok inbox where they can review, edit and finalise
    the post inside the TikTok app."""
    token = _read_token()
    if not token:
        return jsonify({"error": "No token provided"}), 401

    title = request.form.get('title', 'Video from Pianorama Publish')
    filename, file_bytes = _read_video_file()
    if not file_bytes:
        return jsonify({"success": False, "message": "No video file provided"}), 400

    init_body = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": len(file_bytes),
            "chunk_size": len(file_bytes),
            "total_chunk_count": 1,
        },
    }

    status, payload = _post_to_tiktok(
        "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
        init_body, file_bytes, token,
    )

    if status == 200:
        return jsonify({
            "success": True,
            "mode": "upload_draft",
            "publish_id": payload.get("publish_id"),
            "filename": filename,
            "message": f"Video '{title}' uploaded as a draft. Open your TikTok inbox to finalise the post.",
        })

    return jsonify({
        "success": False,
        "mode": "upload_draft",
        "error": payload.get("error", {}),
        "message": payload.get("error", {}).get("message", "Draft upload failed."),
    }), status if status != 200 else 500

# --- TikTok URL verification files ---
# TikTok asks for a static .txt file at the URL we declared as Redirect URI.
# Since Render does not serve static files, we expose the file content
# through a Flask route that matches several common verification paths.
TIKTOK_VERIFICATIONS = {
    "tiktokhgNUP2jOBL4lC10ioiEatBEgMxy0ow8L.txt":
        "tiktok-developers-site-verification=hgNUP2jOBL4lC10ioiEatBEgMxy0ow8L",
}


def _serve_tiktok_verification(filename):
    body = TIKTOK_VERIFICATIONS.get(filename)
    if body is None:
        return "Not Found", 404
    return body, 200, {"Content-Type": "text/plain"}


@app.route('/<path:filename>.txt')
def tiktok_verification_root(filename):
    """Serve TikTok verification files at the domain root, e.g.
    https://pianorama-publish.onrender.com/tiktokXXX.txt"""
    return _serve_tiktok_verification(f"{filename}.txt")


@app.route('/callback/<path:filename>.txt')
def tiktok_verification_under_callback(filename):
    """Serve TikTok verification files directly under /callback, e.g.
    https://pianorama-publish.onrender.com/callback/tiktokXXX.txt"""
    return _serve_tiktok_verification(f"{filename}.txt")


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
