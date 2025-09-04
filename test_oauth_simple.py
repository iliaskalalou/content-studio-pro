#!/usr/bin/env python3
"""
Test OAuth TikTok - Version ULTRA SIMPLE
Teste seulement la connexion basique sans scopes complexes
"""

import webbrowser
import urllib.parse
import time

print("\n" + "="*60)
print("🔧 TEST OAUTH TIKTOK - VERSION MINIMALE")
print("="*60)

CLIENT_KEY = "sbaw9sck9i4u94jbyw"

# Liste des redirect URIs possibles
redirect_uris = [
    "https://iliaskalalou.github.io/Pianorama_publish/TikTok/",
    "https://iliaskalalou.github.io/TikTok/",
    "https://iliaskalalou.github.io/Pianorama_publish/",
]

print("\n📝 Quelle Redirect URI est configurée dans TikTok Developers ?")
for i, uri in enumerate(redirect_uris, 1):
    print(f"{i}. {uri}")
print("4. Autre (entrez manuellement)")

choice = input("\nChoix (1-4): ").strip()

if choice == "1":
    redirect_uri = redirect_uris[0]
elif choice == "2":
    redirect_uri = redirect_uris[1]
elif choice == "3":
    redirect_uri = redirect_uris[2]
elif choice == "4":
    redirect_uri = input("Entrez l'URL exacte: ").strip()
else:
    redirect_uri = redirect_uris[0]

print(f"\n✅ URI sélectionnée: {redirect_uri}")

# Test progressif
tests = [
    ("Sans aucun scope", ""),
    ("Seulement user.info.basic", "user.info.basic"),
    ("user.info.basic + video.publish", "user.info.basic,video.publish"),
]

for test_name, scope in tests:
    print(f"\n{'='*50}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*50}")
    
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": "test123"
    }
    
    if scope:
        params["scope"] = scope
        print(f"Scope demandé: {scope}")
    else:
        print("Aucun scope demandé")
    
    auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
    
    print("\n📎 URL générée:")
    print(auth_url)
    
    print("\n⏳ Ouverture dans 3 secondes...")
    time.sleep(3)
    
    webbrowser.open(auth_url)
    
    result = input("\n❓ Résultat? (success/error/skip): ").strip().lower()
    
    if result == "success":
        print("✅ Ce test fonctionne!")
        url = input("Collez l'URL de redirection ici: ").strip()
        if "code=" in url:
            print("✅ Code d'autorisation reçu!")
            break
    elif result == "error":
        print("❌ Ce test a échoué")
        error = input("Quelle erreur? (tapez Entrée si pas sûr): ").strip()
        if error:
            print(f"Erreur notée: {error}")
    else:
        print("⏭️  Test ignoré")

print("\n" + "="*60)
print("📊 RÉSUMÉ DES TESTS")
print("="*60)

print("""
🔍 SI TOUS LES TESTS ÉCHOUENT:

1. Vérifiez sur TikTok Developers:
   - Status de l'app (doit être "Live" ou vous devez être Test User)
   - Platform (doit inclure "Web")
   - Redirect URI exacte (avec ou sans slash final)

2. Essayez de créer une NOUVELLE app:
   - Plus simple de repartir de zéro
   - Seulement scope user.info.basic
   - Passez directement en Live

3. Vérifiez votre compte TikTok:
   - Compte business ou creator peut avoir des restrictions
   - Essayez avec un compte personnel normal
""")
