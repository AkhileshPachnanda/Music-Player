import os
import threading
import time 
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk
from tkinter import ttk

root = Tk ()
root.geometry = ("300 x 300")
root.resizable(4,4)
statusbar = Label(root, text="Welcome to Music Player", relief=RAISED, anchor=W, bg="#1a1a1a", fg="white", bd=0)
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root, bg="#1a1a1a", fg="white")
root.config(menu=menubar, bg="#1a1a1a", bd= 0)
menubar.configure(background="#1a1a1a", bd=0)
# Create the submenu

subMenu = Menu(menubar, tearoff=0, bg="#1a1a1a", fg="white", bd= 0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function
filename_path= None
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Music Player', 'This is a music player build using Python Tkinter')


subMenu = Menu(menubar, tearoff=0,bg="#1a1a1a", fg="white", bd=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Music Player")
root.iconbitmap(r'Images/favicon.ico')

leftframe = Frame(root, bg="#1a1a1a")
leftframe.pack(side=LEFT, padx=30, pady=30, )

playlistbox = Listbox(leftframe, bg="#1a1a1a", fg="white", bd=5)
playlistbox.pack()


addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="Delete", command=del_song,)
delBtn.pack(side=LEFT)


topframe = Frame(root, bg= "#1a1a1a")
topframe.pack()

lengthlabel = Label(topframe, text='Total Length - 00:00', bd=3, bg="#1a1a1a", fg="white")
lengthlabel.pack( pady=10)

currenttimelabel = Label(topframe, text='Current Time - 00:00', bd=3, bg ="#1a1a1a", fg="white")
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

paused=None
def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(100)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(root, bg="#1a1a1a")
middleframe.pack()

playPhoto = PhotoImage(file='Images/play.png')
playBtn = Button(middleframe, image=playPhoto, command=play_music, bd=2.5)
playBtn.grid(row=4, column=1, pady=30, padx=3)

stopPhoto = PhotoImage(file='Images/square.png')
stopBtn =Button(middleframe, image=stopPhoto, command=stop_music, bd=2.5)
stopBtn.grid(row=4, column=3, pady=30, padx=3)

pausePhoto = PhotoImage(file='Images/pause.png')
pauseBtn = Button(middleframe, bg="white", image=pausePhoto, command=pause_music, bd=2.5)
pauseBtn.grid(row=4, column=4, pady=40, padx=3)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(bg ="#1a1a1a")
bottomframe.pack()

rewindPhoto = PhotoImage(file='Images/rewind.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, command=rewind_music, bd=2.5)
rewindBtn.grid(row=0,column=2,padx=3)

mutePhoto = PhotoImage(file='Images/mute.png')
volumePhoto = PhotoImage(file='Images/speaker.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music, bd=2.5)
volumeBtn.grid(row=0, column=1,padx=3)

scale = Scale(bottomframe,from_=0, to=100, orient=HORIZONTAL,command=set_vol, bg="#1a1a1a", fg ="white", bd=0)

scale.set(100)
mixer.music.set_volume(1.0)
scale.grid(row=0, column=4, pady=40, padx=20)


def on_closing():
    stop_music()
    root.destroy()

root["bg"] = "#1a1a1a"
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()