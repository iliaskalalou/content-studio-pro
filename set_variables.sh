#!/bin/bash

echo "🔧 Configuration des variables Railway"
echo "====================================="
echo ""

# Variables à configurer
export BACKEND_URL="https://purple-imaginative-mercy-production.up.railway.app"

echo "📝 Ajout des variables d'environnement..."
echo ""

# Nouvelle syntaxe Railway
railway variables --set "TIKTOK_CLIENT_KEY=sbaw9sck9i4u94jbyw"
railway variables --set "TIKTOK_CLIENT_SECRET=Iwl5nMhrxo3S5xUfixLam6Ha74DR19am"
railway variables --set "FRONTEND_URL=https://iliaskalalou.github.io/Pianorama_publish"
railway variables --set "BACKEND_URL=$BACKEND_URL"

echo ""
echo "✅ Variables configurées !"
echo ""
echo "📝 Redéploiement..."
railway up

echo ""
echo "====================================="
echo "✅ Backend configuré avec succès !"
echo "====================================="
