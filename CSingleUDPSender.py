import socket
import numpy as np
import sys

class CSingleUDPSender:
    def __init__ (self, ipAddress: str, port: int):
        self.txSocket       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.txIPAddress    = ipAddress
        self.txPort         = port

    def send(self, complexSamples):
        self.txSocket.sendto(complexSamples.tobytes(), (self.txIPAddress, self.txPort))
