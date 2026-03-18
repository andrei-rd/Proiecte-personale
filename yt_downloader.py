import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError
except ImportError:
    raise SystemExit("pip install yt-dlp")


class YTDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HyForce YT Downloader")
        self.root.geometry("800x550")
        self.stop_flag = False
        self.worker = None
        self.root.configure(bg="#f0f0f0")
        self._build_style()
        self._build_ui()

    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("winnative")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f0f0f0")
        style.configure(
            "TLabel", background="#f0f0f0", foreground="black", font=("Tahoma", 8)
        )
        style.configure("Header.TLabel", font=("Tahoma", 14, "bold"))
        style.configure("TButton", font=("Tahoma", 8), padding=3)
        style.configure(
            "TCheckbutton", background="#f0f0f0", foreground="black", font=("Tahoma", 8)
        )

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="HyForce YT Downloader", style="Header.TLabel").pack(
            anchor="w", pady=(0, 10)
        )
        ttk.Label(main, text="Link-uri YouTube:").pack(anchor="w")

        self.txt_urls = tk.Text(
            main,
            height=5,
            bg="white",
            fg="black",
            relief=tk.SUNKEN,
            bd=2,
            font=("Consolas", 9),
        )
        self.txt_urls.pack(fill=tk.X, pady=(3, 10))

        ttk.Label(main, text="Folder:").pack(anchor="w")
        f_frame = ttk.Frame(main)
        f_frame.pack(fill=tk.X, pady=(3, 10))

        self.out_var = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "Downloads")
        )
        ttk.Entry(f_frame, textvariable=self.out_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)
        )
        ttk.Button(f_frame, text="Alege...", command=self.choose_folder, width=10).pack(
            side=tk.LEFT, padx=(0, 3)
        )
        ttk.Button(f_frame, text="Deschide", command=self.open_folder, width=10).pack(
            side=tk.LEFT
        )

        opt_frame = ttk.LabelFrame(main, text=" Setari ", padding=10)
        opt_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(opt_frame, text="Format:").grid(row=0, column=0, padx=(0, 5))
        self.format_var = tk.StringVar(value="video_mp4")
        ttk.Combobox(
            opt_frame,
            textvariable=self.format_var,
            values=["video_mp4", "audio_mp3"],
            state="readonly",
            width=12,
        ).grid(row=0, column=1, padx=(0, 15))

        ttk.Label(opt_frame, text="Calitate:").grid(row=0, column=2, padx=(0, 5))
        self.quality_var = tk.StringVar(value="best")
        ttk.Combobox(
            opt_frame,
            textvariable=self.quality_var,
            values=[
                "best",
                "2160p (4K)",
                "1440p (2K)",
                "1080p",
                "720p",
                "audio_320k",
                "audio_128k",
            ],
            state="readonly",
            width=15,
        ).grid(row=0, column=3, padx=(0, 15))

        self.chk_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            opt_frame, text="Descarca playlist", variable=self.chk_var
        ).grid(row=0, column=4)

        ctrl_frame = ttk.Frame(main)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            ctrl_frame, text="Start Download", command=self.start_download, width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(ctrl_frame, text="Stop", command=self.stop_download, width=10).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(
            ctrl_frame, text="Curata Jurnal", command=self.clear_log, width=12
        ).pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(main, orient=tk.HORIZONTAL, mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(main, text="Jurnal:").pack(anchor="w")
        self.txt_log = tk.Text(
            main,
            height=10,
            bg="white",
            fg="black",
            relief=tk.SUNKEN,
            bd=2,
            font=("Consolas", 8),
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

    def choose_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.out_var.set(p)

    def open_folder(self):
        p = self.out_var.get()
        if os.path.isdir(p):
            if sys.platform.startswith("win"):
                os.startfile(p)
            elif sys.platform == "darwin":
                os.system(f'open "{p}"')
            else:
                os.system(f'xdg-open "{p}"')

    def clear_log(self):
        self.txt_log.delete("1.0", tk.END)

    def log(self, msg):
        self.txt_log.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.txt_log.see(tk.END)
        self.root.update_idletasks()

    def stop_download(self):
        if self.worker and self.worker.is_alive():
            self.stop_flag = True
            self.log("Se cere oprirea...")

    def start_download(self):
        if self.worker and self.worker.is_alive():
            return messagebox.showinfo("Info", "Descarcare in curs.")
        urls = [
            u.strip()
            for u in self.txt_urls.get("1.0", tk.END).splitlines()
            if u.strip()
        ]
        if not urls:
            return messagebox.showwarning("Avertisment", "Introdu un link.")

        outdir = self.out_var.get().strip()
        os.makedirs(outdir, exist_ok=True)
        self.stop_flag = False
        self.progress["value"] = 0
        self.clear_log()
        self.log("Start...")

        self.worker = threading.Thread(
            target=self._download_worker, args=(urls, outdir), daemon=True
        )
        self.worker.start()

    def _get_opts(self):
        fmt, q = self.format_var.get(), self.quality_var.get()
        h = q.split(" ")[0].replace("p", "") if "p" in q else q
        if fmt == "audio_mp3":
            return {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320" if q == "audio_320k" else "128",
                    }
                ],
            }
        return {
            "format": (
                "bv*[ext=mp4]+ba[ext=m4a]/best"
                if q == "best"
                else f"bv*[height<={h}][ext=mp4]+ba[ext=m4a]/bv*[height<={h}]+ba/best"
            ),
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
        }

    def _download_worker(self, urls, outdir):
        def hook(d):
            if self.stop_flag:
                raise DownloadError("Oprit")
            if d.get("status") == "downloading":
                try:
                    self.progress["value"] = float(
                        d.get("_percent_str", "0.0%").replace("%", "")
                    )
                except ValueError:
                    pass
            elif d.get("status") == "finished":
                self.progress["value"] = 100

        opts = {
            "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
            "noplaylist": not self.chk_var.get(),
            "progress_hooks": [hook],
            "ignoreerrors": True,
            "quiet": True,
        }
        opts.update(self._get_opts())

        try:
            with YoutubeDL(opts) as ydl:
                for u in urls:
                    if self.stop_flag:
                        break
                    self.log(f"Procesare: {u}")
                    try:
                        ydl.download([u])
                    except Exception as e:
                        self.log(f"Eroare: {e}")
        finally:
            self.progress["value"] = 0
            self.log("Operatiune anulata." if self.stop_flag else "Finalizat.")


if __name__ == "__main__":
    root = tk.Tk()
    YTDownloaderApp(root)
    root.mainloop()
