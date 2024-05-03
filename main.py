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
    songs_display.delete(0, END)

    # Append songs in flac format to the songs list
    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == ".flac":
            songs.append(song)

    # Add songs to the songs Listbox
    for song in songs:
        songs_display.insert("end", song)

    songs_display.selection_set(0)
    current_song = songs[songs_display.curselection()[0]]


def play_pause():
    global pause

    if current_song == "":
        pass
    elif pause:
        pygame.mixer.music.unpause()
        play_pause_btn.config(image=pause_img)
        pause = False
    else:
        pygame.mixer.music.pause()
        play_pause_btn.config(image=play_img)
        pause = True


def previous():
    global current_song, pause

    songs_display.selection_clear(0, END)

    if songs.index(current_song) == 0:
        songs_display.selection_set(len(songs) - 1)
    else:
        songs_display.selection_set(songs.index(current_song) - 1)

    current_song = songs[songs_display.curselection()[0]]
    pygame.mixer.music.load(os.path.join(window.directory, current_song))
    pygame.mixer.music.play()
    pause = False
    play_pause_btn.config(image=pause_img)


def next():
    global current_song, pause

    songs_display.selection_clear(0, END)

    if songs.index(current_song) == len(songs) - 1:
        songs_display.selection_set(0)
    else:
        songs_display.selection_set(songs.index(current_song) + 1)

    current_song = songs[songs_display.curselection()[0]]
    pygame.mixer.music.load(os.path.join(window.directory, current_song))
    pygame.mixer.music.play()
    pause = False
    play_pause_btn.config(image=pause_img)


def on_double_click(event):
    global current_song, pause

    widget = event.widget
    index = int(widget.curselection()[0])
    current_song = widget.get(index)
    pygame.mixer.music.load(os.path.join(window.directory, current_song))
    pygame.mixer.music.play()
    pause = False
    play_pause_btn.config(image=pause_img)


# Create toolbar and add it to the window
toolbar = Menu(window)
window.config(menu=toolbar)

# Set up toolbar
toolbar_menu = Menu(toolbar, tearoff=False)
toolbar.add_cascade(label="Organize", menu=toolbar_menu)
toolbar_menu.add_command(label="Select folder", command=load_music)

songs_display = Listbox(window, bg="black", fg="white", width=700, height=38)
songs_display.bind("<Double-Button-1>", on_double_click)
songs_display.pack()

play_img = PhotoImage(file="play.png")
pause_img = PhotoImage(file="pause.png")
prev_img = PhotoImage(file="previous.png")
next_img = PhotoImage(file="next.png")

controls = Frame(window)
controls.pack()

play_pause_btn = Button(controls, image=play_img, command=play_pause)
play_pause_btn.grid(row=0, column=1, pady=10)

prev_btn = Button(controls, image=prev_img, command=previous)
prev_btn.grid(row=0, column=0, padx=20, pady=15)

next_btn = Button(controls, image=next_img, command=next)
next_btn.grid(row=0, column=2, padx=20, pady=15)

window.mainloop()
