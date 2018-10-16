# -*- coding: utf-8 -*-
import sys
import socketserver
import threading
import queue

from PyQt5.QtCore import QTimeLine
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

from rescue.rescueclient.ffmpeg_bridge import FfmpegBridge
from rescue.rescueclient.socket_manager import SocketManager
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QStackedWidget, QWidget
from rescue.rescueclient.ui.ui_client_dialog import UiClientDialog
from rescue.rescueclient.ui.ui_signal_widget import UiSignalWidget
from rescue.rescueclient.ui.ui_translucent_widget import UiTranslucentWidget
from rescue.rescueclient.sound import SoundManager
from rescue.rescueclient.codec import OpusCodec
from rescue.rescueclient.streaming import VoiceStreaming

from rescue.common import message
from rescue.common.message import Message
from rescue.common.message_util import MessageUtil
from rescue.common.message_header import Header
from rescue.common.message_body import BodyCommonResponse, BodyEmpty

HOST = '192.0.1.10'
PORT = 9900

REMOTE = '122'

q1 = queue.Queue()
q2 = queue.Queue()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = self.request
        try:
            while True:
                reqMsg = MessageUtil.receive(client)
                print(reqMsg.Header.MSGTYPE)
                if reqMsg == None:
                    continue
                if reqMsg.Header.MSGTYPE == message.REQ_CALL: 
                    global REMOTE
                    print(self.client_address[0])
                    REMOTE = self.client_address[0]
                    q1.put(0)
                    isAccepted = q2.get()

                    rspMsg = Message()
                    rspMsg.Body = BodyCommonResponse(None)
                    if isAccepted:
                        rspMsg.Body.RESPONSE = message.ACCEPTED
                    else:
                        rspMsg.Body.RESPONSE = message.DENIED

                    rspMsg.Header = Header(None)
                    rspMsg.Header.MSGTYPE = message.REP_CALL
                    print(message.REP_CALL)
                    rspMsg.Header.BODYLEN = rspMsg.Body.getSize()
                    MessageUtil.send(client, rspMsg)

                    continue
        except Exception as err:
            print(err)

class CallSignal(QObject):
    callSignal = pyqtSignal()
    
    def run(self):
        self.callSignal.emit()


