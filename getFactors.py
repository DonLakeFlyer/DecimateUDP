import math
import numpy as np

def getFactors(totalDecimation):
    factors = []

    i = 2
    while i <= math.floor(totalDecimation / 2):
        if totalDecimation %  i == 0 and totalDecimation > 1:
            factors.append(i)
        i += 1

    if totalDecimation != 1:
        retList = []
        retList.append(1)
        retList.extend(factors)
        retList.append(totalDecimation)
        return np.array(retList, dtype=int)
    else:
        return np.ones(1, dtype=int)
