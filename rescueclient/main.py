# -*- coding: utf-8 -*-
import sys
import socket
import struct
import time

from common import message
from common.message import Message

from common.message_header import Header
from common.message_body import BodyCommonResponse, BodyEmpty, BodyConnectRequest

from common.message_util import MessageUtil

CHUNK_SIZE = 4096

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: {0} <server IP>".format(sys.argv[0]))
        sys.exit(0)

    serverIp = sys.argv[1]
    serverPort = 9000

    # 음성 통신을 위한 멀티캐스트 주소
    multicastIp = '239.0.0.1'
    multicastPort = 9111

    sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sockMulticast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockMulticast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mreq = struct.pack("4sl", socket.inet_aton(multicastIp), socket.INADDR_ANY)
    sockMulticast.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        ret = -1
        while ret != 0:
            ret = sockServer.connect_ex((serverIp, serverPort))
            time.sleep(2)

        reqMsg = Message()
        reqMsg.Body = BodyConnectRequest(None)
        reqMsg.Body.RESQUER_ID = '1'
        reqMsg.Header = Header(None)
        reqMsg.Header.MSGTYPE = message.REQ_CONNECT
        reqMsg.Header.BODYLEN = reqMsg.Body.getSize()

        MessageUtil.send(sockServer, reqMsg)
        rspMsg = MessageUtil.receive(sockServer)

        if rspMsg.Header.MSGTYPE != message.REP_CONNECT:
            print("Error")
            exit(0)
        if rspMsg.Body.RESPONSE != message.ACCEPTED:
            print("Connection is refused.")
            exit(0)

        print("Connected with server")

        # 버튼 구현 필요
        while True:
            input = input()

            # 카메라
            if input == 'c':
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
            if input == 'v':
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






    except Exception as err:
        print("Exception")
        print(err)

    sockServer.close()
