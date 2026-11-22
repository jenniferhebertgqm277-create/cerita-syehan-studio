# 🎬 Cerita Syehan — 3D Animation Studio (Code-to-Film)

Studio animasi 3D berbasis coding murni yang dirancang untuk serial TikTok **"Cerita Syehan"**, terinspirasi dari filosofi arsitektur *Lemo-Opuscar*. Semua adegan, karakter, lighting, kamera, dan audio disintesis secara deterministik melalui kode dan dirender otomatis via **GitHub Actions**.

---

## 🌟 Ciri Khas & Gaya Studio (Era Modern)
Berbeda dari gaya cyberpunk / fiksi futuristik, serial **Cerita Syehan** mengangkat realita kehidupan modern zaman sekarang:
* **Setting**: Kamar/studio modern estetik (meja kerja kayu minimalis, monitor ultrawide, tanaman hias, lampu kerja hangat, smartphone modern).
* **Karakter (Syehan)**: Pemuda modern santai dengan hoodie sage-slate kekinian, celana santai, sneakers modern, headphone nirkabel di leher, serta ekspresi wajah yang sangat hidup dan relatable.
* **Audio & Meme**: Menggabungkan sulih suara AI natural (Edge-TTS Ardi), musik latar lo-fi santai, dan sound effect meme viral TikTok (*Vine Boom, Windows Error, Bruh, Ding Idea, Huh Cat, Airhorn, Metal Pipe*).

---

## 📁 Struktur Repositori
* `index.html`: Adegan 3D WebGL (Three.js r128) + subtitle kinetik TikTok terintegrasi.
* `render.mjs`: Runner Playwright Chromium headless untuk rendering frame deterministik.
* `mix.py`: Audio mixer presisi tinggi menggabungkan vokal, SFX meme, dan musik latar menggunakan FFmpeg.
* `assets/`: Aset suara vokal (`voice.mp3`), musik latar (`bgm.wav`), dan pustaka sound effect meme (`assets/sfx/`).
* `.github/workflows/render.yml`: Pipeline rendering otomatis di cloud GitHub Actions.

---

## 🚀 Cara Memicu Render di GitHub Actions
Jalankan perintah berikut melalui GitHub CLI (`gh`):
```bash
# Render Full Video 1080x1920 (TikTok 9:16)
gh workflow run render.yml -f resolution="1080x1920" -f fps="30" -f tag="eps0-v1.0"
```
Hasil render video `.mp4` kualitas tinggi akan otomatis terbit di tab **Releases**.
