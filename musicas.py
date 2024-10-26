import os
import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence

# Inicializando o mixer do pygame
pygame.mixer.init()

# Variáveis globais
current_music_index = 0
music_files = []
gif_frames = []
gif_frame_index = 0
gif_animating = False
is_paused = False

# Escolhe a pasta de músicas
def choose_folder():
    global music_files
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        music_files = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith(('.mp3', '.wav', '.ogg'))]
        if music_files:
            play_music(music_files[0])

# Reproduz música
def play_music(file):
    global gif_animating, is_paused
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    music_label.config(text=f"Reproduzindo: {os.path.basename(file)}")
    gif_animating = True
    is_paused = False
    show_playing_image()

# Exibe e anima o GIF
def show_playing_image():
    global gif_frames, gif_frame_index
    img_playing = Image.open(r"C:\Users\rafae\Downloads\44zG.gif")
    gif_frames = [ImageTk.PhotoImage(frame.copy().resize((600, 150), Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(img_playing)]
    gif_frame_index = 0
    if gif_animating:
        animate_gif()

def animate_gif():
    global gif_frame_index
    if gif_animating and gif_frames:
        image_label.config(image=gif_frames[gif_frame_index])
        gif_frame_index = (gif_frame_index + 1) % len(gif_frames)
        if not is_paused:
            root.after(100, animate_gif)

# Avança para a próxima música
def next_music():
    global current_music_index
    if music_files:
        current_music_index = (current_music_index + 1) % len(music_files)
        play_music(music_files[current_music_index])

# Volta para a música anterior
def prev_music():
    global current_music_index
    if music_files:
        current_music_index = (current_music_index - 1) % len(music_files)
        play_music(music_files[current_music_index])

# Pausa ou retoma a música
def pause_resume_music():
    global gif_animating, is_paused
    if pygame.mixer.music.get_busy():
        if not is_paused:
            pygame.mixer.music.pause()
            pause_button.config(text="Retomar")
            gif_animating = False
            is_paused = True
        else:
            pygame.mixer.music.unpause()
            pause_button.config(text="Pausar")
            gif_animating = True
            is_paused = False
            animate_gif()

# Para a música e o GIF
def stop_music():
    global gif_animating, is_paused
    pygame.mixer.music.stop()
    music_label.config(text="Música parada")
    image_label.config(image='')
    gif_animating = False
    is_paused = False

# Interface Tkinter
root = tk.Tk()
root.title("Music Player")
root.configure(bg='black')

music_label = tk.Label(root, text="Nenhuma música reproduzindo", font=('Helvetica', 12), fg='white', bg='black')
music_label.pack(pady=10)

image_label = tk.Label(root, bg='black')
image_label.pack(pady=10)

button_style = {'width': 12, 'padx': 5, 'pady': 5, 'bg': '#333', 'fg': 'white', 'font': ('Helvetica', 10)}

prev_button = tk.Button(root, text="Anterior", command=prev_music, **button_style)
prev_button.pack(side=tk.LEFT, padx=10)

pause_button = tk.Button(root, text="Pausar", command=pause_resume_music, **button_style)
pause_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(root, text="Próxima", command=next_music, **button_style)
next_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(root, text="Parar", command=stop_music, **button_style)
stop_button.pack(side=tk.LEFT, padx=10)

choose_folder_button = tk.Button(root, text="Escolher Pasta de Músicas", command=choose_folder, **button_style)
choose_folder_button.pack(pady=20)

root.mainloop()
