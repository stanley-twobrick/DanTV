import os
import random
import vlc
import time
from gpiozero import RotaryEncoder, Button
from subprocess import call
from collections import deque

#main VLC player class
class Player():
    def __init__(self):
        self._instance = vlc.Instance(['--vout=mmal_vout'])
        self._player = self._instance.media_player_new()
        self._player.set_fullscreen(True)
        self._player.video_set_aspect_ratio("4:3")
        self._player.video_set_scale(2)

    def play(self, path):
        media = self._instance.media_new(path)
        self._player.set_media(media)
        self._player.play()
        playing = set([1,2,3,4])
        time.sleep(0.1)
        while True:
            state = self._player.get_state()
            if state not in playing:
                break
            time.sleep(1)

    def stop(self):
        self._player.stop()

p=Player()

#grab your list of tv show subdirectories
folderslist = []

for root, dirs, files in os.walk("/media/videos/shows/"):
    for dir in sorted(dirs):
        folderslist.append(os.path.join(root,dir))

dfolders = deque(folderslist)

print(dfolders)

#always start on ILL
#selectedfolder = "/media/videos/shows/I Love Lucy"
#unless you don't want to, then uncomment below:
selectedfolder = dfolders[0]

#function to change the show to a new folder
def new_show():
    global selectedfolder
    global showlist
    global show
    showlist = []
    for root, dirs, files in os.walk(selectedfolder):
        for file in files:
            if(file.endswith(".mp4")):
                showlist.append(os.path.join(root,file))
    show = random.choice(showlist)
    print(show)

new_show()

#rotary encoder functions
def rotatingcw():
    global dfolders
    global selectedfolder
    global show
    global showlist
    global playnum
    dfolders.rotate(1)
    selectedfolder = dfolders[0]
    new_show()
    playnum = 1
    p.stop()

def rotatingccw():
    global dfolders
    global selectedfolder
    global showlist
    global show
    global playnum
    dfolders.rotate(-1)
    selectedfolder = dfolders[0]
    new_show()
    playnum = 1
    p.stop()

def buttonstop():
    global playstate
    if playstate==0:
        playstate=1
        p.stop()
    else:
        playstate=0

def buttonshutdown():
    call("sudo shutdown -h now", shell=True)

#set up rotary encoder
rotor = RotaryEncoder(17, 18, wrap=True)
btn = Button(3)

rotor.when_rotated_clockwise = rotatingcw
rotor.when_rotated_counter_clockwise = rotatingccw
btn.when_released = buttonstop
btn.when_held = buttonshutdown

#grab your ads
adlist = []

for root, dirs, files in os.walk("/media/videos/ads/"):
    for file in files:
        if(file.endswith(".mp4")):
            adlist.append(os.path.join(root,file))

#and go
i=0
playstate=0
playnum=1

while i < 1:
    if playstate==1: #button was clicked
        time.sleep(1)
    else:
        if playnum == 1:
            mchoice = random.choice(showlist)
            playnum += 1
        elif 2 <= playnum <= 4:
            mchoice = random.choice(adlist)
            playnum += 1
        else:
            mchoice = random.choice(adlist)
            playnum = 1
        p.play(mchoice)
