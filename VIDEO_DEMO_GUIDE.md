# 📹 GUIDE VIDÉO DE DÉMONSTRATION TIKTOK

## ⚠️ IMPORTANT : Corrections requises pour l'approbation

### 🎯 Résumé du rejet
TikTok a rejeté votre app car :
1. ❌ **Pas d'utilisation du Sandbox** 
2. ❌ **Scopes non démontrés clairement**
3. ❌ **Confusion entre video.publish et video.upload**

---

## ✅ NOUVEAU SCRIPT DE DÉMONSTRATION

### 1️⃣ Préparer le Sandbox

**Avant de commencer :**
- Utilisez le nouveau script `sandbox_demo.py`
- Créez un compte TEST TikTok (pas votre compte principal)
- Préparez 2 vidéos courtes (10-15 secondes) différentes

### 2️⃣ Structure de la vidéo (3-4 minutes)

#### **00:00 - 00:15 | Introduction**
```
"Bonjour, voici la démonstration de Pianorama Publish 
utilisant l'environnement SANDBOX de TikTok avec les 3 scopes requis"
```
- Montrez votre site web
- Montrez clairement les liens Privacy Policy et Terms

#### **00:15 - 00:45 | Scope 1: user.info.basic**
```
"Démonstration du scope USER.INFO.BASIC"
```
1. Lancez: `python3 sandbox_demo.py video1.mp4`
2. Montrez l'écran de connexion OAuth TikTok
3. Acceptez les permissions (montrez clairement les 3 scopes)
4. **MONTREZ le résultat dans le terminal :**
   ```
   ✅ Informations utilisateur récupérées:
   - Display Name: TestUser
   - Avatar: https://...
   - Open ID: xxx
   ```

#### **00:45 - 01:45 | Scope 2: video.publish**
```
"Démonstration du scope VIDEO.PUBLISH - Publication DIRECTE"
```
1. Le script continue automatiquement
2. **MONTREZ clairement dans le terminal :**
   ```
   📹 DÉMONSTRATION SCOPE: video.publish
   → Publication DIRECTE sur le profil TikTok
   ✅ Publication directe initialisée
   - Mode: DIRECT PUBLISH
   ```
3. Ouvrez TikTok dans un autre onglet
4. Montrez la vidéo publiée en mode privé

#### **01:45 - 02:45 | Scope 3: video.upload**
```
"Démonstration du scope VIDEO.UPLOAD - Envoi en BROUILLON"
```
1. Le script continue avec la 2ème vidéo
2. **MONTREZ clairement dans le terminal :**
   ```
   📝 DÉMONSTRATION SCOPE: video.upload
   → Envoi en BROUILLON pour édition dans TikTok
   ✅ Upload en brouillon initialisé
   - Mode: DRAFT/INBOX
   ```
3. Ouvrez TikTok Creator Center
4. Montrez la vidéo dans les brouillons

#### **02:45 - 03:00 | Conclusion**
```
"Démonstration terminée avec succès des 3 scopes en environnement SANDBOX"
```
- Montrez le résumé final dans le terminal
- Revenez sur votre site web

---

## 🎬 Script d'enregistrement étape par étape

### Terminal 1 (principal)
```bash
cd /Users/iliaskalalou/g_tik/TikTok

# Modifier d'abord le script avec vos credentials
nano sandbox_demo.py
# Remplacez YOUR_CLIENT_KEY et YOUR_CLIENT_SECRET

# Lancer la démo
python3 sandbox_demo.py test_video.mp4
```

### Terminal 2 (monitoring)
```bash
# Gardez un œil sur les logs
tail -f /tmp/tiktok_demo.log
```

---

## ⚠️ Points critiques à montrer

### ✅ OBLIGATOIRE dans la vidéo :

1. **URL Sandbox visible** 
   - L'URL doit contenir "sandbox" : `https://open-sandbox.tiktokapis.com`

2. **Les 3 scopes distincts**
   - Montrez CLAIREMENT la différence entre publish et upload
   - Publish = Publication directe
   - Upload = Brouillon/Draft

3. **Résultats concrets**
   - User info : Affichez le nom et avatar
   - Publish : Montrez la vidéo publiée
   - Upload : Montrez le brouillon

4. **Environnement Sandbox**
   - Dites "SANDBOX" plusieurs fois
   - Montrez "MODE SANDBOX ACTIVÉ" dans le terminal

---

## 📝 Checklist avant soumission

- [ ] Script `sandbox_demo.py` configuré avec vos clés
- [ ] Compte TEST TikTok créé
- [ ] 2 vidéos de test préparées (format MP4, <50MB)
- [ ] Terminal en plein écran pour lisibilité
- [ ] Microphone pour narration claire
- [ ] Enregistrement en 1080p minimum

---

## 🚀 Commandes rapides

### Test du script
```bash
# Test rapide
python3 sandbox_demo.py test.mp4
```

### Enregistrement avec QuickTime
```bash
# Ouvrir QuickTime
open -a QuickTime\ Player

# Menu : Fichier > Nouvel enregistrement de l'écran
# Sélectionner la zone
# Inclure l'audio du microphone
```

### Conversion vidéo si nécessaire
```bash
# Si votre vidéo est trop lourde
ffmpeg -i demo.mov -vcodec h264 -acodec aac demo.mp4
```

---

## 💡 Conseils pour l'approbation

1. **Soyez TRÈS clair** sur la différence entre les scopes
2. **Narrez tout** ce que vous faites
3. **Montrez les URLs** (sandbox, privacy, terms)
4. **Gardez la vidéo courte** (3-4 minutes max)
5. **Qualité HD** pour que le texte soit lisible

---

## 🔄 Si rejeté à nouveau

### Option A : Retirer video.upload
Si vous n'avez pas vraiment besoin des brouillons :
- Retirez le scope `video.upload` de votre app
- Gardez seulement `user.info.basic` et `video.publish`
- Refaites une vidéo plus simple

### Option B : Améliorer la démo
- Demandez des précisions à TikTok Support
- Montrez un cas d'usage réel
- Expliquez pourquoi vous avez besoin de chaque scope

---

## 📧 Message pour TikTok Support

Si besoin, voici un template :
```
Hello TikTok Review Team,

I've updated my demo video following your feedback:
1. ✅ Using SANDBOX environment throughout
2. ✅ Demonstrating all 3 scopes clearly:
   - user.info.basic: Showing user profile retrieval
   - video.publish: Direct publication to profile
   - video.upload: Draft/inbox upload for later editing
3. ✅ Each scope is demonstrated with different functionality

The video shows the complete flow in sandbox mode.
Please let me know if any additional clarification is needed.

Best regards,
[Your name]
```

---

## ✨ Bonne chance pour votre soumission !
