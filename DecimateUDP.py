from CSingleUDPReceiver     import *
from stagedDecimateFactors  import *


import socket
import math
import numpy as np
import scipy as sp
from scipy import signal

def DecimateUDP():
    incomingSampleRate                  = 3000000
    outgoingSampleRate                  = 4000
    totalDecimation                     = 3000000 / 4000
    outgoingDecimatedSampleCount        = 1024
    incomingSampleCountPerDecimation    = int(outgoingDecimatedSampleCount * totalDecimation)
    iqSamplesPerFrame                   = 1024


    iqSampleBuffer          = np.empty(incomingSampleCountPerDecimation, dtype=np.csingle)
    iqSampleBufferCount     = 0
    firstUdpBuffer          = True
    stagedFactors           = stagedDecimateFactors(incomingSampleRate, outgoingSampleRate)

    udpReceiver = CSingleUDPReceiver("127.0.0.1", 10000)

    while True:
        iqData  = udpReceiver.read(iqSamplesPerFrame);

        if iqData is not None:
            if firstUdpBuffer:
                expectedSeqNum = int(iqData[0].real)
            actualSeqNum = int(iqData[0].real)
            if actualSeqNum != expectedSeqNum:
                print("OVERFLOW")
            expectedSeqNum += 1
            if expectedSeqNum == 65535:
                expectedSeqNum = 0
            iqSampleCount = iqData.size - 1
            iqSampleBuffer[iqSampleBufferCount : iqSampleBufferCount + iqSampleCount] = iqData[1 : iqSampleCount + 1]
            iqSampleBufferCount += iqSampleCount

            if iqSampleBufferCount > incomingSampleCountPerDecimation:
                raise RuntimeError("Buffer counts are wrong %d %d %d" % (iqSampleCount, iqSampleBufferCount, incomingSampleCountPerDecimation))
            if iqSampleBufferCount == incomingSampleCountPerDecimation:
                decimatedSamples = iqSampleBuffer
                for decimation in stagedFactors:
                    decimatedSamples = sp.signal.decimate(decimatedSamples, decimation)
                iqSampleBufferCount = 0


if __name__ == '__main__':
    DecimateUDP()