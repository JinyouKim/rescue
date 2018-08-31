# -*- coding: utf-8 -*-

import subprocess as sp
import threading


class FfmpegBridge():
    def __init__(self, sm):
        FFMPEG_BIN = "ffmepg/ffmpeg.exe"
        FFPLAY_BIN = "ffmpeg/ffplay.exe"
        rtpAddress = 'rtp://' + sm.multicastIp + ':' + str(sm.multicastPort)
        self.video_command = [FFMPEG_BIN,
                              '-i', '/dev/video0']
        self.audio_send_command = [FFMPEG_BIN,
                                   '-f', 'alsa',
                                   '-i', 'default',
                                   '-c:a', 'libopus',
                                   '-b:a', '12k',
                                   '-ac', '1',
                                   '-f', 'rtp,',
                                   rtpAddress]
        self.audio_recv_command = [FFPLAY_BIN,
                                   '-protocol_whitelist', 'rtp,udp,tcp,file',
                                   '-nodisp'
                                   'res/opus_audio_stream.sdp']
        self.beep_command = [FFPLAY_BIN,
                             '-autoexit',
                             '-nodisp',
                             '-i', 'res/sound/beep.wav']
        self.button_command = [FFPLAY_BIN,
                             '-autoexit',
                             '-nodisp',
                             '-i', 'res/sound/button.wav']

    def playBeep(self):
        threading.Thread(target=sp.call, kwargs={'args':self.beep_command}).start()
        print('y')

    def playButton(self):
        thread = threading.Thread(target=sp.call, kwargs={'args': self.button_command})
        thread.start()

    def sendAudioStream(self):
        thread = threading.Thread(target=sp.call, kwargs={'args': self.audio_send_command})
        thread.start()

    def playAudioStream(self):
        thread = threading.Thread(target=sp.call, kwargs={'args': self.audio_recv_command})
        thread.start()




