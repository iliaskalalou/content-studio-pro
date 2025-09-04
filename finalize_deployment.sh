#!/bin/bash

echo "🎯 FINALISATION DU DÉPLOIEMENT"
echo "=============================="
echo ""

# Récupérer l'URL
echo "📝 Récupération de l'URL Railway..."
RAILWAY_URL=$(railway domain)

if [ -z "$RAILWAY_URL" ]; then
    echo "⚠️  Aucun domaine trouvé. Génération..."
    railway domain generate
    RAILWAY_URL=$(railway domain)
fi

echo "✅ URL du backend : $RAILWAY_URL"
echo ""

# Mettre à jour index_production.html
echo "📝 Mise à jour de index_production.html..."
sed -i '' "s|const BACKEND_URL = '.*';|const BACKEND_URL = 'https://$RAILWAY_URL';|" index_production.html

# Copier vers index.html
echo "📝 Copie vers index.html..."
cp index_production.html index.html

echo ""
echo "✅ Frontend mis à jour avec l'URL : https://$RAILWAY_URL"
echo ""

# Commit et push
echo "📝 Push sur GitHub..."
git add -A
git commit -m "Update frontend with Railway backend URL: $RAILWAY_URL"
git push

echo ""
echo "=============================="
echo "✅ DÉPLOIEMENT TERMINÉ !"
echo "=============================="
echo ""
echo "📌 DERNIÈRE ÉTAPE MANUELLE :"
echo ""
echo "1. Allez sur TikTok Developers"
echo "2. Dans 'Redirect URIs', ajoutez :"
echo "   https://$RAILWAY_URL/callback"
echo ""
echo "3. Testez votre app :"
echo "   https://iliaskalalou.github.io/Pianorama_publish/"
echo ""
echo "🎉 Votre app est prête pour l'approbation TikTok !"
