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

        signalArray = data['exo'].values

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

        nDays = len(signalArray)

        sphIndicator = np.zeros(nDays)
        splIndicator = np.zeros(nDays)

        sphLevel = np.zeros(nDays)
        splLevel = np.zeros(nDays)


        for dday in range(nDays):

            if signalArray[dday] > currentHigh:
                currentHigh = signalArray[dday]
                sphMaxDay = dday
                sphDays = 0
            else:
                sphDays = sphDays + 1

            if signalArray[dday] < currentLow:
                currentLow = signalArray[dday]
                splMinDay = dday
                splDays = 0
            else:
                splDays = splDays + 1

            if sphDays > sphThreshold:
                sphLevel[dday] = currentHigh
                sphIndicator[dday] = 1

                for dd in range(sphStart, dday):  # ?? or dday-1
                    sphLevel[dd] = prevHigh

                prevHigh = currentHigh
                prevHVol = currentHVol
                sphStart = dday
                sphDays = 0
                currentHigh = -np.inf  # intmin('int32');


            if splDays > splThreshold:
                splLevel[dday] = currentLow
                splIndicator[dday] = 1

                for dd in range(splStart, dday):  # ??? or dday-1
                    splLevel[dd] = prevLow

                prevLow = currentLow
                prevLVol = currentLVol
                splStart = dday
                splDays = 0
                currentLow = np.inf  # intmax('int32');


            # fill to the end
            for dd in range(sphStart, nDays):
                sphLevel[dd] = prevHigh

            for dd in range(splStart, nDays):
                splLevel[dd] = prevLow

        return pd.DataFrame(
            {
                 'sphIndicator': pd.Series(sphIndicator, index=data.exo.index),
                 'splIndicator': pd.Series(splIndicator, index=data.exo.index),
                 'sphLevel': pd.Series(sphLevel, index=data.exo.index),
                 'splLevel': pd.Series(splLevel, index=data.exo.index),
                 'price':  pd.Series(data.exo, index=data.exo.index)
            },
            index=data.exo.index)