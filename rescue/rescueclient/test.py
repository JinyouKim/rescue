from rescue.rescueclient.sound import SoundManager
from rescue.rescueclient.codec import OpusCodec
from rescue.rescueclient.streaming import VoiceStreaming
import ctypes
from array import array

sm = SoundManager(inputDeviceName='default')
oc = OpusCodec()
vs = VoiceStreaming('192.0.1.62', 8000)
sm.startRecord()

isStarted = False

while True:

    #print(type(b'\x00'*100))
    #print(sm.getInputFrame().tostring())

    c = sm.getInputFrame()
    a = c.tobytes()
    b = oc.encodeFrames(a)
    vs.sendVoicePacket(b)
    d = oc.decodeFrames(b)

    sm.pushFrame(d)
    if isStarted is False:
        sm.startPlay()
        isStarted = True

    
    
#    print(oc.decodeFrames(b))
    
