import socket
import numpy as np
import sys

class CSingleFileReceiver:
    def __init__ (self, filename):
        self.fd = open(filename, "rb")

    def read(self, complexSampleCount: int):
        # complexSampleCount: buffer size in complex samples
        bytesToRead = complexSampleCount * 4 * 2
        bytes = self.fd.read(bytesToRead)
        bytesRead = len(bytes)
        if bytes == 0 or bytesRead == 0:
            return None
        if bytesRead != bytesToRead:
            raise
        return np.frombuffer(bytes, dtype = np.csingle)

    def clear(self):
        self.rxSocket.setblocking(False)
        while True:
            try:
                bytes = self.rxSocket.recvfrom(1024)
            except BlockingIOError:
                # No port on the other side
                break
            else:
                if not len(bytes):
                    break
        self.rxSocket.setblocking(True)
