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
lock = threading.Lock();


class RescuerManager:
    def __init__(self):
        self.rescuers = {}  # {rescuer ID: (socket, address), ...}

    def addRescuer(self, rescuerId, conn, address):
        if rescuerId in self.rescuers:
            conn.send()


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("클라이언트 접속: {0}".format(self.client_address[0]))

        client = self.request  # client socket

        while True:
            reqMsg = MessageUtil.receive(client);
            print(reqMsg.Header.BODYLEN)
            print(reqMsg.Header.MSGTYPE)

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
                requestDialog = RequestDialog("구조대원 4");
                requestDialog.showDialog()

            elif reqMsg.Header.MSGTYPE == message.REQ_EXIT_VIDEO_STREAMING:
                None
            elif reqMsg.Header.MSGTYPE == message.REP_EXIT_VIDEO_STREAMING:
                None


if __name__ == '__main__':
    server = socketserver.TCPServer((HOST, PORT), RequestHandler)
    threading.Thread(target=server.serve_forever).start()
