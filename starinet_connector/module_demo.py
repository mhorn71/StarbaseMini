__author__ = 'mark'
import time

import starinet_connector

starinet_connector.StarinetConnectorStart('192.168.1.20', '1206', '/dev/tty.usbserial-142', '57600', '30')

while 1:
    time.sleep(60)
