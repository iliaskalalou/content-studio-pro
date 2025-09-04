#!/usr/bin/env python3
"""
Script simplifié avec seulement 2 scopes pour l'approbation TikTok
Retire video.upload pour éviter la confusion
"""

import os
import sys
import time
import requests
import webbrowser
import urllib.parse
import re

class TikTokSimplifiedDemo:
    def __init__(self, client_key, client_secret):
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = "https://iliaskalalou.github.io/TikTok/"  # URL vérifiée sur TikTok !
        self.access_token = None
        # SANDBOX pour la démo
        self.base_url = "https://open-sandbox.tiktokapis.com"
        self.graph_version = "v2"
        
    def run_demo(self, video_path):
        """Démonstration simplifiée avec 2 scopes seulement"""
        
        print("\n" + "=" * 60)
        print("🎬 DÉMONSTRATION SIMPLIFIÉE - 2 SCOPES SEULEMENT")
        print("   Sandbox Environment")
        print("=" * 60)
        
        # 1. OAuth avec seulement 2 scopes
        print("\n📱 ÉTAPE 1: AUTORISATION (2 scopes)")
        print("-" * 40)
        
        params = {
            "client_key": self.client_key,
            "response_type": "code",
            "scope": "user.info.basic,video.publish",  # Seulement 2 scopes!
            "redirect_uri": self.redirect_uri,
            "state": "state123"
        }
        
        auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
        
        print("Scopes demandés:")
        print("  1. user.info.basic ✅")
        print("  2. video.publish ✅")
        print("  3. video.upload ❌ (NON DEMANDÉ)")
        print("\nOuvrez cette URL:")
        print(auth_url)
        
        webbrowser.open(auth_url)
        redirect_url = input("\nCollez l'URL de redirection: ").strip()
        
        code_match = re.search(r'code=([^&]+)', redirect_url)
        if not code_match:
            print("❌ Erreur: Code non trouvé")
            sys.exit(1)
            
        auth_code = code_match.group(1)
        print("✅ Code obtenu")
        
        # 2. Token
        print("\n🔑 ÉTAPE 2: TOKEN D'ACCÈS")
        print("-" * 40)
        
        token_url = "https://open-api.tiktok.com/oauth/access_token/"
        token_params = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(token_url, data=token_params)
        if response.status_code != 200:
            print(f"❌ Erreur token: {response.text}")
            sys.exit(1)
            
        result = response.json()
        self.access_token = result.get("data", {}).get("access_token")
        print("✅ Token obtenu")
        
        # 3. Demo user.info.basic
        print("\n👤 DÉMO SCOPE 1: user.info.basic")
        print("-" * 40)
        
        user_url = f"{self.base_url}/{self.graph_version}/user/info/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json().get("data", {}).get("user", {})
            print("✅ Informations utilisateur:")
            print(f"   Nom: {user_data.get('display_name', 'N/A')}")
            print(f"   ID: {user_data.get('open_id', 'N/A')}")
            
        # 4. Demo video.publish
        print("\n📹 DÉMO SCOPE 2: video.publish")
        print("-" * 40)
        print("Publication directe en mode privé (sandbox)")
        
        file_size = os.path.getsize(video_path)
        
        publish_url = f"{self.base_url}/{self.graph_version}/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        publish_params = {
            "post_info": {
                "title": "Test Sandbox - Publication Directe",
                "privacy_level": "SELF_ONLY",
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
        
        response = requests.post(publish_url, headers=headers, json=publish_params)
        if response.status_code == 200:
            result = response.json()
            if result.get("error", {}).get("code") == "ok":
                publish_id = result["data"]["publish_id"]
                upload_url = result["data"]["upload_url"]
                print("✅ Publication initialisée")
                print(f"   ID: {publish_id}")
                
                # Upload
                print("\n📤 Upload de la vidéo...")
                with open(video_path, 'rb') as f:
                    video_data = f.read()
                    
                upload_headers = {
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                    "Content-Length": str(file_size),
                    "Content-Type": "video/mp4"
                }
                
                response = requests.put(upload_url, headers=upload_headers, data=video_data)
                if response.status_code in [200, 201]:
                    print("✅ Vidéo uploadée")
                    
                    # Vérifier statut
                    print("\n⏳ Vérification du statut...")
                    status_url = f"{self.base_url}/{self.graph_version}/post/publish/status/fetch/"
                    
                    for i in range(5):
                        time.sleep(2)
                        response = requests.post(
                            status_url, 
                            headers={"Authorization": f"Bearer {self.access_token}",
                                   "Content-Type": "application/json"},
                            json={"publish_id": publish_id}
                        )
                        
                        if response.status_code == 200:
                            status = response.json().get("data", {}).get("status", "")
                            print(f"   Status: {status}")
                            if status == "PUBLISHED":
                                print("✅ Vidéo publiée avec succès!")
                                break
        
        print("\n" + "=" * 60)
        print("✅ DÉMONSTRATION TERMINÉE")
        print("   Scopes démontrés: 2/2")
        print("   - user.info.basic ✅")
        print("   - video.publish ✅")
        print("=" * 60)


if __name__ == "__main__":
    CLIENT_KEY = "sbaw9sck9i4u94jbyw"
    CLIENT_SECRET = "Iwl5nMhrxo3S5xUfixLam6Ha74DR19am"
    
    if len(sys.argv) < 2:
        print("Usage: python3 simple_demo.py <video.mp4>")
        sys.exit(1)
    
    demo = TikTokSimplifiedDemo(CLIENT_KEY, CLIENT_SECRET)
    demo.run_demo(sys.argv[1])
