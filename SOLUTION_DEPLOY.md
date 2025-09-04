# 🚀 SOLUTION : Déploiement avec Railway (login --browserless)

## ❌ Le problème :
Railway ne peut pas ouvrir automatiquement le navigateur sur votre Mac.

## ✅ La solution : Utilisez `--browserless`

---

## 📝 MÉTHODE 1 : Déploiement manuel étape par étape

### Étape 1 : Connexion à Railway

```bash
railway login --browserless
```

**Vous verrez quelque chose comme :**
```
Press Enter to open the browser (^C to quit)
Or visit this URL: https://railway.app/cli-login?d=ABC123...
```

**👉 Copiez l'URL et ouvrez-la dans votre navigateur**

### Étape 2 : Créer le projet

```bash
cd /Users/iliaskalalou/g_tik/TikTok
railway init
```

Choisissez "Create new project"

### Étape 3 : Configurer les variables

```bash
railway variables set TIKTOK_CLIENT_KEY=sbaw9sck9i4u94jbyw
railway variables set TIKTOK_CLIENT_SECRET=Iwl5nMhrxo3S5xUfixLam6Ha74DR19am  
railway variables set FRONTEND_URL=https://iliaskalalou.github.io/Pianorama_publish
```

### Étape 4 : Déployer

```bash
railway up
```

### Étape 5 : Obtenir l'URL

```bash
railway domain
```

**Exemple de résultat :** `pianorama-production.up.railway.app`

---

## 📝 MÉTHODE 2 : Script automatisé (plus simple)

J'ai créé un nouveau script qui gère le `--browserless` :

```bash
cd /Users/iliaskalalou/g_tik/TikTok
./deploy_manual.sh
```

---

## 🎯 MÉTHODE 3 : Alternative avec Render.com (PLUS SIMPLE)

Si Railway pose trop de problèmes, utilisez **Render** (gratuit aussi) :

### 1. Créez un compte sur render.com

### 2. Créez un fichier `render.yaml` :

```bash
cat > render.yaml << EOF
services:
  - type: web
    name: pianorama-tiktok
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: TIKTOK_CLIENT_KEY
        value: sbaw9sck9i4u94jbyw
      - key: TIKTOK_CLIENT_SECRET
        value: Iwl5nMhrxo3S5xUfixLam6Ha74DR19am
      - key: FRONTEND_URL
        value: https://iliaskalalou.github.io/Pianorama_publish
EOF
```

### 3. Poussez sur GitHub :

```bash
git add render.yaml
git commit -m "Add Render deployment config"
git push
```

### 4. Sur render.com :
- "New" → "Web Service"
- Connectez votre repo GitHub
- Sélectionnez le repo `Pianorama_publish`
- Cliquez "Create Web Service"

**C'est tout ! Render déploiera automatiquement.**

---

## 🔧 MÉTHODE 4 : Utiliser Replit (Le plus simple pour tester)

1. Allez sur **replit.com**
2. Créez un nouveau Repl Python
3. Copiez le contenu de `app.py`
4. Dans Shell : `pip install flask flask-cors requests`
5. Cliquez "Run"

**Vous aurez une URL comme :** `https://pianorama-tiktok.username.repl.co`

---

## ⚡ SOLUTION RAPIDE MAINTENANT :

```bash
# Option 1 : Avec Railway (utilisez --browserless)
cd /Users/iliaskalalou/g_tik/TikTok
railway login --browserless
# Copiez l'URL dans votre navigateur
railway init
railway up
railway domain

# Option 2 : Avec le script automatisé
./deploy_manual.sh
```

---

## 📌 Après le déploiement :

### 1. Mettez à jour `index_production.html` (ligne 179) :
```javascript
const BACKEND_URL = 'https://votre-url.railway.app';
```

### 2. Dans TikTok Developers :
Ajoutez : `https://votre-url.railway.app/callback`

### 3. Déployez le frontend :
```bash
cp index_production.html index.html
git add -A && git commit -m "Update backend URL" && git push
```

---

## 💡 Si vous voulez tester en local d'abord :

```bash
# Installer Flask
pip3 install flask flask-cors requests

# Lancer en local
python3 app.py

# Ouvrir dans le navigateur
open http://localhost:5000
```

**Note :** Pour le test local, ajoutez `http://localhost:5000/callback` dans TikTok Developers.

---

## ✅ Le plus important :

**Railway fonctionne bien**, il faut juste utiliser `--browserless` !

Lancez :
```bash
railway login --browserless
```

Et suivez les instructions à l'écran. 🚀
