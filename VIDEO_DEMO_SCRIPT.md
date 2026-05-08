Demo video script for the TikTok app review
============================================

This is the script to follow while recording the demo video that ships
with the TikTok review submission. It explicitly demonstrates BOTH posting
modes (Direct Post and Upload-to-draft), which was the gap that caused the
previous rejection.

------------------------------------------------------------
0. Pre-flight checks (must be done before pressing record)
------------------------------------------------------------

1. **Render service**: open https://content-studio-pro.onrender.com/health
   in a browser. If it doesn't return `{"status":"healthy"}` instantly,
   wait 30-60 s for Render to wake the service from sleep, then retry.

2. **Frontend**: open https://iliaskalalou.github.io/content-studio-pro/
   in a private/incognito window. Verify the redesigned landing page
   loads (header reading "Content Studio Pro").

3. **TikTok Developer Portal**:
   - App is in **Sandbox** mode (the badge "Sandbox" is visible in the
     top of the app page).
   - **Platforms** section: only **Web** is checked. Desktop is
     unchecked.
   - **Web URL** points to https://iliaskalalou.github.io/content-studio-pro/
   - **Redirect URI**: https://content-studio-pro.onrender.com/callback
   - **Scopes**: user.info.basic, video.publish, video.upload (all 3
     are listed — we cannot uncheck video.upload because it is bundled
     with the Content Posting API product).
   - **Sandbox settings → Target users**: the TikTok account you will
     authenticate with is listed. The invite was accepted from the
     TikTok mobile app.

4. **Render env vars** (Settings → Environment on Render):
   ```
   TIKTOK_CLIENT_KEY     = sbaw9sck9i4u94jbyw
   TIKTOK_CLIENT_SECRET  = Iwl5nMhrxo3S5xUfixLam6Ha74DR19am
   FRONTEND_URL          = https://iliaskalalou.github.io/content-studio-pro
   BACKEND_URL           = https://content-studio-pro.onrender.com
   ```

5. **Record set-up**:
   - QuickTime Player or OBS, screen recording at 1080p.
   - Mac in "Do Not Disturb" mode.
   - Two short test videos ready on the desktop:
       test_video_publish.mp4   (10-15 s, will be used in scene 5)
       test_video_draft.mp4     (10-15 s, will be used in scene 6)
   - One Chrome window with two tabs: one on Content Studio Pro,
     one on the TikTok Developer Portal page of the app.

------------------------------------------------------------
1. Plan of the video (target: 90 to 120 seconds)
------------------------------------------------------------

| Scene | Content                                | Duration |
|-------|----------------------------------------|----------|
| 1     | Site walkthrough, legal links visible  | ~10 s    |
| 2     | TikTok Sandbox visible (CRITICAL)      | ~10 s    |
| 3     | OAuth flow with the 3 scopes shown     | ~25 s    |
| 4     | Pick file + manual privacy + disclosure| ~15 s    |
| 5     | Direct Post (video.publish)            | ~15 s    |
| 6     | Upload to draft (video.upload)         | ~15 s    |

------------------------------------------------------------
2. Scene 1 — Landing page (10 s)
------------------------------------------------------------

ACTION:
- Switch to the Content Studio Pro tab.
- Stay 2 s on the hero ("Schedule and publish video content with confidence").
- Hover over the navigation, click "Privacy" — stay 2 s on the page.
- Browser back.
- Click "Terms" — stay 2 s on the page.
- Browser back.

VOICE-OVER (optional):
"Content Studio Pro is a content management platform for video creators.
The Privacy Policy and Terms of Service are accessible from every page."

------------------------------------------------------------
3. Scene 2 — Sandbox proof (10 s) — DO NOT SKIP
------------------------------------------------------------

This is the scene that makes or breaks the review.

ACTION:
- Switch to the TikTok Developer Portal tab.
- Make sure the page shows the Sandbox view of the app.
- Zoom in (Cmd +) on the "Sandbox" badge or label until it is clearly
  legible at video playback resolution.
- Pan the cursor over the Scopes block so the three scopes are also
  visible (user.info.basic, video.publish, video.upload).
- Reset zoom (Cmd 0).

VOICE-OVER (optional):
"The integration is being demonstrated in the official TikTok Sandbox
environment. The app requests three scopes: user.info.basic, video.publish
and video.upload."

------------------------------------------------------------
4. Scene 3 — OAuth flow (25 s)
------------------------------------------------------------

