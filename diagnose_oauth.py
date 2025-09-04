#!/usr/bin/env python3
"""
Script de test minimal pour diagnostiquer le problème OAuth TikTok
"""

import webbrowser
import urllib.parse

print("\n🔍 DIAGNOSTIC OAUTH TIKTOK")
print("=" * 50)

# Configuration
CLIENT_KEY = "sbaw9sck9i4u94jbyw"
REDIRECT_URI = "https://iliaskalalou.github.io/Pianorama_publish/TikTok/"

print("\n📝 Configuration actuelle :")
print(f"   Client Key: {CLIENT_KEY}")
print(f"   Redirect URI: {REDIRECT_URI}")

print("\n⚠️  VÉRIFICATIONS IMPORTANTES :")
print("\n1️⃣  Votre app est-elle en mode 'Live' ?")
print("   → Sur TikTok Developers, vérifiez le statut")
print("   → Si elle est en 'Development', passez-la en 'Live'")

print("\n2️⃣  Utilisez-vous un compte test ?")
print("   → Pour le sandbox, il faut un compte TEST TikTok")
print("   → Pas votre compte personnel")

print("\n3️⃣  Test avec UN SEUL scope :")
print("   → On va tester seulement user.info.basic")

input("\nAppuyez sur Entrée pour continuer...")

# Test 1: Seulement user.info.basic
print("\n🧪 TEST 1: Seulement user.info.basic")
params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": "user.info.basic",  # UN SEUL SCOPE
    "redirect_uri": REDIRECT_URI,
    "state": "test123"
}

auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
print("\nURL générée:")
print(auth_url)
print("\n✅ Ouvrir dans le navigateur...")
webbrowser.open(auth_url)

response = input("\nQu'est-ce qui s'est passé? (success/error): ").strip()

if response == "error":
    print("\n❌ Si erreur avec user.info.basic seul, vérifiez :")
    print("   1. Le mode de l'app (Live vs Development)")
    print("   2. La redirect URI exacte dans TikTok Developers")
    print("   3. Les Test Users si en mode Development")
    
    print("\n🧪 TEST 2: Sans aucun scope")
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "",  # AUCUN SCOPE
        "redirect_uri": REDIRECT_URI,
        "state": "test123"
    }
    
    auth_url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
    print("\nEssayons sans scope:")
    print(auth_url)
    print("\n✅ Ouvrir dans le navigateur...")
    webbrowser.open(auth_url)

print("\n📋 SOLUTIONS POSSIBLES :")
print("\n1. Passer l'app en mode 'Live' sur TikTok Developers")
print("2. Ajouter votre compte comme Test User si en Development")
print("3. Vérifier que la Redirect URI est EXACTEMENT:")
print(f"   {REDIRECT_URI}")
print("4. Retirer temporairement video.publish des scopes")
print("5. Créer un nouveau compte TikTok pour les tests")
