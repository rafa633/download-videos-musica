import customtkinter as ctk
from tkinter import messagebox, filedialog
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
        progress_bar.set(percent)
    elif d['status'] == 'finished':
        progress_var.set("Download completo!")
        progress_bar.set(100)

# Função para baixar o vídeo ou áudio
def baixar_video(url, format_id, somente_audio=False):
    save_path = filedialog.askdirectory(title="Escolha a pasta de destino")
    if not save_path:
        messagebox.showwarning("Aviso", "Nenhum diretório selecionado.")
        return

    ydl_opts = {
        'format': 'bestaudio/best' if somente_audio else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    }
    
    if somente_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Download concluído: {url}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar: {e}")

# Função para atualizar os formatos disponíveis de um vídeo do YouTube
def atualizar_formatos(url):
    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            format_choices = [
                f"{f['format_id']} ({f.get('width', 'N/A')}x{f.get('height', 'N/A')}, {f['ext']})"
                for f in formats if f['ext'] in ['mp4', 'mp3']
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
            format_menu.configure(values=formats)
            format_var.set(formats[0])
        else:
            format_menu.configure(values=[])
            format_var.set("Nenhum formato disponível")

# Configurações iniciais para o CustomTkinter
ctk.set_appearance_mode("dark")  # Modo dark
ctk.set_default_color_theme("blue")  # Tema azul

# Configura a janela principal
root = ctk.CTk()
root.title("Baixar Vídeo do YouTube")
root.geometry("600x600")

# Fonte e cores
font_style = ('Helvetica', 14)
button_color = '#FF3C38'
label_color = '#BDBDBD'

# Widgets
label = ctk.CTkLabel(root, text="Digite o link do vídeo do YouTube:", font=font_style)
label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

url_entry = ctk.CTkEntry(root, width=400, font=font_style)
url_entry.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

update_formats_button = ctk.CTkButton(root, text="Atualizar Formatos", command=atualizar_lista_formatos, font=font_style)
update_formats_button.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

format_var = ctk.StringVar(root)
format_menu = ctk.CTkComboBox(root, variable=format_var, values=["Selecione um formato"], font=font_style)
format_menu.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

somente_audio_var = ctk.BooleanVar()
somente_audio_check = ctk.CTkCheckBox(root, text="Baixar apenas o áudio (MP3)", variable=somente_audio_var, font=font_style)
somente_audio_check.grid(row=4, column=0, padx=20, pady=10, sticky='w')

download_button = ctk.CTkButton(root, text="Baixar Vídeo", command=baixar_video_gui, font=font_style)
download_button.grid(row=5, column=0, padx=20, pady=20, sticky='ew')

progress_var = ctk.StringVar()
progress_var.set("Progresso: 0%")
progress_label = ctk.CTkLabel(root, textvariable=progress_var, font=font_style)
progress_label.grid(row=6, column=0, padx=20, pady=10, sticky='w')

progress_bar = ctk.CTkProgressBar(root, width=500)
progress_bar.grid(row=7, column=0, padx=20, pady=10, sticky='ew')

root.grid_columnconfigure(0, weight=1)

root.mainloop()