class ClientDialog():
    def __init__(self, sm, thriftUi):
        self.sm = sm
        self.thriftUi = thriftUi
        self.soundManager= SoundManager()
        self.isVoiceCalling = False
        self.isClickedSignal = False
        self.ffmpegBridge = FfmpegBridge(sm)
        self.ffmpegBridge.playAudioStream()
        self.callSignal = CallSignal()
        self.callSignal.callSignal.connect(self.call_handle)
        self.streamThread = threading.Thread(target = self.streaming_handle, args = ("tast",))
        self.playThread = threading.Thread(target = self.play_thread, args = ("tast",))
        self.multicastSendThread = threading.Thread(target = self.multicast_stream_thread, args=("task",))
        
        self.multicastRecvThread = threading.Thread(target = self.multicast_play_thread, args=("task",))
        self.multicastRecvThread.start()

        self.vs = None
        self.oc = OpusCodec()
        
        requestListener = ThreadedTCPServer((HOST, PORT), RequestHandler)
        threading.Thread(target=requestListener.serve_forever).start()
        callThread = threading.Thread(target = self.call_thread)
        callThread.start()

    def multicast_stream_thread(self, arg):
        vs = VoiceStreaming(self.sm.myIp, self.sm.multicastPort, self.sm.multicastIp, self.sm.multicastPort)
        self.soundManager.startRecord()
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            pcm = self.soundManager.getInputFrame().tobytes()
            vs.sendVoicePacket(self.oc.encodeFrames(pcm))

        self.soundManager.stopRecord()
        vs.closeSocket()

    def play_thread(self, arg):
        t = threading.currentThread()
        isStarted = False
        while getattr(t, "do_run", True):
            opusFrame = self.vs.recvVoicePacket()
            pcm = self.oc.decodeFrames(opusFrame)
            self.soundManager.pushFrame(pcm)
            if isStarted is False:
                 self.soundManager.startPlay()
            isStarted = True

        self.soundManager.stopPlay()

    def multicast_play_thread(self, arg):
        vs = VoiceStreaming(self.sm.myIp, self.sm.multicastPort, self.sm.multicastIp, self.sm.multicastPort)
        isStarted = False
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            opusFrame = vs.recvVoicePacket()
            pcm = self.oc.decodeFrames(opusFrame)
            self.soundManager.pushFrame(pcm)
            if isStarted is False:
                 self.soundManager.startPlay()
            isStarted = True

        vs.closeSocket()
        self.soundManager.stopPlay()
             
        
    def streaming_handle(self, arg):        
        self.vs = VoiceStreaming('192.0.1.10', 8000, REMOTE, 8000)
        print(REMOTE)
        self.soundManager.startRecord()
        self.playThread.start()
        t = threading.currentThread()

        while getattr(t, "do_run", True):
            pcm = self.soundManager.getInputFrame().tobytes()
            self.vs.sendVoicePacket(self.oc.encodeFrames(pcm))

        self.playThread.do_run = False
        self.soundManager.stopRecord()
        self.vs.closeSocket()
            
        
    def call_handle(self):
        self.soundManager.playRing()
        choice = QMessageBox.question(self.dialog, "Call", "Calling from Rescuee, Accept?", QMessageBox.Yes | QMessageBox.No)
        isAccepted = False
        if choice == QMessageBox.Yes:
            q2.put(True)
            self.multicastRecvThread.do_run = False
            self.streamThread.start()
            # rtp Thread
            
        else:
            q2.put(False)
        self.soundManager.stopRing()

    def call_thread(self):
        while True:
            q1.get()        
            self.callSignal.run()

    def showDialog(self):
        app = QApplication(sys.argv)
        self.dialog = QDialog()
        self.ui = UiClientDialog()
        self.ui.setupUi(self.dialog)

        # 클릭 이벤트
        self.ui.cameraButton.clicked.connect(self.clickedCameraButton)
        self.ui.voiceButton.pressed.connect(self.pressedVoiceButton)
        self.ui.voiceButton.released.connect(self.releasedVoiceButton)
        self.ui.signalButton.clicked.connect(self.clickedSignalButton)

        self.dialog.show()

        # 시그널 전송 프레임
        self.signalFrame = UiSignalWidget(self.ui.frame)
        self.signalFrame.searchCompleteBtn.clicked.connect(self.clickedSearchCompleteButton)
        self.signalFrame.findRescueeBtn.clicked.connect(self.clickedFindRescueeButton)
        self.signalFrame.findRescuerBtn.clicked.connect(self.clickedFindRescuerButton)
        self.signalFrame.move(50, 50)

        return app.exec_()


    def clickedCameraButton(self):
        self.ffmpegBridge.playButton()
        choice = QMessageBox.question(self.dialog, "Video Streaming", "지휘PC로 영상을 전송 하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        isAccepted = False
        if choice == QMessageBox.Yes:
            self.ui.stack.setPage2()
            isAccepted = self.sm.requestVideoCall()

            # 카메라 전송 처리
            if isAccepted:
                None

        print(isAccepted)

    def pressedVoiceButton(self):
        isAccepted = self.sm.requestVoice()

        # 요청 성공
        if isAccepted:
            self.isVoiceCalling = True
            self.ffmpegBridge.playBeep()
            self.popupFrame = UiTranslucentWidget(self.dialog)
            self.popupFrame.move(0, 0)
            self.popupFrame.resize(self.dialog.width(), self.dialog.height())
            self.popupFlag = True
            self.popupFrame.show()

            #self.ffmpegBridge.sendAudioStream()

            # 음성 전송 처리
            self.multicastSendThread = threading.Thread(target = self.multicast_stream_thread, args=("task",))
            self.multicastSendThread.start()        
           
        # 요청 실패
        else:
            None

    def releasedVoiceButton(self):
        if self.isVoiceCalling:
            isAccepted = self.sm.returnToken()
            self.isVoiceCalling = False
            self.popupFrame.close()
            self.popupFlag = False
            self.multicastSendThread.do_run = False

    def clickedSignalButton(self):
        self.ffmpegBridge.playButton()
        if not self.isClickedSignal:

            self.isClickedSignal = not self.isClickedSignal
            self.signalFrame.show()

        else:
            self.isClickedSignal = not self.isClickedSignal
            self.signalFrame.close()

    def clickedSearchCompleteButton(self):
        self.ffmpegBridge.playButton()


    def clickedFindRescueeButton(self):
        self.ffmpegBridge.playButton()

    def clickedFindRescuerButton(self):
        self.ffmpegBridge.playButton()

