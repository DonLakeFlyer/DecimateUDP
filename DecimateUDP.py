from CSingleUDPReceiver     import *
from CSingleUDPSender       import *
from stagedDecimateFactors  import *

import socket
import math
import numpy as np
import scipy as sp
from scipy import signal

def DecimateUDP():
    incomingSampleRate                  = 3000000
    outgoingSampleRate                  = 4000
    totalDecimation                     = incomingSampleRate / outgoingSampleRate
    outgoingDecimatedSampleCount        = 1024
    incomingSampleCountPerDecimation    = int(outgoingDecimatedSampleCount * totalDecimation)
    iqSamplesPerFrame                   = 2048

    incomingSampleBuffer        = np.empty(incomingSampleCountPerDecimation, dtype=np.csingle)
    incomingSampleBufferCount   = 0
    firstUdpBuffer              = True
    stagedFactors               = stagedDecimateFactors(incomingSampleRate, outgoingSampleRate)

    outgoingSequenceNumber      = 0
    outgoingSampleBuffer        = np.empty(outgoingDecimatedSampleCount + 1, dtype=np.csingle)
    outgoingSampleBuffer[0]     = complex(outgoingSequenceNumber, 0)

    udpReceiver = CSingleUDPReceiver("127.0.0.1", 10000)
    udpSender   = CSingleUDPSender  ("10.0.0.180", 20000)

    while True:
        iqData  = udpReceiver.read(iqSamplesPerFrame);

        if iqData is not None:
            if firstUdpBuffer:
                incomingExpectedSeqNum = int(iqData[0].real)
            actualSeqNum = int(iqData[0].real)
            if actualSeqNum != incomingExpectedSeqNum:
                print("OVERFLOW")
            incomingExpectedSeqNum += 1
            if incomingExpectedSeqNum == 65536:
                incomingExpectedSeqNum = 0
            iqSampleCount = iqData.size - 1
            incomingSampleBuffer[incomingSampleBufferCount : incomingSampleBufferCount + iqSampleCount] = iqData[1:]
            incomingSampleBufferCount += iqSampleCount

            if incomingSampleBufferCount > incomingSampleCountPerDecimation:
                raise RuntimeError("Buffer counts are wrong %d %d %d" % (iqSampleCount, incomingSampleBufferCount, incomingSampleCountPerDecimation))
            if incomingSampleBufferCount == incomingSampleCountPerDecimation:
                decimatedSamples = incomingSampleBuffer
                for decimation in stagedFactors:
                    decimatedSamples = sp.signal.decimate(decimatedSamples, decimation, 4, ftype='iir')
                    if not np.all(np.isfinite(decimatedSamples)):
                        raise RuntimeError("Decimate failed")
                outgoingSampleBuffer[1:] = decimatedSamples
                udpSender.send(outgoingSampleBuffer)
                print(",", end="")
                incomingSampleBufferCount = 0
                outgoingSampleBuffer[0]   = complex(outgoingSequenceNumber, 0)
                outgoingSequenceNumber += 1
                if outgoingSequenceNumber == 65536:
                    outgoingSequenceNumber = 0


if __name__ == '__main__':
    DecimateUDP()