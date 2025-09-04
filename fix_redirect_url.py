#!/usr/bin/env python3
"""
Script pour tester et configurer la bonne URL de redirection TikTok
"""

import sys
import webbrowser

print("\n🔧 CONFIGURATION REDIRECT_URI POUR TIKTOK")
print("=" * 50)

print("\n📝 URLs possibles :")
print("1. https://iliaskalalou.github.io/TikTok")
print("2. https://iliaskalalou.github.io/TikTok/")
print("3. https://iliaskalalou.github.io/Pianorama_publish")
print("4. https://iliaskalalou.github.io/Pianorama_publish/")

print("\n❓ Quelle URL est configurée dans TikTok Developers ?")
print("   (Vérifiez sur https://developers.tiktok.com/)")

choice = input("\nEntrez le numéro (1-4) ou tapez l'URL exacte : ").strip()

urls = {
    "1": "https://iliaskalalou.github.io/TikTok",
    "2": "https://iliaskalalou.github.io/TikTok/",
    "3": "https://iliaskalalou.github.io/Pianorama_publish",
    "4": "https://iliaskalalou.github.io/Pianorama_publish/"
}

if choice in urls:
    redirect_uri = urls[choice]
elif choice.startswith("http"):
    redirect_uri = choice
else:
    print("❌ Choix invalide")
    sys.exit(1)

print(f"\n✅ URL sélectionnée : {redirect_uri}")

# Mettre à jour simple_demo.py
print("\n📝 Mise à jour de simple_demo.py...")
with open('simple_demo.py', 'r') as f:
    content = f.read()

# Remplacer l'URL
import re
content = re.sub(
    r'self\.redirect_uri = "https://[^"]*"', 
    f'self.redirect_uri = "{redirect_uri}"',
    content
)

with open('simple_demo.py', 'w') as f:
    f.write(content)

print("✅ simple_demo.py mis à jour")

# Mettre à jour sandbox_demo.py
print("\n📝 Mise à jour de sandbox_demo.py...")
with open('sandbox_demo.py', 'r') as f:
    content = f.read()

content = re.sub(
    r'self\.redirect_uri = "https://[^"]*"', 
    f'self.redirect_uri = "{redirect_uri}"',
    content
)

with open('sandbox_demo.py', 'w') as f:
    f.write(content)

print("✅ sandbox_demo.py mis à jour")

print("\n" + "=" * 50)
print("🎉 Configuration terminée !")
print("\n📌 IMPORTANT : Sur TikTok Developers, assurez-vous que cette URL")
print(f"   est bien dans 'Redirect URIs' : {redirect_uri}")
print("\n🚀 Lancez maintenant : ./RUN_DEMO_NOW.sh")
print("=" * 50)
