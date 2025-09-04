#!/bin/bash

echo "🚀 DÉPLOIEMENT RAPIDE POUR APPROBATION TIKTOK"
echo "============================================"
echo ""

# Vérifier si Railway est installé
if ! command -v railway &> /dev/null; then
    echo "📦 Installation de Railway CLI..."
    brew install railway
fi

echo "📝 Fichiers prêts pour le déploiement :"
echo "   ✅ app.py (backend Flask)"
echo "   ✅ requirements.txt"
echo "   ✅ Procfile"
echo ""

echo "🔐 Connexion à Railway..."
railway login

echo ""
echo "🚂 Initialisation du projet Railway..."
railway init

echo ""
echo "⚙️  Configuration des variables d'environnement..."
railway variables set TIKTOK_CLIENT_KEY=sbaw9sck9i4u94jbyw
railway variables set TIKTOK_CLIENT_SECRET=Iwl5nMhrxo3S5xUfixLam6Ha74DR19am
railway variables set FRONTEND_URL=https://iliaskalalou.github.io/Pianorama_publish

echo ""
echo "🚀 Déploiement en cours..."
railway up

echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📌 PROCHAINES ÉTAPES :"
echo "1. Récupérez l'URL de votre backend : railway domain"
echo "2. Ajoutez cette URL dans TikTok Developers comme Redirect URI"
echo "3. Mettez à jour index_production.html avec l'URL du backend"
echo "4. Copiez index_production.html vers index.html"
echo "5. Poussez sur GitHub"
echo ""
echo "🎥 Enregistrez ensuite votre vidéo de démonstration !"
