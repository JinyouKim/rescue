# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QTimeLine
from PyQt5.QtGui import QPainter, QPixmap

from rescue.rescueclient.ffmpeg_bridge import FfmpegBridge
from rescue.rescueclient.socket_manager import SocketManager
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QStackedWidget, QWidget
from rescue.rescueclient.ui.ui_client_dialog import UiClientDialog
from rescue.rescueclient.ui.ui_signal_widget import UiSignalWidget
from rescue.rescueclient.ui.ui_translucent_widget import UiTranslucentWidget

class ClientDialog():
    def __init__(self, sm):
        self.sm = sm
        self.isVoiceCalling = False
        self.isClickedSignal = False
        self.ffmpegBridge = FfmpegBridge(sm)
        self.ffmpegBridge.playAudioStream()

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

            self.ffmpegBridge.sendAudioStream()
            # 음성 전송 처리
            None
        # 요청 실패
        else:
            None

    def releasedVoiceButton(self):
        if self.isVoiceCalling:
            isAccepted = self.sm.returnToken()
            self.isVoiceCalling = False
            self.popupFrame.close()
            self.popupFlag = False
            self.ffmpegBridge.stopSendingAudioStream()

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

