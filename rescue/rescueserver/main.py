# -*- coding: utf-8 -*-
import socketserver
import threading

from rescue.common import message
from rescue.common.message import Message
from rescue.common.message_util import MessageUtil
from rescue.common.message_header import Header
from rescue.common.message_body import BodyCommonResponse
from rescue.rescueserver.request_dialog import RequestDialog
import vlc

HOST = ''
PORT = 9000



class RescuerManager:

    def __init__(self):
        self.rescuers = {}  # {rescuer ID: (socket, address), ...}
        self.isCalling = False
        self.hasToken = True
        self.lock = threading.Lock();

    def addRescuer(self, rescuerId, conn, address):
        if rescuerId in self.rescuers:
            conn.send()
    def lockCall(self):
        with self.lock:
            self.isCalling = True
    def freeCall(self):
        with self.lock:
            self.isCalling = False
    def getCallStatus(self):
        with self.lock:
            return self.isCalling

    def lockToken(self):
        with self.lock:
            self.hasToken = False
    def freeToken(self):
        with self.lock:
            self.hasToken = True
    def getTokenStatus(self):
        with self.lock:
            return self.hasToken


class RequestHandler(socketserver.BaseRequestHandler):
    rm = RescuerManager()

    def handle(self):
        print("클라이언트 접속: {0}".format(self.client_address[0]))

        client = self.request  # client socket

        while True:
            reqMsg = MessageUtil.receive(client);
            if reqMsg == None:
                continue

            if reqMsg.Header.MSGTYPE == message.REQ_CONNECT:  # 전송 요청 처리
                rspMsg = Message()
                rspMsg.Body = BodyCommonResponse(None)
                rspMsg.Body.RESPONSE = message.ACCEPTED

                rspMsg.Header = Header(None)
                rspMsg.Header.MSGTYPE = message.REP_CONNECT
                rspMsg.Header.BODYLEN = rspMsg.Body.getSize()

                MessageUtil.send(client, rspMsg)
                continue

            elif reqMsg.Header.MSGTYPE == message.REQ_GET_TOKEN:    # 음성 토큰 요청
                rspMsg = Message()
                rspMsg.Body = BodyCommonResponse(None)
                rspMsg.Body.RESPONSE = message.ACCEPTED

                rspMsg.Header = Header(None)
                rspMsg.Header.MSGTYPE = message.REP_GET_TOKEN
                rspMsg.Header.BODYLEN = rspMsg.Body.getSize()

                if self.rm.getTokenStatus() == True:
                    self.rm.lockToken()
                    print('token 방출')
                else:
                    rspMsg.Body.RESPONSE = message.DENIED
                    print('token 없음')

                MessageUtil.send(client, rspMsg)
                continue

            elif reqMsg.Header.MSGTYPE == message.REQ_RETURN_TOKEN:
                None
            elif reqMsg.Header.MSGTYPE == message.REQ_VIDEO_STREAMING:
                if self.rm.getCallStatus() == False:
                    self.rm.lockCall()
                    requestDialog = RequestDialog("구조대원 4")

                    # ret == 0: 연결 수락 / ret == 1: 연결 거절
                    ret = requestDialog.showDialog()
                    rspMsg = Message()
                    rspMsg.Header = Header(None)
                    rspMsg.Body = BodyCommonResponse(None)
                    rspMsg.Body.RESPONSE = message.ACCEPTED

                    rspMsg.Header.MSGTYPE = message.REP_VIDEO_STREAMING
                    rspMsg.Header.BODYLEN = rspMsg.Body.getSize()
                    print(ret)
                    if (ret == 0):
                        MessageUtil.send(client, rspMsg)

                        #VLC 플레이어 실행
                        instance = vlc.Instance()
                        player = instance.media_player_new()
                        media = instance.media_new('rtp://141.223.84.110:1234')
                        media.get_mrl()
                        player.set_media(media)
                        player.play()
                        print("abcd")

                    else:
                        rspMsg.Body.RESPONSE = message.DENIED
                        MessageUtil.send(client, rspMsg)


                    self.rm.freeCall()
                else:
                    print("통화 거절")

                continue

            elif reqMsg.Header.MSGTYPE == message.REQ_EXIT_VIDEO_STREAMING:
                None
            elif reqMsg.Header.MSGTYPE == message.REP_EXIT_VIDEO_STREAMING:
                None

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), RequestHandler)
    threading.Thread(target=server.serve_forever).start()
