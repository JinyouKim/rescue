import os
import socketserver
import sys
import threading

from PyQt5.QtWidgets import QApplication, QDialog

from common import message
from common.message import Message
from common.message_util import MessageUtil
from common.message_header import Header
from common.message_body import BodyCommonResponse
from rescueserver.request_dialog import RequestDialog
from rescueserver.ui.ui_request_dialog import Ui_RequestDialog

HOST = ''
PORT = 9000



class RescuerManager:

    def __init__(self):
        self.rescuers = {}  # {rescuer ID: (socket, address), ...}
        self.isCalling = False
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

            elif reqMsg.Header.MSGTYPE == message.REQ_GET_TOKEN:
                None
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

                    else:
                        rspMsg.Body.RESPONSE = message.DENIED
                        MessageUtil.send(client, rspMsg)


                    self.rm.freeCall()
                else:
                    print("통화 거절")

            elif reqMsg.Header.MSGTYPE == message.REQ_EXIT_VIDEO_STREAMING:
                None
            elif reqMsg.Header.MSGTYPE == message.REP_EXIT_VIDEO_STREAMING:
                None

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    server = ThreadedTCPServer((HOST, PORT), RequestHandler)
    threading.Thread(target=server.serve_forever).start()
