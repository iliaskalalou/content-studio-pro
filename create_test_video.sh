#!/bin/bash

# Script pour créer une vidéo de test simple avec ffmpeg
# Crée une vidéo de 10 secondes avec un fond coloré et du texte

echo "🎬 Création d'une vidéo de test pour TikTok..."

# Vérifier si ffmpeg est installé
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg n'est pas installé."
    echo "Installez-le avec: brew install ffmpeg"
    exit 1
fi

# Créer une vidéo de test de 10 secondes
ffmpeg -f lavfi -i color=c=blue:s=720x1280:d=10 \
    -vf "drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Test Video TikTok Sandbox':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2" \
    -c:v libx264 -pix_fmt yuv420p test_video.mp4 -y

if [ $? -eq 0 ]; then
    echo "✅ Vidéo créée: test_video.mp4"
    echo "   Taille: $(du -h test_video.mp4 | cut -f1)"
    echo ""
    echo "📝 Prochaine étape:"
    echo "   python3 simple_demo.py test_video.mp4"
else
    echo "❌ Erreur lors de la création de la vidéo"
fi