ACTION:
- Switch back to the Content Studio Pro tab.
- Click the "Get started" button in the top navigation. The page scrolls
  down to the dashboard panel.
- Click the black button "Connect with TikTok".
- The browser leaves the site and lands on TikTok's authorization page.
- If asked, sign in with the test-user TikTok account.
- On the consent screen, slow down: the three requested scopes are
  visible (user.info.basic, video.publish, video.upload). Stay 2 s here.
- Click "Authorize" / "Continue".
- After the redirect, the dashboard now shows:
    - A green "Account connected successfully" banner.
    - The connected account card with the creator's nickname.
    - The publish form expanded.

VOICE-OVER (optional):
"I authenticate via OAuth and grant the three requested scopes. The
dashboard now displays the connected creator's nickname."

CRITICAL: the creator's nickname must appear on screen — it is a
mandatory UX requirement from TikTok.

------------------------------------------------------------
5. Scene 4 — File + manual privacy + disclosure (15 s)
------------------------------------------------------------

ACTION:
- Click the dropzone, select test_video_publish.mp4 from the desktop.
- The file name appears in blue under the dropzone.
- Type a short caption: "Direct Post demo — Sandbox".
- Click the Privacy dropdown to open it. Hold for 1.5 s so all four
  options are visible:
    - Public — everyone can see
    - Friends — followers you follow back
    - Followers only
    - Private — only me
- Select "Private — only me" (only SELF_ONLY works in Sandbox).
- Leave the "This content promotes a brand, product or service"
  checkbox unchecked.

VOICE-OVER (optional):
"I manually pick the privacy level — there is no default. The commercial
disclosure toggle is off by default, as required by TikTok's guidelines."

------------------------------------------------------------
6. Scene 5 — Direct Post via video.publish (15 s)
------------------------------------------------------------

ACTION:
- Click the dark "Publish content" button.
- The button changes to "Publishing..." for ~1 s.
- A green status banner appears:
    "Content published successfully" (or similar).

VOICE-OVER (optional):
"The video is published directly to the connected creator's profile
using the video.publish scope. Because we selected Private, the video
is only visible to the creator on TikTok."

------------------------------------------------------------
7. Scene 6 — Upload as draft via video.upload (15 s)
------------------------------------------------------------

ACTION:
- Click the dropzone again, this time select test_video_draft.mp4.
- Update the caption to: "Draft upload demo — Sandbox".
- The privacy and disclosure fields keep the previous values, that's
  fine.
- Click the lighter "Save as draft" button (next to "Publish content").
- A status banner appears:
    "Video uploaded as a draft. Review and post it from your TikTok inbox."

VOICE-OVER (optional):
"For the second mode, I save the video as a draft using the video.upload
scope. The video lands in the creator's TikTok inbox where they can
finalise the post directly inside the TikTok app."

------------------------------------------------------------
8. Things NOT to do in the video
------------------------------------------------------------

- Do not show the CLIENT_SECRET, the Render dashboard secrets, or any
  TikTok dashboard settings dialog where credentials are visible.
- No music behind the narration; either keep it silent or short voice-over.
- No system notifications popping up — Do Not Disturb is a must.
- No watermark, logo, or text overlay added to the test videos —
  TikTok forbids it explicitly.
- Total duration: stay under 120 seconds. Reviewers do not watch long
  videos.

------------------------------------------------------------
9. After recording
------------------------------------------------------------

1. Watch the video back, verifying:
   - The Sandbox badge is legible.
   - The creator nickname appears after OAuth.
   - The privacy dropdown shows all four options before any is picked.
   - Both buttons (Publish content, Save as draft) are clicked,
     and both produce a success banner.
   - No secrets visible anywhere.

2. Compress to under 25 MB if needed (HandBrake → Web Optimized).

3. Submit on https://developers.tiktok.com → Pianorama_publish app
   → "Submit for review".
   - Description (copy-paste from README_APP_REVIEW.md).
   - Upload the demo video.
   - Submit.

4. Decision arrives 5-10 business days later, by email at
   ilias.kalalou@gmail.com.

------------------------------------------------------------
10. If TikTok rejects again, common causes
------------------------------------------------------------

- The Render service was sleeping when the reviewer tried it. Solution:
  upgrade to Render Starter ($7/month) or pre-warm the service before
  the review window.
- Wrong Redirect URI declared (must match exactly what the backend
  redirects from).
- Test user not invited or invitation not accepted.
- Branding / watermark in the demo video.

If you get a new rejection email, paste it back to me and we iterate
from there.
