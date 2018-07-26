import sys
import socket
import struct
import time

from common import message
from common.message import Message

from common.message_header import Header
from common.message_body import BodyCommonResponse
from common.message_body import BodyConnectRequest


from common.message_util import MessageUtil


CHUNK_SIZE = 4096

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("usage: {0} <server IP>".format(sys.argv[0]))
		sys.exit(0)
	
	serverIp = sys.argv[1]
	serverPort = 9111

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		ret = -1
		print("1")
		while ret != 0:
			print('2')
			ret = sock.connect_ex((serverIp, serverPort))
			time.sleep(2)

		print('3')
		reqMsg = Message()
		regMsg.Body = BodyConnectRequest(None)
		self.RESQUER_ID = 1

		reqMsg.Header = Header(None)
		reqMsg.Header.MSGTYPE = message.REQ_CONNECT
		reqMsg.Header.BODYLEN = reqMsg.Body.GetSize()

		MessageUtil.send(sock, reqMsg)
		print('abc')
		rspMsg = MessageUtil.receive(sock)

		if rspMsg.Header.MSGTYPE != message.REP_CONNECT:
			print("Error")
			exit(0)
		if rspMsg.Body.RESPONSE != message.ACCEPT:
			print("Connection is refused.")
			exit(0)

	except Exception as err:
		print("Exception")
		print(err)

	sock.close()



