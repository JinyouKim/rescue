#!/usr/bin/python3

# install thriftpy
# pip3 install cython thriftpy

from thrift_ui import ThriftUI

thriftUI = ThriftUI()
thriftUI.connect('192.168.0.110', 9090, 'definition.thrift')
thriftUI.reportRescuerPosition(1, 1, 2, False, True)
sensorData = thriftUI.retrieveSensorData()
iplImageData = thriftUI.downloadMapIplImage()
iplImageData = thriftUI.downloadMapIplImage()
iplImageData = thriftUI.downloadMapIplImage()

#i = THRIFT_IPLIMAGE()
print(type(iplImageData))
#print(type(iplImageData))
