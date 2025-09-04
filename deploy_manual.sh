#!/bin/bash

echo "🚀 DÉPLOIEMENT MANUEL RAILWAY POUR TIKTOK"
echo "=========================================="
echo ""

# Étape 1 : Login
echo "📝 ÉTAPE 1 : Connexion à Railway"
echo "================================"
echo ""
echo "Exécutez cette commande :"
echo "👉 railway login --browserless"
echo ""
echo "Vous verrez un lien - copiez-le et ouvrez-le dans votre navigateur"
echo "Connectez-vous et revenez au terminal"
echo ""
read -p "Appuyez sur Entrée quand vous êtes connecté..."

# Étape 2 : Init
echo ""
echo "📝 ÉTAPE 2 : Initialiser le projet"
echo "==================================="
echo ""
echo "Créer un nouveau projet Railway..."
railway init

# Étape 3 : Variables
echo ""
echo "📝 ÉTAPE 3 : Configuration des variables"
echo "========================================"
echo ""
echo "Ajout des variables d'environnement..."

railway variables set TIKTOK_CLIENT_KEY=sbaw9sck9i4u94jbyw
railway variables set TIKTOK_CLIENT_SECRET=Iwl5nMhrxo3S5xUfixLam6Ha74DR19am
railway variables set FRONTEND_URL=https://iliaskalalou.github.io/Pianorama_publish

echo "✅ Variables configurées"

# Étape 4 : Deploy
echo ""
echo "📝 ÉTAPE 4 : Déploiement"
echo "========================"
echo ""
echo "Déploiement en cours..."
railway up

# Étape 5 : Domain
echo ""
echo "📝 ÉTAPE 5 : Récupérer l'URL"
echo "============================"
echo ""
echo "Génération du domaine..."
railway domain

echo ""
echo "=========================================="
echo "✅ DÉPLOIEMENT TERMINÉ !"
echo "=========================================="
echo ""
echo "📌 PROCHAINES ÉTAPES :"
echo ""
echo "1. Copiez l'URL du domaine Railway (ex: your-app.up.railway.app)"
echo ""
echo "2. Mettez à jour index_production.html ligne 179 :"
echo "   const BACKEND_URL = 'https://your-app.up.railway.app';"
echo ""
echo "3. Dans TikTok Developers, ajoutez comme Redirect URI :"
echo "   https://your-app.up.railway.app/callback"
echo ""
echo "4. Copiez index_production.html vers index.html :"
echo "   cp index_production.html index.html"
echo ""
echo "5. Poussez sur GitHub :"
echo "   git add -A && git commit -m 'Update backend URL' && git push"
echo ""
echo "🎉 Votre app sera alors prête pour l'approbation TikTok !"
