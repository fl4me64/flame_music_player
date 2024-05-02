from tkinter import *
from tkinter import filedialog
import pygame
import os

# Create window
window = Tk()
window.title("Flame Music Player")
window.geometry("700x700")

# Initialize pygame.mixer
pygame.mixer.init()

songs = []
current_song = ""
pause = True


def load_music():
    global current_song

    # Request directory from the user
    window.directory = filedialog.askdirectory()

    # Clear songs
    songs.clear()
    songs_display.delete(0, 'end')

    # Append songs in mp3 format to the songs list
    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == ".flac":
            songs.append(song)

    # Add songs to the songs Listbox
    for song in songs:
        songs_display.insert("end", song)

    songs_display.selection_set(0)
    current_song = songs[songs_display.curselection()[0]]


def play():
    global pause

    if pause:
        pygame.mixer.music.load(os.path.join(window.directory, current_song))
        pygame.mixer.music.play()
        play_pause.config(image=pause_img)
        pause = False
    else:
        pygame.mixer.music.pause()
        play_pause.config(image=play_img)
        pause = True


def on_select(event):
    global current_song

    widget = event.widget
    index = int(widget.curselection()[0])
    current_song = widget.get(index)
    print("Selected " + current_song)


# Create toolbar and add it to the window
toolbar = Menu(window)
window.config(menu=toolbar)

# Set up toolbar
toolbar_menu = Menu(toolbar, tearoff=False)
toolbar_menu.add_command(label="Select folder", command=load_music)
toolbar.add_cascade(label="Organize", menu=toolbar_menu)

songs_display = Listbox(window, bg="black", fg="white", width=700, height=38)
songs_display.bind("<<ListboxSelect>>", on_select)
songs_display.pack()

play_img = PhotoImage(file="play.png")
pause_img = PhotoImage(file="pause.png")

play_pause = Button(image=play_img, command=play)
play_pause.pack()

window.mainloop()
