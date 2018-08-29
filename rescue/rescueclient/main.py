# -*- coding: utf-8 -*-
import sys
import socket
import struct
import time

from PyQt5 import QtWidgets
from rescue.rescueclient.client_dialog import ClientDialog
from rescue.rescueclient.socket_manager import SocketManager

from rescue.rescueclient.ui.ui_client_dialog import UiClientDialog

CHUNK_SIZE = 4096

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: {0} <server IP> <server port>".format(sys.argv[0]))
        sys.exit(0)

    serverIp = sys.argv[1]
    serverPort = int(sys.argv[2])

    sm = SocketManager(serverIp, serverPort)
    sm.connectServer()
    sm.joinMuticastGroup(multicastIp='239.0.0.1')

    clientDialog = ClientDialog(sm)

    sys.exit(clientDialog.showDialog())





'''

        # 버튼 구현 필요
        while True:
            inputC = input()

            # 카메라
            if inputC == 'c':
                reqMsg = Message()
                reqMsg.Body = BodyEmpty()
                reqMsg.Header = Header(None)
                reqMsg.Header.MSGTYPE = message.REQ_VIDEO_STREAMING
                reqMsg.Header.BODYLEN = 0
                # 스트리밍 연결 요청
                MessageUtil.send(sockServer, reqMsg)
                # 통화음 또는 연결 화면 보이는 로직 필요

                # 연결 수락 대기
                rspMsg = MessageUtil.receive(sockServer)

                if rspMsg.Header.MSGTYPE != message.REP_VIDEO_STREAMING:
                    print('Error')
                    exit(0)

                # 서버에서 수락하면
                if rspMsg.Body.RESPONSE == message.ACCEPTED:
                    print('streaming accept')
                    
                # 서버에서 거절하면
                else:
                    print('streaming denied')

            # 음성 전송
            elif inputC == 'v':
                reqMsg = Message()
                reqMsg.Body = BodyEmpty()
                reqMsg.Header = Header(None)
                reqMsg.Header.MSGTYPE = message.REQ_GET_TOKEN
                reqMsg.Header.BODYLEN = 0

                # 토큰 요청
                MessageUtil.send(sockServer, reqMsg)

                # 요청 결과
                rspMsg = MessageUtil.receive(sockServer)

                if rspMsg.Header.MSGTYPE != message.REP_GET_TOKEN:
                    print('Error')
                    exit(0)

                # 서버에서 수락하면
                if rspMsg.Body.RESPONSE == message.ACCEPTED:
                    print('voice accept')
                    # 보이스 전송

                # 서버에서 거절하면
                else:
                    print('voice denied')

'''

