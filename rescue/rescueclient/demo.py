#!/usr/bin/python3

# install thriftpy
# pip3 install cython thriftpy

from ThriftUI import ThriftUI

thriftUI = ThriftUI()
thriftUI.connect('192.168.0.108', 9090, 'definition.thrift')
thriftUI.reportRescuerPosition(1, 1, 2, False, True)
sensorData = thriftUI.retrieveSensorData()
iplImageData = thriftUI.downloadMapIplImage()

print(sensorData)
print(iplImageData)
