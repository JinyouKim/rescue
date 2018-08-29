# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class UiClientDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 800)
        Dialog.setModal(True)

        # Dialog 레이아웃
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(2, 2, 2, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 프레임
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")

        # 버튼 3개를 위한 레이아웃
        self.verticalLayout.addWidget(self.frame)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 카메라 버튼
        self.cameraButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraButton.sizePolicy().hasHeightForWidth())
        self.cameraButton.setSizePolicy(sizePolicy)
        self.cameraButton.setMinimumSize(QtCore.QSize(150, 150))
        self.cameraButton.setText("camera")
        self.cameraButton.setCheckable(False)
        self.cameraButton.setObjectName("cameraButton")
        self.horizontalLayout.addWidget(self.cameraButton)

        # 음성 버튼
        self.voiceButton = QtWidgets.QPushButton(Dialog)
        self.voiceButton.setSizePolicy(sizePolicy)
        self.voiceButton.setMinimumSize(QtCore.QSize(150, 150))
        self.voiceButton.setText("")
        self.voiceButton.setIconSize(QtCore.QSize(150, 150))
        self.voiceButton.setCheckable(False)
        self.voiceButton.setChecked(False)
        self.voiceButton.setObjectName("voiceButton")
        self.horizontalLayout.addWidget(self.voiceButton)
        self.voiceButton.setText("voice")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voiceButton.sizePolicy().hasHeightForWidth())

        # 응급신호 버튼
        self.signalButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signalButton.sizePolicy().hasHeightForWidth())
        self.signalButton.setSizePolicy(sizePolicy)
        self.signalButton.setMinimumSize(QtCore.QSize(150, 150))
        self.signalButton.setObjectName("signalButton")
        self.horizontalLayout.addWidget(self.signalButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.signalButton.setText("signal")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiClientDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
