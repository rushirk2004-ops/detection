# Mobile Application Support Guide 📱🌿
**Guava Leaf & Fruit Disease Detection System (PWA & Mobile Ready)**

This system is fully optimized for smartphones and tablets (Android and iOS). Farmers can run the app directly in the field, snap live leaf photos using their phone's camera, and install it on their home screen like a native mobile app!

---

## 📲 Option 1: Instant Mobile Access (Over Local Wi-Fi / Hotspot)

1. Make sure your smartphone and your PC/Laptop are connected to the **same Wi-Fi network** (or connect your PC to your mobile hotspot).
2. On your PC terminal, note your network IP when Streamlit starts:
   ```text
   Network URL: http://192.168.x.x:8501
   ```
3. Open **Google Chrome** (Android) or **Safari** (iPhone) on your mobile phone and type:
   ```text
   http://<YOUR-PC-IP>:8501
   ```
   *(For example: `http://192.168.1.102:8501`)*

---

## 📲 Option 2: Install as a Mobile App (Progressive Web App - PWA)

You can turn this web application into a standalone Android / iOS mobile app with an icon on your home screen without downloading from the Play Store:

### On Android (Google Chrome):
1. Open the app URL on your phone's Chrome browser.
2. Tap the **3 dots menu (⋮)** in the top right corner.
3. Tap **"Install App"** (or **"Add to Home Screen"**).
4. An icon named **"Guava Agri-AI"** will appear on your phone's home screen.
5. Tap the icon anytime — it opens in full-screen standalone mode with no browser URL bar!

### On iPhone (Apple Safari):
1. Open the app URL in Safari.
2. Tap the **Share icon (square with upward arrow)** at the bottom.
3. Scroll down and tap **"Add to Home Screen"**.
4. Tap **Add**. The app will now launch full-screen directly from your home screen.

---

## 📸 In-Field Mobile Camera Scanning

When inspecting guava trees in the orchard:
1. Tap **"📸 मोबाईल कॅमेराने फोटो काढा (Live Camera)"**.
2. Tap the capture button.
3. The phone's camera captures the leaf image in high-resolution and immediately passes it to the AI inference engine.
4. The diagnosis and remedies appear in Marathi or English within 1 to 2 seconds.

---

## 📦 Option 3: Exporting to Native Android APK (Cordova / Capacitor / Bubblewrap)

To build a standalone installable `.apk` file:
1. **Google Bubblewrap (TWA - Trusted Web Activity)**:
   ```bash
   npm install -g @bubblewrap/cli
   bubblewrap init --manifest="http://<YOUR-SERVER>:8501/static/manifest.json"
   bubblewrap build
   ```
   This outputs an optimized `app-release.apk` signed for Android devices.

2. **Capacitor / Cordova**:
   Wrap `http://<SERVER-IP>:8501` inside an Android Studio WebView activity with camera permissions (`android.permission.CAMERA`).
