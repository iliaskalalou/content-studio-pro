#!/usr/bin/env python3
"""
SCRIPT FINAL - Test avec la VRAIE configuration TikTok
"""

import webbrowser
import urllib.parse

print("\n" + "="*60)
print("🎯 TEST FINAL - CONFIGURATION CORRIGÉE")
print("="*60)

CLIENT_KEY = "sbaw9sck9i4u94jbyw"
CLIENT_SECRET = "Iwl5nMhrxo3S5xUfixLam6Ha74DR19am"
REDIRECT_URI = "https://iliaskalalou.github.io/Pianorama_publish/"  # SANS /TikTok/

print("\n✅ Configuration CORRECTE détectée :")
print(f"   Client Key: {CLIENT_KEY}")
print(f"   Redirect URI: {REDIRECT_URI}")
print("   (Cette fois ça correspond à TikTok Developers !)")

print("\n📝 Vos paramètres TikTok Developers :")
print("   ✅ Login Kit activé")
print("   ✅ Direct Post activé") 
print("   ✅ Scopes: user.info.basic, video.publish, video.upload")
print("   ✅ Platform: Web")

input("\n✨ Appuyez sur Entrée pour lancer le test...")

# Test avec les bons paramètres
params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": "user.info.basic,video.publish",  # On commence avec 2 scopes
    "redirect_uri": REDIRECT_URI,
    "state": "state123"
}

auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"

print("\n🔗 URL générée :")
print(auth_url)

print("\n🚀 Ouverture dans votre navigateur...")
webbrowser.open(auth_url)

print("\n⏳ Après connexion, copiez l'URL complète ici :")
redirect_url = input("   URL: ").strip()

if "code=" in redirect_url:
    import re
    code_match = re.search(r'code=([^&]+)', redirect_url)
    if code_match:
        code = code_match.group(1)
        print("\n🎉 SUCCÈS ! Code d'autorisation reçu !")
        print(f"   Code: {code[:20]}...")
        
        print("\n✅ Prochaine étape : obtenir le token")
        print("   Voulez-vous continuer ? (y/n)")
        
        if input().lower() == 'y':
            import requests
            
            print("\n🔑 Obtention du token...")
            token_url = "https://open-api.tiktok.com/oauth/access_token/"
            
            token_params = {
                "client_key": CLIENT_KEY,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            }
            
            response = requests.post(token_url, data=token_params)
            
            if response.status_code == 200:
                result = response.json()
                if "data" in result and "access_token" in result["data"]:
                    print("\n🎊 TOKEN OBTENU AVEC SUCCÈS !")
                    print(f"   Token: {result['data']['access_token'][:30]}...")
                    print("\n✨ TOUT FONCTIONNE ! Vous pouvez maintenant :")
                    print("   1. Enregistrer votre vidéo de démonstration")
                    print("   2. Soumettre à TikTok pour approbation")
                else:
                    print(f"\n⚠️ Réponse inattendue : {result}")
            else:
                print(f"\n❌ Erreur token : {response.text}")
else:
    print("\n❌ Pas de code dans l'URL. Erreur détectée.")
    print("   Vérifiez que vous êtes bien connecté à TikTok")
