Script vidéo pour la review TikTok
==================================

Ce script te dit exactement quoi faire pendant l'enregistrement de la vidéo
de démo, dans quel ordre, et sur quels boutons cliquer. Il suit strictement
les corrections demandées par TikTok lors du précédent rejet.

------------------------------------------------------------
0. Pré-requis avant d'enregistrer
------------------------------------------------------------

1. Backend redéployé : sur Railway, vérifier que les 4 variables d'env
   sont bien renseignées :
     TIKTOK_CLIENT_KEY        = (ta clé sandbox, commence par "sb")
     TIKTOK_CLIENT_SECRET     = (à régénérer si compromise — voir plus bas)
     FRONTEND_URL             = https://iliaskalalou.github.io/TikTok
     BACKEND_URL              = https://<ton-app>.up.railway.app

2. Frontend redéployé : push de ton index.html mis à jour, puis vérifier
   que https://iliaskalalou.github.io/TikTok charge bien la nouvelle page
   "Content Studio Pro".

3. Dans index.html, à la ligne :
     const BACKEND_URL = 'https://your-app.up.railway.app';
   remplacer par ton vraie URL Railway. Sinon le bouton de connexion
   ouvrira une page d'erreur.

4. Sur https://developers.tiktok.com :
   - Sélectionner ton app
   - Onglet "Manage app"
   - Vérifier que tu es bien en mode SANDBOX (pas Production)
   - Section "Login Kit" : scopes activés = user.info.basic + video.publish
   - Section "Redirect URIs" : ajouter https://<ton-app>.up.railway.app/callback
   - Section "Sandbox" : ajouter ton compte TikTok comme Test User et
     accepter l'invitation depuis l'app TikTok mobile

5. Avoir une courte vidéo prête (10-30 secondes, MP4, < 50 Mo) sur le
   bureau. Nom suggéré : test_video.mp4

6. Outil d'enregistrement : QuickTime Player (Mac) ou OBS Studio.
   Résolution recommandée : 1920x1080.

------------------------------------------------------------
1. Plan de la vidéo (durée totale visée : 60 à 90 secondes)
------------------------------------------------------------

Scène 1 — Présentation du site web                  ~10 s
Scène 2 — Affichage du mode SANDBOX                 ~10 s
Scène 3 — Flow OAuth                                ~20 s
Scène 4 — Sélection du privacy + disclosure         ~15 s
Scène 5 — Publication                               ~15 s

------------------------------------------------------------
2. Scène 1 : présentation du site (10 s)
------------------------------------------------------------

