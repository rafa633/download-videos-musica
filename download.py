import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sys
import yt_dlp
import threading
import os

# Função de progresso para a barra de progresso
def progress_hook(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)
        percent = (downloaded / total_size) * 100 if total_size else 0
        progress_var.set(f"{percent:.2f}%")
        progress_bar['value'] = percent
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress_var.set("Download completo!")
        progress_bar['value'] = 100
        root.update_idletasks()

# Função para baixar o vídeo ou áudio
def baixar_video(url, format_id, somente_audio=False):
    save_path = filedialog.askdirectory(title="Escolha a pasta de destino")
    if not save_path:
        messagebox.showwarning("Aviso", "Nenhum diretório selecionado.")
        return

    if somente_audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Download concluído: {url}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar: {e}")

# Função para atualizar os formatos disponíveis de um vídeo do YouTube
def atualizar_formatos(url):
    try:
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            format_choices = [
                f"{f['format_id']} ({f.get('width', 'N/A')}x{f.get('height', 'N/A')}, {f['ext']})"
                for f in formats
                if f['ext'] in ['mp4', 'mp3']
            ]
            return format_choices
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter formatos: {e}")
        return []

# Função de download integrada à GUI em uma thread
def baixar_video_gui():
    url = url_entry.get()
    format_id = format_var.get()
    somente_audio = somente_audio_var.get()

    if url and format_id:
        thread = threading.Thread(target=baixar_video, args=(url, format_id, somente_audio))
        thread.start()
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um link válido e selecione um formato.")

# Função para atualizar a lista de formatos na GUI
def atualizar_lista_formatos():
    url = url_entry.get()
    if url:
        formats = atualizar_formatos(url)
        if formats:
            format_menu['values'] = formats
            format_menu.set(formats[0])
        else:
            format_menu['values'] = []
            format_menu.set("Nenhum formato disponível")

# Configura a janela principal
root = tk.Tk()
root.title("Baixar Vídeo do YouTube")

root.geometry("600x600")
root.resizable(True, True)
root.configure(bg='#1E1E1E')

font_style = ('Helvetica', 14)
button_color = '#FF3C38'
button_hover_color = '#149911'
entry_bg = '#BEBBB2'
entry_fg = 'black'
label_color = '#BDBDBD'

label = tk.Label(root, text="Digite o link do vídeo do YouTube:", font=font_style, bg='#1E1E1E', fg=label_color)
label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

url_entry = tk.Entry(root, width=50, font=font_style, borderwidth=2, relief="flat", bg=entry_bg, fg=entry_fg)
url_entry.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

update_formats_button = tk.Button(root, text="Atualizar Formatos", command=atualizar_lista_formatos, font=font_style, bg=button_color, fg='white', borderwidth=0, relief="raised")
update_formats_button.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

format_var = tk.StringVar(root)
format_var.set("Selecione um formato")

format_menu = ttk.Combobox(root, textvariable=format_var, state="readonly", font=font_style)
format_menu.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

somente_audio_var = tk.BooleanVar()
somente_audio_check = tk.Checkbutton(root, text="Baixar apenas o áudio (MP3)", variable=somente_audio_var, font=font_style, bg='#1E1E1E', fg=label_color, selectcolor='#FF5722')
somente_audio_check.grid(row=4, column=0, padx=20, pady=10, sticky='w')

download_button = tk.Button(root, text="Baixar Vídeo", command=baixar_video_gui, font=font_style, bg=button_color, fg='white', borderwidth=0, relief="raised")
download_button.grid(row=5, column=0, padx=20, pady=20, sticky='ew')

progress_var = tk.StringVar()
progress_var.set("Progresso: 0%")
progress_label = tk.Label(root, textvariable=progress_var, font=font_style, bg='#1E1E1E', fg=label_color)
progress_label.grid(row=6, column=0, padx=20, pady=10, sticky='w')

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.grid(row=7, column=0, padx=20, pady=10, sticky='ew')

root.grid_columnconfigure(0, weight=1)

root.mainloop()
