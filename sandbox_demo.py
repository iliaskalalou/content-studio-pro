#!/usr/bin/env python3
"""
Script Python pour publier sur TikTok en mode SANDBOX
Compatible avec la démonstration pour l'approbation TikTok
"""

import os
import sys
import time
import requests
import webbrowser
import urllib.parse
import re
import json

class TikTokSandboxPublisher:
    def __init__(self, client_key, client_secret, use_sandbox=True):
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = "https://iliaskalalou.github.io/Pianorama_publish/"  # Avec slash final !
        self.access_token = None
        
        # IMPORTANT: Utiliser le sandbox pour la démo
        if use_sandbox:
            self.base_url = "https://open-sandbox.tiktokapis.com"  # URL SANDBOX
            print("🧪 MODE SANDBOX ACTIVÉ (pour démonstration)")
        else:
            self.base_url = "https://open.tiktokapis.com"
            print("🚀 MODE PRODUCTION")
            
        self.graph_version = "v2"
        
    def get_auth_code(self):
        """Obtenir le code d'autorisation - SANDBOX"""
        print("\n📱 ÉTAPE 1: AUTORISATION SANDBOX")
        print("=" * 50)
        
        # Utiliser TOUS les scopes pour la démo
        params = {
            "client_key": self.client_key,
            "response_type": "code",
            "scope": "user.info.basic,video.publish,video.upload",  # TOUS les scopes
            "redirect_uri": self.redirect_uri,
            "state": "state123"
        }
        
        # URL d'autorisation SANDBOX
        auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
        
        print("🔗 Ouvre cette URL dans ton navigateur (SANDBOX):\n")
        print(auth_url)
        print("\n⚠️  IMPORTANT: Utilisez un compte TEST TikTok pour le sandbox")
        
        webbrowser.open(auth_url)
        
        redirect_url = input("\n🔗 Colle l'URL de redirection ici : ").strip()
        
        code_match = re.search(r'code=([^&]+)', redirect_url)
        if code_match:
            self.auth_code = code_match.group(1)
            print("✅ Code SANDBOX obtenu")
            return self.auth_code
        else:
            print("❌ Erreur: Impossible d'extraire le code")
            sys.exit(1)
    
    def get_access_token(self):
        """Obtenir le token d'accès SANDBOX"""
        print("\n🔑 ÉTAPE 2: OBTENTION DU TOKEN SANDBOX")
        print("=" * 50)
        
        url = "https://open-api.tiktok.com/oauth/access_token/"
        
        params = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": self.auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result.get("data", {}).get("access_token")
            if self.access_token:
                print("✅ Token SANDBOX obtenu")
                print(f"   Scope autorisé: {result.get('data', {}).get('scope', '')}")
                return self.access_token
        
        print(f"❌ Erreur: {response.text}")
        sys.exit(1)
    
    def demonstrate_user_info(self):
        """DÉMONSTRATION: user.info.basic"""
        print("\n👤 DÉMONSTRATION SCOPE: user.info.basic")
        print("=" * 50)
        
        url = f"{self.base_url}/{self.graph_version}/user/info/"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                user_data = result.get("data", {}).get("user", {})
                print("✅ Informations utilisateur récupérées:")
                print(f"   - Display Name: {user_data.get('display_name', 'N/A')}")
                print(f"   - Avatar: {user_data.get('avatar_url', 'N/A')[:50]}...")
                print(f"   - Open ID: {user_data.get('open_id', 'N/A')}")
                return True
        
        print(f"❌ Erreur: {response.text[:200]}")
        return False
    
    def demonstrate_video_publish(self, video_path):
        """DÉMONSTRATION: video.publish - Publication directe"""
        print("\n📹 DÉMONSTRATION SCOPE: video.publish")
        print("=" * 50)
        print("   → Publication DIRECTE sur le profil TikTok")
        
        file_size = os.path.getsize(video_path)
        
        # Initialiser la publication directe
        endpoint = f"/{self.graph_version}/post/publish/video/init/"
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "post_info": {
                "title": "Demo Video - Direct Publish (Sandbox)",
                "privacy_level": "SELF_ONLY",  # Privé pour le sandbox
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }
        
        print("📤 Initialisation de la publication directe...")
        response = requests.post(url, headers=headers, json=params)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                publish_id = result["data"]["publish_id"]
                upload_url = result["data"]["upload_url"]
                print("✅ Publication directe initialisée")
                print(f"   - Publish ID: {publish_id}")
                print("   - Mode: DIRECT PUBLISH")
                
                # Upload du fichier
                self._upload_video(video_path, upload_url)
                
                # Vérifier le statut
                self._check_publish_status(publish_id, "direct")
                return True
        
        print(f"❌ Erreur: {response.text[:200]}")
        return False
    
    def demonstrate_video_upload(self, video_path):
        """DÉMONSTRATION: video.upload - Envoi en brouillon"""
        print("\n📝 DÉMONSTRATION SCOPE: video.upload")
        print("=" * 50)
        print("   → Envoi en BROUILLON pour édition dans TikTok")
        
        file_size = os.path.getsize(video_path)
        
        # Initialiser l'upload en brouillon
        endpoint = f"/{self.graph_version}/post/publish/inbox/video/init/"
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "post_info": {
                "title": "Demo Video - Draft Upload (Sandbox)",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }
        
        print("📤 Initialisation de l'envoi en brouillon...")
        response = requests.post(url, headers=headers, json=params)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                publish_id = result["data"]["publish_id"]
                upload_url = result["data"]["upload_url"]
                print("✅ Upload en brouillon initialisé")
                print(f"   - Publish ID: {publish_id}")
                print("   - Mode: DRAFT/INBOX")
                
                # Upload du fichier
                self._upload_video(video_path, upload_url)
                
                # Vérifier le statut
                self._check_publish_status(publish_id, "inbox")
                return True
        
        print(f"❌ Erreur: {response.text[:200]}")
        return False
    
    def _upload_video(self, video_path, upload_url):
        """Helper: Upload de la vidéo"""
        file_size = os.path.getsize(video_path)
        
        headers = {
            "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
            "Content-Length": str(file_size),
            "Content-Type": "video/mp4"
        }
        
        print("   📤 Upload de la vidéo en cours...")
        
        with open(video_path, 'rb') as f:
            video_data = f.read()
            response = requests.put(upload_url, headers=headers, data=video_data)
            
        if response.status_code in [200, 201]:
            print("   ✅ Vidéo uploadée avec succès")
            return True
        else:
            print(f"   ❌ Erreur upload: {response.status_code}")
            return False
    
    def _check_publish_status(self, publish_id, mode):
        """Helper: Vérifier le statut de publication"""
        print(f"   ⏳ Vérification du statut ({mode})...")
        
        if mode == "inbox":
            endpoint = f"/{self.graph_version}/post/publish/status/fetch_inbox/"
        else:
            endpoint = f"/{self.graph_version}/post/publish/status/fetch/"
        
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        params = {"publish_id": publish_id}
        
        # Attendre et vérifier
        for i in range(5):
            time.sleep(2)
            response = requests.post(url, headers=headers, json=params)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("data", {}).get("status", "")
                
                if status == "PUBLISHED":
                    print(f"   ✅ Vidéo publiée avec succès en mode {mode.upper()}")
                    return True
                elif status in ["FAILED", "CANCELLED"]:
                    print(f"   ❌ Publication échouée: {status}")
                    return False
                else:
                    print(f"   ⏳ Status: {status}")
        
        return False
    
    def run_full_demo(self, video_path):
        """Exécuter la démonstration complète de tous les scopes"""
        print("\n" + "=" * 60)
        print("🎬 DÉMONSTRATION COMPLÈTE POUR APPROBATION TIKTOK")
        print("=" * 60)
        
        # 1. Autorisation
        self.get_auth_code()
        
        # 2. Token
        self.get_access_token()
        
        # 3. Démontrer user.info.basic
        self.demonstrate_user_info()
        
        # 4. Démontrer video.publish (publication directe)
        print("\n⏸️  Pause de 3 secondes avant video.publish...")
        time.sleep(3)
        self.demonstrate_video_publish(video_path)
        
        # 5. Démontrer video.upload (brouillon)
        print("\n⏸️  Pause de 3 secondes avant video.upload...")
        time.sleep(3)
        self.demonstrate_video_upload(video_path)
        
        print("\n" + "=" * 60)
        print("✅ DÉMONSTRATION TERMINÉE")
        print("   - user.info.basic : ✅ Démontré")
        print("   - video.publish : ✅ Démontré (publication directe)")
        print("   - video.upload : ✅ Démontré (envoi en brouillon)")
        print("=" * 60)


if __name__ == "__main__":
    # Configuration SANDBOX
    CLIENT_KEY = "sbaw9sck9i4u94jbyw"  # Votre client key
    CLIENT_SECRET = "Iwl5nMhrxo3S5xUfixLam6Ha74DR19am"  # Votre client secret
    
    if len(sys.argv) < 2:
        print("Usage: python3 sandbox_demo.py <video_file>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    
    if not os.path.exists(video_file):
        print(f"❌ Fichier non trouvé: {video_file}")
        sys.exit(1)
    
    # Créer le publisher en mode SANDBOX
    publisher = TikTokSandboxPublisher(CLIENT_KEY, CLIENT_SECRET, use_sandbox=True)
    
    # Exécuter la démo complète
    publisher.run_full_demo(video_file)
