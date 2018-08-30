# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimeLine
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QStackedWidget, QTextEdit
from PyQt5.QtWidgets import QWidget


class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class StackedWidget(QStackedWidget):

    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def setPage1(self):
        self.setCurrentIndex(0)

    def setPage2(self):
        self.setCurrentIndex(1)


class UiClientDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 800)
        Dialog.setModal(True)
        Dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        mainWidget = QWidget()

        # Dialog 레이아웃
        self.verticalLayout = QtWidgets.QVBoxLayout(mainWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 프레임
        self.frame = QtWidgets.QFrame(mainWidget)
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
        self.line = QtWidgets.QFrame(mainWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 카메라 버튼
        self.cameraButton = QtWidgets.QPushButton(mainWidget)
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
        self.voiceButton = QtWidgets.QPushButton(mainWidget)
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
        self.signalButton = QtWidgets.QPushButton(mainWidget)
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

        self.stack = StackedWidget()
        self.stack.addWidget(mainWidget)
        self.stack.addWidget(QTextEdit())

        layout = QVBoxLayout(Dialog)
        layout.addWidget(self.stack)

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
