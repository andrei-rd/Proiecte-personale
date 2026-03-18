# HyForce YT Downloader 🎥

O aplicație desktop ușoară, creată în Python, pentru descărcarea de videoclipuri și playlist-uri de pe YouTube. Interfața are un aspect clasic (retro 2015), este rapidă și rulează procesele de descărcare în background pentru a nu bloca aplicația.

# 🚀 Funcționalități
* **Descărcare Multiplă:** Introduci mai multe link-uri (unul sub altul) și se descarcă pe rând.
* **Suport Playlist:** Poți bifa descărcarea unui playlist întreg.
* **Selecție Format și Calitate:** * Video: MP4 (suportă calități de la 720p până la 4K / 2160p).
  * Audio: MP3 (128kbps sau 320kbps).
* **Multithreading:** Interfața nu îngheață în timpul descărcării.
* **Log-uri în timp real:** Urmărești exact ce se întâmplă direct din aplicație.

# 🛠️ Tehnologii folosite
* **Python 3.x**
* **Tkinter & ttk** (pentru Interfața Grafică)
* **yt-dlp** (motorul de descărcare principal)
* **FFmpeg** (necesar pentru conversia video/audio)

## 📦 Instalare și Rulare

1. Asigură-te că ai [Python](https://www.python.org/) și [FFmpeg](https://ffmpeg.org/download.html) instalate pe sistem.
2. Clonează acest repository:
   ```bash
   git clone [https://github.com/numele-tau/HyForce-YT-Downloader.git](https://github.com/numele-tau/HyForce-YT-Downloader.git)
   cd HyForce-YT-Downloader
3. Instalează dependențele:
pip install -r requirements.txt
4. Rulează aplicația: yt_downloader.py

Bash
python main.py
