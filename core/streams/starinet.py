__author__ = 'Mark'

import asyncio
import logging

from core.configLoader import confLoader


logger = logging.getLogger('core.streams.starinet')


class UdpStream:
    # This was lifted directly from https://docs.python.org/3/library/asyncio-protocol.html#udp-echo-client-protocol

    def __init__(self, message, loop):

        self.config = confLoader()
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()
