# -*- coding: utf-8 -*-

import subprocess as sp

FFMPEG_BIN = "ffmpeg"

class Streamer():
    def __init__(self):
        self.video_command = [FFMPEG_BIN,
                              '-i', '/dev/video0']
        

