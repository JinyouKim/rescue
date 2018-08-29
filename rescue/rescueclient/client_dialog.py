# -*- coding: utf-8 -*-
import sys


from rescue.rescueclient.socket_manager import SocketManager
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from rescue.rescueclient.ui.ui_client_dialog import UiClientDialog


class ClientDialog():
    def __init__(self, sm):
        self.sm = sm
        self.isVoiceCalling = False

    def showDialog(self):
        app = QApplication(sys.argv)
        self.dialog = QDialog()
        ui = UiClientDialog()
        ui.setupUi(self.dialog)

        # 클릭 이벤트
        ui.cameraButton.clicked.connect(self.clickedCameraButton)
        ui.voiceButton.pressed.connect(self.pressedVoiceButton)
        ui.voiceButton.released.connect(self.releasedVoiceButton)
        print("2")
        self.dialog.show()

        return app.exec_()

    def clickedCameraButton(self):
        choice = QMessageBox.question(self.dialog, "Voice Streaming", "지휘PC로 영상을 전송 하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        isAccepted = False
        if choice == QMessageBox.Yes:
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
            # 음성 전송 처리
            None
        # 요청 실패
        else:
            None

    def releasedVoiceButton(self):
        if self.isVoiceCalling:
            isAccepted = self.sm.returnToken()
            self.isVoiceCalling = False


        print("y")

