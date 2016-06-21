import pandas as pd
import numpy as np


def swingpoints(sphThreshold, splThreshold, data):
        '''
        !Required for mat file loading! from scipy.io import loadmat, savemat

        sphTreshold - int number of days from breakout
        splTreshold - int number of days from breakout
        data - exo data (including exo price and volume)

        returns -> df with sphLevel/volume and splLevel/volume pd series with exo prices index.
                    Plus VolumeSeries and price with exo prices index
        '''

        signalArray = data.exo.values
        volumeArray = data.volume.values

        OPEN  = 0
        HIGH  = 1
        LOW   = 2
        CLOSE = 3

        if len(signalArray) == 1:
            OPEN = HIGH = LOW = CLOSE = 0

        currentHigh = -np.inf  # intmin('int32');
        currentLow = np.inf  # intmax('int32');

        currentHVol = 0
        currentLVol = 0
        sphDays = 0
        splDays = 0
        sphStart = 1
        splStart = 1
        sphMaxDay = 0
        splMinDay = 0
        prevHigh = signalArray[0]
        prevLow = signalArray[0]
        prevHVol = volumeArray[0]
        prevLVol = volumeArray[0]

        nDays = len(signalArray)

        sphIndicator = np.zeros(nDays)
        splIndicator = np.zeros(nDays)

        sphLevel = np.zeros(nDays)
        splLevel = np.zeros(nDays)

        sphVolume = np.zeros(nDays)
        splVolume = np.zeros(nDays)

        for dday in range(nDays):

            if signalArray[dday] > currentHigh:
                currentHigh = signalArray[dday]
                currentHVol = volumeArray[dday]
                sphMaxDay = dday
                sphDays = 0
            else:
                sphDays = sphDays + 1

            if signalArray[dday] < currentLow:
                currentLow = signalArray[dday]
                currentLVol = volumeArray[dday]
                splMinDay = dday
                splDays = 0
            else:
                splDays = splDays + 1

            if sphDays > sphThreshold:
                sphLevel[dday] = currentHigh
                sphIndicator[dday] = 1
                sphVolume[dday] = currentHVol

                for dd in range(sphStart, dday):  # ?? or dday-1
                    sphLevel[dd] = prevHigh
                    sphVolume[dd] = prevHVol

                prevHigh = currentHigh
                prevHVol = currentHVol
                sphStart = dday
                sphDays = 0
                currentHigh = -np.inf  # intmin('int32');

            elif dday > 1:
                sphVolume[dday] = sphVolume[dday - 1]
            elif dday == 1:
                sphVolume[dday] = volumeArray[dday]

            if splDays > splThreshold:
                splLevel[dday] = currentLow
                splIndicator[dday] = 1
                splVolume[dday] = currentLVol

                for dd in range(splStart, dday):  # ??? or dday-1
                    splLevel[dd] = prevLow
                    splVolume[dd] = prevLVol

                prevLow = currentLow
                prevLVol = currentLVol
                splStart = dday
                splDays = 0
                currentLow = np.inf  # intmax('int32');
            elif dday > 1:
                splVolume[dday] = splVolume[dday - 1]
            elif dday == 1:
                splVolume[dday] = volumeArray[dday]

            # fill to the end
            for dd in range(sphStart, nDays):
                sphLevel[dd] = prevHigh
                sphVolume[dd] = prevHVol

            for dd in range(splStart, nDays):
                splLevel[dd] = prevLow
                splVolume[dd] = prevLVol

        return pd.DataFrame(
            {
                 'sphIndicator': pd.Series(sphIndicator, index=data.exo.index),
                 'splIndicator': pd.Series(splIndicator, index=data.exo.index),
                 'sphLevel': pd.Series(sphLevel, index=data.exo.index),
                 'splLevel': pd.Series(splLevel, index=data.exo.index),
                 'sphVolume': pd.Series(sphVolume, index=data.exo.index),
                 'splVolume': pd.Series(splVolume, index=data.exo.index),
                 'volumeSeries': pd.Series(volumeArray, index=data.exo.index),
                 'price':  pd.Series(data.exo, index=data.exo.index)
            },
            index=data.exo.index)