ACTION : ouvre une fenêtre Chrome propre (mode invité, pas de bookmark, pas
d'autocomplete) à l'URL https://iliaskalalou.github.io/TikTok

CE QUI DOIT ETRE VISIBLE :
- En haut : barre de navigation "Content Studio Pro" avec les liens
  "Features", "How it works", "Privacy", "Terms" et "Get started"
- Le titre "Schedule and publish video content with confidence"
- Pas de référence à TikTok dans le branding (juste sur le bouton de
  connexion)

CE QUE TU FAIS :
1. Reste 2 secondes sur la page d'accueil
2. Survole avec le curseur les liens Privacy et Terms (pour bien les
   montrer)
3. Clique sur le lien "Privacy" dans la nav. Reste 2 s.
4. Reviens en arrière (bouton retour du navigateur)
5. Clique sur le lien "Terms". Reste 2 s.
6. Reviens en arrière

NARRATION VOIX OFF (optionnelle) :
  "Content Studio Pro is a content management platform for video creators.
   Privacy Policy and Terms of Service are clearly accessible."

------------------------------------------------------------
3. Scène 2 : montrer le SANDBOX (10 s — CRITIQUE)
------------------------------------------------------------

C'est cette scène qui a fait planter la dernière review. Il faut prouver
visuellement que tu es en mode Sandbox.

ACTION : ouvre un nouvel onglet Chrome sur https://developers.tiktok.com,
connecte-toi, puis clique sur ton app.

CE QUI DOIT ETRE VISIBLE :
- Le nom de ton app
- Un badge ou un encart qui dit "Sandbox" ou "Sandbox mode"
- La section Scopes avec user.info.basic et video.publish cochés
- L'environnement Sandbox URL ou la mention de Test Users

CE QUE TU FAIS :
1. Survole et zoome (Cmd+ ou Ctrl+) sur le badge SANDBOX pour qu'il soit
   bien lisible à la lecture vidéo
2. Survole les Scopes pour les rendre visibles
3. Reviens à 100% de zoom (Cmd+0)

NARRATION (optionnelle) :
  "I am demonstrating the integration in the official TikTok Sandbox
   environment, with the user.info.basic and video.publish scopes."

------------------------------------------------------------
4. Scène 3 : flow OAuth (20 s)
------------------------------------------------------------

Reviens sur l'onglet Content Studio Pro.

CE QUE TU FAIS :
1. Clique sur le bouton "Get started" dans la nav (en haut à droite). Cela
   te scrolle jusqu'à la section "Your dashboard".
2. Reste 1 s sur la card "Connect a creator account"
3. Clique sur le bouton noir "Connect with TikTok"

   -> Le navigateur quitte ton site et arrive sur TikTok

4. Sur la page d'auth de TikTok :
   - Si déjà connecté : tu vois directement la page d'autorisation
   - Sinon : connecte-toi avec ton compte Test User
5. Sur la page d'autorisation TikTok, attends 1 s. Les deux scopes sont
   listés (user.info.basic et video.publish). Clique sur le bouton
   "Authorize" (ou "Continue", selon la langue).

   -> Tu es redirigé vers ton backend Railway, puis vers le frontend.

6. De retour sur Content Studio Pro, le panneau dashboard montre :
   - Un bandeau vert "Account connected successfully"
   - Une carte qui affiche ton nickname TikTok et l'avatar
   - Le formulaire de publication apparaît automatiquement

NARRATION (optionnelle) :
  "I click Connect with TikTok, authenticate, grant access. The dashboard
   now shows my connected creator account."

POINT CRITIQUE TIKTOK : ton nickname (display_name) doit être visible
clairement sur la card. C'est une exigence UX explicite de TikTok.

------------------------------------------------------------
5. Scène 4 : choix du privacy + disclosure (15 s)
------------------------------------------------------------

CE QUE TU FAIS :
1. Dans la dropzone, clique pour ouvrir le file picker
2. Sélectionne ton test_video.mp4 sur le bureau
3. Le nom du fichier apparait en bleu sous la dropzone
4. Tape une caption courte dans la zone de texte, par exemple :
     "Test publication via Content Studio Pro"
5. Sur le menu déroulant Privacy :
   - Clique pour l'ouvrir et MONTRE LES OPTIONS pendant 1 s :
     - Public — everyone can see
     - Friends — followers you follow back
     - Followers only
     - Private — only me
   - **IMPORTANT** : sélectionne "Private — only me"
   - (En sandbox, seul SELF_ONLY fonctionne réellement)
6. Sur la checkbox "This content promotes a brand, product, or service" :
   - **Laisse-la décochée** (ne coche pas la case)
   - Le but est de montrer que la valeur par défaut est OFF, c'est une
     exigence TikTok

POINT CRITIQUE TIKTOK : la sélection du privacy doit être manuelle (pas
de valeur pré-cochée par défaut). Le help-text sous le menu le dit
explicitement et le code force la validation. Bien le souligner avec le
curseur.

NARRATION (optionnelle) :
  "I manually select a privacy level. There is no default value. The
   commercial content disclosure toggle is off by default, as required."

------------------------------------------------------------
6. Scène 5 : publication (15 s)
------------------------------------------------------------

CE QUE TU FAIS :
1. Clique sur le bouton "Publish content" en bas du formulaire
2. Le bouton change en "Publishing..." pendant ~1 s
3. Un bandeau vert apparait : "Content published successfully."

NARRATION (optionnelle) :
  "The video is published with the privacy level I selected. In sandbox
   mode, the content is only visible to me, as expected."

------------------------------------------------------------
7. À ne pas faire pendant la vidéo
------------------------------------------------------------

- Ne pas montrer ton CLIENT_SECRET ni ta clé Railway
- Ne pas montrer d'autres onglets que Content Studio Pro et TikTok Devs
- Ne pas avoir de notif macOS qui apparait : passer en mode "Ne pas déranger"
- Ne pas passer plus de 90 s — TikTok regarde rapidement
- Pas de musique de fond, narration courte ou aucune narration
- Pas de logo, pas de watermark dans la vidéo demo elle-même
- Pas de caption qui parle de TikTok dans ton contenu : c'est interdit
  par les guidelines

------------------------------------------------------------
8. Après l'enregistrement
------------------------------------------------------------

1. Re-regarder la vidéo pour vérifier :
   - Le badge SANDBOX est lisible
   - Le nickname apparait bien après OAuth
   - Le menu Privacy s'ouvre clairement avec aucune option pré-sélectionnée
   - La case "commercial" est bien décochée
   - Pas de fuite de secret

2. Compresser la vidéo si > 25 Mo (HandBrake → Web Optimized)

3. Aller sur https://developers.tiktok.com → ton app → "Submit for
   Review"
   - Description (à recopier-coller depuis README_APP_REVIEW.md) :
     "Content Studio Pro is a content management platform for creators
      to schedule and publish video content..."
   - Upload la vidéo
   - Soumettre

4. Attendre 5 à 10 jours ouvrés. Tu recevras la réponse à
   ilias.kalalou@gmail.com

------------------------------------------------------------
9. Risques de re-rejet à anticiper
------------------------------------------------------------

Même avec le script ci-dessus, TikTok peut encore rejeter si :

- Le BACKEND_URL en production n'est pas exactement celui dans la
  Redirect URI déclarée chez TikTok Developers
- Tu as oublié d'ajouter ton compte TikTok comme Test User
- Le scope video.upload est encore activé alors qu'il n'est pas
  démontré dans la vidéo (à désactiver si tu n'en as pas besoin)
- L'app affiche du contenu lié à TikTok dans son branding (logo,
  watermark, etc.)

En cas de nouveau rejet, le mail détaille toujours la raison. Tu pourras
me l'envoyer et on itère.
