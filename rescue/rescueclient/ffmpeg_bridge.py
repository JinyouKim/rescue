# -*- coding: utf-8 -*-

import subprocess as sp
import threading


class FfmpegBridge():
    def __init__(self):
        FFMPEG_BIN = "ffmepg/ffmpeg.exe"
        FFPLAY_BIN = "ffmpeg/ffplay.exe"
        self.video_command = [FFMPEG_BIN,
                              '-i', '/dev/video0']
        self.beep_command = [FFPLAY_BIN,
                             '-autoexit',
                             '-nodisp',
                             '-i', 'res/sound/beep.wav']
        self.button_command = [FFPLAY_BIN,
                             '-autoexit',
                             '-nodisp',
                             '-i', 'res/sound/button.wav']

    def playBeep(self):
        print(self.beep_command)
        threading.Thread(target=sp.call, kwargs={'args':self.beep_command}).start()
        print('y')

    def playButton(self):
        threading.Thread(target=sp.call, kwargs={'args': self.button_command}).start()
        print('y')



