from getFactors import *

def stagedDecimateFactors(rawSampleRate, decimatedSampleRate):
    remainingDecimation     = rawSampleRate / decimatedSampleRate
    maxDecimationPerStage   = 13
    stagedFactors           = []

    while remainingDecimation != 1:
        remainingDivisors   = getFactors(remainingDecimation)
        validDivisors       = remainingDivisors[remainingDivisors <= maxDecimationPerStage]
        currDivisor         = validDivisors[-1]
        remainingDecimation = remainingDecimation / currDivisor

        stagedFactors.append(currDivisor)

    return np.array(stagedFactors, dtype=int)